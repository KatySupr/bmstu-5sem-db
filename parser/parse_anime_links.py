import requests
from bs4 import BeautifulSoup

pages = range(1, 15)
with open('./links/anime_links_new.txt', 'w') as anime_links:
    for page in pages:
        url = 'https://animego.org/anime/filter/type-is-tv/status-is-released/apply' # + str(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        urls = []

        links = soup.find_all('div', class_='h5 font-weight-normal mb-1')
        for link in links:
            hrefval = link.find('a').get('href')
            ind = hrefval.rfind('-')
            hrefval = hrefval[:ind+1] + 'm' + hrefval[ind+1:]
            urls.append(hrefval)
            print(link)
        for elem in urls:
            anime_links.write(elem + '\n')