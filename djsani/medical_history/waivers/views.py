# -*- coding: utf-8 -*-

"""Forms for medical history."""

import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from djsani.core.utils import get_manager
from djsani.medical_history.waivers.models import Sicklecell
from djtools.fields import NEXT_YEAR
from djtools.fields.helpers import handle_uploaded_file
from djtools.utils.convert import str_to_class


@login_required
def index(request, stype, wtype):
    """Generic waivers form."""
    cid = request.user.id
    # user student type and waiver type to build table name
    table = 'cc_{0}_{1}_waiver'.format(stype, wtype)

    # check for student manager record
    manager = get_manager(cid)
    # form name
    fname = str_to_class(
        'djsani.medical_history.waivers.forms',
        '{0}Form'.format(wtype.capitalize()),
    )
    sicklecell = None
    if wtype == 'sicklecell':
        sicklecell = Sicklecell.objects.filter(college_id=cid).filter(
            Q(proof=1) | Q(created_at > settings.START_DATE)
        ).first()

    # check to see if they already submitted this form.
    # redirect except for sicklecell waiver
    # or wtype does not return a form class (fname)
    if (manager and getattr(manager, table, None) and wtype != 'sicklecell') \
      or not fname:
        return HttpResponseRedirect( reverse_lazy('home') )

    if request.method=='POST':
        form = fname(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            # deal with file uploads
            if request.FILES.get('results_file'):
                folder = 'sicklecell/{}/{}'.format(
                    cid, manager.created_at.strftime('%Y%m%d%H%M%S%f')
                )
                phile = handle_uploaded_file(
                    request.FILES['results_file'],
                    os.path.join(settings.UPLOADS_DIR, folder),
                )
                data['results_file'] = '{0}/{1}'.format(folder, phile)

            if sicklecell:
                # update student's sicklecell waiver record
                data['updated_at'] = datetime.datetime.now()
                for key, value in data.items():
                    setattr(sicklecell, key, value)
            else:
                # insert
                data['college_id'] = cid
                data['manager_id'] = manager.id
                model = str_to_class(
                    'djsani.medical_history.waivers.models',
                    wtype.capitalize(),
                )
                s = model(**data)
                session.add(s)
            # update the manager
            setattr(manager, table, True)
            manager.save()

            return HttpResponseRedirect(reverse_lazy('waiver_success'))
    else:
        form = fname

    # check for a valid template or redirect home
    try:
        template = 'medical_history/waivers/{0}_{1}.html'.format(stype, wtype)
        os.stat(os.path.join(settings.ROOT_DIR, 'templates', template))
    except Exception:
        return HttpResponseRedirect(reverse_lazy('home'))

    return render(
        request,
        template,
        {
            'form': form,
            'next_year': NEXT_YEAR,
            'student': sicklecell,
        },
    )
