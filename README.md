# 507 Final Project: A Source Integrated Movie Recommender
## Github link
<https://github.com/Stzzzzy/507_final_proj/tree/master>
## Overview
This project is aiming to scrap data from __IMDB__ and __Douban__, both websites present url information, quantativitive information and basic information. The program would perform following functions:
a) Scraping the page and access IMDB and Douban using bs4.
b) Cache data in json file to prevent the token expire issue.
c) Create a database which is loaded from different source.
d) Enable users-interaction function to input their preference about movies such as years, categories. actors and their previous favorite movie to provide a set of recommendation.
## Introduction to Running the Project
### Pakage needed
Pakage: The needed pakage is listd below. The scrapy_cache_data is the scrapy_cache_data.py file in this repository. 
```python3
import requests
from bs4 import BeautifulSoup
import re
from lxml import etree
import json
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scrapy_cache_data as scd
```
All other pakages could be installed as running
```console
pip install {pakage_name}
```
The running of project is simple as
```console
terminal:~$ python3 final_project.py
```
Notice: If you want to cache the file from imdb and douban, the scrapy and caching may takes up to 5 minutes! Please be patience because the scrapy is retriving data from each listed movie page. 
##Interaction with Users
As for the movie recommender. The user firstly has the option to choose for movie source, IMDB and Douban. The menu also offers choice to exit the program. 
```console
Please select source of recommendation:
1. IMDB
2. Douban
3. Exit
```
After choosing the data source for recommendation, the users could have their search preference. For each movie name search, Users can type in the movie's keyword or full name, and if they can't find it in the selected resource, they are given the option to search for the movie in another source. If a matching movie name is found, the user can choose to add the details of the movie to the favorite list, which is a JSON file for future lookup. The structure of favorite list largely facilitate the users' experience with movie search. 
```console
Please enter the Search Preference:
1. Search by Movie Name
2. Search by Movie Genre
3. Search by Movie Year
4. Search by Ranking in Source Top 250
5. Visualize Rating of top 250 movies by year
6. Back to source selection
```
JSON file lists the link and every necessary information to search this movie.
```json
{
        "name": "The Dark Knight",
        "imdb_info": {
            "url": "https://www.imdb.com/title/tt0468569/",
            "movie_id": "tt0468569"
        },
        "basic_info": {
            "genre": " Action Crime Drama",
            "year": "2008",
            "duration": "2h 32m",
            "actors": " Christian Bale, Heath Ledger",
            "directors": "Christopher Nolan "
        },
        "quantitative_info": {
            "ranking": "3",
            "rating": "8.984378110538634",
            "review_num": "8.1K",
            "top_review_content": "Best movie ever. Heath ledger's work is phenomenal no words......"
        }
    }
```
## Data Source
### Data Overview
__IMDB top 250:__ 
Whole top 250 movie in one page:
link: <http://www.imdb.com/chart/top>
Format: HTML
__IMDB detailed data:__ 
The movie_id is retrived from top250 page. 
Link:<https://www.imdb.com/title/movie_id/>
Format: HTML
records available: each group of data contains 11 dimension of information and 250 groups of data is available.
__Douban__:
The Douban data information is not in single page so we have to get the url by setting page parameter.
Format:HTML
Link: <https://www.imdb.com/list/ls066077036/?sort=list_order,asc&st_dt=&mode=detail&page={}'>
records available: each group of data contains 11 dimension of information and 249 groups of data is available.
## Data Structure
The data scraped from data source is organize as a 2-level tree, as below. The information of two
source is quite similar so I organized it as website information/basic information/ quantitative
information. I create a class for each object to facilitate the data caching and following data
presentation. For this tree structure, I could link two data source for basic information and
quantitative information relationship.
![image](https://user-images.githubusercontent.com/52030298/166087747-f1a2588b-5ba0-4cbe-8e11-3c66baca0798.png)
## Demo Link
<https://drive.google.com/file/d/1APV5IRRbiFcFoYlhZxKPi6OGV_kbxR6D/view?usp=sharing>
