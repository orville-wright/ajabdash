#!/usr/bin/python3

SLOOP_URL = "https://www.schoolloop.com/"
SLOOP_MY_SCHOOL = "https://ois-orinda-ca.schoolloop.com/"
LOGIN = "portal/login/"

# Portal main URL home pages
PARENT_HOME = "portal/parent_home/"
MAIL = "loopmail/inbox?d=x"
CALENDAR = "calendar/month/"

# Print page URL's
# https://ois-orinda-ca.schoolloop.com/portal/parent_home?d=x&template=print
PRINT_PHOME_1 = "?d=x&template=print"         # not sure of diff between these 2
PRINT_PHOME_2 = "?template=print"             # not sure of diff between these 2
PRINT_ATTEND = "?template=print_attendance"

# Zero alert url
#  https://ois-orinda-ca.schoolloop.com/student/zeros?d=x&return_url=1569955562286
# I am unsure of the diff between the yet (at the moment
ZERO_ALERT_0 = "student/zeros"
ZERO_ALERT_1 = "student/zeros?d=x&return_url=1569955562286"

# Progress report URL structure
# https://ois-orinda-ca.schoolloop.com/progress_report/report?d=x&id=1500709128492&period_id=1563866703231&mark_id=current
PROGRESS_REPORT = "progress_report/"
PROGRESS_MTH = "report?d=x&id=1500709128492&period_id=1563866702852&mark_id=current"
PROGRESS_SCI = "report?d=x&id=1500709128492&period_id=1563866702812&mark_id=current"
PROGRESS_COR = "report?d=x&id=1500709128492&period_id=1563866703090&mark_id=current"
PROGRESS_WWK = "report?d=x&id=1500709128492&period_id=1563866703279&mark_id=current"
PROGRESS_PHE = "report?d=x&id=1500709128492&period_id=1563866703231&mark_id=current"
