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

''' Function to manipulate the selenium driver'''
# def sel_sess(commd, driver, url=""):
#     if commd == "get":
#         driver.implicitly_wait(10)
#         driver.get(url)
#         return driver.page_source
#     elif commd == "done":
#         driver.quit()
#         return None
    
''' Function to parse page source and retrieve category information'''
def get_category(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    asis_cat = soup.find_all("div", class_="box-content ng-binding")
    if len(asis_cat) == 2:
        return(re.sub('\s+',' ',asis_cat[0].text))
    else:
        return("categoryNotFound")

'''function to clean up the data to adhere to url required formatting'''
def format_url_field(param):
    param_l = param.lower() #convert to lowercase
    param_c = re.sub(r"[^a-zA-Z0-9]+", " ", param_l) #remove special characters except for spaces
    res = param_c.replace(" ", "-") #replace spaces with dashes
    return res

'''function to build nutritionix url from item tuple'''
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



###ONE TIME CODE
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
    for curr_url in file_processor:#curr_url in file_processor:
# curr_url = "https://www.nutritionix.com/i/h-e-b/thin-sliced-natural-cheese-carolina-reaper-pepper/61acc46e244643000aabe8f1"
        url_list.append(curr_url)
        # print(f'current item processed {line_number}')   

for i in range(30, 500, 20):
    with futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(get_category_from_url, url_list[i:i+20]))

    # print(results)
    # ##Code to write in item urls into file for easier processing
    with open('product_categories.txt', 'a') as file_handle:
        for item in results:
            file_handle.write(item+"\n")

    print ("Completed {} to {}".format(i, i+20))




##Command needed to quit selenium driver
# print(processed_item)
print("--- %s seconds ---" % (time.time() - start_time))


##ARCHIVED code
##Temporary code to write page_source contents into a local file
# fileToWrite = open("page_source.html", "w")
# ret_ps = sel_sess("get",curr_driver,curr_url)
# fileToWrite.write(ret_ps)
# fileToWrite.close()

##Temporary code to read in page_source contents from local file for manipulation
# fileToRead = open("page_source.html", "r")
# ret_ps = fileToRead.read()
# fileToRead.close()

# print(type(driver.page_source))

# soup = BeautifulSoup(driver.page_source, "html.parser")
# # items = soup.select("div")
# # print(items)
# mydivs = soup.find_all("div", class_="box-content ng-binding")
# print(mydivs)

# print(soup.prettify())

# print(driver.title)
# h1 = driver.find_element(By.CLASS_NAME, "box-content ng-binding")
# print(h1)
# driver.implicitly_wait(0.5)
# element = driver.find_element(By.CSS_SELECTOR, "div[class='box-content ng-binding']")
# print(element)

# driver.quit()





# soup = BeautifulSoup(browser.page_source,"html.parser")
# items=soup.select(".box-title")
# print(items)






# driver.quit()
# # faas_station_list = ['KATP','KBBF','KBQX','KCMB','KCRH','KCVW','KDLP','KEHC','KEIR','KEMK','KGBK','KGHB','KGRY','KGUL','KGVX','KHHV','KHQI','KIKT','KIPN','KMDJ','KMIS','KMIU','KMYT','KMZG','KOPM','KSCF','KSPR','KSQE','KSTZ','KVAF','KVBS','KVKY','KVNP','KVOA','KVQT','KXIH','KXPY']

# # for station in faas_station_list:
# # Request to website and download HTML contents
# url='https://www.nutritionix.com/i/nabisco/100-cal-chips-ahoy-thin-crisps/51c3bdc897c3e6d8d3b479e5' #need to determine the id
# req=requests.get(url)
# content=req.text
# soup = BeautifulSoup(content,'html.parser')

# # print(soup.prettify())
# mydivs = soup.find_all("div", {"class": "col-sm-7.col-lg-7"})
# print(mydivs)



# raw = soup.findAll('meta')
# lat_log_string = str(raw[3])
# pattern = '\((.*?)\)'
# coord = re.search(pattern, lat_log_string).group(1)
# station_lat_lon = coord.split()
# print(station,station_lat_lon)#station_name)