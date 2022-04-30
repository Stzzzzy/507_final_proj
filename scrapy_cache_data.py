import requests
from bs4 import BeautifulSoup
import re
from lxml import etree
import json


IMDB_MOVIE_FILENAME = "imdb_top_250.json"
DOUBAN_MOVIE_FILENAME = "douban_top_250.json"
FAVORIATE_MOVIE_FILENAME = "favoriate_movies.json"


class imdb_movie:
    """
    A class to imdb movie.

    ...

    Attributes
    ----------
    name : movie name
    url : movie url
    rating : movie rating
    duration : movie duration
    short_description : movie short description
    year : movie year
    actors : movie actors
    directors : movie directors

    Methods
    -------
    movie_imdb_info():
        return a dict of imdb movie info
    movie_basic_info():
        return a dict of basic movie info
    quantitative_info():
        return a dict of quantitative movie info
    movie_info():
        return a dict of movie info
    """
    def __init__(self ,movie_id = None, url = None, name = None, rating = None, duration = None, short_description = None, year = None, genre = None, directors = None, actors = None, ranking = None, review_num = None, top_review_content = None):
        self.url = url
        self.name = name
        self.rating = rating
        self.duration = duration
        self.short_description = short_description
        self.year = year
        self.genre = genre
        self.directors = directors
        self.actors = actors
        self.ranking = ranking
        self.movie_id = movie_id
        self.review_num = review_num
        self.top_review_content = top_review_content

    def movie_imdb_info(self):
        data = {
            "url": self.url,
            "movie_id": self.movie_id
        }
        return data

    def movie_basic_info(self):
        data = {
            "genre": self.genre,
            "year": self.year,
            "duration": self.duration,
            "actors": self.actors,
            "directors": self.directors}
        return data

    def quantitative_info(self):
        data = {
            "ranking": self.ranking,
            "rating": self.rating,
            "review_num": self.review_num,
            "top_review_content": self.top_review_content}
        return data

    def movie_info(self):
        data = { "name": self.name, 
                "imdb_info": self.movie_imdb_info(),
                "basic_info": self.movie_basic_info(),
                "quantitative_info": self.quantitative_info()}
        return data


class douban_movie:
    """
    A class of douban movie.

    ...

    Attributes
    ----------
    name : movie name
    url : movie url
    rating : movie rating
    duration : movie duration
    short_description : movie short description
    year : movie year
    actors : movie actors
    directors : movie directors

    Methods
    -------
    movie_imdb_info():
        return a dict of imdb movie info
    movie_basic_info():
        return a dict of basic movie info
    quantitative_info():
        return a dict of quantitative movie info
    movie_info():
        return a dict of movie info
    """
    def __init__(self, url = None, name = None, movie_id = None, rating = None, duration = None, short_description = None, year = None, genre = None, directors = None, actors = None, ranking = None, rating_num = None):
        self.name = name
        self.rating = rating
        self.duration = duration
        self.short_description = short_description
        self.year = year
        self.genre = genre
        self.directors = directors
        self.actors = actors
        self.ranking = ranking
        self.rating_num = rating_num
        self.movie_id = movie_id
        self.url = url
        
    def movie_imdb_info(self):
        data = {
            "url": self.url,
            "movie_id": self.movie_id
        }
        return data
    
    def movie_basic_info(self):
        data = {
            "genre": self.genre,
            "year": self.year,
            "duration": self.duration,
            "actors": self.actors,
            "directors": self.directors}
        return data
    
    def quantitative_info(self):
        data = {
            "ranking": self.ranking,
            "rating": self.rating,
            "rating_num": self.rating_num,
            "short_description": self.short_description}
        return data
    
    def movie_info(self):
        data = { "name": self.name, 
                "imdb_info": self.movie_imdb_info(),
                "basic_info": self.movie_basic_info(),
                "quantitative_info": self.quantitative_info()}
        return data



