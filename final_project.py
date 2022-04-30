
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


def check_cache_file():
    '''
        Check if the cache file exists.
        If not, create it.
            Parameters:
                None
            Returns:
                None
    '''
    if os.path.exists(scd.IMDB_MOVIE_FILENAME) and os.path.exists(scd.DOUBAN_MOVIE_FILENAME):
        print("Cache file existance: Yes")
    else:
        print("Cache file existance: No")
        print("Please wait for the cache file to be created.")
        imdb_list = scd.build_imdb_list_from_sub_html()
        scd.save_imdb_cache(imdb_list)
        douban_list = scd.build_douban_top_250()
        scd.save_douban_cache(douban_list)
        print("Cache file created.")


def movie_name_search(movie_name, movie_json):
    '''
        Perform a movie name search.
            Parameters:
                movie_name: the movie name to be searched
                movie_json: the movie json file
            Returns:
                movie_list: the list of movies that match the movie name
    '''
    name_list = []
    for index in range(0, len(movie_json)):
        name_list.append(movie_json[index]['name'].lower())
    match_list = [k for k in name_list if movie_name.lower() in k]
    for i in match_list:
        print("Found: " + i.title())
    ori_name_list = [k for k in movie_json if k['name'].lower() in match_list]
    return ori_name_list

def save_movie_to_favorite(movie_json: dict):
    '''
        Save the movie to favorite list.
            Parameters:
                movie_json: the movie json file
            Returns:
                None
    '''
    with open(scd.FAVORIATE_MOVIE_FILENAME, 'a') as f:
        f.write(json.dumps(movie_json, indent=4))
    print("Movie saved to favorite.")


def movie_name_search_menu(json_one, json_two):
    '''
        Perform a movie name search.
            Parameters:
                movie_json: the movie json file
            Returns:
                movie_list: the list of movies that match the movie name
    '''
    movie_name = input("Please enter the movie name: ").lower()
    first_result = movie_name_search(movie_name, json_one)
    if first_result == [] or first_result == None:
        choice = input("No result found. Do you want to search again in another source? [Y/N]").lower()
        if choice == 'y':
            second_result = movie_name_search(movie_name, json_two)
            if second_result == [] or second_result == None:
                print("No result found.")
                input("Press Enter to continue...")
            else :
                print(json.dumps(second_result, indent=4))
                save_choice = input("Do you want to save those movie to your favorite list? [Y/N]")
                if save_choice == 'y':
                    save_movie_to_favorite(second_result)
                    input("Press Enter to continue...")
    elif first_result != None:
            print(json.dumps(first_result, indent=4))
            save_choice = input("Do you want to save this movie to your favorite list? [Y/N]")
            if save_choice == 'y':
                    save_movie_to_favorite(first_result)
            input("Press Enter to continue...")


def movie_genre_search(genre, movie_json):
    '''
        Perform a movie genre search.
            Parameters:
                movie_json: the movie json file
                genre: the movie genre to be searched
            Returns:
                movie_list: the list of movies that match the movie genre
    '''
    genre_list = []
    for index in range(0, len(movie_json)):
        if genre in movie_json[index]['basic_info']['genre'].lower():
            genre_list.append(movie_json[index])
    for i in genre_list:
        print("Name: {}".format(i['name']))
    return genre_list

def movie_genre_search_menu(json_one, json_two):
    '''
        Perform a movie genre search.
            Parameters:
                movie_json: the movie json file
            Returns:
                movie_list: the list of movies that match the movie genre
    '''
    genre = input("Please enter the movie genre: ").lower()
    first_result = movie_genre_search(genre, json_one)
    if first_result == [] or first_result == None:
        choice = input("No result found. Do you want to search again in another source? [Y/N]").lower()
        if choice == 'y':
            second_result = movie_genre_search(genre, json_two)
            if second_result == [] or second_result == None:
                print("No result found.")
                input("Press Enter to continue...")
            else :
                # print(json.dumps(second_result['name'], indent=4))
                save_choice = input("Do you want to save those movie to your favorite list? [Y/N]")
                if save_choice == 'y':
                    save_movie_to_favorite(second_result)
                    input("Press Enter to continue...")
    elif first_result != None:
            # print(json.dumps(first_result['name'], indent=4))
            save_choice = input("Do you want to save this movie to your favorite list? [Y/N]")
            if save_choice == 'y':
                    save_movie_to_favorite(first_result)
            input("Press Enter to continue...")

def movie_year_search(year, movie_json):
    '''
        Perform a movie year search.
            Parameters:
                movie_json: the movie json file
                year: the movie year to be searched
            Returns:
                movie_list: the list of movies that match the movie year
    '''
    year_list = []
    for index in range(0, len(movie_json)):
        if year in movie_json[index]['basic_info']['year'].lower():
            year_list.append(movie_json[index])
    for i in year_list:
        print("Name: {} ({})".format(i['name'], i['basic_info']['year']))
    return year_list

def movie_year_search_menu(json_one, json_two):
    '''
        Perform a movie year search.
            Parameters:
                movie_json: the movie json file
            Returns:
                movie_list: the list of movies that match the movie year
    '''
    year = input("Please enter the movie year: ").lower()
    first_result = movie_year_search(year, json_one)
    if first_result == [] or first_result == None:
        choice = input("No result found. Do you want to search again in another source? [Y/N]").lower()
        if choice == 'y':
            second_result = movie_year_search(year, json_two)
            if second_result == [] or second_result == None:
                print("No result found in another source, sorry.")
                input("Press Enter to continue...")
            else :
                # print(json.dumps(second_result['name'], indent=4))
                save_choice = input("Do you want to save those movie to your favorite list? [Y/N]")
                if save_choice == 'y':
                    save_movie_to_favorite(second_result)
                    input("Press Enter to continue...")
    elif first_result != None:
            # print(json.dumps(first_result['name'], indent=4))
            save_choice = input("Do you want to save this movie to your favorite list? [Y/N]")
            if save_choice == 'y':
                    save_movie_to_favorite(first_result)
            input("Press Enter to continue...")

