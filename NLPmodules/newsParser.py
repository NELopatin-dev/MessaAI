import requests
from bs4 import BeautifulSoup


class parser:
    def __init__(self):
        self.main_url = r'https://russian.rt.com'
        self.parse_url = r'https://russian.rt.com/listing/tag.neft/prepare/all-new/'

    def getNews(self, countNews: int = 100, page: int = 0):
        url = f"{self.parse_url}{countNews}/{page}"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            news_elements = soup.find_all('div', class_='card card_all-new')
            
            result = []

            for news in news_elements:
                title = news.find('a', class_='link').text.strip()
                link = self.main_url + news.find('a', class_='link')['href']
                content = news.find('div', class_='card__summary').text.strip()
                date = news.find('time', class_='date')['datetime']
                img_link = news.find('img', class_='cover__image')

                fullContent = self.getFullContent(link)

                result.append({
                    'title': title,
                    'link': link,
                    'content': content,
                    'full_content': fullContent,
                    'date': date,
                    'img_link': img_link if img_link is None else img_link['src']
                })
            
            return result

        else:
            print('Ошибка при выполнении запроса:', response.status_code)
            return []


    def getFullContent(self, link: str = None):
        if link is not None:
            response = requests.get(link)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                result = soup.find('div', class_='article__text').text.strip()
                
                return result

            else:
                print('Ошибка при выполнении запроса:', response.status_code)
                return []


