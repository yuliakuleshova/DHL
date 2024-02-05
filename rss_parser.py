from rss_parser import Parser
from requests import get  # noqa

rss_url = "https://www.reddit.com/.rss"
response = get(rss_url)

rss = Parser.parse(response.text)

# Print out rss meta data
print("Language", rss.channel.language)
print("RSS", rss.version)

# Iteratively print feed items
for item in rss.channel.items:
    print(item.title)
    print(item.description[:50])