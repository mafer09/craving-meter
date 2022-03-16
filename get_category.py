from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import urllib.request

''' Function to manipulate the selenium driver'''
def sel_sess(commd, driver, url=""):
    if commd == "get":
        driver.implicitly_wait(10)
        driver.get(url)
        return driver.page_source
    elif commd == "done":
        driver.quit()
        return None
    
''' Function to parse page source and retrieve category information'''
def get_category(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    asis_cat = soup.find("div", class_="box-content ng-binding").text
    clean_cat = re.sub('\s+',' ',asis_cat)
    return clean_cat

'''function to clean up the data to adhere to url required formatting'''
def format_url_field(param):
    param = param[1:-1] #remove wrapping quotes
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



start_time = time.time()
##Code to set up selenium driver and get data
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# curr_driver = webdriver.Chrome(options=chrome_options)

# curr_url='https://www.nutritionix.com/i/nabisco/100-cal-chips-ahoy-thin-crisps/51c3bdc897c3e6d8d3b479e5' #need to determine the id

##Temporary code to write page_source contents into a local file
# fileToWrite = open("page_source.html", "w")
# ret_ps = sel_sess("get",curr_driver,curr_url)
# fileToWrite.write(ret_ps)
# fileToWrite.close()

##Temporary code to read in page_source contents from local file for manipulation
# fileToRead = open("page_source.html", "r")
# ret_ps = fileToRead.read()

# # print(get_category(ret_ps))



# fileToRead.close()

##Code to read in item_fields
with open('item_fields.txt') as fp:
    item = fp.readline()
    #need to implement while loop here
    res_item = tuple(map(str,item.split(','))) #turn string into tuple of 3 elements
    item_url = build_url(res_item)
    # print(url_ok(item_url))

##Command needed to quit selenium driver
# sel_sess("done", curr_driver)
print("--- %s seconds ---" % (time.time() - start_time))

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