from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent import futures

##Code to set up selenium driver and get data
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

''' Function to parse page source and retrieve category information'''
def get_category(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    asis_cat = soup.find_all("div", class_="box-content ng-binding")
    if len(asis_cat) == 2:
        return(re.sub('\s+',' ',asis_cat[0].text))
    else:
        return("categoryNotFound")

''' Function to clean up the data to adhere to url required formatting'''
def format_url_field(param):
    param_l = param.lower() #convert to lowercase
    param_c = re.sub(r"[^a-zA-Z0-9]+", " ", param_l) #remove special characters except for spaces
    res = param_c.replace(" ", "-") #replace spaces with dashes
    return res

''' Function to build nutritionix url from item tuple'''
def build_url(item_tup):
    init_url = "https://www.nutritionix.com/i/" #https://www.nutritionix.com/i/h-e-b/couscous-quinoa-with-vegetables/546a07262bc0b27b2a676a8a
    brand_name = format_url_field(item_tup[0])
    item_name = format_url_field(item_tup[1])
    item_id = item_tup[2]
    full_url = init_url+brand_name+"/"+item_name+"/"+item_id
    return full_url

def get_category_from_url(url):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    item_id = url.split('/')
    try:
        # wait 10 seconds before looking for element
        # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fb-root")))
        time.sleep(2)
        item_cat = get_category(driver.page_source)
        return("{},\"{}\"".format(item_id[-1].strip(), item_cat))
        # print(type(item_cat))
    except Exception as e:
        print(e)
        return("{},\"{}\"".format(item_id[-1].strip(), "urlError"))
    finally:
        driver.quit()

##Tracker for runtime
start_time = time.time()

# ##Code below reads item_fields.txt file and generates product_urls.txt file. *Only needs to run once*
# ##Code to read in item_fields
# all_urls = []
# with open('item_fields.txt') as csv_file:
#     # for item in fp:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     for row in csv_reader: #specific to the first 2 lines #for line_number, row in zip(range(2), csv_reader):
#         item_url = build_url(row)
#         all_urls.append(item_url)

# ##Code to write in item urls into file for easier processing
# with open('product_urls.txt', 'w') as file_handle:
#     for item in all_urls:
#         file_handle.write('%s\n' % item)

##Code to read item urls and extract categories
url_list = []
with open('product_urls.txt', 'r') as file_processor:
    for curr_url in file_processor:
        url_list.append(curr_url)  

##Due to varying errors (of which at times ignore the try catch), the range of the products processed needs to be manually updated
for i in range(84500, len(url_list), 20):
    with futures.ThreadPoolExecutor() as executor: #parallelize the retrieval of products
        retries = 0
        while retries < 3:
            try:
                results = list(executor.map(get_category_from_url, url_list[i:i+20]))
                break
            except ConnectionRefusedError as cre:
                print("Connection refused error caught, retrying... Attempt {}".format(retries))
                retries+=1
            except ConnectionResetError as cre:
                print("Connection reset error caught, retrying... Attempt {}".format(retries))
                retries+=1
        if retries >= 3:
            print("Failure after multiple retries, abort")
            exit(1) 

    ##Code to write in item urls into file for later use
    with open('product_categories.txt', 'a') as file_handle:
        for item in results:
            file_handle.write(item+"\n")

    print ("Completed {} to {}".format(i, i+20))

print("--- %s seconds ---" % (time.time() - start_time))