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

def create_result_data(date: list):
    """
    :param date:
    :return: write search results to the file
    """
    HEADER = '<!DOCTYPE html><html lang="RU"><head><title>All newses</title></head><body><ul id="navigation">'
    BODY = ''
    FOOTER = '</ul></body></html>'

    for item in date:
        BODY = BODY+f'<li><a href="{item['link']}">{item['title']}</a></li>'
    return HEADER+BODY+FOOTER


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


def get_search_interval(date: str):
    """
    :param date: Input data for search into dd:mm:yyyy format
    :return:
    """
    search_date = date.split(":")
    start_interval = datetime(int(search_date[2]), int(search_date[1]), int(search_date[0]), 0, 0, 0)
    end_interval = datetime(int(search_date[2]), int(search_date[1]), int(search_date[0]), 23, 59, 59)
    start_interval = time.mktime(start_interval.timetuple())
    end_interval = time.mktime(end_interval.timetuple())
    search_interval = [start_interval, end_interval]
    return search_interval


def create_result_file(date: list):
    """
    :param date:
    :return: write search results to the file
    """


def get_news_from_date(date: str):
    """
    :param date: Input data for search into dd:mm:yyyy format
    :return: List of dictionaries of news from the date
    """
    search_interval = get_search_interval(date)
    news_from_date = cur.execute("SELECT link, title, date, description FROM rss WHERE date <= ? AND date >= ?",
                                 (search_interval[1], search_interval[0])).fetchall()
    print(news_from_date)
    return news_from_date


for i in range(len(answer.split("\n"))):
    if answer.split("\n")[i] == '<item>':
        news = {}
        news['title'] = answer.split("\n")[i + 1].replace("<title>", "").replace("</title>", "").replace("    ", "")
        news['link'] = answer.split("\n")[i + 2].replace("<link>", "").replace("</link>", "").replace("    ", "")
        news['date'] = convert_to_unixtime(answer.split("\n")[i + 3].replace("<pubDate>", "").replace("</pubDate>", "").replace("    ", ""))
        news['decription'] = answer.split("\n")[i + 4].replace("<description>", "").replace("</description>",
                                                                                            "").replace("    ", "")
        #print(news['link'])
        query = cur.execute("SELECT 1 link FROM rss WHERE link=?", [news['link']]).fetchone()
        if not query:
            cur.execute("INSERT INTO rss VALUES (?, ?, ?, ?)",
                        (news['link'], news['title'], news['date'], news['decription']))
            #print('Added to DB')
            con.commit()
        #else:
            #print('Found in DB')
        all_news.append(news)

#print(str(all_news).replace('\'', '"'))
# news_json = json.loads(str(all_news).replace('\'', '"'))
# #print(news_json)
# # Homework: Use json.load to put raw strings into news_json
# news_yaml = yaml.dump(news_json, allow_unicode=True)
# #print(news_yaml)
# data_yaml = {}
# data_yaml['RSS'] = news_json
# print(yaml.dump(data_yaml, allow_unicode=True))

print(create_result_data(all_news))
# with open('template.j2', 'r', encoding='utf-8') as j2:
#     html_text = jinja2.Template(j2)
#
# print(html_text.render(yaml.dump(data_yaml, allow_unicode=True)))

# Homework: find out about sorting
# Template

#get_news_from_date("05:10:2023")