def movie_ranking_search(lower, upper, movie_json):
    '''
        Perform a movie ranking search.
            Parameters:
                movie_json: the movie json file
                lower: the lower bound of the movie ranking to be searched
                upper: the upper bound of the movie ranking to be searched
            Returns:
                movie_list: the list of movies that match the movie ranking
    '''
    ranking_list = []
    for index in range(lower-1, upper):
        ranking_list.append(movie_json[index])
    for i in ranking_list:
        print("Name: {} ({})".format(i['name'], i['quantitative_info']['ranking']))
    return ranking_list

def movie_ranking_search_menu(json_one, json_two):
    '''
        Perform a movie ranking search.
            Parameters:
                movie_json: the movie json file
            Returns:
                movie_list: the list of movies that match the movie ranking
    '''
    upper = int(input("Please enter the higher ranking index, for example, if you want to search from 1 to 5, enter 5: "))
    lower = int(input("Please enter the lower ranking index, for example, if you want to search from 1 to 5, enter 1: "))
    first_result = movie_ranking_search(lower, upper, json_one)
    if first_result == [] or first_result == None:
        choice = input("No result found. Do you want to search again in another source? [Y/N]").lower()
        if choice == 'y':
            second_result = movie_ranking_search(lower, upper, json_two)
            if second_result == [] or second_result == None:
                print("No result found in another source, sorry.")
                input("Press Enter to continue...")
            else :
                # print(json.dumps(second_result['name'], indent=4))
                save_choice = input("Do you want to save those movie to your favorite list? [Y/N]")
                if save_choice == 'y':
                    save_movie_to_favorite(second_result)
                    input("Press Enter to continue...")
    elif first_result != None:
            # print(json.dumps(first_result['name'], indent=4))
            save_choice = input("Do you want to save this movie to your favorite list? [Y/N]")
            if save_choice == 'y':
                    save_movie_to_favorite(first_result)
            input("Press Enter to continue...")


# This function is used to calculate the mean rating of movies in a year and plot the result

def visualize_movie_rating_distribution_by_year(json_one):
    '''
        Visualize the distribution of movie ratings by year.
            Parameters:
                json_one: the movie json file
            Returns:
                None
    '''
    year_list = []
    for index in range(0, len(json_one)):
        year_list.append(json_one[index]['basic_info']['year'])
    year_list = list(set(year_list))
    year_list.sort()
    for year in year_list:
        year_rating_list = []
        for index in range(0, len(json_one)):
            if json_one[index]['basic_info']['year'] == year:
                year_rating_list.append(json_one[index]['quantitative_info']['rating'])
        year_rating_list = list(map(float, year_rating_list))
        mean_rating = round(sum(year_rating_list)/len(year_rating_list), 2)
        #print("Year: {}\tMean Rating: {}".format(year, mean_rating))
        plt.bar(year, mean_rating, color='blue')
    plt.xlabel('Year')
    plt.ylabel('Mean Rating')
    plt.title('Mean Rating of Movies in Different Years')
    plt.xticks(rotation=270)
    plt.show()
    input("Press Enter to continue...")

def search_menu(json_one, json_two):
    '''
        Perform a search.
            Parameters:
                json_one: the movie json file
                json_two: the movie json file
            Returns:
                None
    '''
    print("Please enter the Search Preference:")
    print("1. Search by Movie Name")
    print("2. Search by Movie Genre")
    print("3. Search by Movie Year")
    print("4. Search by Ranking in Source Top 250")
    print("5. Visualize Rating of top 250 movies by year")
    print("6. Back to source selection")
    while True:
        try:
            search_preference = int(input("Please enter the number of your preference: "))
            if search_preference < 1 or search_preference > 6:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid number.")
            continue
    if search_preference == 6:
        return
    if search_preference == 1:
        movie_name_search_menu(json_one, json_two)
    if search_preference == 2:
        movie_genre_search_menu(json_one, json_two)
    if search_preference == 3:
        movie_year_search_menu(json_one, json_two)
    if search_preference == 4:
        movie_ranking_search_menu(json_one, json_two)
    if search_preference == 5:
        visualize_movie_rating_distribution_by_year(json_one)


def main():
    '''
        The main function.
    '''
    print("Welcome to Movie Recommender!")
    print("The Movie Recommender is an application that recommends movies based on your preferences.")
    print("Check out the cache file existance.")
    check_cache_file()
    imdb_json = json.load(open(scd.IMDB_MOVIE_FILENAME))
    douban_json = json.load(open(scd.DOUBAN_MOVIE_FILENAME))
    
    
    while True:
        print("Please select source of recommendation:")
        print("1. IMDB")
        print("2. Douban")
        print("3. Exit")
        source = input("Please enter the number of the source: ")
        if source == '1':
            search_menu(imdb_json, douban_json)
        elif source == '2':
            search_menu(douban_json, imdb_json)
        elif source == '3':
            print("Thank you for using the Movie Recommender!")
            return
        else:
            print("Please enter a valid number.")


if __name__ == '__main__':
     main()


