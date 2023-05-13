import csv
def process_genre():
    # 处理类型
    path='info/info.csv'
    with open(path,encoding='utf-8') as fb,open('info/genre.txt','w') as wfb:
        reader=csv.reader(fb)
        title=reader.__next__()
        genre_set=set()
        for line in reader:
            if line[4]:
                genre_set.update(line[4].split('|'))
        for g in genre_set:
            wfb.write(g+'\n')
    pass
if __name__ == '__main__':
    process_genre()
    pass