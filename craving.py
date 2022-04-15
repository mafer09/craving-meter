import inquirer
import pandas as pd

#offline processing
category_df = pd.read_csv('product_categories_v2.csv') #read in file
category_df.loc[category_df['category_level_1'] != "categoryNotFound"] #remove items without category
category_df.drop(['category_level_1', 'category_level_2', 'category_level_5','category_level_6', 'category_level_7'], axis=1, inplace=True) #remove irrelevant category levels
category_df = category_df[category_df['category_level_3'].notna()] #drop empty category level 3
for col in category_df.columns: #strip out white space from both ends of remaining columns
    category_df[col] = category_df[col].str.strip()

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
if category_lvl_3 in lvl_4:
    cat_choice = getSubcategoryList(category_lvl_3)
    c_3 = [inquirer.List('choice_3',
                message="What kind of "+category_lvl_3+" would you prefer?",
                choices=cat_choice,),]
    c3_response = inquirer.prompt(c_3)
    #print(c3_response["choice_3"])
    product_list = getProductList(c3_response["choice_3"],4)
else: #cat has no lvl 4
    #print(f'final result: {category_lvl_3}')
    product_list = getProductList(category_lvl_3,3)

#print(len(product_list))


# name = input("Enter name: ")

# print("data_type of name: ", type(name))