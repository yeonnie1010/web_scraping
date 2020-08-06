import requests
from bs4 import BeautifulSoup

URL = "https://movie.naver.com/movie/running/current.nhn"
# 해당 url로 get 요청을 보냄
response = requests.get(URL)
# response의 텍스트를 파싱하기 위해 bs4로 html 만들어준다.
# 0805 - 어제 만든 soup을 movie_code_soup으로 이름 변경(뒤에서 또 soup 쓸 거니까!)
movie_code_soup = BeautifulSoup(response.text, 'html.parser')
# print(soup)

# 0805 - 여기도 'soup.select'였던 것을 위에서 바꿔줬으니까 movie_code_soup으로 똑같이 바꿔주기
movies_list = movie_code_soup.select(
    '#content > .article > div:nth-child(1) > .lst_wrap > ul > li'
)

fin_movies_list = []

for movie in movies_list:
    a_tag = movie.select_one('dl > dt > a')

    movie_title = a_tag.contents[0]
    movie_code = a_tag["href"].split("code=")[1]

    movie_data = {
        'title' : movie_title,
        'code'  : movie_code
    }

    fin_movies_list.append(movie_data)
# print(fin_movies_list)

# 0805 - 영화 리뷰 & 평점 가져오기

# import requests

headers = {
    'authority': 'movie.naver.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'iframe',
    'referer': 'https://movie.naver.com/movie/bi/mi/point.nhn?code=189069',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5',
    'cookie': 'NNB=SSC6GRBLRJBV4; ASID=daebc5490000017037e3bb1700000052; NID_AUT=bPmxdbriYlJDbLqriV8tBPaZNdHvY5YJXmIkuEcnD1VXBJRvLhfrpsQmQxDhDm6F; NID_JKL=EATbCxeAEt9/YlwujZ5X5j3YbF3sCRg12YEDswDQ6Go=; NRTK=ag#20s_gr#4_ma#2_si#2_en#2_sp#-2; MM_NEW=1; NFS=2; MM_NOW_COACH=1; nx_ssl=2; _ga=GA1.1.565851281.1591833711; _ga_7VKFYR6RV1=GS1.1.1595952946.14.1.1595952986.20; BMR=s=1596594597415&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.nhn%3FblogId%3Dbluefish850%26logNo%3D220696377742%26proxyReferer%3Dhttps%3A%252F%252Fwww.google.com%252F&r2=https%3A%2F%2Fapp.swit.io%2Fgj-aischool%2Fchannel%2F200805020608186mLdt%2Fchat; page_uid=UyqMvwprvmZssQB+q8Kssssstz4-064238; NID_SES=AAABnCzmFAHuwxPiSfD2NXUDcPqwqA1zaZowB5vU8ez5MC6FeWOM4oCmpewoABPRTiJ6pX6vseA8iFFW11LEA6edN9X0gX4HCmEdhIILe+Fz9PVAu0mWy66PiFVULOaWUN5QoX9ElX6Vck9pUKNkFXLRxlScAX+9gsxc8RJoWRmJj4TcYfFh6YuENKJ6WmH0m2JjMRJ6o4Aj9w3pC1hCEx2o/OACoxrwwa4jNr6r/OfH2plBR4Ti+5aVz0UiMUM7iYXXI/iwe5ySXoZgfkszM2etLGCPRv6mEbTOhPrsQvKYs0C5VfszvtkZifq6H0Zzu9d7yD6sUccXyA159NSAYXmfZ/7GsAtD/oyBAeU+UYeaWdXFNFBMPkJJz4ox0u2slEE7gjU9N6UgvCuUDggQUw4eBnZ/hXO1kEaTJMUPSashFQXsEVB+xMAe1z1o5/lWoPYljF+Lr9bxk3E3dnrnel8VKqyDgKxMdZvmRe5AGJcc2W9Rfmv0YJbA12fHhf8B92XlB2fOoWARS2Dq8VEdLkK81UWqIP8yZOMVQRX32N5TwC1j; csrf_token=b84e484e-1044-47dd-a50b-658bdb747ee1',
}


#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=189069&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false', headers=headers)


for movie in fin_movies_list:
    movie_code = movie['code']
    # print(movie_code)
    params = (
        ('code', movie_code),
        ('type', 'after'),
        ('isActualPointWriteExecute', 'false'),
        ('isMileageSubscriptionAlready', 'false'),
        ('isMileageSubscriptionReject', 'false'),
    )

    review_response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', headers=headers, params=params)
    # REVIEW_URL = f'https://movie.naver.com/movie/bi/mi/point.nhn?code={}'
    # review_response = requests.get(REVIEW_URL)
    # print(review_response.text)

    # 그러나 이렇게 'body > div > div > div.score_result > ul > li'하면 아무 것도 안 옴.
    # Why? : 위에 iframe 때문에. src로 크롤링하면 되긴 하는데, 혹시 나중에 자바 스크립트 때문에 못하는 경우가 있을 수도 있으니!
    # 그것을 대비하여 연습해보자.


    review_soup = BeautifulSoup(review_response.text, 'html.parser')
    # 영화 리뷰 부분 파싱해오기


    # ※엔드 포인트? < 어디에, 어떤 일을 할 지 요청을 보내는 것(e.g., url 맨 뒤에 /login, /post 이런 식으로 붙이는 거)
    # API를 만든다? 요청을 하는 문을 열어둔다?

    # "robots.txt" (e.g., www.naver,com/robots.txt) 어디까지 allow or disallow 하는지 지침서!?

    # F12 > (상단) Network > ※ 웬만하면 'Preserve log' 체크해둘 것(이전에 불러온 로그들 남기는 용도) > (중간 좌측) Name 클릭하면 원하는 정보 확인 가능

    review_list = review_soup.select(
        'body > div > div > div.score_result > ul > li ')

    fin_review_list = []

    for review in review_list:
        review_stc = review.select_one('div.score_reple > p > span').get_text().strip()
        review_rating = review.select_one('div.star_score > em').get_text()

        movie_review_data = {
            'rating' : review_rating,
            'review_stc' : review_stc
        }

        fin_review_list.append(movie_review_data)

print(fin_review_list)
