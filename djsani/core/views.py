from django.conf import settings
from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from djsani.core import STUDENT_VITALS, SPORTS
from djzbar.utils.informix import do_sql as do_esql
from djzbar.utils.decorators import portal_login_required
from djtools.utils.date import calculate_age
from djtools.fields import TODAY

import logging
logger = logging.getLogger(__name__)

def get_data(table,cid,fields=None,date=None):
    """
    table   = name of database table
    fields  = list of database fields to return
    key     = dict with unique identifier and value
    """
    status = False
    sql = "SELECT "
    if fields:
        sql += ','.join(fields)
    else:
        sql += "*"
    sql += " FROM %s WHERE cid=%s" % (table,cid)
    if date:
        sql += " AND created_at?"
    result = do_esql(sql)
    return result

def put_data(dic,table,cid=None,noquo=None):
    """
    dic:    dictionary of data
    table:  the name of the table in the database
    cid:    create or update
    noquo:  a list of field names that do not require quotes
    """
    if cid:
        prefix = "UPDATE %s SET " % table
        for key,val in dic.items():
            # informix expects 1 or 0
            if val == True:
                val = 1
            if val == False:
                val = 0
            prefix += "%s=" % key
            if noquo and key in noquo:
                prefix += "%s," % val
            else:
                prefix += "'%s'," % val
        sql = "%s WHERE cid=%s" % (prefix[:-1],cid)
    else:
        prefix = "INSERT INTO %s" % table
        fields = "("
        values = "VALUES ("
        for key,val in dic.items():
            # informix expects 1 or 0
            if val == True:
                val = 1
            if val == False:
                val = 0
            fields +='%s,' % key
            if noquo and key in noquo:
                values +="%s," % val
            else:
                values +="'%s'," % val
        fields = "%s)" % fields[:-1]
        values = "%s)" % values[:-1]
        sql = "%s %s %s" % (prefix,fields,values)
    do_esql(sql,key=settings.INFORMIX_DEBUG)

def update_manager(field,cid):
    """
    simple method to update the manager table
    which we use throughout the app
    """
    put_data(
        {field:1,"cid":cid},
        "cc_student_medical_manager",
        cid=cid,
        noquo=[field,"cid"]
    )

@portal_login_required
def home(request):
    cid = request.session["cid"]
    adult = False
    # get student
    obj = do_esql("%s'%s'" % (STUDENT_VITALS,cid))
    if obj:
        student = obj.fetchone()
    if student:
        # adult or minor?
        age = calculate_age(student.birth_date)
        if age >= 18:
            adult = True
        obj = get_data("cc_student_medical_manager",cid)
        if obj:
            manager = obj.fetchone()
    return render_to_response(
        "home.html",
        {
            "switch_earl": reverse_lazy("set_type"),
            "student":student,
            "manager":manager,
            "sports":SPORTS,
            "adult":adult
        },
        context_instance=RequestContext(request)
    )

@csrf_exempt
def set_type(request):
    field = request.POST.get("field")
    cid = request.POST.get("cid")
    table="cc_student_medical_manager"
    # check for student manager record
    student = get_data(table,cid).fetchone()
    update = None
    if student:
        update = cid

    # student or athlete
    if field == "stype":
        switch = request.POST.get("switch")
        athlete = 0
        if switch == "athlete":
            athlete = 1
        dic = {"athlete":athlete,"cid":cid}
        noquo=["athlete","cid"]
    # sports
    if field == "sports":
        switch = ','.join(request.POST.getlist("switch[]"))
        logger.debug("sports = %s" % switch)
        dic = {"sports":switch,"cid":cid}
        noquo=["cid"]

    # set the session variable for use at UI level
    request.session[field] = switch
    logger.debug("dic = %s" % dic)
    put_data( dic, table, cid = update, noquo=noquo )

    return HttpResponse(switch, mimetype="text/plain; charset=utf-8")

def responsive_switch(request,action):
    if action=="go":
        request.session['desktop_mode']=True
    elif action=="leave":
        request.session['desktop_mode']=False
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", ""))

