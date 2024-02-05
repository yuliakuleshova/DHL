""" RSS reader """

#TODO Add config file with some sources (urls)
# Refactor function get_news_from_site()
# - Use parcer for xml
# OpenNet RSS https://www.opennet.ru/opennews/opennews_all_utf.rss to parse with rss-parser, xmltodict, elementtree
# in separate python scripts. Write down the questions.
# Add read-only to DB
# Add DB for each source
#

import argparse
import sqlite3
import sys
import json
import time
from datetime import datetime
import pytz
import requests

url = 'https://www.opennet.ru/opennews/opennews_all_utf.rss'
con = sqlite3.connect("opennet.sqlite")
cur = con.cursor()
answer = requests.get(url, timeout=10).text
all_news = []

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='Uses one of parameters',
                    epilog='Text at the bottom of help')

parser.add_argument('-c', '--count', help="Number of news to print")
parser.add_argument('-sd', '--search_by_date',
                    help="Search by date, input date in dd:mm:yyyy format")
parser.add_argument('-st', '--search_by_title', help="Search by title")
args = parser.parse_args()


def create_result_data(data: list):
    """
    :param data: list of dictionary all news
    :return: generate html code
    """

    html_header = (
        '<!DOCTYPE html>'
        '<html lang="RU">'
        '<meta http-equiv="Content-Type" '
        'content="text/html; '
        'charset=UTF-8" '
        '/>'
        '<head>'
        '<title>All newses</title>'
        '</head>'
        '<body>'
        '<ul id="navigation">'
    )
    html_body = ''
    html_footer = '</ul></body></html>'

    for item in data:
        html_body = html_body + f'<li><a href="{item['link']}">{item['title']}</a></li>'
    return html_header + html_body + html_footer


def print_news(all_news, num=5):
    """
    :param all_news: list of dictionary all news
    :param num: number of news to print
    :return: print news
    """

    for i in range(num):
        print(all_news[i])
        print('/n')


def convert_to_unixtime(datatime: str):
    """
    :param datatime: input string with data and time
    :return: unix timestamp
    """

    mnth = dict(
        Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12
    )
    dt = datatime.split(" ")
    tm = dt[4].split(":")
    tz1 = pytz.timezone('Europe/Moscow')
    tz2 = pytz.timezone('UTC')
    new_dt = datetime(int(dt[3]), int(mnth[dt[2]]), int(dt[1]), int(tm[0]), int(tm[1]), int(tm[2]))
    dt = tz1.localize(new_dt)
    return time.mktime(dt.astimezone(tz2).timetuple())


def get_search_interval(date: str):
    """
    :param date: Input data for search into dd:mm:yyyy format
    :return:
    """
    search_date = date.split(":")
    start_interval = datetime(
        int(search_date[2]), int(search_date[1]), int(search_date[0]), 0, 0, 0
    )
    end_interval = datetime(
        int(search_date[2]), int(search_date[1]), int(search_date[0]), 23, 59, 59
    )
    start_interval = time.mktime(start_interval.timetuple())
    end_interval = time.mktime(end_interval.timetuple())
    search_interval = [start_interval, end_interval]
    return search_interval


def create_result_file(data: list):
    """
    :param data: list of dictionary all news
    :return: write generated html code to the file
    """

    f = open("news.html", "w", encoding="utf-8") #TODO rewrite to use with
    f.write(create_result_data(data))
    f.close()


def json_to_text(json_data: json):
    """
    :param json_data:
    :return:
    """

    text_from_json = ""
    for news in json_data:
        for value in news.values():
            text_from_json = text_from_json + str(value) + '\n'
    return text_from_json


def get_news_from_date(date: str):
    """
    :param date: Input data for search into dd:mm:yyyy format
    :return: List of dictionaries of news from the date
    """
    search_interval = get_search_interval(date)
    print(int(search_interval[1]), int(search_interval[0]))
    news_from_date = cur.execute(
        "SELECT link, title, date, description FROM rss WHERE date <= ? AND date >= ?",
        (int(search_interval[1]), int(search_interval[0]))
    ).fetchall()

    return news_from_date


def search_by_title(title_par: str):
    """
    :param title: Input data for search by title
    :return: List of dictionaries of news contained title
    """
    title_par = "%" + title_par + "%"
    news_by_title = cur.execute(
        "SELECT link, title, date, description FROM ("
        "SELECT * FROM rss ORDER BY link DESC"
        ") WHERE title LIKE ?",
        (str(title_par),)
    ).fetchall()

    news_from_db = []
    for title, link, date, description in news_by_title:
        news = {}
        news['title'] = title
        news['link'] = link
        news['date'] = date
        news['description'] = description
        news_from_db.append(news)
    return news_from_db


def get_news_from_site(): #TODO refactor the function
    """
    :return:
    """
    for i in range(len(answer.split("\n"))):
        if answer.split("\n")[i] == '<item>':
            news = {}
            news['title'] = answer.split("\n")[i + 1].replace("<title>", "").replace("</title>", "").replace("    ", "")
            news['link'] = answer.split("\n")[i + 2].replace("<link>", "").replace("</link>", "").replace("    ", "")
            news['date'] = convert_to_unixtime(
                answer.split("\n")[i + 3].replace("<pubDate>", "").replace("</pubDate>", "").replace("    ", ""))
            news['description'] = answer.split("\n")[i + 4].replace("<description>", "").replace("</description>",
                                                                                                "").replace("    ", "")
            query = cur.execute("SELECT 1 link FROM rss WHERE link=?", [news['link']]).fetchone()
            if not query:
                cur.execute("INSERT INTO rss VALUES (?, ?, ?, ?)",
                            (news['link'], news['title'], news['date'], news['decription']))
                con.commit()
            all_news.append(news)
    return all_news


def get_from_db(count: int):
    """
    :param count:
    :return:
    """
    limit = count
    news_from_site_db = []
    get_news_from_site()
    cur.execute(
    "SELECT link, title, date, description FROM ("
          "SELECT * FROM rss ORDER BY link DESC"
          ") AS A LIMIT ?", (str(limit),)
    )
    rows = cur.fetchall()
    for title, link, date, description in rows:
        news = {}
        news['title'] = title
        news['link'] = link
        news['date'] = date
        news['description'] = description
        news_from_site_db.append(news)
    return news_from_site_db


def qwert():

    if args.count:
        if 1 <= int(args.count) <= 50:
            print(json_to_text(all_news[0:int(args.count)]))
        elif int(args.count) > 50:
            print(len(get_from_db(int(args.count))))
        else:
            print(f"{args.count} is unacceptable value. Should be positive value")
        sys.exit(0)

    if args.search_by_date:
        print("Search in DB by date in dd:mm:yyyy format")
        print(get_news_from_date(str(args.search_by_date)))

        sys.exit(0)

    if args.search_by_title:
        print("Search in DB by title") #TODO to find how to search case insensitive in RU
        print(json_to_text(search_by_title(args.search_by_title)))
        sys.exit(0)

    create_result_file(all_news) #TODO fix function create_result_file


if __name__ == '__main__':
    qwert()
