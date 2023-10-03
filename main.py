""" DHL Tracking """


import requests
import yaml

with open("dhl.secret", "r", encoding="utf-8") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# print(config['id'])
# print(config['base_url'])

# new_url = f"{config['base_url']}{config['id'][0]}"
# print(new_url)
headers = {'user-agent': 'Chrome/116.0.0.0'}

new_url = f"{config['base_url']}{config['id'][0]}"
print(new_url)

answer = requests.get(new_url, headers=headers).text
print(answer)

exit(0)

def get_content(new_url):
    answer = requests.get(new_url, headers=headers).text
    print(answer)
    # используя каждый url из списка делать обращение на сайт и возвращать контент


def get_urls(config):
    for i in range(len(config['id'])):
        new_url = f"{config['base_url']}{config['id'][i]}"
        print(new_url)
        get_content(new_url)
    return
    # создать n-urls из base_url и id


get_urls(config)
