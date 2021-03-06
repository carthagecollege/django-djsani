# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.conf import settings


# e.g. 2015-05-01 00:00:00
START_DATE = settings.START_DATE
# Informix likes DATE("2015-06-01") when using an IDE like Squirrel or RazorSQL
# or DATE("06/01/15")

SPORTS_STUDENT="""
SELECT
    TRIM(IT.invl) AS sport_code,
    TRIM(IT.txt) AS sport_name,
    INR.id AS id,
    INR.beg_date,
    INR.end_date
FROM
    invl_table IT
INNER JOIN
    involve_rec INR
ON
    TRIM(IT.invl) = TRIM(INR.invl)
AND
    IT.sanc_sport = 'Y'
WHERE
    TODAY BETWEEN IT.active_date AND NVL(IT.inactive_date, TODAY)
AND
    YEAR(INR.end_date) = {year}
AND
    INR.id = {cid}
""".format


STUDENTS_ALPHA = """
SELECT
    UNIQUE
    (
        SELECT
            COUNT(*)
        FROM
            invl_table IT
        INNER JOIN
            involve_rec INR
        ON
            TRIM(IT.invl) = TRIM(INR.invl)
        AND
            IT.sanc_sport = 'Y'
        WHERE
            TODAY BETWEEN IT.active_date AND NVL(IT.inactive_date, TODAY)
        AND
            YEAR(INR.end_date) > YEAR(TODAY)
        AND
            INR.id = id_rec.id
    ) as athlete,
    CASE
        WHEN NVL(stu_serv_rec.intend_hsg, 'C') IN ('C', 'O') THEN 'Commuter' ELSE 'Resident'
    END AS residency_status,
    id_rec.lastname, id_rec.firstname, id_rec.middlename,
    id_rec.id, profile_rec.birth_date,
    TRIM(cvid_rec.ldap_name) as ldap_name,
    cc_student_medical_manager.id as manid,
    cc_student_medical_manager.created_at,
    cc_student_medical_manager.staff_notes,
    cc_student_medical_manager.sitrep,
    cc_student_medical_manager.sitrep_athlete,
    cc_student_medical_manager.concussion_baseline,
    cc_student_medical_manager.emergency_contact,
    cc_student_medical_manager.covid19_vaccine_card,
    cc_student_medical_manager.covid19_vaccine_card_status,
    cc_student_medical_manager.medical_consent_agreement,
    cc_student_medical_manager.medical_consent_agreement_status,
    cc_student_medical_manager.physical_evaluation_1,
    cc_student_medical_manager.physical_evaluation_2,
    cc_student_medical_manager.cc_student_medical_history,
    cc_student_medical_manager.cc_student_health_insurance,
    cc_student_medical_manager.cc_student_meni_waiver,
    cc_student_medical_manager.cc_student_immunization,
    cc_student_medical_manager.cc_athlete_medical_history,
    cc_student_medical_manager.cc_athlete_privacy_waiver,
    cc_student_medical_manager.cc_athlete_reporting_waiver,
    cc_student_medical_manager.cc_athlete_risk_waiver,
    cc_student_medical_manager.cc_athlete_sicklecell_waiver,
    cc_student_health_insurance.primary_policy_type,
    cc_athlete_sicklecell_waiver.updated_at,
    cc_athlete_sicklecell_waiver.waive,
    cc_athlete_sicklecell_waiver.proof,
    cc_athlete_sicklecell_waiver.results,
    cc_athlete_sicklecell_waiver.results_file
FROM
    id_rec
INNER JOIN
    prog_enr_rec
ON
    id_rec.id = prog_enr_rec.id
LEFT JOIN
    cvid_rec
ON
    id_rec.id = cvid_rec.cx_id
LEFT JOIN
    stu_acad_rec
ON
    id_rec.id = stu_acad_rec.id
LEFT JOIN
    stu_serv_rec
ON
    id_rec.id = stu_serv_rec.id
LEFT JOIN
    profile_rec
ON
    id_rec.id = profile_rec.id
LEFT JOIN
    cc_student_medical_manager
ON
    id_rec.id = cc_student_medical_manager.college_id
    AND
    cc_student_medical_manager.created_at > "{0}"
LEFT JOIN
    cc_student_health_insurance
ON
    cc_student_medical_manager.id = cc_student_health_insurance.manager_id
LEFT JOIN
    cc_athlete_sicklecell_waiver
ON
    id_rec.id = cc_athlete_sicklecell_waiver.college_id
    AND
    (
        cc_athlete_sicklecell_waiver.proof = 1
    OR
        cc_athlete_sicklecell_waiver.created_at > "{1}"
    )
WHERE
    prog_enr_rec.subprog
NOT IN
    ("UWPK","RSBD","SLS","PARA","MSW","KUSD","ENRM","CONF","CHWK")
AND
    prog_enr_rec.lv_date IS NULL
AND
    stu_acad_rec.sess
IN
    ("RA","RC","AM","GC","PC","TC","GD","GA","GC")
""".format(START_DATE, START_DATE)

