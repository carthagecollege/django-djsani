django-djsani
==============

Django apps for the Health and Counseling Centre

# Apache Configuration

    # Health & Counceling medical forms app
    <Location /campus-life/medical/forms>
    WSGIProcessGroup djsani
    WSGIApplicationGroup djsani
    </Location>
    WSGIDaemonProcess djsani user=www-data group=www-data processes=1 threads=5
    #WSGIImportScript /d2/django_projects/djsani/wsgi process-group=djsani application-group=djsani
    WSGIScriptAlias /campus-life/medical/forms "/data2/django_projects/djsani/wsgi.py"

# odbc.ini configuration

    [MSSQL-PYTHON]
    Description             = PortalMSSQL
    Driver                  = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
    #Driver                  = FreeTDS [works with tools like osql, isql, etc
    Server                  = 10.2.6.24
    Port                    = 1433
    User                    = xxxxxxxxx
    Password                = xxxxxxxxx
    Database                = ICS_NET
    Trace                   = Yes
    TraceFile               = /tmp/odbc.trace
    TDS_Version             = 8.0

# odbcinst.ini configuration

    [FreeTDS]
    Description     = TDS driver (Sybase/MS SQL)
    Driver          = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
    Setup           = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so
    CPTimeout       =
    CPReuse         =
    FileUsage       = 1

# Informix schemas

    /opt/carsi/schema/development/

    CCAthleteMedicalHistory
    CCAthletePrivacyWaiver
    CCAthleteReportingWaiver
    CCAthleteRiskWaiver
    CCAthleteSickleCellWaiver
    CCStudentHealthInsurance
    CCStudentMedicalContentType
    CCStudentMedicalHistory
    CCStudentMedicalLogEntry
    CCStudentMedicalManager
    CCStudentMeniWaiver

# Notes

Reminder for sqlalchemy and informix with Django:

Informix Boolean uses SMALLINT on the DDL side (0 or 1)
and on the Python side we deal in True or False. For
Django templates you have to use explicit comparisons:

{% if oo == "True" %}

whereas the following will resolve to true:

{% if oo %}

if oo has a value of "False".
