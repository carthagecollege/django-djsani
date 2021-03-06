SELECT UNIQUE
    id_rec.lastname,id_rec.firstname,id_rec.id,
    cc_student_medical_manager.athlete,
    cc_student_medical_manager.sports,
    cc_student_medical_manager.cc_student_medical_history,
    cc_student_medical_manager.cc_student_health_insurance,
    cc_student_medical_manager.cc_student_meni_waiver,
    cc_student_medical_manager.cc_student_immunization,
    cc_student_medical_manager.cc_athlete_medical_history,
    cc_student_medical_manager.cc_athlete_privacy_waiver,
    cc_student_medical_manager.cc_athlete_reporting_waiver,
    cc_student_medical_manager.cc_athlete_risk_waiver,
    cc_student_medical_manager.cc_athlete_sicklecell_waiver,
    cc_athlete_sicklecell_waiver.waive,
    cc_athlete_sicklecell_waiver.proof,
    cc_athlete_sicklecell_waiver.results,
    prog_enr_rec.lv_date,
    prog_enr_rec.re_entry_date,
    prog_enr_rec.subprog,
    prog_enr_rec.acst,
    stu_acad_rec.sess,
    stu_acad_rec.reg_hrs
FROM
    id_rec
INNER JOIN
    prog_enr_rec ON  id_rec.id = prog_enr_rec.id
LEFT JOIN
    cc_student_medical_manager ON id_rec.id = cc_student_medical_manager.college_id
LEFT JOIN
    cc_athlete_sicklecell_waiver ON id_rec.id = cc_athlete_sicklecell_waiver.college_id
LEFT JOIN
    stu_acad_rec ON  id_rec.id = stu_acad_rec.id
WHERE
    id_rec.id = 1311939;