STUDENT_VITALS = """
SELECT
    UNIQUE
    CASE
        WHEN NVL(stu_serv_rec.intend_hsg, 'C') IN ('C', 'O') THEN 'Commuter' ELSE 'Resident'
    END AS residency_status,
    stu_serv_rec.stusv_no,
    id_rec.id, id_rec.lastname, id_rec.firstname, id_rec.middlename,
    id_rec.addr_line1, id_rec.addr_line2, id_rec.city, id_rec.st,
    id_rec.zip, id_rec.ctry, id_rec.phone,
    TRIM(cvid_rec.ldap_name) as ldap_name,
    cc_student_medical_manager.id as manid,
    cc_student_medical_manager.created_at,
    cc_student_medical_manager.sitrep,
    cc_student_medical_manager.sitrep_athlete,
    cc_student_medical_manager.concussion_baseline,
    cc_student_medical_manager.covid19_vaccine_card,
    cc_student_medical_manager.covid19_vaccine_card_status,
    cc_student_medical_manager.medical_consent_agreement,
    cc_student_medical_manager.medical_consent_agreement_status,
    cc_student_medical_manager.physical_evaluation_1,
    cc_student_medical_manager.physical_evaluation_status_1,
    cc_student_medical_manager.physical_evaluation_2,
    cc_student_medical_manager.physical_evaluation_status_2,
    cc_student_medical_manager.cc_student_immunization,
    cc_student_medical_manager.cc_student_meni_waiver,
    cc_student_medical_manager.cc_athlete_privacy_waiver,
    cc_student_medical_manager.cc_athlete_reporting_waiver,
    cc_student_medical_manager.cc_athlete_risk_waiver,
    cc_student_medical_manager.cc_athlete_sicklecell_waiver,
    cc_student_health_insurance.primary_card_front_status,
    cc_student_health_insurance.primary_card_back_status,
    cc_athlete_sicklecell_waiver.id as sicklecell_id,
    cc_athlete_sicklecell_waiver.updated_at,
    cc_athlete_sicklecell_waiver.waive,
    cc_athlete_sicklecell_waiver.proof,
    cc_athlete_sicklecell_waiver.results,
    cc_athlete_sicklecell_waiver.results_file,
    cc_athlete_sicklecell_waiver.results_file_status,
    cc_athlete_privacy_waiver.id as privacy_id,
    cc_athlete_privacy_waiver.news_media,
    cc_athlete_privacy_waiver.parents_guardians,
    cc_athlete_privacy_waiver.disclose_records,
    cc_student_meni_waiver.id as menid,
    cc_athlete_risk_waiver.id as risk_id,
    cc_athlete_reporting_waiver.id as reporting_id,
    profile_rec.birth_date,
    profile_rec.sex,
    prog_enr_rec.cl,
    mobile_rec.phone as mobile
FROM
    id_rec
INNER JOIN
    prog_enr_rec
ON
    id_rec.id = prog_enr_rec.id
LEFT JOIN
    cvid_rec
ON
    id_rec.id = cvid_rec.cx_id
LEFT JOIN
    cc_student_medical_manager
ON
    id_rec.id = cc_student_medical_manager.college_id
LEFT JOIN
    cc_student_meni_waiver
ON
    cc_student_medical_manager.id = cc_student_meni_waiver.manager_id
LEFT JOIN
    cc_student_health_insurance
ON
    cc_student_medical_manager.id = cc_student_health_insurance.manager_id
LEFT JOIN
    cc_athlete_sicklecell_waiver
ON
    id_rec.id = cc_athlete_sicklecell_waiver.college_id
AND
    (
        cc_athlete_sicklecell_waiver.proof = 1
    OR
        cc_athlete_sicklecell_waiver.created_at > "{0}"
    )
LEFT JOIN
    cc_athlete_privacy_waiver
ON
    cc_student_medical_manager.id = cc_athlete_privacy_waiver.manager_id
LEFT JOIN
    cc_athlete_risk_waiver
ON
    cc_student_medical_manager.id = cc_athlete_risk_waiver.manager_id
LEFT JOIN
    cc_athlete_reporting_waiver
ON
    cc_student_medical_manager.id = cc_athlete_reporting_waiver.manager_id
LEFT JOIN
    profile_rec
ON
    id_rec.id = profile_rec.id
LEFT JOIN
    stu_serv_rec
ON
    id_rec.id = stu_serv_rec.id
LEFT JOIN
    aa_rec as mobile_rec
ON
    (id_rec.id = mobile_rec.id AND mobile_rec.aa = "ENS")
""".format(START_DATE)

ACADEMIC_YEAR = """
SELECT
    id_rec.lastname, id_rec.firstname,
    cc_student_medical_manager.id,
    cc_student_medical_manager.college_id,
    cc_student_health_insurance.primary_policy_holder
FROM
    id_rec
LEFT JOIN
    cc_student_medical_manager
  ON
    id_rec.id = cc_student_medical_manager.college_id
LEFT JOIN
    cc_student_health_insurance
  ON
    cc_student_medical_manager.id = cc_student_health_insurance.manager_id
WHERE
    cc_student_medical_manager.college_id=
"""
