import re
import requests
from lxml import etree


def urlChange(url, page_num):
    page_group = []
    page_group.append('http://www.bytravel.cn/view/index109_list.html')
    now_page = int(re.search(('_list(\d+)'), url, re.S).group(1))
    for i in range(now_page, page_num):
        link = re.sub('_list\d+', '_list%d' % i, url, re.S)
        page_group.append(link)
    return page_group


def viewDict(html, title_xpath, content_xpath, img_xpath):
    selector = etree.HTML(html)
    title = selector.xpath(title_xpath)
    content = selector.xpath(content_xpath)
    img = selector.xpath(img_xpath)
    return title,content,img


def total_html(url):
    html = requests.get(url)
    html.encoding = 'gb2312'
    return html.text


def saveinfo(classinfo):
    f = open("/pythonWorkSpace/info.txt", 'a', encoding='utf-8')
    for each in classinfo:
        f.writelines('title:' + each['title:'] + '\n')
        f.writelines('content:' + each['content:'] + '\n')
        f.writelines('img:' + each['img:'] + '\n\n')
    f.close()


new_url = urlChange('http://www.bytravel.cn/view/index109_list1.html', 15)
# print(new_url)
classinfo = []
for url in new_url:
    html = total_html(url)
    title,content,img = viewDict(html, '//*[@id="tctitle"]/a/text()',
                                 '// *[ @ id = "tcjs"]/text()',
                                 '//*[@id="bright"]/a/img/@src')
    for i in range(0,len(title)):
        dict = {}
        dict['title:']=title[i]
        dict['content:']=content[i]
        dict['img:']=img[i]
        classinfo.append(dict)
# print(classinfo)
saveinfo(classinfo)

