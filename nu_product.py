class NuProduct:
    def __init__(self, item_id, item_name, brand_name, calories, protein, total_fat, saturated_fat, sodium, sugars, total_carbs, 
        category_lvl_1, category_lvl_2=None, category_lvl_3=None, category_lvl_4=None, category_lvl_5=None, category_lvl_6=None, category_lvl_7=None):
        """
        Create nutritionix product with category data
        """
        self._item_id = item_id
        self._item_name = item_name
        self._brand_name = brand_name
        self._calories = calories
        self._protein = protein
        self._total_fat = total_fat
        self._saturated_fat = saturated_fat
        self._sodium = sodium
        self._sugars = sugars
        self._total_carbs = total_carbs
        self._category_lvl_1 = category_lvl_1
        self._category_lvl_2 = category_lvl_2
        self._category_lvl_3 = category_lvl_3
        self._category_lvl_4 = category_lvl_4
        self._category_lvl_5 = category_lvl_5
        self._category_lvl_6 = category_lvl_6
        self._category_lvl_7 = category_lvl_7
