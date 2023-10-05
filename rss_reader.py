""" RSS reader """


import sqlite3
import requests
import pytz
import time
from datetime import datetime, timezone, timedelta


url = 'https://www.opennet.ru/opennews/opennews_all_utf.rss'
con = sqlite3.connect("opennet.sqlite")
cur = con.cursor()
answer = requests.get(url).text
all_news = []


def print_news(all_news, num = 5):
    """
    :param all_news:
    :param num:
    :return:
    """
    for i in range(num):
        print(all_news[i])
        print('/n')


def convert_to_unixtime(datatime: str):
    """
    :param datatime: input string with data and time
    :return: unix timestamp
    """
    mnth = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Sep': 9, 'Oct': 10}
    dt = datatime.split(" ")
    tm = dt[4].split(":")
    tz1 = pytz.timezone('Europe/Moscow')
    tz2 = pytz.timezone('UTC')
    new_dt = datetime(int(dt[3]), int(mnth[dt[2]]), int(dt[1]), int(tm[0]), int(tm[1]), int(tm[2]))
    dt = tz1.localize(new_dt)
    #print(dt, dt.astimezone(tz2))
    return time.mktime(dt.astimezone(tz2).timetuple())


for i in range(len(answer.split("\n"))):
    if answer.split("\n")[i] == '<item>':
        news = {}
        news['title'] = answer.split("\n")[i + 1].replace("<title>", "").replace("</title>", "").replace("    ", "")
        news['link'] = answer.split("\n")[i + 2].replace("<link>", "").replace("</link>", "").replace("    ", "")
        news['date'] = convert_to_unixtime(answer.split("\n")[i + 3].replace("<pubDate>", "").replace("</pubDate>", "").replace("    ", ""))
        news['decription'] = answer.split("\n")[i + 4].replace("<description>", "").replace("</description>",
                                                                                            "").replace("    ", "")
        query = cur.execute("SELECT 1 link FROM rss WHERE link=?", [news['link']]).fetchone()
        if not query:
            cur.execute("INSERT INTO rss VALUES (?, ?, ?, ?)",
                        (news['link'], news['title'], news['date'], news['decription']))
            con.commit()
        all_news.append(news)
