from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=chrome_options)


url='https://www.nutritionix.com/i/nabisco/100-cal-chips-ahoy-thin-crisps/51c3bdc897c3e6d8d3b479e5' #need to determine the id
# service = ChromeService(executable_path='/home/mfbricen/chromedriver_win32/chromedriver')
# driver = webdriver.Chrome(service=service)




# browser = webdriver.Chrome(executable_path="/home/mfbricen/chromedriver_win32/chromedriver.exe")
driver.implicitly_wait(10)
driver.get(url)


soup = BeautifulSoup(driver.page_source, "html.parser")
# items = soup.select("div")
# print(items)
mydivs = soup.find_all("div", class_="box-content ng-binding")
print(mydivs)

# print(soup.prettify())

# print(driver.title)
# h1 = driver.find_element(By.CLASS_NAME, "box-content ng-binding")
# print(h1)
# driver.implicitly_wait(0.5)
# element = driver.find_element(By.CSS_SELECTOR, "div[class='box-content ng-binding']")
# print(element)

driver.quit()





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