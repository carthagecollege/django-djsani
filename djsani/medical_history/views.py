from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

from djsani.medical_history.forms import StudentMedicalHistoryForm
from djsani.medical_history.forms import AthleteMedicalHistoryForm
from djsani.medical_history.models import StudentMedicalHistory
from djsani.medical_history.models import AthleteMedicalHistory
from djsani.core.utils import get_manager

from djzbar.utils.informix import get_session
from djtools.utils.convert import str_to_class
from djtools.utils.database import row2dict

EARL = settings.INFORMIX_EARL

@login_required
def form(request, stype, display=None):
    # dictionary for initial values if "update" else empty
    init = {}
    # student id
    cid = request.user.id
    # student gender
    gender=request.session.get('gender')
    # model name
    mname = "{}MedicalHistory".format(stype.capitalize())
    # form name
    fclass = str_to_class(
        "djsani.medical_history.forms",
        "{}Form".format(mname)
    )
    if not fclass:
        raise Http404
    # default template
    template = "medical_history/form.html"
    # check for student record(s)
    update = False
    table = "cc_{}_medical_history".format(stype)

    # create database session
    session = get_session(EARL)

    # retrieve student manager record
    manager = get_manager(session, cid)

    # retrieve our model and check to see if they already
    # submitted this form or we have data from previous years
    model = str_to_class(
        "djsani.medical_history.models", mname
    )
    if model:
        obj = session.query(model).filter_by(college_id=cid).\
            filter(model.current(settings.START_DATE)).first()
    else:
        raise Http404

    # dictionary for 'yes' answer values
    data = {}
    if obj:
        data["id"] = obj.id
        # if current update then use the xeditable form
        # otherwise we have data from the previous year but
        # the student needs to verify it
        if getattr(manager, table):
            update = True
            if display == "print":
                template = "medical_history/print.html"
            else:
                template = "medical_history/form_update.html"
        # put it in a dict
        init = row2dict(obj)
    if request.method == 'POST':
        post = request.POST.copy()
        form = fclass(post, gender=gender)
        if form.is_valid():
            data = form.cleaned_data
            # insert else update
            if not obj:
                data["college_id"] = cid
                data["manager_id"] = manager.id
                # set 'yes' responses with value from temp field
                for n,v in data.items():
                    if v == "Yes":
                        data[n] = post["%s_2" % n]
                # remove temp fields
                for n,v in data.items():
                    if n[-2:] == "_2":
                        data.pop(n)
                # insert
                s = model(**data)
                session.add(s)
            else:
                # update
                for key, value in data.iteritems():
                    setattr(obj, key, value)

            # update the manager
            setattr(manager,table,True)
            session.commit()
            session.close()
            return HttpResponseRedirect(
                reverse_lazy("medical_history_success")
            )
        else:
            if not obj:
                # for use at template level with dictionary filter
                for n,v in post.items():
                    if n[-2:] == "_2" and v:
                        data[n[:-2]] = v

    else:
        form = fclass(initial=init, gender=gender)
    return render_to_response(
        template,
        {
            "form":form,"stype":stype,"table":table,"cid":cid,
            "update":update,"data":data
        },
        context_instance=RequestContext(request)
    )

