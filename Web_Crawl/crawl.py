import requests
from lxml import etree
import csv
import re
import time
import os
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}


def index_pages(number):
    mo_urls = []
    url = 'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=%s01&ref_=adv_nxt' % number
    index_response = requests.get(url=url, headers=headers)
    tree = etree.HTML(index_response.text)
    m_urls = tree.xpath("/html/body/div/div/div/div/div/div/div/div/div/div/h3/a/@href")
    for m_url in m_urls:
        mo_urls.append('https://www.imdb.com/' + m_url)
    return mo_urls


def parse_pages(url):
    movie_pages = requests.get(url=url, headers=headers)
    parse_movie = etree.HTML(movie_pages.text)

    # Ranking
    ranking = parse_movie.xpath("/html/body/div/main/div/section/div/section/div/div/section[1]/div/div/a/text()")

    # Name
    name = parse_movie.xpath("/html/body/div/main/div/section/section/div/section/section/div/div/h1/span/text()")

    # Score
    score = parse_movie.xpath("/html/body/div/main/div/section/section/div/section/section/div/div/div/div/div/div/a/span/div/div/div/span[1]/text()")

    # Reviews
    value = parse_movie.xpath("/html/body/div/main/div/section/section/div/section/section/div/div/div/ul/li/a/span/span[1]/text()")
    number = [" ".join(['Reviews：'] + value)]
    # value = parse_movie.xpath("//a[@class='rating_people']")
    # string = [value[0].xpath('string(.)')]
    # number = [a.strip() for a in string]
    # print(number)

    # type
    value = parse_movie.xpath("//span[@class='ipc-chip__text']/text()")[:2]
    types = [" ".join(['Type ：'] + value)]

    # Countries of origin
    value = parse_movie.xpath("/html/body/div/main/div/section/div/section/div/div/section[11]/div[2]/ul/li[2]/div/ul/li[2]/a/text()")
    country = [" ".join(['Country:'] + value )]


    # Time
    value = parse_movie.xpath("/html/body/div/main/div/section/section/div/section/section/div/div/ul/li[3]/text()")
    time = [" ".join(['Time：'] + value)]


    # director
    value = parse_movie.xpath("/html/body/div/main/div/section/section/div/section/section/div/div/div/div/div/div/div/ul/li[1]/div/ul/li/a/text()")
    director = [" ".join(['Director:'] + value)]


    # URL
    m_url = ['Url：' + movie_url]


    # Poster
    poster = parse_movie.xpath("/html/head/script[3]/text()")
    res = json.loads(poster[0])
    response = requests.get(res['image'])
    poster_name = str(name[0] + '.jpg')
    dir_name = 'douban_poster'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    poster_path = dir_name + '/' + poster_name
    with open(poster_path, "wb")as f:
        f.write(response.content)

    return zip(ranking, name, score, number, types, country, time, director, m_url)
    #return ranking

def save_results(data):
    with open('douban.csv', 'a', encoding="utf-8-sig") as fp:
        writer = csv.writer(fp)
        writer.writerow(data)


if __name__ == '__main__':
    num = 0
    for i in range(0, 250, 25):
        movie_urls = index_pages(i)
        for movie_url in movie_urls:
            results = parse_pages(movie_url)
            for result in results:
                num += 1
                save_results(result)
                print('No ' + str(num) + 'Saved')
                time.sleep(1)
