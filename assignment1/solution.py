# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_movies_from_tastedive("Bridesmaids")
# get_movies_from_tastedive("Black Panther")

import requests
import json 
import requests_with_caching 

def get_movies_from_tastedive(searchStr):
    BASE_URL = "https://tastedive.com/api/similar"
    params = {}
    params['limit'] = 5
    params['type'] = 'movies'
    params['q'] = searchStr
    result = (requests_with_caching.get(BASE_URL, params)).json()
    return result

def extract_movie_titles(respDict):
    result = []
    for record in respDict['Similar']['Results']:
        result.append(record["Name"])
    return result

def get_related_titles(movieLst):
    result = []
    for movie in movieLst:
        batch = extract_movie_titles(get_movies_from_tastedive(movie))
        for title in batch:
            if not(title in result):
                result.append(title)
    return result


def get_movie_data(title):
    BASE_URL = "http://www.omdbapi.com/"
    params = {}
    params['t'] = title
    params['r'] = "json"
    result = (requests_with_caching.get(BASE_URL, params)).json()
    return result


def get_movie_rating(omdbDic):
    for rating in omdbDic["Ratings"]:
        if (rating["Source"] == "Rotten Tomatoes"):
            strRating = rating["Value"]
            return int(strRating[:len(strRating) - 1])
    return 0
print("boo")
print(get_movies_from_tastedive("Black Panther"))
#with open("this_page_cache.txt", "r") as pageFile:
#    content = pageFile.read()
#    print("---------------------------")
#    print(content)

with open("permanent_cache.txt", "r") as permFile:
	content = permFile.read()
	print(content) 


with open("this_page_cache.txt", "r") as pageFile:
	content = pageFile.read()
	print(content) 