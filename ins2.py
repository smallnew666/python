# -*- coding: utf-8 -*-
import json
import requests
from lxml import etree
from urllib import parse
import os  #导入os模块

from ins import load_rest


class instagramPicture():
    def __init__(self,name):  # 类的初始化操作
        self.BASE_URL = "https://www.instagram.com/"+name
        self.headers = {
        "Origin": "https://www.instagram.com/",
        "Referer": "https://www.instagram.com/"+name+"/",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "cookie": "shbid=17582; mid=W2OqxwAEAAG0kthQcimh0r6VnzZY; rur=ASH; mcd=3; fbm_124024574287414=base_domain=.instagram.com; csrftoken=LTV3OZMArvyHUBp8nlyXwtf7FigQt1Go; ds_user_id=3462580244; sessionid=IGSCf466c7d6ca72a7f2f2acd8d0dc8e8dd5b02f298eae780e2d2fe96b92c78e1a5e%3AG1zkkb2IkHBatwioP1FxONlEii8Q35if%3A%7B%22_auth_user_id%22%3A3462580244%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_platform%22%3A4%2C%22_token_ver%22%3A2%2C%22_token%22%3A%223462580244%3AJxXQZhUr6NqiyzrKOE38EsUTQQvFnU0O%3Acc111edcd666f17a509d157188c87f17bea78f35258d9451413117a833b9c09e%22%2C%22last_refreshed%22%3A1533261693.825915575%7D; fbsr_124024574287414=P2BENsNy0BI74TVQE-uBGm0Gs9vyMblSoKXbNHZqJEA.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUURsYjQ3Y01SSUlSMDR6Ylg2cVlmeVVaaTVkeENEWGtkYVllblBkcjR6M1dObV9uXzNEa1kzVjBncTNyc2xCTkRkYk5hR1hPdWJMN0VtVjNwSzgtS21ZLTF5YzB6aFpYMERqdkFORDN4YUxyaGFHck81R3d5QXRXN1Q1QWpCQy1KanZ6SVdEaXpCTTlSN3dkVm44ek5qQW4wWE9nb2Y4a0RkczI3Y0lJUnZ0UDd6aDdOdzVlX0dGYlUza2I3cVNzNUdNWnh4c0RmckxJR2ZYT1dyNmJfdW16djVjNmdEQ2ZsaEpmM0M5SlVTYUJrQmtHWjh1Q05lZl9FOEw2VDFycjEwTXBNTXpkbGh3RUtjTnlfRTFXd1p0cHZXc2psOWNFTVgxblFYTGxtUDNjbFRhdW5JYTNRdnNWVkV1LWU0a1lkWjZsOWlGbF9jMEYyYUFCR0lyUEtBQiIsImlzc3VlZF9hdCI6MTUzMzI2NDk3MSwidXNlcl9pZCI6IjEwMDAwMjI2Mzc3NzExNiJ9; urlgen=",
        "Host": "www.instagram.com"}#header
        self.folder_path = 'F:\BeautifulPicture'  # 设置图片要存放的文件目录

    def load_rest(table, has_next_page):
        rest = []
        while has_next_page:
            text = json.dumps(table)
            URL = 'https://www.instagram.com/graphql/query/?query_hash=bd0d6d184eefd4d0ce7036c11ae58ed9&variables=' + parse.quote(text)
            res = requests.get(URL, headers=headers)
            dic = json.loads(res.content.decode(), encoding='utf-8')

            data = dic['data']['user']['edge_owner_to_timeline_media']
            nodes = data['edges']
            end_cursor = data['page_info']['end_cursor']
            has_next_page = data['page_info']['has_next_page']

            for node in nodes:
                rest.append(node['node']['display_url'])
                print(node['node']['display_url'])
            table['after'] = end_cursor
            print('加载..')
        print('加载完成')
        return rest

    def get_pic(self):
        res = requests.get(self.BASE_URL, headers=self.headers)
        html = etree.HTML(res.content.decode())
        #    h = html.xpath('''//script[@type="text/javascript"]/text()''')[1].replace('window._sharedData =','').strip()
        h = html.xpath('''//script[@type="text/javascript"]''')[3].text.replace('window._sharedData = ', '').strip()[
            :-1]
        dic = json.loads(h, encoding='utf-8')
        data = dic['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']
        nodes = data['edges']
        end_cursor = data['page_info']['end_cursor']
        has_next_page = data['page_info']['has_next_page']
        lee_id = dic['entry_data']['ProfilePage'][0]['graphql']['user']["id"]  # '88976'
        src_list = []
        # print(nodes[0]['node']['display_url'])
        for node in nodes:
            src_list.append(node['node']['display_url'])
            print(node['node']['display_url'])
        print('加载')

        table = {
            'id': lee_id,
            'first': 12,
            'after': end_cursor}
        rest = load_rest(table, has_next_page)
        src_list = src_list + rest
        print('开始创建文件夹')
        is_new_folder = self.mkdir(self.folder_path)  # 创建文件夹
        print('开始切换文件夹')
        os.chdir(self.folder_path)  # 切换路径至上面创建的文件夹

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/58.0.3029.110 Safari/537.36", }
        for i in range(len(src_list)):
            url = src_list[i].strip()
            print("正在保存第"+str(i+1)+"张图片")
            imgurls = url.split('/')
            img_name = imgurls[len(imgurls)-1]
            res = requests.get(url, headers=headers)
            with open(img_name, 'wb') as ff:
                ff.write(res.content)
        ff.close()
        #print(len(src_list))

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print('创建名字叫做', path, '的文件夹')
            os.makedirs(path)
            print('创建成功！')
        else:
            print(path, '文件夹已经存在了，不再创建')

inspic = instagramPicture("smallnew666")  #创建类的实例
inspic.get_pic()  #执行类中的方法

