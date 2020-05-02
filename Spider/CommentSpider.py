#coding:utf-8
import requests
import codecs
import re
import json
from SpiderBase import SpiderBase


class CommentSpider(SpiderBase):
    def __init__(self, pid):
        super().__init__()
        self.baseUrl='https://club.jd.com/comment/productPageComments.action?callback=' \
              'fetchJSON_comment98vv37157&productId={}&score=0' \
              '&sortType=6&page={}&pageSize=10&isShadowSku=0&fold=1'.format(pid,"{}")

    def get_data(self, filename):
        with open(filename, 'a', encoding='utf-8') as file:
            for page in range(1000):
                try:
                    url = self.baseUrl.format(page)
                    data = self.session.get(url)
                    data = re.sub(r'fetchJSON_comment98vv37157\(', '',
                                  data.text)
                    data = data[:-2]
                    data = json.loads(data)
                    for each in data['comments']:
                        file.write(each['content'].strip('\n') + '\n')
                    print(url)
                    print('Finished!')
                except:
                    print('error')
                    pass