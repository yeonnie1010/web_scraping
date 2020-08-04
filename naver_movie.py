import requests
from bs4 import BeautifulSoup

URL = "https://movie.naver.com/movie/running/current.nhn"
response = requests.get(URL)

soup = BeautifulSoup(response.text, 'html.parser')

movie_data = []
for a in soup.select('dt.tit a'):
    movie_dict = {}
    movie_dict['title'] = a.text
    movie_dict['code'] = a['href'].split('code=')[1]
    movie_data.append(movie_dict)
print(movie_data)