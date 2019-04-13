# coding: utf-8

# In[2]:


import csv
import requests
from bs4 import BeautifulSoup
import re
from multiprocessing import Process, Queue, Pool


def get_text(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    return plain_text


def parser_movie_name_year(movie_tag):
    # need to handle Frozen (I) (2013)
    token = movie_tag.find('h3', 'lister-item-header')
    movie_name = token.find('a').text
    movie_link = token.find('a').attrs['href']
    movie_year = token.find('span', 'lister-item-year').text.replace(')', '')
    movie_year = movie_year.split("(")[-1].strip()
    return movie_name, movie_year, movie_link


def parser_movie_certificate_runtime_genre(movie_tag):
    token_list = movie_tag.find('p', 'text-muted')
    movie_cert = token_list.find('span', 'certificate').text
    movie_runtime = token_list.find('span', 'runtime').text
    movie_genre = token_list.find('span', 'genre').text.strip()
    return movie_cert, movie_runtime, movie_genre


def parser_movie_rating(movie_tag):
    token = movie_tag.find('div', 'ratings-bar')
    movie_rating = token.find('strong').text
    return movie_rating


def parser_gross(movie_tag):
    token = movie_tag.find('p', "sort-num_votes-visible")
    movie_gross = token.find_all('span')[-1].text
    return movie_gross


def parser_director_star(movie_tag):
    token = movie_tag.find('p', "")
    match1 = re.search(r'(Director:)([\w\W]*)(Stars:)', token.text)
    match2 = re.search(r'(Directors:)([\w\W]*)(Stars:)', token.text)
    match_star = re.search(r'(Stars:)([\w\W]*)', token.text)

    if match1:
        movie_director = match1.group(2).strip().replace('|', '').replace('\n', '')
    else:
        movie_director = match2.group(2).strip().replace('|', '').replace('\n', '')
    movie_star = match_star.group(2).strip().replace('\n', '')

    return movie_director, movie_star


def spider_writer_lang_country_production(url):
    plain_text = get_text(url)
    soup = BeautifulSoup(plain_text, "html.parser")
    movie_content = soup.find_all('div', 'credit_summary_item')[1]
    match1 = re.search(r'(Writer:)([\w\W]*)', movie_content.text)
    match2 = re.search(r'(Writers:)([\w\W]*)', movie_content.text)
    if match1:
        movie_writer = match1.group(2).split('|')[0].replace('\n', '').strip()
    else:
        movie_writer = match2.group(2).split('|')[0].replace('\n', '').strip()

    # language
    movie_content = soup.find('div', {"id": 'titleDetails'})
    movie_country = movie_content.find_all('div', 'txt-block')[1].find('a').text
    movie_language = movie_content.find_all('div', 'txt-block')[2].find('a').text
    movie_production_str = movie_content.find(text="Production Co:").parent.parent.text
    match = re.search(r'(Production Co:)([\w\W]*)(See more)', movie_production_str)
    movie_production = match.group(2).strip().replace('See more', '').strip()
    return movie_writer, movie_country, movie_language, movie_production


def spider(movie_idx, movie_no_initial, debug_en, movie_table):
    movie_idx_begin = movie_idx * 50 + 1
    url = "https://www.imdb.com/search/title?title_type=feature&sort=boxoffice_gross_us,desc&start={}&ref_=adv_nxt".format(
        movie_idx_begin)
    plain_text = get_text(url)
    soup = BeautifulSoup(plain_text, "html.parser")

    movie_content = soup.find_all('div', 'lister-item mode-advanced')
    movie_no = movie_no_initial
    for index, movie in enumerate(movie_content):
        try:
            print("    crawling movie{} begined...".format(movie_idx_begin))
            movie_idx_begin += 1
            movie_table.append([])
            movie_no = movie_no + 1

            movie_table[movie_no].append(movie_no)

            # movie_name, movie_year
            movie_name, movie_year, movie_link = parser_movie_name_year(movie)
            movie_table[movie_no].append(movie_name)
            movie_table[movie_no].append(movie_year)

            movie_cert, movie_runtime, movie_genre = parser_movie_certificate_runtime_genre(movie)
            movie_table[movie_no].append(movie_cert)
            movie_table[movie_no].append(movie_runtime)
            movie_table[movie_no].append(movie_genre)

            # movie_director and movie_stars
            movie_director, movie_stars = parser_director_star(movie)
            movie_table[movie_no].append(movie_director)
            movie_table[movie_no].append(movie_stars)

            movie_link = "https://www.imdb.com{}".format(movie_link)
            movie_writer, movie_country, movie_language, movie_production = spider_writer_lang_country_production(
                movie_link)
            movie_table[movie_no].append(movie_country)
            movie_table[movie_no].append(movie_language)
            movie_table[movie_no].append(movie_writer)
            movie_table[movie_no].append(movie_production)

            # movie_rating
            movie_rating = parser_movie_rating(movie)
            movie_table[movie_no].append(movie_rating)

            # #  movie_gross
            # movie_gross = parser_gross(movie)
            # movie_table[movie_no].append(movie_gross)
            print("    crawling movie{} finished...".format(movie_idx_begin))
        except Exception:
            movie_table.pop()
            movie_no -= 1


def worker(idx):
    print("process{} started...".format(idx))
    movie_table = []
    page_no = idx
    movie_no_initial = - 1
    debug_en = 0
    spider(page_no, movie_no_initial, debug_en, movie_table)
    print("process{} finished...".format(idx))
    return movie_table


n_cpu = 8
print("----------start running----------")
with Pool(processes=n_cpu) as pool:
    results = pool.map(worker, range(1))
    print("----------finish running----------")
    with open('imdb.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(
            ['title', 'release year', 'rating', 'runtime', 'genres', 'director', 'starring',
             'countries', 'languages', 'writers', 'production', 'company', 'score'])
        counter = 0
        for movie_table in results:
            for table in movie_table:
                table[0] = counter
                counter += 1
                writer.writerow(table)
