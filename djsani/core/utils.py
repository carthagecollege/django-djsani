# -*- coding: utf-8 -*-

"""Utilities that are used in views."""

import os

from django.conf import settings
from django.core.cache import cache
from djsani.core.models import StudentMedicalContentType
from djsani.core.models import StudentMedicalManager
from djsani.insurance.models import StudentHealthInsurance
from djsani.medical_history.models import AthleteMedicalHistory
from djsani.medical_history.models import StudentMedicalHistory
from djsani.medical_history.waivers.models import Sicklecell
from djtools.fields import TODAY


DEC = settings.DECEMBER


def doop(mod, man):
    """Check for an object and duplicate it. Returns the new object or None."""
    instance = mod.objects.using('informix').filter(
        college_id=man.college_id,
    ).order_by('-id').first()

    if instance:
        # copy the previous object to new
        instance.pk = None
        instance.created_at = None
        # associate the new obj with the new manager
        instance.manager_id = man.id
        instance.save(using='informix')

    return instance


def get_content_type(name):
    """Return a content type from cache or fetch and set it in cache."""
    ct = cache.get(name)
    if not ct:
        ct = StudentMedicalContentType.objects.using('informix').filter(
            name=name,
        ).first()
        cache.set(name, ct, None)
    return ct


def get_term():
    """Obtain the current academic term."""
    sd = settings.START_DATE
    term = 'RA'
    year = TODAY.year
    if ((TODAY.month < sd.month) or (TODAY.month == DEC and TODAY.day > 10)):
        term = 'RC'
        if TODAY.month == DEC:
            year = year + 1
    return {'yr': year, 'sess': term}


def get_manager(cid):
    """
    Returns the current student medical manager.

    it is based on the date created in relation to the medical forms
    collection process start date.

    if we don't have a current manager, we create one.

    requires the student's college ID and START_DATE in settings file.
    """
    # try to fetch a current manager
    # from cache or database
    manager = StudentMedicalManager.objects.using('informix').filter(
        college_id=cid,
    ).filter(created_at__gte=settings.START_DATE).first()
    # if we don't have a current manager:
    # (could be a first time returning student or new FR or transfer)
    # create the new student profile by copying some things from
    # the previous manager, in addition to copying the insurance,
    # medical histories, sicklecell waiver if they exists.
    if not manager:
        immunization = False
        sicklecell = False
        concussion_baseline = False
        # do we have a past manager?
        past_man = StudentMedicalManager.objects.using('informix').filter(
            college_id=cid,
        ).order_by('-id').first()

        if past_man:
            # returning student
            if past_man.cc_student_immunization:
                immunization = True
            if past_man.concussion_baseline:
                concussion_baseline = True
            # if sicklecell waiver, check the latest for proof,
            # which means always True
            if past_man.cc_athlete_sicklecell_waiver:
                # fetch the latest sicklecell waiver
                sc = Sicklecell.objects.using('informix').filter(
                    college_id=cid,
                ).order_by('-id').first()
                if sc.proof:
                    sicklecell = True

        # create new manager
        manager = StudentMedicalManager(
            college_id=cid,
            cc_student_immunization=immunization,
            cc_athlete_sicklecell_waiver=sicklecell,
            sitrep=False,
            sitrep_athlete=False,
            concussion_baseline=concussion_baseline,
        )
        manager.save(using='informix')

        # check for insurance object
        doop(StudentHealthInsurance, manager)
        # check for student medical history
        doop(StudentMedicalHistory, manager)
        # check for athlete medical history
        doop(AthleteMedicalHistory, manager)

    return manager
