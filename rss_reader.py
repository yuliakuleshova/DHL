""" RSS reader """


import requests


def print_news(all_news, num = 5):
    """
    :param all_news:
    :param num:
    :return:
    """
    for i in range(num):
        print(all_news[i])
        print('/n')

#    print(all_news[0:num-1])


url = 'https://www.opennet.ru/opennews/opennews_all_utf.rss'

answer = requests.get(url).text
# print(len(answer.split("\n")))
# print(answer.split("\n"))
all_news = []

for i in range(len(answer.split("\n"))):
    if answer.split("\n")[i] == '<item>':
        news = {}
        news['title'] = answer.split("\n")[i+1].replace("<title>", "").replace("</title>", "").replace("    ", "")
        news['link'] = answer.split("\n")[i + 2].replace("<link>", "").replace("</link>", "").replace("    ", "")
        news['date'] = answer.split("\n")[i + 3].replace("<pubDate>", "").replace("</pubDate>", "").replace("    ", "")
        news['decription'] = answer.split("\n")[i + 4].replace("<description>", "").replace("</description>", "").replace("    ", "")
        all_news.append(news)

print_news(all_news)
