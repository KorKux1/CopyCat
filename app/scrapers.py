# Requests
import requests

# Bs4
from bs4 import BeautifulSoup

# pandas
import pandas as pd

# Scrapy
import scrapy
from scrapy.crawler import CrawlerProcess

# Selenium 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# Others
from multiprocessing import Process, Queue
from twisted.internet import reactor


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


class FalabellaSpider():
    """
    [Responsible for scraping the Falabella website]
    """
    def __init__(self, product_searched='Mugs', *args, **kwargs): 
        """[This constructor initializes the FalabellaScraper class with the useful values in order to obtain the information correctly.]

        Keyword Arguments:
            product_searched {str} -- [Product to look for, this comes from the flask form] (default: {'Mugs'})
        """
        self.url = f'https://www.falabella.com.co/falabella-co/search?Ntt={product_searched}'
        self.base_url = 'https://www.falabella.com.co'

    def scrape(self):
        """[It is responsible for initializing the scraping]

        Returns:
            products_list {list} -- [scraped products list]
        """
        shop = 'Falabella'
        products_list = []
        try:
            request = requests.get(self.url)
            if request.status_code == 200:
                soup = BeautifulSoup(request.text, 'lxml')
                products = soup.find_all('div', attrs={'class': 'jsx-2743978790 jsx-3886284353 pod pod-4_GRID'})
                for product in products:
                    try:
                        url = product.a.get('href')
                        title = product.find('div', {
                                            'class': 'jsx-2743978790 jsx-3886284353 pod-details pod-details-4_GRID'}).find('a').find('span').find('b').text
                        img = product.a.img.get('src')
                        price = product.find(
                            'a', {'class': 'jsx-2743978790 jsx-3886284353 pod-summary pod-link pod-summary-4_GRID'}).find('span').text
                        products_list.append({'shop': shop, 'shop_url': request.request.url,
                                            'url': url, 'title': title, 'img': img, 'price': price})
                    except Exception as e:
                        print(f'Error with the data {e}')       
            else:
                print(f'Url not response code 200. Error: {request.status_code}')   
        except Exception as e:
            print('Error conection with Falabella')
            print(e)
        return products_list


class AmazonSpider():
    """
    [Responsible for scraping the Amazon website using Selenium]
    """

    def __init__(self, product_searched='Mugs', *args, **kwargs):
        """[This constructor initializes the AmazonScraper class with the useful values in order to obtain the information correctly.]

        Keyword Arguments:
            product_searched {str} -- [Product to look for, this comes from the flask form] (default: {'Mugs'})
        """
        self.url = f'https://www.amazon.com/s?k={product_searched}'
        self.base_url = 'https://www.amazon.com/'

    def configure_driver(self):
        """
        [Configure the values for the driver]

        Returns:
            [driver] -- [driver with the settings to work]
        """

        options = webdriver.ChromeOptions()
        options.add_argument('--incognito')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        params = {
            "latitude": 4.570868,
            "longitude": -74.2973328,
            "accuracy": 100
        }
        driver.execute_cdp_cmd("Page.setGeolocationOverride", params)
        return driver

    def clean_data(self):
        """[It is responsible for removing products that do not have complete data]

        Returns:
            [df] {dict}-- [Returns a dataframe with the products that have the complete data]
        """
        data = self.scrape()
        df = pd.DataFrame(data)
        df.dropna()
        return df.iterrows()

    def scrape(self):
        """
        [It is responsible for initializing the scraping]

        Returns:
            products_list {list} -- [scraped products list]
        """
        shop = 'Amazon'
        driver = self.configure_driver()
        delay = 5
        products_list = []
        try:
            driver.get(self.url)
            products = WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="s-expand-height s-include-content-margin s-border-bottom s-latency-cf-section"]/div')))
            for product in products:
                url = product.find_element_by_xpath(
                    './/h2[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-4"]/a').get_attribute('href')
                title = product.find_element_by_xpath('.//h2[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-4"]/a/span').text
                img = product.find_element_by_xpath('.//span[@class="rush-component"]//img').get_attribute('src')
                price = product.find_element_by_xpath('.//a[@class="a-size-base a-link-normal a-text-normal"]//span[@class="a-price-whole"]').text
                products_list.append({'shop': shop, 'shop_url': self.url, 'url': url, 'title': title, 'img': img, 'price': price})
        except Exception as e:
            print('Error with Amazon')
            print(e)
        driver.close()
        return products_list


def run_spider2(spider):
    process = CrawlerProcess()
    process.crawl(spider)
    process.start()
    

def run_spider(spider):
    """[Method to run scrapers made with Scrapy]

    Arguments:
        spider -- [Scraper made with Scrapy]
    """
    def f(q):
        try:
            runner = scrapy.crawler.CrawlerRunner()
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






   

        
