INSERT INTO cc_student_health_insurance (
primary_company,
secondary_member_id,
secondary_policy_type,
secondary_address,
primary_policy_state,
primary_phone,
primary_dob,
secondary_group_no,
secondary_company,
primary_group_no,
secondary_dob,
cid,
primary_address,
primary_policy_holder,
secondary_phone,
secondary_dob,
primary_policy_type,
secondary_policy_state,
primary_member_id,
opt_out,
secondary_policy_holder)
VALUES (
'company1',
'432523467',
'State Insurance',
'1313 mockingbird lane springfield MA 08003 suite16',
'',
'333-444-5555',
'1972-02-02',
'3456772346',
'company2',
'343423566',
'1979-02-04',
1338012,
'1313 mockingbird lane springfield MA 08003',
'policy1',
'333-555-6666',
'1974-12-21',
'PPO',
'AK',
'980808080',
0,
'policy2')

UPDATE cc_student_health_insurance SET primary_company='company1',
secondary_member_id='432523467',
secondary_policy_type='State Insurance',
primary_policy_state='',
primary_phone='333-444-5555',
primary_dob=TO_DATE('1972-12-21', '%Y-%m-%d'),
secondary_group_no='3456772346',
secondary_company='company2',
primary_group_no='343423566',
secondary_dob=TO_DATE('1974-05-01', '%Y-%m-%d'),
cid=1338012,
primary_policy_address='1313 mockingbird lane
suite 16
Springfield, MA 08003',
secondary_policy_address='1313 mockingbird lane
suite 16
Springfield, MA 08003',
primary_policy_holder='policy1',
secondary_phone='357-980-8338',
primary_policy_type='PPO',
secondary_policy_state='HI',
primary_member_id='980808080',
opt_out=0,
secondary_policy_holder='policy2' WHERE cid=1338012
