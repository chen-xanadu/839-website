from multiprocessing.pool import ThreadPool

import pandas as pd
import requests
from bs4 import BeautifulSoup


CUSTOM_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4)'


def get_movie_summary(link):
    r = requests.get(link, headers={'User-Agent': CUSTOM_USER_AGENT})
    soup = BeautifulSoup(r.content, 'html.parser')
    summary = {}

    title_tag = soup.find('div', class_='product_page_title')
    summary['title'] = title_tag.h1.string
    summary['release year'] = title_tag.find(class_='release_year').string

    summary['rating'] = soup.find('div', class_='rating').contents[3].get_text(strip=True)
    if 'TV' in summary['rating']:
        raise ValueError("This is a TV program!")

    summary['score'] = soup.find('div', class_='ms_wrapper').find('span', class_='metascore_w').string

    summary['starring'] = soup.find('span', string='Starring:').find_next_sibling('span').get_text(strip=True)
    summary['director'] = soup.find('div', class_='director').a.string
    summary['genres'] = soup.find('div', class_='genres').contents[3].get_text(strip=True)
    summary['runtime'] = soup.find('div', class_='runtime').contents[3].get_text(strip=True)

    return summary


def get_movie_details(link):
    r = requests.get(link, headers={'User-Agent': CUSTOM_USER_AGENT})
    soup = BeautifulSoup(r.content, 'html.parser')
    details = {}

    details['countries'] = soup.find('tr', class_='countries').find('td', class_='data').get_text(strip=True)
    details['languages'] = soup.find('tr', class_='languages').find('td', class_='data').get_text(strip=True)
    details['production company'] = soup.find('tr', class_='company').find('td', class_='data').get_text(strip=True)

    writer_tags = soup.find('th', class_='person', string='Writer').parent.parent.find_next_sibling('tbody').find_all('a')
    details['writers'] = ','.join([tag.string.strip() for tag in writer_tags])

    return details


def get_movie_attrs(movie_tag):
    title_tag = movie_tag.find('a', {'class': 'title'})
    try:
        summary = get_movie_summary('https://www.metacritic.com' + title_tag.get('href'))
        details = get_movie_details('https://www.metacritic.com' + title_tag.get('href') + '/details')

        print(title_tag.get_text().strip())
        return {**summary, **details}
    except (ValueError, AttributeError):
        return None


table = []

pool = ThreadPool()

base_url = 'https://www.metacritic.com/browse/movies/score/metascore/all?sort=desc&view=condensed&page={}'

for i in range(60):
    result = requests.get(base_url.format(i), headers={'User-Agent': CUSTOM_USER_AGENT})

    soup = BeautifulSoup(result.content, 'html.parser')

    movie_list = soup.find_all('td', {'class': 'clamp-summary-wrap'})

    table += pool.map(get_movie_attrs, movie_list)

table = [row for row in table if row is not None]
df = pd.DataFrame(table, columns=['title', 'release year', 'rating', 'runtime', 'genres', 'director', 'starring',
                                  'countries', 'languages', 'writers', 'production', 'company', 'score'])
df.to_csv('metacritic.csv', index_label='id')
