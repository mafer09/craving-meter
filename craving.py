import inquirer
cat_1 = [inquirer.List('category_1',
            message="Are you hungry or thirsty?",
                choices=['Hungry', 'Thirsty'],),]
ans_1 = inquirer.prompt(cat_1)
print(ans_1["category_1"])

if ans_1["category_1"] == "Hungry":
    cat_2 = [inquirer.List('category_2',
                message="What are you in the mood for?",
                choices=['Diet Conscious Foods', 'Snack Foods', 'Nuts & Seeds', 'Nutritional Foods'],),]

else:
    cat_2 = [inquirer.List('category_2',
                message="What are you in the mood for?",
                choices=['Coffee & Tea','Dairy & Alternative Milk','Energy Drinks','Juice Beverage','Soft/Carbonated Drinks','Sports Drinks','Water'],),]

    # caff = {
    # inquirer.Confirm('caffeine',
    #                  message="Do you need caffeine?" ,
    #                  default=True),}
    # confirmation = inquirer.prompt(caff)
    #print(confirmation["caffeine"])
    # if confirmation["caffeine"]:#caffeinated
    #     cat_2 = [inquirer.List('category_2',
    #                 message="What are you in the mood for?",
    #                 choices=['Coffee', 'Tea', 'Energy Drinks'],),]
    # else: #others

ans_2 = inquirer.prompt(cat_2)
print(ans_2["category_2"])

# questions = [
#   inquirer.List('size',
#                 message="What size do you need?",
#                 choices=['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
#             ),
# ]
# answers = inquirer.prompt(questions)
# print(answers["size"])
# name = input("Enter name: ")

# print("data_type of name: ", type(name))