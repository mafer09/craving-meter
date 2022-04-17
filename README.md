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
- `craving.py`
    - Requirements:
      - Configurations: 
        - Python (3.8.8) or newer
        - locally hosted Solr (8.11.1) already indexed with 87,716 product files and 1 category file (`product_categories_v2.csv`)
      - Installation: Inquirer package (pip install inquirer)
      - Limitation: There is a known [bug](https://github.com/magmax/python-inquirer/issues/117) within Inquirer that does not allow for list selection when script is ran in powershell. Current workaround: run script from VSCode Powershell terminal 

<br>

Note: the following notebooks are for references purposes only and are not necessary to execute/run CravingMeter
- `get_subcats_and_trace_cats.ipynb`
- `getBrandAndProductId.ipynb`
- `Product_Recommendation.ipynb`
- `Solr_Category.ipynb`
- `Solr_Queries.ipynb`
    