import inquirer
import requests
import json
import pandas as pd
import numpy as np
import copy
import time

URL = 'http://localhost:8983/solr/craving/'
print()
print("Loading Craving Meter...")

#offline processing
category_df = pd.read_csv('product_categories_v2.csv') #read in file
category_df.loc[category_df['category_level_1'] != "categoryNotFound"] #remove items without category
category_df.drop(['category_level_1', 'category_level_2', 'category_level_5','category_level_6', 'category_level_7'], axis=1, inplace=True) #remove irrelevant category levels
category_df = category_df[category_df['category_level_3'].notna()] #drop empty category level 3
for col in category_df.columns: #strip out white space from both ends of remaining columns
    category_df[col] = category_df[col].str.strip()


def print_results(dict_returns, num_returns, query, category):
    '''
    dict_returns: dictionary converted from JSON results (after ranking)
    return_limit: number of returned results
    query: input for Solr
    '''
    if category is not None: 
        query = category
    print()
    print('Here are the top %s healthy options for "%s":' %(str(num_returns), query))
    for doc in dict_returns['response']['docs'][:num_returns]:
        print('******************************************')
        print(doc['fields.brand_name'][0], doc['fields.item_name'][0])
        print('   Nutrition Facts per serving (%s %s):' %(doc['fields.nf_serving_size_qty'][0],
                                                          doc['fields.nf_serving_size_unit'][0]))
        print('\tSugar:', doc['fields.nf_sugars'][0])
        print('\tSodium:', doc['fields.nf_sodium'][0])
        print('\tSaturated fat:', doc['fields.nf_saturated_fat'][0])
        print('\tDietary fiber:', doc['fields.nf_dietary_fiber'][0])
        print('\tProtein:', doc['fields.nf_protein'][0])
        print()

