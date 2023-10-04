""" Converting date and time"""

import datetime
import time
from datetime import datetime, timezone, timedelta

dt = "Sat, 30 Sep 2023 07:39:52 +0300".split(" ")
print(dt)
mnth = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Sep': 9}
tm = dt[4].split(":")
print(dt[3], mnth[dt[2]], dt[1], tm[0], tm[1], tm[2])

new_dt = datetime(int(dt[3]), int(mnth[dt[2]]), int(dt[1]), int(tm[0]), int(tm[1]), int(tm[2]))
# unix_timestamp = time.mktime(new_dt.timetuple())
# utc_timestamp = time.mktime(new_dt.utctimetuple())
# print(unix_timestamp)
# print(utc_timestamp)

naive = datetime.now()
print("Naive DateTime:", naive)
UTC = datetime.now(timezone.utc)
print("UTC DateTime", UTC)
#msk_dateTime = datetime.now(timezone(timedelta(hours=+3), 'MCK'))
tz = list(dt[5])
print(tz)
tz1 = ''.join(tz[0:3])
print(tz1)
msk_dateTime = datetime.now(timezone(timedelta(hours=int(tz1)), 'MCK'))
print("In MSK::", msk_dateTime)