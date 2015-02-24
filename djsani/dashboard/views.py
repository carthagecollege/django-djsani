from django.conf import settings
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from djsani.core import *
from djsani.core.views import get_data, put_data, is_member
from djsani.medical_history.forms import StudentForm as SmedForm
from djsani.medical_history.forms import AthleteForm as AmedForm

from djzbar.utils.informix import do_sql as do_esql
from djtools.decorators.auth import group_required
from djtools.utils.date import calculate_age

def emergency_information(cid):
    """
    returns all of the emergency contact information for any given student
    OJO: Formating is shit. Needs a template but for now plain text will do.
    """
    FIELDS = [
        'beg_date','end_date','line1','line2','line3',
        'phone','phone_ext','opt_out'
    ]
    CODES = ['ICE','ICE2']

    ens = ""
    for c in CODES:
        sql = "SELECT * FROM aa_rec WHERE aa = '%s' AND id='%s'" % (c,cid)
        try:
            result = do_esql(
                sql,key=settings.INFORMIX_DEBUG,
                earl=settings.INFORMIX_EARL).fetchone()
            ens +=  "++%s++++++++++++++++++++++\n" % c
            for f in FIELDS:
                if result[f]:
                    ens += "%s = %s\n" % (f,result[f])
        except:
            pass
    return ens

@group_required('Medical Staff')
def home(request):
    """
    dashboard home with a list of students
    """
    students = None
    sql = '%s WHERE prog_enr_rec.cl IN ("FF","FR") ' % STUDENTS_ALPHA
    sql += "ORDER BY lastname"
    objs = do_esql(sql,key=settings.INFORMIX_DEBUG,earl=settings.INFORMIX_EARL)

    if objs:
        students = [dict(row) for row in objs.fetchall()]
        for s in students:
            adult = "minor"
            if s["birth_date"]:
                age = calculate_age(s["birth_date"])
                if age > 17:
                    adult = "adult"
            s["adult"] = adult

    return render_to_response(
        "dashboard/home.html",
        {"students":students,"sports":SPORTS},
        context_instance=RequestContext(request)
    )

def get_students(request):
    """
    ajax POST returns a list of students
    """
    if request.POST and (is_member(request.user,"Medical Staff") \
      or request.user.is_superuser):
        sport = request.POST.get("sport")
        sql = " %s WHERE prog_enr_rec.cl IN (%s)" % (
            STUDENTS_ALPHA,request.POST["class"]
        )
        if sport and sport != '0':
            sql += """
                AND cc_student_medical_manager.sports like '%%%s%%'
            """ % sport
        #sql += GROUP_BY
        objs = do_esql(
            sql,key=settings.INFORMIX_DEBUG,earl=settings.INFORMIX_EARL
        )
        students = None
        if objs:
            students = objs.fetchall()
        return render_to_response(
            "dashboard/students_data.inc.html",
            {"students":students,"sports":SPORTS,},
            context_instance=RequestContext(request)
        )
    else:
        return HttpResponse("error", mimetype="text/plain; charset=utf-8")

def panels(request,table,cid):
    """
    Takes database table and student ID.
    Returns the template data that paints the panels in the
    student detail view.
    """
    form = None
    obj = get_data(table,cid)
    if obj:
        data = obj.fetchone()
        if data:
            innit = {}
            if table == "cc_student_medical_history":
                for k,v in data.items():
                    innit[k] = v
                form = SmedForm(initial=innit)
            if table == "cc_athlete_medical_history":
                for k,v in data.items():
                    innit[k] = v
                form = AmedForm(initial=innit)
    t = loader.get_template("dashboard/panels/%s.html" % table)
    c = RequestContext(request, {'data':data,'form':form})
    return t.render(c)

@group_required('Medical Staff')
def student_detail(request,cid=None,content=None):
    """
    main method for displaying student data
    """
    template = "dashboard/student_detail.html"
    if content:
        template = "dashboard/student_print_%s.html" % content
    my_sports = None
    if not cid:
        # search form
        cid = request.POST.get("cid")
    if cid:
        # get student
        obj = do_esql(
            "%s WHERE id_rec.id = '%s'" % (STUDENT_VITALS,cid),
            key=settings.INFORMIX_DEBUG,earl=settings.INFORMIX_EARL
        )
        if obj:
            student = obj.fetchone()
            if student:
                try:
                    age = calculate_age(student.birth_date)
                except:
                    age = None
                ens = emergency_information(cid)
                shi = panels(request,"cc_student_health_insurance",cid)
                smh = panels(request,"cc_student_medical_history",cid)
                amh = panels(request,"cc_athlete_medical_history",cid)
                # used for staff who update info on the dashboard
                stype = "student"
                if student.athlete:
                    stype = "athlete"
                if student.sports:
                    my_sports = student.sports.split(",")
            else:
                age=ens=shi=smh=amh=student=stype=None
            return render_to_response(
                template,
                {
                    "student":student,"age":age,"ens":ens,
                    "shi":shi,"amh":amh,"smh":smh,"cid":cid,
                    "switch_earl": reverse_lazy("set_type"),
                    "sports":SPORTS, "my_sports":my_sports,
                    "stype":stype
                },
                context_instance=RequestContext(request)
            )
        else:
            raise Http404
    else:
        raise Http404


@csrf_exempt
def xeditable(request):
    field = request.POST.get("name")
    value = request.POST.get("value")
    cid = request.POST.get("cid")
    table = request.POST.get("table")
    dic = {field:value}
    put_data( dic, table, cid )

    return HttpResponse(dic, mimetype="text/plain; charset=utf-8")
