
import requests
from lxml import etree
import csv
import time
import os
import urllib.request
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
#print(crawl.index_pages(2))
#print(crawl.parse_pages('https://www.imdb.com//title/tt0071411/?ref_=adv_li_tt'))

def index_pages(price):
    mo_urls = []
    url = 'https://www.thegioididong.com/dtdd#c=42&ext=new&o=17&pi=%s' % price
    index_response = requests.get(url=url, headers=headers)
    tree = etree.HTML(index_response.text)
    m_urls = tree.xpath("/html/body/div/section/div/ul/li/a[1]/@href")
    for m_url in m_urls:
        mo_urls.append('https://www.thegioididong.com' + m_url)
    return mo_urls
def parse_pages(url):
    movie_pages = requests.get(url=url, headers=headers)
    parse_movie = etree.HTML(movie_pages.text)
    # Data json
    po_data = parse_movie.xpath("/html/body/section/script[2]/text()")
    res = json.loads(po_data[0])
    # Rank
    sku = [res["sku"]]

    # Name
    name = parse_movie.xpath("/html/body/section[1]/h1/text()")
    # Score
    score = parse_movie.xpath("/html/body/section/div/div/div/div[1]/div/div/div/p/text()")
    # Reviews
    price = [res["offers"]['price']]
    # type
    brand = res["brand"]['name']
    # Time
    date = parse_movie.xpath("/html/body/section/div/div/div/div/div/div/div/div[9]/ul/li[4]/div[2]/span/text()")
    # additionalProperty
    additionalProperty = res["additionalProperty"]
    # Poster

    poster = parse_movie.xpath("/html/body/section/script[2]/text()")
    res = json.loads(poster[0])
    #response = requests.get(res['image'][0])

    poster_name = str(name[0] + '.jpg')
    dir_name = 'poster'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    poster_path = dir_name + '/' + poster_name
    urllib.request.urlretrieve(res['image'][0], poster_path)

    return zip(sku, name, score, price, brand, date, additionalProperty)
def save_results(data):
    with open('tgdd.csv') as fp:
        writer = csv.writer(fp)
        writer.writerow(data)


if __name__ == '__main__':
    num = 0
    for i in range(2, 3):
        movie_urls = index_pages(i)
        for movie_url in movie_urls:
            results = parse_pages(movie_url)
            for result in results:
                num += 1
                save_results(result)
                print('No ' + str(num) + 'Saved')
                time.sleep(3)
