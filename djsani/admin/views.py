from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

import logging
logger = logging.getLogger(__name__)

#@login_required
def home(request):
    return render_to_response(
        "admin/home.html",
        context_instance=RequestContext(request)
    )

