import requests
from bs4 import BeautifulSoup
import unicodedata
import logging
import csv
import time


class Model():
    def __init__(self):
        # 请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.o (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        # 存放每一步电影的id和imdb的id
        self.movie_dct = {}
        # 存放已经处理完的movie id
        self.white_lst = []
        # 电影详情的初始url
        self.url = 'https://www.imdb.com/title/'
        self.movie_csv_path = '../ml-latest-small/links.csv'
        # 海报的保存路径
        self.poster_save_path = './poster'
        # 电影信息的保存文件
        self.info_save_path = './info/info.csv'
        # logging的配置，记录运行日志
        logging.basicConfig(filename="run.log", filemode="a+", format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)
        # 表示当前处理的电影
        self.cur_movie_id = None
        self.cur_imdb_id = None

    def get_white_lst(self):
        '''获取处理完的白名单'''
        with open('white_list') as fb:
            for line in fb:
                line = line.strip()
                self.white_lst.append(line)

    def get_movie_id(self):
        '''获取电影的id和imdb的id'''
        with open(self.movie_csv_path) as fb:
            fb.readline()
            for line in fb:
                line = line.strip()
                line = line.split(',')
                # 电影id 对应 imdbid
                self.movie_dct[line[0]] = line[1]

    def update_white_lst(self, movie_id):
        '''更新白名单'''
        with open('white_list', 'a+') as fb:
            fb.write(movie_id + '\n')

    def update_black_lst(self, movie_id, msg=''):
        with open('black_list', 'a+') as fb:
            # 写入movie id 和imdb id，并且加上错误原因
            # msg=1是URL失效，msg=2是电影没有海报
            fb.write(movie_id + ' ' + self.movie_dct[movie_id] + ' ' + msg + '\n')

    def get_url_response(self, url):
        '''访问网页请求，返回response'''
        logging.info(f'get {url}')
        i = 0
        # 超时重传，最多5次
        while i < 5:
            try:
                response = requests.get(url, timeout=6)
                if response.status_code == 200:
                    logging.info(f'get {url} sucess')
                    # 正常获取，直接返回
                    return response
                # 如果状态码不对，获取失败，返回None，不再尝试
                logging.error(f'get {url} status_code error: {response.status_code} movie_id is {self.cur_movie_id}')
                return None
            except requests.RequestException:
                # 如果超时
                logging.error(f'get {url} error, try to restart {i + 1}')
                i += 1
        # 重试5次都失败，返回None
        return None

    def process_html(self, html):
        '''解析html，获取海报，电影信息'''
        soup = BeautifulSoup(html, 'lxml')
        # 名字和发布日期 如：Toy Story (1995)
        name = soup.find(class_='title_wrapper').h1.get_text()
        # 去掉html的一些/x20等空白符
        name = unicodedata.normalize('NFKC', name)
        # print(name)
        poster_url = ''
        try:
            # 海报的URL
            poster_url = soup.find(class_='poster').a.img['src']
            poster_re = self.get_url_response(poster_url)
            # 保存图片
            self.save_poster(self.cur_movie_id, poster_re.content)
        except AttributeError as e:
            # 如果没有海报链接，那么在黑名单中更新它
            # msg=2表示没有海报链接
            self.update_black_lst(self.cur_movie_id, '2')

        # 电影的基本信息   1h 21min | Animation, Adventure, Comedy | 21 March 1996 (Germany)
        info = []
        try:
            # 时长时间
            info.append(soup.find(class_='subtext').time.get_text().strip())
        except AttributeError as e:
            # 没有则添加空字符串
            info.append('')

        # 基本信息和详细发布时间 Animation, Adventure, Comedy | 21 March 1996 (Germany)
        for tag in soup.find(class_='subtext').find_all('a'):
            info.append(tag.get_text().strip())
        # 简介
        intro = soup.find(class_='summary_text').get_text().strip()
        intro = unicodedata.normalize('NFKC', intro)
        # 卡司。D W S C，分别表示 导演，编剧，明星，导演
        case_dict = {'D': [], 'W': [], 'S': [], 'C': []}
        for i, tags in enumerate(soup.find_all(class_='credit_summary_item')):
            for h4 in tags.find_all('h4'):
                title = h4.get_text()
                ch = title[0]
                for _, a in enumerate(h4.next_siblings):
                    if a.name == 'a':
                        case_dict[ch].append(a.get_text())

        for k, v in case_dict.items():
            # 去掉多余的信息，只保留关键人名。
            # 例如Pete Docter (original story by) | 6 more credits »。我们不需要|后面的字符
            if v and (v[-1].find('credit') != -1 or v[-1].find('full cast') != -1):
                case_dict[k] = case_dict[k][:-1]

        # 有时候导演名会用Creator代替
        if 'C' in case_dict.keys():
            case_dict['D'].extend(case_dict['C'])
        # id，电影名称，海报链接，时长，类型，发行时间，简介，导演，编剧，演员
        detail = [self.cur_movie_id, name, poster_url, info[0], '|'.join(info[1:-1]),
                  info[-1], intro,
                  '|'.join(case_dict['D']), '|'.join(case_dict['W']), '|'.join(case_dict['S'])]
        self.save_info(detail)

    def save_poster(self, movie_id, content):
        with open(f'{self.poster_save_path}/{movie_id}.jpg', 'wb') as fb:
            fb.write(content)

    def save_info(self, detail):
    	# 存储到CSV文件中
        with open(f'{self.info_save_path}', 'a+', encoding='utf-8', newline='') as fb:
            writer = csv.writer(fb)
            writer.writerow(detail)

    def run(self):
        # 开始爬取信息
        # 先读入文件
        self.get_white_lst()
        self.get_movie_id()
        for movie_id, imdb_id in self.movie_dct.items():
            if movie_id in self.white_lst:
                continue
            self.cur_movie_id = movie_id
            self.cur_imdb_id = imdb_id
            # 休眠，防止被封IP，大概3秒处理完一部电影的信息，如果注释掉，会减少大约2.5小时的运行时间
            # IMDB好像没有反爬机制，可以放心的注释掉
            time.sleep(1)
            response = self.get_url_response(self.url + 'tt' + self.cur_imdb_id)
            # 找不到电影详情页的url，或者超时，则仅仅保留id，之后再用另一个脚本处理
            if response == None:
                self.save_info([self.cur_movie_id, '' * 9])
                # 仍然更新白名单，避免重复爬取这些失败的电影
                self.update_white_lst(self.cur_movie_id)
                # 更新黑名单，爬完之后用另一个脚本再处理
                self.update_black_lst(self.cur_movie_id, '1')
                continue
            # 处理电影详情信息
            self.process_html(response.content)
            # 处理完成，增加movie id到白名单中
            self.update_white_lst(self.cur_movie_id)
            logging.info(f'process movie {self.cur_movie_id} success')


if __name__ == '__main__':
    s = Model()
    s.run()
