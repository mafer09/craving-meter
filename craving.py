import inquirer

#Category phase 1: Grocery or Beverage
final_category = ""
c_1 = [inquirer.List('choice_1',
            message="Are you hungry or thirsty?",
                choices=['Hungry', 'Thirsty'],),]
c1_response = inquirer.prompt(c_1)
#print(ans_1["choice_1"])

#Grocery
if c1_response["choice_1"] == "Hungry":
    c_2 = [inquirer.List('choice_2',
                message="What are you in the mood for?",
                choices=['Diet Conscious Foods', 'Snack Foods', 'Nuts & Seeds', 'Nutritional Foods'],),]
    c2_response = inquirer.prompt(c_2)
    if c2_response["choice_2"] == 'Diet Conscious Foods':
        final_category = "Dietary Supplement Foods"
    elif c2_response["choice_2"] == 'Nutritional Foods':
        final_category = "Non-Supplement Nutritional Foods"
    else:
        final_category = c2_response["choice_2"]

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
        final_category = ct_bev["coffee_tea_1"]

        ct_powder = [inquirer.List('coffee_tea_2',
                message="What method would you prefer?",
                choices=['Already made (liquid)','Make it yourself (powder)'],),]
        ct_powder_bev = inquirer.prompt(ct_powder)
        
        if ct_powder_bev["coffee_tea_2"] == 'Make it yourself (powder)':
            final_category = 'Coffee / Tea Variety Packs'

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
        
        final_category = dam_bev
    elif choice_bev["drink_1"] == 'Sports Drinks':
        sd_1 = [inquirer.List('sport_1',
                message="What method would you prefer?",
                choices=['Already made (liquid)','Mix it yourself (powder)'],),]
        sd_bev = inquirer.prompt(sd_1)

        if sd_bev["sport_1"] == 'Already made (liquid)':
            sd_bev = "Sports Drinks"
        else:
            sd_bev = "Drink Mixes & Flavorings"
        
        final_category = sd_bev
    else:
        final_category = choice_bev["drink_1"]

# print(f'final result: {final_category}')




# name = input("Enter name: ")

# print("data_type of name: ", type(name))