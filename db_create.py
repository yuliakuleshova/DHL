""" DB create """

import sqlite3
import requests
import argparse

con = sqlite3.connect("opennet.sqlite")
cur = con.cursor()
# cur.execute("create table rss(link, title, date, description)")

url = 'https://www.opennet.ru/opennews/opennews_all_utf.rss'
answer = requests.get(url).text
all_news = []

# link = "http://qqq.qq"
# query = cur.execute("SELECT 1 link FROM rss WHERE link=?", [link]).fetchone()
# print(query)

for i in range(len(answer.split("\n"))):
    if answer.split("\n")[i] == '<item>':
        news = {}
        news['title'] = answer.split("\n")[i + 1].replace("<title>", "").replace("</title>", "").replace("    ", "")
        news['link'] = answer.split("\n")[i + 2].replace("<link>", "").replace("</link>", "").replace("    ", "")
        news['date'] = answer.split("\n")[i + 3].replace("<pubDate>", "").replace("</pubDate>", "").replace("    ", "")
        news['decription'] = answer.split("\n")[i + 4].replace("<description>", "").replace("</description>",
                                                                                            "").replace("    ", "")
        query = cur.execute("SELECT 1 link FROM rss WHERE link=?", [news['link']]).fetchone()
        if not query:
            cur.execute("INSERT INTO rss VALUES (?, ?, ?, ?)",
                        (news['link'], news['title'], news['date'], news['decription']))
            con.commit()
        all_news.append(news)