def build_imdb_list_from_top_250():
    '''
    Returns a list of imdb movie.

            Parameters:
            -----------

            Returns:
                    A list of imdb movie.
    '''
    imdb_url = 'http://www.imdb.com/chart/top'
    imdb_req = requests.get(imdb_url)
    imdb_soup = BeautifulSoup(imdb_req.text, 'lxml')
    imdb_movies = imdb_soup.select('td.titleColumn')

    imdb_url = ['https://www.imdb.com' + a.attrs.get('href') for a in imdb_soup.select('td.titleColumn a')]
    imdb_actors = [a.attrs.get('title') for a in imdb_soup.select('td.titleColumn a')]
    imdb_ratings = [b.attrs.get('data-value') for b in imdb_soup.select('td.posterColumn span[name=ir]')]

    imdb_list_in = []

    for index in range(0, len(imdb_movies)):
        movie_string = imdb_movies[index].get_text()
        movie = (' '.join(movie_string.split()).replace('.', ''))
        movie_crew_split = imdb_actors[index].split(',')
        movie_dir = movie_crew_split[0].strip('(.dir)')
        movie_actor = re.sub('^[^,]*(?=,),', '', imdb_actors[index])
        movie_title = movie[len(str(index))+1:-7]
        year = re.search('\((.*?)\)', movie_string).group(1)
        ranking = movie[:len(str(index))-(len(movie))]
        movie_ids = imdb_url[index].split('/')[-2]
        imdb_data = imdb_movie(url = imdb_url[index], movie_id = movie_ids, name  = movie_title, rating = imdb_ratings[index], year = year, actors = movie_actor, ranking = ranking, directors=movie_dir)
        imdb_list_in.append(imdb_data)
    return imdb_list_in


def build_imdb_list_from_sub_html():
    '''
        Returns a list of imdb movie from detailed html.

            Parameters:
            -----------

            Returns:
                    A list of imdb movie.
    '''
    imdb_list = build_imdb_list_from_top_250()
    for index in range(0, len(imdb_list)):
        sub_url = imdb_list[index].url
        sub_req = requests.get(sub_url)
        sub_soup = BeautifulSoup(sub_req.text, 'lxml')
        sub_time = sub_soup.find('div', class_='sc-94726ce4-3 eSKKHi').find_all("li")[-1].get_text()
        sub_description = sub_soup.select('span.sc-16ede01-1.kgphFu')[0].get_text()
        sub_rated_num = sub_soup.find('div', class_= 'sc-66a20916-0').select('span')[0].get_text()
        sub_top_review_content = sub_soup.find_all('div', class_='ipc-html-content-inner-div')[-1].get_text()
        try:
            init_genre = sub_soup.find_all('div', class_='sc-16ede01-4')[-1].get_text()
        except : IndexError
        pattern = "[A-Z]"
        sub_genre = re.sub(pattern, lambda x: " " + x.group(0), init_genre)
        imdb_list[index].genre = sub_genre
        imdb_list[index].duration = sub_time
        imdb_list[index].short_description = sub_description
        imdb_list[index].review_num = sub_rated_num
        imdb_list[index].top_review_content = sub_top_review_content

    return imdb_list

# imdb_list = build_imdb_list_from_sub_html() # This may run slow, please be patient


def save_imdb_cache(imdb_list: imdb_movie):
    '''
        Save imdb movie list to cache.
            Parameters:
                    imdb_list: A list of imdb movie.

            Returns:
                    None
    '''
    f = open(IMDB_MOVIE_FILENAME, 'w').close()
    for index in range(0, len(imdb_list)):
        imdb_list[index].movie_info()
        with open(IMDB_MOVIE_FILENAME, 'a') as f:
            f.write(json.dumps(imdb_list[index].movie_info(), indent=4))
            if index != len(imdb_list)-1:
                f.write(',')
    with open(IMDB_MOVIE_FILENAME, 'a') as f:
        f.write(']')
    with open(IMDB_MOVIE_FILENAME, 'r+') as file:
        content = file.read()
        file.seek(0)
        file.write('[' + content)
    f.close()


def get_douban_url():
    '''
        Returns a list of douban movie url.
            Parameters:
                    None

            Returns:
                    url_list: A list of douban movie url.
    '''
    urls = []
    for i in range(1, 4):
        url = 'https://www.imdb.com/list/ls066077036/?sort=list_order,asc&st_dt=&mode=detail&page={}'.format(i)
        urls.append(url)
    return urls

