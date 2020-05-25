# Requests
import requests

# Bs4
from bs4 import BeautifulSoup

# pandas
import pandas as pd

# Scrapy
import scrapy


class LinioSpider():
    """
    [This class is responsible for scraping the linio website]
    """
    def __init__(self, product_searched='Mugs', *args, **kwargs):
        """[This constructor initializes the LinioSpider class with the useful values in order to obtain the information correctly.]

        Keyword Arguments:
            product_searched {str} -- [Product to look for, this comes from the flask form] (default: {'Mugs'})
        """
        self.url = f'https://www.linio.com.co/search?scroll=&q={product_searched}'
        self.base_url = 'https://www.linio.com.co'

    def scrape(self):
        """[It is responsible for initializing the scraping]

        Returns:
            products_list {list} -- [scraped products list]
        """
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

    def clean_data(self):
        """[It is responsible for removing products that do not have complete data]

        Returns:
            [df] {dict}-- [Returns a dataframe with the products that have the complete data]
        """
        data = self.scrape()
        df = pd.DataFrame(data)
        df.dropna()
        return df


class FalabellaSpider(scrapy.Spider):
    name = 'falabella_spider'
    custom_settings = {'FEED_FORMAT': 'json',
                    'FEED_URI': 'results.json',
                    }

    def __init__(self, product_searched='Mugs', *args, **kwargs):
        super(FalabellaSpider, self).__init__(*args, **kwargs)

        self.allowed_domains = ['falabella.com.co', ]
        
        self.start_urls = [f'https://www.falabella.com.co/falabella-co/search?Ntt={product_searched}']

    def parse(self, response):
        shop = 'Falabella'
        for product in response.xpath('//div[@class="jsx-2743978790 jsx-3886284353 pod pod-4_GRID"]').getall():
            sel = scrapy.Selector(text=product)
            url = sel.xpath('//a[@class="jsx-3185677989  layout_grid-view"]/@href').get()
            title = sel.xpath('//b[@class="jsx-2743978790 copy2 primary  jsx-2849163555 normal   pod-subTitle"]/text()').get()
            img = sel.xpath('//img/@src').get()
            price = sel.xpath('//span[@class="copy1 primary high jsx-2849163555 normal  "]/text()').get()
            yield {'shop': shop, 'shop_url':response.url, 'url': url, 'title': title, 'img': img, 'price': price}



def run_spider(spider):
    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            deferred = runner.crawl(spider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result



   

        
