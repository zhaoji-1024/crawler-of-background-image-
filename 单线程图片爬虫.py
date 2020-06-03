import  requests
from lxml import etree

class ImageSpider(object):

    def __init__(self):
        self.base_url = "http://sc.chinaz.com/tupian/beijingtupian_{}.html"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
        }

    # 请求方法
    def get_html_text(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.content.decode()
        else:
            return None


    #解析列表页返回图片url列表
    def parse_list_page(self, text):
        html = etree.HTML(text)
        images_tag = html.xpath("//div[@class='box picblock col3']")
        items = []
        for i_t in images_tag:
            item = {}
            item["title"] = i_t.xpath(".//img/@alt")[0]
            item["url"] = i_t.xpath(".//img/@src2")[0]
            items.append(item)
        return items


    #保存图片到本地
    def save_imgs_toLocal(self, img_url, img_title):
        with open("./data/单线程背景图片爬虫/" + img_title + ".jpg", "wb") as fp:
            fp.write(requests.get(img_url, headers=self.headers).content)
            print(img_title + "save to local direction sucessfully...")



    #主方法
    def run(self):
        for i in range(2,80):
            text = self.get_html_text(self.base_url.format(i))
            data = self.parse_list_page(text)
            for d in data:
                self.save_imgs_toLocal(d["url"], d["title"])



if __name__ == '__main__':
    isr = ImageSpider()
    isr.run()