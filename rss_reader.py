""" RSS reader """

import argparse
import sqlite3
import requests
import pytz
import sys
import json

import time
from datetime import datetime

url = 'https://www.opennet.ru/opennews/opennews_all_utf.rss'
con = sqlite3.connect("opennet.sqlite")
cur = con.cursor()
answer = requests.get(url).text
all_news = []

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='Uses one of parameters',
                    epilog='Text at the bottom of help')

parser.add_argument('-c', '--count', help="Number of news to print")
parser.add_argument('-sd', '--search_by_date', help="Search by date")
parser.add_argument('-st', '--search_by_title', help="Search by title")
args = parser.parse_args()


def create_result_data(data: list):
    """
    :param data: list of dictionary all news
    :return: generate html code
    """

    html_header = ('<!DOCTYPE html><html lang="RU"><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" '
                   '/><head><title>All newses</title></head><body><ul id="navigation">')
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

    mnth = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12)
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
    start_interval = datetime(int(search_date[2]), int(search_date[1]), int(search_date[0]), 0, 0, 0)
    end_interval = datetime(int(search_date[2]), int(search_date[1]), int(search_date[0]), 23, 59, 59)
    start_interval = time.mktime(start_interval.timetuple())
    end_interval = time.mktime(end_interval.timetuple())
    search_interval = [start_interval, end_interval]
    return search_interval


def create_result_file(data: list):
    """
    :param data: list of dictionary all news
    :return: write generated html code to the file
    """

    f = open("news.html", "w", encoding="utf-8")
    f.write(create_result_data(data))
    f.close()


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


def json_to_text(json_data: json):
    ... # Написать функцию преобразования json данных в человеко-читаемый текст для отображения на экране
    text_from_json = ""
    return text_from_json # TODO следует использовать переносы строк '\n'


if __name__ == '__main__':
    for i in range(len(answer.split("\n"))):
        if answer.split("\n")[i] == '<item>':
            news = {}
            news['title'] = answer.split("\n")[i + 1].replace("<title>", "").replace("</title>", "").replace("    ", "")
            news['link'] = answer.split("\n")[i + 2].replace("<link>", "").replace("</link>", "").replace("    ", "")
            news['date'] = convert_to_unixtime(
                answer.split("\n")[i + 3].replace("<pubDate>", "").replace("</pubDate>", "").replace("    ", ""))
            news['decription'] = answer.split("\n")[i + 4].replace("<description>", "").replace("</description>",
                                                                                                "").replace("    ", "")
            query = cur.execute("SELECT 1 link FROM rss WHERE link=?", [news['link']]).fetchone()
            if not query:
                cur.execute("INSERT INTO rss VALUES (?, ?, ?, ?)",
                            (news['link'], news['title'], news['date'], news['decription']))
                con.commit()
            all_news.append(news)

    if args.count:
        if 1 <= int(args.count) <= 50:
            print(all_news[0:int(args.count)]) # TODO исправить отображение на человекочитаемое через фукцию обработки json'а
            # json_to_text(all_news[0:int(args.count)])
        elif int(args.count) > 50:
            print("print 50 news from url and count-50 from DB without DB update") # TODO всё что и выше + вытянуть из DB*
            # json_to_text(...)
        else:
            print(f"{args.count} is unacceptable value. Should be positive value")
        sys.exit(0)

    if args.search_by_date:
        print("Search in DB by date")
        sys.exit(0)

    if args.search_by_title:
        print("Search in DB by title")
        sys.exit(0)

    create_result_file(all_news)
