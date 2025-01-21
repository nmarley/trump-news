# import requests
from bs4 import BeautifulSoup

# url = 'https://www.example.com'  # Replace with actual URL
# html = requests.get(url).text
with open('wh.html', 'r', encoding='utf-8') as f:
    html = f.read()
soup = BeautifulSoup(html, 'html.parser')

for li in soup.find_all('li', class_='wp-block-post'):
    a = li.find('h2').find('a')
    title = a.text.strip()
    link = a['href']
    timestamp = li.find('time')['datetime']
    print({'title': title, 'link': link, 'timestamp': timestamp})
