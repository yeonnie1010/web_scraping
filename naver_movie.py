import requests
from bs4 import BeautifulSoup

URL = "https://movie.naver.com/movie/running/current.nhn"
response = requests.get(URL)

soup = BeautifulSoup(response.text, 'html.parser')

movie_list = soup.select{'#content > .article > .obj_section >.lst_wrap > ul > li'}

final_movie_data = []

for movie in movie_list :
    a_tag = movie.select_one('dl > dt > a')
    movie_title = a_tag.contents[0]
    movie_link = a_tag['href']
    movie_link = movie_link[movie_link.find('?code=') + len('?code='):] 
    print(movie_link)

    movie_data = {
        'title' : movie_title,
        'link' : movie_link
    }

    final_movie_data.append(movie_data)