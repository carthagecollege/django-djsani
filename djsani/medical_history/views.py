from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect

from djsani.medical_history.forms import StudentForm
from djsani.medical_history.forms import AthleteForm
from djsani.core.views import put_data, update_manager

from djzbar.utils.decorators import portal_login_required
from djtools.fields import NEXT_YEAR

@portal_login_required
def form(request,stype):
    cid = request.session["cid"]
    # form name
    fname = "%sForm" % stype.capitalize()
    if request.method=='POST':
        form = eval(fname)(request.POST)
        form.is_valid()
        forms = form.cleaned_data
        table = "%s_medical_history" % stype
        # insert
        put_data(forms,table=table)
        # update the manager
        update_manager(table,cid)
        return HttpResponseRedirect(
            reverse_lazy("medical_history_success")
        )
    else:
        form = eval(fname)
    return render_to_response(
        "medical_history/form.html",
        {
            "form":form,"stype":stype
        },
        context_instance=RequestContext(request)
    )
