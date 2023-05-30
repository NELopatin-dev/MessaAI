import requests
import pandas as pd
from bs4 import BeautifulSoup

from NLPmodules import translateRU_EN

class parser:
    def __init__(self):
        self.main_url = r'https://oilgasinform.ru'
        self.parse_url = r'https://oilgasinform.ru/science/glossary/?SHOWALL_1=1'

    def getWiki(self):
        url = f"{self.parse_url}"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            news_elements = soup.find_all('tr', class_='item')
            
            result = []

            for i, news in enumerate(news_elements):
                print(i, '/', len(news_elements))

                term = news.find('b').text.strip()
                content = news.find('td').text.strip().split('-\n')
                content = content[1 if len(content) > 1 else 0]

                result.append({
                    'term': term,
                    # 'term_en': translateRU_EN.translate(term),
                    'discription': content,
                    # 'discription_en': translateRU_EN.translate(content),
                })

            return result

        else:
            print('Ошибка при выполнении запроса:', response.status_code)
            return []
