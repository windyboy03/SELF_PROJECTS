
import requests
from lxml import etree
import csv
import time
import os
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
#print(crawl.index_pages(2))
#print(crawl.parse_pages('https://www.imdb.com//title/tt0071411/?ref_=adv_li_tt'))

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
    # Data json
    mo_data = parse_movie.xpath("/html/head/script[3]/text()")
    res = json.loads(mo_data[0])
    # Rank
    ranking = parse_movie.xpath("/html/body/div/main/div/section/div/section/div/div/section[1]/div/div/a/text()")

    # Name
    name = [res["name"]]
    # Score
    score = parse_movie.xpath("/html/body/div/main/div/section/section/div/section/section/div/div/div/div/div/div/a/span/div/div/div/span[1]/text()")
    # Reviews
    number = [res["aggregateRating"]["ratingCount"]]
    # type
    types = res["genre"]
    # Time
    time = [res["duration"]]
    # director
    director = [[res["director"][0]["name"]]]
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

    return zip(ranking, name, score, number, types, time, director)
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
