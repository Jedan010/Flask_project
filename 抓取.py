
# coding: utf-8

# In[ ]:
import pandas as pd

url = 'https://movie.douban.com/cinema/nowplaying/beijing/'

from bs4 import BeautifulSoup
import requests

res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')

now_playing = soup.find('div', id='nowplaying').find('ul', class_='lists').find_all('li',class_="list-item")
contents_NowPlaying = []
for li in now_playing:
    try:
        content = {}
        content['name'] = li.get('data-title')
        content['score'] = li.get('data-score')
        content['region'] = li.get('data-region')
        content['release'] = li.get('data-release')
        content['actors'] = li.get('data-actors')
        content['duration'] = li.get('data-duration')
        content['href'] = li.a.get('href')
        content['img'] = li.img.get('src')    
        contents_NowPlaying.append(content)
    except:
        print(li)

data_NowPlaying = pd.DataFrame(contents_NowPlaying)

upcoming = soup.find('div', id='upcoming').find_all('li', class_="list-item")
contents_UpComing = []
for li in upcoming:
    try:
        content = {}
        content['name'] = li.get('data-title')
       #  content['score'] = li.get('data-score')
        content['region'] = li.get('data-region')
        content['release_date'] = li.find('li', class_="release-date").get_text().replace(' ','').replace('\n','')
        content['actors'] = li.get('data-actors')
        content['duration'] = li.get('data-duration')
        content['href'] = li.a.get('href')
        content['img'] = li.img.get('src')    
        contents_UpComing.append(content)
    except:
        print(li)

data_UpComing = pd.DataFrame(contents_UpComing)

from sqlalchemy import create_engine

engine = create_engine('sqlite:///data.sqlite')

data_NowPlaying.to_sql('NowPlaying', engine, index=False, if_exists='replace')

data_UpComing.to_sql('Upcoming', engine, index=False, if_exists='replace')

