""" Converting date and time"""

import datetime
import time

dt = "Sat, 30 Sep 2023 07:39:52 +0300".split(" ")
print(dt)
mnth = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Sep': 9}
tm = dt[4].split(":")
print(dt[3], mnth[dt[2]], dt[1], tm[0], tm[1], tm[2])

new_dt = datetime.datetime(int(dt[3]), int(mnth[dt[2]]), int(dt[1]), int(tm[0]), int(tm[1]), int(tm[2]))
unix_timestamp = time.mktime(new_dt.timetuple())
utc_timestamp = time.mktime(new_dt.utctimetuple())
print(unix_timestamp)
print(utc_timestamp)
