import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import re

#Declaring the headers 
headers = {"Accept-Language": "en-US,en;q=0.5"}

imdb_rankings = []
imdb_user_ratings = []
imdb_metascores = []
imdb_votes = []

film_names = []
film_year_of_releases = []
film_certificates = []
film_runtimes = []
film_genres = []
film_descriptions = []
film_directors = []
film_stars = []
film_grosses = []


# array of values from 1 to 1000 incrementing by 100
# values will be used to change the url aming it dynamic
pages = np.arange(1,1000,100)
# pages = np.arange(1,100,100)


try:

    for page in pages:
        page = requests.get("https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start="+str(page)+"&ref_=adv_nxt")
        soup = BeautifulSoup(page.text, 'html.parser')
        film_data = soup.findAll('div', attrs = {'class': 'lister-item mode-advanced'})
        
        # pauses the script until the stated number of seconds has elapsed.
        # This has been set to a random int between and including 2 and 7
        sleep(randint(2,7))

        # for each object in movie_data
        for html_obj in film_data:

            # get IMDb ranking
            imdb_ranking_text = html_obj.h3.span.text
            imdb_ranking_formatted = imdb_ranking_text.strip(' .')
            imdb_rankings.append(imdb_ranking_formatted)

            # get IMDb user rating
            imdb_user_rating_text = html_obj.find('div', class_ = "inline-block ratings-imdb-rating").text
            imdb_user_rating_formatted = imdb_user_rating_text.replace('\n', '').strip()
            imdb_user_ratings.append(imdb_user_rating_formatted)
            
            # get IMDb metascore rating
            if html_obj.find('span', class_ = "metascore"):
                imdb_metascore_text = html_obj.find('span', class_ = "metascore").text
                imdb_metascore_formatted = imdb_metascore_text.replace('\n', '').strip()
            else :
                imdb_metascore_formatted = "**"
            imdb_metascores.append(imdb_metascore_formatted)


            # get number of IMDb votes
            nv_object = html_obj.find_all('span', attrs = {'name': "nv"})
            imdb_votes_text = nv_object[0].text
            imdb_votes_formatted = imdb_votes_text.strip()
            imdb_votes.append(imdb_votes_formatted)

            # get film name
            film_name_text = html_obj.h3.a.text
            film_name_formatted = film_name_text.strip()
            film_names.append(film_name_formatted)

            # get film year of release
            film_year_text = html_obj.h3.find('span', class_ = "lister-item-year text-muted unbold").text
            film_year_formatted = re.sub('[^0-9]','', film_year_text)
            film_year_of_releases.append(film_year_formatted)

            # get film certificate
            if html_obj.find('span', class_ = "certificate") :
                film_certificate_text = html_obj.find('span', class_ = "certificate").text
                film_certificate_formatted = film_certificate_text.strip()
            else :
                film_certificate_formatted = "**"
            film_certificates.append(film_certificate_formatted)

            # get film runtime
            film_runtime_text = html_obj.p.find("span", class_ = 'runtime').text
            film_runtime_formatted = film_runtime_text.rstrip(' mins')
            film_runtimes.append(film_runtime_formatted)

            # get film genre
            film_genre_text = html_obj.find('span', class_ = "genre").text
            film_genre_formatted = film_genre_text.strip()
            film_genres.append(film_genre_formatted)

            # get film directors and stars
            cast_text = html_obj.find("p", class_ = '').text
            cast_list = cast_text.replace('\n', '').split('|')
            # get directors
            film_directors_text = cast_list[0]
            film_directors_formatted = film_directors_text.replace('Director:', '').replace('Directors:', '').strip()
            film_directors.append(film_directors_formatted)
            # get stars
            film_stars_text = cast_list[1]
            film_stars_formatted = film_stars_text.replace('Stars:', '').strip()
            film_stars.append(film_stars_formatted)

            # get film description
            describe = html_obj.find_all('p', class_ = 'text-muted')
            if len(describe) > 1 :
                film_description_text = describe[1].text
                film_description_formatted = film_description_text.replace('\n', '') 
            else :
                film_description_formatted = '****'
            film_descriptions.append(film_description_formatted)
            
            # get film gross
            span_objects = html_obj.find('p', class_ = 'sort-num_votes-visible').find_all('span')
            l = len(span_objects)
            film_gross_formatted = '****'
            for i in range(l):
                if span_objects[i].text == "Gross:" :
                    film_gross_text = span_objects[i+1]["data-value"]
                    film_gross_formatted = film_gross_text.strip()
            film_grosses.append(film_gross_formatted)
            

except Exception as e:
    print(e)



# Check for complete data. If every list has length 1000 then the code has not run into errors when extracting from each page of the website.
print('imdb rankings count: ' + str(len(imdb_rankings)) )
print('imdb user ratings count: ' + str(len(imdb_user_ratings)) )
print('imdb metascores count: ' + str(len(imdb_metascores)) )
print('imdb votes count: ' + str(len(imdb_votes)) )
print('film name count: ' + str(len(film_names)) )
print('film year of release count: ' + str(len(film_year_of_releases)) )
print('film certificates count: ' + str(len(film_certificates)) )
print('film runtimes count: ' + str(len(film_runtimes)) )
print('film genres count: ' + str(len(film_genres)) )
print('film directors count: ' + str(len(film_directors)) )
print('film stars count: ' + str(len(film_stars)) )
print('film descriptions count: ' + str(len(film_descriptions)) )
print('film grosses count: ' + str(len(film_grosses)) )


# creating a dataframe 
film_list = pd.DataFrame({ "IMDb Ranking": imdb_rankings, 
                           "IMDb User Rating": imdb_user_ratings, 
                           "IMDb Metascore": imdb_metascores, 
                           "IMDb Votes": imdb_votes, 
                           "Film Name": film_names, 
                           "Year of Release": film_year_of_releases, 
                           "Certificate": film_certificates, 
                           "Runtime (mins)": film_runtimes, 
                           "Genres": film_genres, 
                           "Directors": film_directors, 
                           "Stars": film_stars, 
                           "Description": film_descriptions, 
                           "Gross (USD)": film_grosses })


# Save the dataframe to csv format with no indexing column.
# Mode set to overwrite if existing filename already.
film_list.to_csv('raw_data_top_1000_IMDb_movies.csv', index=False, mode='w')