def query_with_pagination(query='*', return_limit=5000):
    '''
    Query with pagination, returns ranked results.
    '''
    offset = 0
    dict_returns = {}
    while True:
        payload = json.dumps({
        'query': query,
        'filter': 'fields.nf_sugars:[* TO *], fields.nf_sodium:[* TO *], fields.nf_saturated_fat:[* TO *], \
                   fields.nf_dietary_fiber:[* TO *], fields.nf_protein:[* TO *]',
        'offset': offset,
        'limit': return_limit,
        'sort': 'fields.nf_sugars asc, fields.nf_sodium asc, fields.nf_saturated_fat asc, \
                 fields.nf_dietary_fiber desc, fields.nf_protein desc',
        'params':{'q.op': 'AND'}
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", URL+'query', headers=headers, data=payload)
        page_returns = response.json()
        if offset == 0:
            dict_returns = copy.deepcopy(page_returns)
        else:
            dict_returns['response']['docs'].extend(page_returns['response']['docs'])
            dict_returns['response']['numFound'] += len(page_returns['response']['docs'])        
        if len(page_returns['response']['docs']) < return_limit:
            break
        else:
            offset += return_limit
    return dict_returns

DICT_RETURNS_NO_QUERY = query_with_pagination(query='*')

def filter_with_ids(dict_returns, id_limit=[]):
    '''
    Filter result with id_limit
    '''
    id_limit = set(id_limit)
    if len(id_limit) > 0:
        print('Filtering query results...')
        time_start = time.time()
        dict_filter = copy.deepcopy(dict_returns)
        dict_filter['response']['docs'] = []
        dict_filter['response']['numFound'] = 0
        
        for doc in dict_returns['response']['docs']:
            if doc['item_id'][0] in id_limit:
                dict_filter['response']['docs'].append(doc)
                dict_filter['response']['numFound'] += 1

        dict_returns = copy.deepcopy(dict_filter)
        
    return dict_returns

def product_recommend(query='*', num_options=3, return_limit=5000, id_limit=[], preference=[], allergy=[], category=None):
    '''
    Given a product, find healthy options
    Criteria: low sugar, low sodium, low unsaturated fats
              high fiber, high protein
    Input: query - string, no field name required
           num_options: number of recommendations desired
           return_limit: number of products listed per page
           id_limit: list of item ids for filtering ranked results
           preference: list of user dietary preferences
           allergy: list of user allergies
    '''
    # Query in Solr 
    # print('Gathering query results...')
    time_start = time.time()
    if query == '*':
        dict_returns = DICT_RETURNS_NO_QUERY
    else:
        dict_returns = query_with_pagination(query=query, return_limit=return_limit)
    # print('Query time:', time.time() - time_start)
    
    # filter with id_limit   
    dict_returns = filter_with_ids(dict_returns, id_limit=id_limit)
    # print('Filtering time:', time.time() - time_start)
    
    # print results
    num_found = dict_returns['response']['numFound']
    if num_found > 0:
        print_results(dict_returns, min(num_options, num_found), query, category)
    else:
        print('The query "%s" did not match any products.' % query)

'''Function to retrieve level 4 categories to display for user'''
def getSubcategoryList(category_level_3):
    lvl4 = category_df.drop(columns='item_id').loc[category_df['category_level_3'] == category_level_3]
    rest = lvl4['category_level_4'].unique()
    return rest.tolist()

'''Function to retrieve all products within a given category'''
def getProductList(category_value, level_number):
    category_column = 'category_level_'+str(level_number)
    products = category_df.loc[category_df[category_column] == category_value, 'item_id']
    return products.values.tolist()

print("... Loading complete\n")
#print("\n")
print('******************************************')
print('Welcome to Craving Meter!\n')
# product_recommend(query='kind banana')
#Product or Category
starter = {inquirer.Confirm('confirmed',
            message="Do you have a product in mind?" ,default=True),}
starter_response = inquirer.prompt(starter)
#print(starter_response["confirmed"])

if starter_response["confirmed"]: #product
    pdct = [inquirer.Text("product", message="What is the product name?"),]
    pdct_response = inquirer.prompt(pdct)
    product_recommend(pdct_response["product"])
else: #Category
    #Category phase 1: Grocery or Beverage
    c_1 = [inquirer.List('choice_1',
                message="Are you hungry or thirsty?",
                    choices=['Hungry', 'Thirsty'],),]
    c1_response = inquirer.prompt(c_1)
    #print(ans_1["choice_1"])

    category_lvl_3 = ""
    #Grocery
    if c1_response["choice_1"] == "Hungry":
        c_2 = [inquirer.List('choice_2',
                    message="What are you in the mood for?",
                    choices=['Diet Conscious Foods', 'Snack Foods', 'Nuts & Seeds', 'Nutritional Foods'],),]
        c2_response = inquirer.prompt(c_2)
        if c2_response["choice_2"] == 'Diet Conscious Foods':
            category_lvl_3 = "Dietary Supplement Foods"
        elif c2_response["choice_2"] == 'Nutritional Foods':
            category_lvl_3 = "Non-Supplement Nutritional Foods"
        else:
            category_lvl_3 = c2_response["choice_2"]

    #Beverage
    else: #thirsty
        c_bev = [inquirer.List('drink_1',
                    message="What are you in the mood for?",
                    choices=['Coffee & Tea','Dairy & Alternative Milk','Energy Drinks','Juice Beverage','Soft/Carbonated Drinks','Sports Drinks','Water'],),]
        choice_bev = inquirer.prompt(c_bev)

        if choice_bev["drink_1"] == 'Coffee & Tea':
            ct_1 = [inquirer.List('coffee_tea_1',
                    message="Coffee or Tea?",
                    choices=['Coffee','Tea'],),]
            ct_bev = inquirer.prompt(ct_1)
            category_lvl_3 = ct_bev["coffee_tea_1"]

            ct_powder = [inquirer.List('coffee_tea_2',
                    message="What method would you prefer?",
                    choices=['Already made (liquid)','Make it yourself (powder)'],),]
            ct_powder_bev = inquirer.prompt(ct_powder)
            
            if ct_powder_bev["coffee_tea_2"] == 'Make it yourself (powder)':
                category_lvl_3 = 'Coffee / Tea Variety Packs'

            # c2_response = ct_bev
        elif choice_bev["drink_1"] == 'Dairy & Alternative Milk':
            dam_1 = [inquirer.List('dairy_1',
                    message="Dairy or Non-Dairy?",
                    choices=['Dairy','Non-Dairy'],),]
            dam_bev = inquirer.prompt(dam_1)

            if dam_bev["dairy_1"] == 'Dairy':
                dam_bev = "Dairy-Based Drinks (Shelf-Stable)"
            else:
                dam_bev = "Dairy Substitute Based Drinks (Shelf Stable)"
            
            category_lvl_3 = dam_bev
        elif choice_bev["drink_1"] == 'Sports Drinks':
            sd_1 = [inquirer.List('sport_1',
                    message="What method would you prefer?",
                    choices=['Already made (liquid)','Mix it yourself (powder)'],),]
            sd_bev = inquirer.prompt(sd_1)

            if sd_bev["sport_1"] == 'Already made (liquid)':
                sd_bev = "Sports Drinks"
            else:
                sd_bev = "Drink Mixes & Flavorings"
            
            category_lvl_3 = sd_bev
        elif choice_bev["drink_1"] == 'Juice Beverage':       
            category_lvl_3 = "Fruit & Vegetable Drinks"

        elif choice_bev["drink_1"] == 'Soft/Carbonated Drinks':       
            category_lvl_3 = "Soda / Flavored Drinks"
        else:
            category_lvl_3 = choice_bev["drink_1"]

    # print(f'final result: {category_lvl_3}')
    lvl_4 = ["Snack Foods","Nuts & Seeds","Dietary Supplement Foods","Non-Supplement Nutritional Foods","Coffee","Water","Soda / Flavored Drinks","Dairy-Based Drinks (Shelf-Stable)","Tea","Sports Drinks"]
    # valid_categories = ["Snack Foods","Nuts & Seeds","Dietary Supplement Foods","Non-Supplement Nutritional Foods","Coffee","Water","Soda / Flavored Drinks","Fruit & Vegetable Drinks","Drink Mixes & Flavorings","Dairy-Based Drinks (Shelf-Stable)","Tea","Dairy Substitute Based Drinks (Shelf Stable)","Energy Drinks","Coffee / Tea Variety Packs","Sports Drinks"]

    product_list = []
    final_choice = ""
    if category_lvl_3 in lvl_4:
        cat_choice = getSubcategoryList(category_lvl_3)
        c_3 = [inquirer.List('choice_3',
                    message="What kind of "+category_lvl_3+" would you prefer?",
                    choices=cat_choice,),]
        c3_response = inquirer.prompt(c_3)
        final_choice = c3_response["choice_3"]
        #print(c3_response["choice_3"])
        product_list = getProductList(c3_response["choice_3"],4)
    else: #cat has no lvl 4
        #print(f'final result: {category_lvl_3}')
        final_choice = category_lvl_3
        product_list = getProductList(category_lvl_3,3)

    product_recommend(id_limit=product_list, category=final_choice)

#print(product_list)


# name = input("Enter name: ")

# print("data_type of name: ", type(name))