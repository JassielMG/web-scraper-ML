
from crawler import Spider
import os
import itertools
import pandas as pd

def get_files(total_products,spider):
    """ The data for each category caching by the spider
         is structured as an object to be manipulate """

    df = {"product":[],"brand":[],"price":[],"price_discount":[],"link_img":[]}

    for l in total_products:
        print("* Extracting data from "+l)
        content_html = spider.url_connection(l)
        feactures = spider.catching_preys(content_html)
        df["product"].append(feactures[0])
        df["brand"].append(feactures[1])
        df["price"].append(feactures[2])
        df["price_discount"].append(feactures[3])
        df["link_img"].append(feactures[4])
    file = pd.DataFrame(df)
    file.price = file.price.astype("int32")
    file.price_discount = file.price_discount.astype("int32")
    return file

def save(files):
   """This function saves all the obtained files in the product 
      files directory as a file csv format."""

   files_names = ["laptops.csv","bebidas.csv","fitness.csv","mas-vendido.csv"]
   for i,file in enumerate(files):
       file.to_csv(os.path.join(os.getcwd(),"Files_Downloaded",files_names[i]),index = False)

def main(urls):
    """ This function is the entry point to initialize the webspider and
        get all data by each link for category"""
    
    files = []
    for url in urls:
        spider = Spider(url,2,10)
        """The second parameter of the class is the time_sleep, 
        if this paramerte ir very low the web driver would be crash 
        because it will not charged completed the page and the button
        to click next page could not apper"""
        products_by_page = spider.trace_spiderweb()
        total_products = list(itertools.chain(*products_by_page))

        file = get_files(total_products,spider)
        files.append(file)
    save(files)


if __name__ == "__main__":
    urls = ("https://laptops.mercadolibre.com.mx/laptops-accesorios/#menu=categories",
            "https://listado.mercadolibre.com.mx/supermercado/bebidas/",
            "https://listado.mercadolibre.com.mx/_Deal_deportes-y-fitness-accesorios",
            "https://www.mercadolibre.com.mx/mas-vendidos/MLM1144")

    main(urls)