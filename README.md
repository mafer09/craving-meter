# craving-meter   
COMP 631 Final Project: Product Recommendation Based on Nutrition Tracking   
_Maria Briceno-Rojas (mfb2) and Bo Gong (bg46)_   

Code summary:
- `Nutritionix_query_API_Loop.ipynb`: Retrieve item/product information from Nutritionix API and write item files (.json) into Google Drive
    - Required credentials: Request API Key from [Nutritionix site](https://developer.nutritionix.com/signup) 
    - Input requirement: `new_snack_brands.csv` & `snack_brands_merge.csv`
    - Output: 87,716 product files written into Google Drive directly
- `get_brand_and_item_id.ipynb`: Get brand & item name and item id from API generated files and save into output file
    - Input requirement: Google Drive folder titled `COMP631-CravingMeter/Files` which contain 87,716 product files 
    - Output (generated file): `item_fields.txt` 
- `get_category.py`: Webscrape nutritionix website to get category product information and save into output file
    - Required installations: 
        1. Selenium Webdriver 4.1.0
        2. Chromedriver (Version number MUST match the installed (or to be installed) version of Google Chrome web browser)
    - Input requirement: `item_fields.txt`
    - Output (generated file): `product_ids.txt`
- `Solr_Queries.ipynb`: Dynamic interaction with Solr
    - Required configuration: locally hosted Solr (8.11.1) already indexed with 87,716 product files and 1 category file