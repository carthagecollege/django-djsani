# -*- coding: utf-8 -*-

"""Data models."""

from django.db import models
from djsani.core.models import StudentMedicalManager
from djtools.fields.helpers import upload_to_path


class StudentHealthInsurance(models.Model):
    """Student health insurance data, for both students and athletes."""

    # core
    college_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    manager = models.ForeignKey(
        StudentMedicalManager, on_delete=models.CASCADE,
    )
    opt_out = models.NullBooleanField()
    # primary
    primary_policy_holder = models.CharField(max_length=128)
    primary_dob = models.DateField(default='')
    primary_company = models.CharField(max_length=128)
    primary_phone = models.CharField(max_length=12)
    primary_policy_address = models.CharField(max_length=255)
    primary_member_id = models.CharField(max_length=64)
    primary_group_no = models.CharField(max_length=64)
    primary_policy_type = models.CharField(max_length=128)
    primary_policy_state = models.CharField(max_length=2)
    primary_card_front = models.FileField(
        upload_to=upload_to_path,
        max_length=128,
        null=True,
        blank=True,
    )
    primary_card_front_status = models.BooleanField()
    primary_card_back = models.FileField(
        upload_to=upload_to_path,
        max_length=128,
        null=True,
        blank=True,
    )
    primary_card_back_status = models.BooleanField()
    # secondary
    secondary_policy_holder = models.CharField(max_length=128)
    secondary_dob = models.DateField(default='')
    secondary_company = models.CharField(max_length=128)
    secondary_phone = models.CharField(max_length=12)
    secondary_policy_address = models.CharField(max_length=255)
    secondary_member_id = models.CharField(max_length=64)
    secondary_group_no = models.CharField(max_length=64)
    secondary_policy_type = models.CharField(max_length=128)
    secondary_policy_state = models.CharField(max_length=2)
    # tertiary
    tertiary_policy_holder = models.CharField(max_length=128)
    tertiary_dob = models.DateField(default='')
    tertiary_company = models.CharField(max_length=128)
    tertiary_phone = models.CharField(max_length=12)
    tertiary_policy_address = models.CharField(max_length=255)
    tertiary_member_id = models.CharField(max_length=64)
    tertiary_group_no = models.CharField(max_length=64)
    tertiary_policy_type = models.CharField(max_length=128)
    tertiary_policy_state = models.CharField(max_length=2)
    tertiary_card = models.FileField(
        upload_to=upload_to_path,
        max_length=128,
        null=True,
        blank=True,
    )

    class Meta:
        """Attributes about the data model and admin options."""

        db_table = 'cc_student_health_insurance'

    def __repr__(self):
        """Default data for display."""
        return str(self.college_id)

    def get_slug(self):
        """Used for the upload_to_path helper for file uplaods."""
        return 'insurance'

    def set_opt_out(self):
        """
        Empty the table when a student opts out.

        After a student has previously submitted insurance info we
        have to reset the values to an empty string.
        """
        for field in self._meta.fields:
            if field.name == 'opt_out':
                setattr(self, field.name, True)
            elif field.name not in {'manager', 'college_id', 'created_at'}:
                setattr(self, field.name, '')

    def current(self, day):
        """Determine if this is the current object for the academic year."""
        return self.created_at > day
