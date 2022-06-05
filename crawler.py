
import requests
from bs4 import BeautifulSoup
import os
import re
import lxml
import itertools
import pandas as pd     
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains



class Spider:
    """ The spiders wild often build her spider web as a trap for catching that preys"""

    def __init__(self,url,delay_sleep,n_pages):
        self.url = url
        self.delay_sleep = delay_sleep
        self.n_pages = n_pages

    def url_connection(self,link):
        """this function sends a GET request and tests the operation of the url"""

        try:
            if requests.get(link).status_code == 200:
                return requests.get(link).content
            else:
                raise ServerError
        except:
            print('error al establecer coneccion')

    def trace_url_product(self,soup):
        """ Testing all kind of format page from Mercado Libre"""

        url1 = soup.select("a[class='ui-search-item__group__element ui-search-link']")
        url2 = soup.select("a[class='ui-search-result__content ui-search-link']")
        url3 = soup.select("a[class='promotion-item__link-container']")

        if url1:
            return [l["href"] for l in url1]
        elif url2:
            return [l["href"] for l in url2]
        elif url3:
            return [l["href"] for l in url3]
    
    def trace_spiderweb(self):
        """This function simulates the navigation through each page
           in each product category link of MercadoLibre website, 
           and returns all the links of the products explored in the first 10 pages."""

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(self.url)  #Initialized webdriver
        time.sleep(self.delay_sleep)

        links_page = []
        for _ in range(0,self.n_pages):
                t = 20
                while t > 0:
                        pix = 15000
                        driver.execute_script(f'window.scrollBy(0,{pix//t})')
                        t -= 1
                content = self.url_connection(self.url)
                soup = BeautifulSoup(content,'lxml')
                products_links = self.trace_url_product(soup)
                links_page.append(products_links)
                
                try:
                    new_link = soup.select("li[class='andes-pagination__button andes-pagination__button--next'] a[title='Siguiente']")
                    new_link = new_link[0]["href"]
                    self.url = new_link

                    time.sleep(0.01)
                    element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li[class='andes-pagination__button andes-pagination__button--next'] a[title='Siguiente']"))).click()
                    time.sleep(self.delay_sleep)
                except:
                    break


        driver.quit() #Finalized webdriver
        return links_page
    
    def catching_preys(self,content):
        """This function scrapy the necessary data on each product
            page using css selectors and regular expressions.
            Then return all features collected"""

        soup = BeautifulSoup(content,'lxml')

        des  = soup.select("h1[class='ui-pdp-title']")[0].text

        img  = soup.select("img[class='ui-pdp-image ui-pdp-gallery__figure__image']")[0]['src']

        price = soup.find("span",class_="andes-money-amount__fraction")
        price = re.findall(r">(\d+[,.]?\d*)<",str(price).replace(",",""))[0]

        brand = soup.find("span",class_="andes-table__column--value")
        brand = re.findall(r">([\w*|\W?]*)<",str(brand))
        brand = None if not brand else brand[0]
     
        discount_price = soup.find("span",class_="andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact")
        discount_price = re.findall(r">([0-9]+)\s",str(discount_price))[0]

        return (des,brand,price,discount_price,img)