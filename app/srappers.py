import requests
from bs4 import BeautifulSoup

class LinioSpider():
    def __init__(self, product_searched='Mugs', *args, **kwargs):    
        self.url = f'https://www.linio.com.co/search?scroll=&q={product_searched}'
        self.base_url = 'https://www.linio.com.co'

    def scrape(self):
        shop = 'Linio'
        products_list = []
        try:
            request = requests.get(self.url)
            if request.status_code == 200:
                soup = BeautifulSoup(request.text, 'lxml')
                for product in soup.select('div[class*="catalogue-product row"]'):
                    url = self.base_url+product.find('a').get('href')
                    title = product.find('a').get('title')
                    img = product.find('a').find('meta', {'itemprop': 'image'} ).get('content')
                    price = product.find('div',{'class':'price-section'}).find('meta', {'itemprop':"price"}).get('content')
                    products_list.append({'shop': shop, 'shop_url':request.request.url, 'url': url, 'title': title, 'img': img, 'price': price})
            else:
                print(f'Url not response code 200. Error: {request.status_code}') 
        except Exception as e:
            print('Error conection with Linio')
            print(e)
        return products_list

   

        
