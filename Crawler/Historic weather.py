import requests
from pyquery import PyQuery as pq
import csv

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
}
# 获取所有的月份的a标签连接。
def get_html():
    links = []
    url = 'https://lishi.tianqi.com/xian/index.html'
    r1 = requests.get(url,headers)
    html_doc = pq(r1.text)
    ul = html_doc('.tqtongji1 > ul:nth-child(1)')
    lis = ul('li').items()
    for li in lis:
        a = li('a')
        links.append(a.attr('href'))
    return links
# 获取详细页的具体天气信息
def get_detail(url):
    r1 = requests.get(url,headers)
    html_doc = pq(r1.text)
    uls = html_doc('.tqtongji2').find('ul')
    lis = uls.items('li')
    list = []
    l = '.'.join(li.text() for li in lis).split('.')
    # 由于标题信息只有['日期', '最高气温', '最低气温', '天气', '风向', '风力']所以需要字符串截取
    for i in range(len(l)):
        if i%6 == 0:
            temp = l[i:i+5]
            list.append(temp)
    return list

# 保存至weather.csv
def save_to_csv(data):
    with open('weather.csv','a') as csv_file:
        writer = csv.writer(csv_file)
        for row in data:
            writer.writerow(row)

if __name__ == '__main__':
    url_list = get_html()
    for url in url_list:
        print(url)
        data = get_detail(url)
        save_to_csv(data)