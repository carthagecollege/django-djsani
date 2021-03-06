/* table cc_student_medical_history */

CREATE TABLE cc_student_medical_history
(
    /* core */
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    cid                     INT(11) NOT NULL,
    created_at DATETIME NOT NULL,
    /* medical questions/explanations */
    allergies_medical       VARCHAR(255),
    allergies_other         VARCHAR(255),
    anemia                  VARCHAR(255),
    anxiety                 VARCHAR(255),
    bronchospasm            VARCHAR(255),
    adhd_add                VARCHAR(255),
    birth_defect            VARCHAR(255),
    blood_disorder          VARCHAR(255),
    bronchitis              VARCHAR(255),
    cancer                  VARCHAR(255),
    chicken_pox             VARCHAR(255),
    counseling              VARCHAR(255),
    depression              VARCHAR(255),
    diabetes                VARCHAR(255),
    eating_disorder         VARCHAR(255),
    ent_disorder            VARCHAR(255),
    headaches               VARCHAR(255),
    head_injury             VARCHAR(255),
    heart_condition         VARCHAR(255),
    hepatitis               VARCHAR(255),
    hernia                  VARCHAR(255),
    hyper_tension           VARCHAR(255),
    hiv_aids                VARCHAR(255),
    hospitalizations        VARCHAR(255),
    ibd                     VARCHAR(255),
    kidney_urinary          VARCHAR(255),
    medications             VARCHAR(255),
    meningitis              VARCHAR(255),
    mononucleosis           VARCHAR(255),
    mrsa                    VARCHAR(255),
    organ_loss              VARCHAR(255),
    pneumonia               VARCHAR(255),
    rheumatic_fever         VARCHAR(255),
    seizure_disorder        VARCHAR(255),
    stroke                  VARCHAR(255),
    substance_abuse         VARCHAR(255),
    thyroid_disorder        VARCHAR(255),
    tuberculosis            VARCHAR(255),
    other_condition         VARCHAR(255)
);
