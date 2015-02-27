# -*- coding: utf-8 -*-
import os, sys

# env
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/data2/django_1.7/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djsani.settings")

from djsani.insurance.models import StudentHealthInsurance
from djsani.insurance.models import STUDENT_HEALTH_INSURANCE

from djzbar.settings import INFORMIX_EARL_TEST as INFORMIX_EARL
from djzbar.utils.informix import get_engine
from sqlalchemy.orm import sessionmaker

from optparse import OptionParser

from datetime import datetime

"""
Grabs a student's health insurance profile
"""

# set up command-line options
desc = """
Accepts as input a student's college ID
"""

parser = OptionParser(description=desc)
parser.add_option(
    "-i", "--ID",
    help="Studnet's college ID.",
    dest="cid"
)

def main():
    """
    main function
    """

    print "Student's college ID = {}".format(cid)

    engine = get_engine(INFORMIX_EARL)

    Session = sessionmaker(bind=engine)
    session = Session()
    #session.query(StudentHealthInsurance).\
    shi = session.query(StudentHealthInsurance).\
        filter_by(college_id=cid).first()
    #    update(STUDENT_HEALTH_INSURANCE)

    #shi.secondary_policy_holder = "Lauren Hansen"
    #dob = "1974-12-03"

    #dob = datetime.strptime("1974-12-03", "%Y-%m-%d")

    #shi.secondary_dob = "TO_DATE('{}', '%%Y-%%m-%%d')".format(dob)
    #shi.secondary_dob = dob

    print shi.__dict__

    #session.commit()

    session.close()

######################
# shell command line
######################

if __name__ == "__main__":
    (options, args) = parser.parse_args()
    cid = options.cid

    mandatories = ['cid',]
    for m in mandatories:
        if not options.__dict__[m]:
            print "mandatory option is missing: %s\n" % m
            parser.print_help()
            exit(-1)

    sys.exit(main())
