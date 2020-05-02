import re
import json
from lxml import etree
from urllib.parse import quote
from SpiderBase import SpiderBase
from MyThread import MyThread


class SearchSpider(SpiderBase):
    def __init__(self, keyword):
        super().__init__()
        #print(keyword)
        self.data = []
        self.baseUrl = 'https://search.jd.com/Search?keyword=' + quote(
            keyword) + '&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page={}&s=1&click=0'

    def get_data(self):
        print('搜索开始')
        try:
            head = {
                'authority':
                'search.jd.com',
                'method':
                'GET',
                'path':
                '/s_new.php?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=4&s=84&scrolling=y&log_id=1529828108.22071&tpl=3_M&show_items=7651927,7367120,7056868,7419252,6001239,5934182,4554969,3893501,7421462,6577495,26480543553,7345757,4483120,6176077,6932795,7336429,5963066,5283387,25722468892,7425622,4768461',
                'scheme':
                'https',
                'referer':
                'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=3&s=58&click=0',
                'user-agent':
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
                'x-requested-with':
                'XMLHttpRequest',
                'Cookie':
                'qrsc=3; pinId=RAGa4xMoVrs; xtest=1210.cf6b6759; ipLocation=%u5E7F%u4E1C; _jrda=5; TrackID=1aUdbc9HHS2MdEzabuYEyED1iDJaLWwBAfGBfyIHJZCLWKfWaB_KHKIMX9Vj9_2wUakxuSLAO9AFtB2U0SsAD-mXIh5rIfuDiSHSNhZcsJvg; shshshfpa=17943c91-d534-104f-a035-6e1719740bb6-1525571955; shshshfpb=2f200f7c5265e4af999b95b20d90e6618559f7251020a80ea1aee61500; cn=0; 3AB9D23F7A4B3C9B=QFOFIDQSIC7TZDQ7U4RPNYNFQN7S26SFCQQGTC3YU5UZQJZUBNPEXMX7O3R7SIRBTTJ72AXC4S3IJ46ESBLTNHD37U; ipLoc-djd=19-1607-3638-3638.608841570; __jdu=930036140; user-key=31a7628c-a9b2-44b0-8147-f10a9e597d6f; areaId=19; __jdv=122270672|direct|-|none|-|1529893590075; PCSYCityID=25; mt_xid=V2_52007VwsQU1xaVVoaSClUA2YLEAdbWk5YSk9MQAA0BBZOVQ0ADwNLGlUAZwQXVQpaAlkvShhcDHsCFU5eXENaGkIZWg5nAyJQbVhiWR9BGlUNZwoWYl1dVF0%3D; __jdc=122270672; shshshfp=72ec41b59960ea9a26956307465948f6; rkv=V0700; __jda=122270672.930036140.-.1529979524.1529984840.85; __jdb=122270672.1.930036140|85.1529984840; shshshsID=f797fbad20f4e576e9c30d1c381ecbb1_1_1529984840145'
            }
            k = 1
            data = self.session.get(self.baseUrl.format(k), headers=head)
            text = data.text.encode(data.encoding).decode('utf-8')
            html = etree.HTML(text)
            lis = html.xpath('//*[@id="J_goodsList"]/ul/li[@class="gl-item"]')
            for li in lis:
                pid = li.xpath('./@data-sku')
                name = li.xpath(
                    './/div[contains(@class, "p-name")]//em/text()')
                price = li.xpath(
                    './/div[contains(@class, "p-price")]//i/text()')
                img = li.xpath('.//div[contains(@class,"p-img")]//img/@src')
                shop = li.xpath('.//div[contains(@class, "p-shop")]//a/text()')
                self.data.append({
                    'name':
                    ",".join(str(i) for i in name),
                    'price':
                    'null' if len(price) == 0 else price[0],
                    'shop':
                    'null' if len(shop) == 0 else shop[0],
                    'img':
                    'null' if len(img) == 0 else img[0],
                    'pid':
                    'null' if len(pid) == 0 else pid[0]
                })
            print('搜索完成')
            return self.data
        except Exception as e:
            print('SearchSpiderError:%s' % e)
            pass