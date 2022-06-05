### This project consist on extrating data from differents categoryes on the web site Mercado Libre, to performace project it build a spider to get the data necessary to download data and resctructred the data in file with csv format.

#### A navigation with selenium is simulated through the links to the pages of product categories, the spider extracts all the links of each product browsing through the first 10 pages.

#### the description, price, discount price, brand and an image link are extracted from the links of all the products by category as if the spider ate its collection; this data is extracted with BeutifulSoup implementing css selectors and regular expressions.

#### Once the data has been extracted, it is given a structure to be saved as files in csv format in the path of our file system. 

Intructions:

* Download the project from the repository on your computer.
* Install the web driver from the folder WebDriver and save the executable in the same folder,
  There is a zip file with the chromdriver for windows (check the site https://chromedriver.chromium.org/downloads to download de chrome driver if you are using other operate system), if your are using other navigator check the documentation: https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/, just remember put the executable in WebDriver folder.
* Install all dependeces necessary with pip executing the requeriments.txt file.
* Run the main.py file.
* Wait the data completed the extracting and downloaded of the files csv.
* once completed the download check the files in folder Files_Downloaded.