def build_douban_top_250():
    '''
        Returns a list of douban movie.
            Parameters:
                    None
            returns:
                    A list of douban movie.
    '''
    douban_url_list = get_douban_url()
    douban_list_in = []
    for i in range(0, len(douban_url_list)):
        douban_req = requests.get(douban_url_list[i])
        douban_soup = BeautifulSoup(douban_req.text, 'lxml')
        if i != 2:
            for j in range(0, 100):
                douban_movies = douban_soup.find_all('div', class_='lister-list')[0].find_all('div', class_='lister-item-content')[j]
                douban_url = douban_movies.find('a')['href']
                douban_movie_id = douban_url.split('/')[-2]
                douban_in_imdb_url = 'https://www.imdb.com' + douban_url
                douban_name = douban_movies.find('h3').find('a').text
                douban_rating = douban_movies.find('span', class_='ipl-rating-star__rating').text
                douban_ranking = douban_movies.find('h3').find('span', class_ = "lister-item-index unbold text-primary").text.replace('.', '')
                try:
                    douban_duration = douban_movies.find('span', class_='runtime').text.replace(' min', '')
                    douban_duration = str(int(douban_duration)//60) + "h" + " " + str(int(douban_duration)%60) + "m"
                except: AttributeError
                douban_short_description = douban_movies.find('p', class_='').text.replace('\n', '')
                douban_genre = douban_movies.find('span', class_='genre').text.replace('\n', '').replace(' ', '').replace(',', '/')
                movie_year = douban_movies.find('span', class_='lister-item-year text-muted unbold').text.replace('(', '').replace(')', '')
                douban_directors = douban_movies.find_all('p', class_='text-muted')[1].find('a').text
                douban_actors = douban_movies.find_all('p', class_='text-muted')[1].find_all('a')[1:]
                douban_actors = [actor.text for actor in douban_actors]
                douban_actors = ', '.join(douban_actors)
                douban_review_num = douban_movies.find_all('p', class_ = 'text-muted')[-1].find_all('span')[1].text
                douban_data = douban_movie(name = douban_name, rating = douban_rating, ranking = douban_ranking, duration = douban_duration, 
                                           short_description = douban_short_description, genre = douban_genre, directors = douban_directors, actors = douban_actors, rating_num = douban_review_num, 
                                           movie_id = douban_movie_id, url = douban_in_imdb_url, year = movie_year)
                print(j)
                douban_list_in.append(douban_data)
        if i == 2:
            for j in range(0, 49):
                douban_movies = douban_soup.find_all('div', class_='lister-list')[0].find_all('div', class_='lister-item-content')[j]
                douban_url = douban_movies.find('a')['href']
                douban_movie_id = douban_url.split('/')[-2]
                douban_in_imdb_url = 'https://www.imdb.com' + douban_url
                douban_name = douban_movies.find('h3').find('a').text
                douban_rating = douban_movies.find('span', class_='ipl-rating-star__rating').text
                douban_ranking = douban_movies.find('h3').find('span', class_ = "lister-item-index unbold text-primary").text.replace('.', '')
                try:
                    douban_duration = douban_movies.find('span', class_='runtime').text.replace(' min', '')
                    douban_duration = str(int(douban_duration)//60) + "h" + " " + str(int(douban_duration)%60) + "m"
                except: AttributeError
                douban_short_description = douban_movies.find('p', class_='').text.replace('\n', '')
                douban_genre = douban_movies.find('span', class_='genre').text.replace('\n', '').replace(' ', '').replace(',', '/')
                douban_directors = douban_movies.find_all('p', class_='text-muted')[1].find('a').text
                douban_actors = douban_movies.find_all('p', class_='text-muted')[1].find_all('a')[1:]
                douban_actors = [actor.text for actor in douban_actors]
                douban_actors = ', '.join(douban_actors)
                douban_review_num = douban_movies.find_all('p', class_ = 'text-muted')[-1].find_all('span')[1].text
                douban_data = douban_movie(name = douban_name, rating = douban_rating, ranking = douban_ranking, duration = douban_duration, 
                                           short_description = douban_short_description, genre = douban_genre, directors = douban_directors, actors = douban_actors, rating_num = douban_review_num, 
                                           movie_id = douban_movie_id, url = douban_in_imdb_url, year = movie_year)
                douban_list_in.append(douban_data)
                print(j)
    return douban_list_in


def save_douban_cache(douban_list: douban_movie):
    '''
        Save douban_list to cache
            Parameters:
                douban_list: douban_movie
            return:
                None
    '''
    f = open(DOUBAN_MOVIE_FILENAME, 'w').close()
    for index in range(0, len(douban_list)):
        douban_list[index].movie_info()
        with open(DOUBAN_MOVIE_FILENAME, 'a') as f:
            f.write(json.dumps(douban_list[index].movie_info(), indent=4))
            if index != len(douban_list)-1:
                f.write(',')
    with open(DOUBAN_MOVIE_FILENAME, 'a') as f:
        f.write(']')
    with open(DOUBAN_MOVIE_FILENAME, 'r+') as file:
        content = file.read()
        file.seek(0)
        file.write('[' + content)
    f.close()