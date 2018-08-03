# -*- coding: utf-8 -*-
import json
import requests
from lxml import etree
from urllib import parse

BASE_URL = "https://www.instagram.com/urnotchrislee/"
headers = {
    "Origin": "https://www.instagram.com/",
    "Referer": "https://www.instagram.com/chen_ai_ling51/",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Host": "www.instagram.com"}


def load_rest(table, has_next_page):
    rest = []
    while has_next_page:
        text = json.dumps(table)
        end_cursor = data['page_info']['end_cursor']
        has_next_page = data['page_info']['has_next_page']

        for node in nodes:
            rest.append(node['node']['display_url'])
            # print(node['node']['display_url'])
        table['after'] = end_cursor
        print('加载..')
    print('加载完成')
    return rest


if __name__ == '__main__':

    res = requests.get(BASE_URL, headers=headers)
    html = etree.HTML(res.content.decode())
    #    h = html.xpath('''//script[@type="text/javascript"]/text()''')[1].replace('window._sharedData =','').strip()
    h = html.xpath('''//script[@type="text/javascript"]''')[1].text.replace('window._sharedData = ', '').strip()[:-1]
    dic = json.loads(h, encoding='utf-8')

    data = dic['entry_data']['ProfilePage'][0]['user']['media']
    nodes = data['nodes']
    end_cursor = data['page_info']['end_cursor']
    has_next_page = data['page_info']['has_next_page']
    lee_id = nodes[0]["owner"]["id"]  # '1161353543'

    src_list = []
    for node in nodes:
        src_list.append(node['display_src'])
        print(node['display_src'])
    print('加载')

    table = {
        'id': lee_id,
        'first': 12,
        'after': end_cursor}
    rest = load_rest(table, has_next_page)
    src_list = src_list + rest
    print(len(src_list))

    #    with open('abc', 'w') as f:
    #    for s in src_list:
    #        f.write(s)
    #        f.write('\n')

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/58.0.3029.110 Safari/537.36", }
    for i in range(len(src_list)):
        url = src_list[i].strip()
        res = requests.get(url, headers=headers)
        with open('第' + str(i + 1) + '张.jpg', 'wb') as ff:
            ff.write(res.content)
