from random import randrange
import re

import config.configuration_module as Config
import interfaces.notion_module as Notion
import interfaces.sql_module as SQL
import interfaces.tg_module as Telegram

config = Config.Config()

emoji_food_pot = u'\U0001F372'
emoji_cooking = u'\U0001F373'
emoji_bullet_point = u'\U0001F538'
emoji_scroll = u'\U0001F4DC'

class MealsLogic:
    
    def __init__(self):
        self.db = SQL.SqlConnect(db_file = config.db_file)
        self.notion = Notion.NotionConnect(oauth_secret = config.notion_oauth)
        self.db.create_tables()
        self.meal_dict = [
            {
                "name": "\u0417\u0430\u0432\u0442\u0440\u0430\u043a",
                "readable_name": "breakfast"
            },
            {
                "name": "\u041e\u0431\u0435\u0434",
                "readable_name": "dinner"
            },
            {
                "name": "\u041f\u0435\u0440\u0435\u043a\u0443\u0441",
                "readable_name": "nooning"
            },
            {
                "name": "\u0423\u0436\u0438\u043d",
                "readable_name": "supper"
            }
        ]
        self.spices_list = [
            "зелень",
            "кориандр",
            "куркума",
            "соль",
            "перец",
            "сахарозаменитель",
            "чеснок",
            "чеснок сушеный",
            "соус чили",
            "имбирь сухой молотый",
            "розмарин",
            "паприка",
            "хмели-сунели",
            "горчица",
            "лимонный сок",
            "разрыхлитель",
            "сода",
            "лимон",
            "корица",
            "ваниль",
            "бальзамический уксус",
            "карри",
            "тимьян"
        ]
        
    def _get_data_from_db(self, recipe_tag, table_name):
        recipe_data = self.db.get_recipe_with_tag_from_table(recipe_tag, table_name)
        return recipe_data

    def update_db(self):
        self.db.clear_recipe_table("TodayMeal")
        if self.db.check_if_table_empty("TomorrowMeal"):
            for meal in self.meal_dict:
                database_request_body = {
                    "filter": {
                        "property": "Tags",
                        "multi_select": {
                            "contains": meal["name"]
                        }
                    }
                }
                nt_database_output = self.notion.get_database_data(target_id = "0eb3f467210247428ddf6513dc38e1b8", json_body=database_request_body)
                random_meal = nt_database_output[randrange(len(nt_database_output))]
                random_meal_name = random_meal["properties"]["Name"]["title"][0]["text"]["content"]
                random_meal_id = random_meal["id"].replace("-","")
                self.db.add_recipe_to_table(meal_table="TodayMeal", recipe_name_str=random_meal_name, recipe_id_str=random_meal_id, recipe_tag_str=meal["name"])
        else:
            for meal in self.meal_dict:
                meal_data = self._get_data_from_db(meal["name"], "TomorrowMeal")
                self.db.add_recipe_to_table(meal_table="TodayMeal", recipe_name_str=meal_data["meal_name"], recipe_id_str=meal_data["meal_page"], recipe_tag_str=meal["name"])
            
        self.db.clear_recipe_table("TomorrowMeal")
        for meal in self.meal_dict:
            database_request_body = {
                "filter": {
                    "property": "Tags",
                    "multi_select": {
                        "contains": meal["name"]
                    }
                }
            }
            nt_database_output = self.notion.get_database_data(target_id = "0eb3f467210247428ddf6513dc38e1b8", json_body=database_request_body)
            random_meal = nt_database_output[randrange(len(nt_database_output))]
            random_meal_name = random_meal["properties"]["Name"]["title"][0]["text"]["content"]
            random_meal_id = random_meal["id"].replace("-","")
            self.db.add_recipe_to_table(meal_table="TomorrowMeal", recipe_name_str=random_meal_name, recipe_id_str=random_meal_id, recipe_tag_str=meal["name"])

    def get_today_recipe(self, recipe_tag):
        message_list = []
        image_link = ""
        meal_data = self._get_data_from_db(recipe_tag, "TodayMeal")
        message_list.append(f"{emoji_food_pot} {meal_data["meal_name"]} {emoji_food_pot}")
        recipe_blocks = self.notion.get_blocks_data(target_id = meal_data["meal_page"])
        for recipe_block in recipe_blocks:
            if recipe_block["type"] == "image":
                image_link = recipe_block["image"]["file"]["url"]
            elif recipe_block["type"] == "bulleted_list_item":
                message_list.append(f"{emoji_bullet_point} {recipe_block["bulleted_list_item"]["rich_text"][0]["text"]["content"]}")
            elif recipe_block["type"] == "heading_3":
                message_list.append(f"{emoji_cooking} {recipe_block["heading_3"]["rich_text"][0]["text"]["content"]}")
            elif recipe_block["type"] == "heading_2":
                message_list.append(f"## {recipe_block["heading_2"]["rich_text"][0]["text"]["content"]}")
            elif recipe_block["type"] == "heading_1":
                message_list.append(f"{emoji_food_pot} {recipe_block["heading_1"]["rich_text"][0]["text"]["content"]}")
            elif recipe_block["type"] == "paragraph":
                if recipe_block["paragraph"]["rich_text"]:
                    message_list.append(f"{recipe_block["paragraph"]["rich_text"][0]["text"]["content"]}")
        #print(f"DEBUG IMAGE:\n{image_link}")
        #print(f"DEBUG TEXT:")
        #for message_list_line in message_list:
        #    print(message_list_line)
        return image_link, message_list

    def get_tomorrow_shoplist(self):
        shoplist_dict = {
            "spices": [],
            "ingredients": {}
        }
        for meal in self.meal_dict:
            meal_data = self._get_data_from_db(meal["name"], "TomorrowMeal")
            meal_data_blocks = self.notion.get_blocks_data(target_id = meal_data["meal_page"])
            for meal_data_block in meal_data_blocks:
                if meal_data_block["type"] == "bulleted_list_item":
                    shoplist_item = meal_data_block["bulleted_list_item"]["rich_text"][0]["text"]["content"]
                    shoplist_item_name = re.match("^.* - ", shoplist_item)
                    shoplist_item_count = re.sub(shoplist_item_name.group(), "", shoplist_item)
                    shoplist_item_name = re.sub(" - ", "", shoplist_item_name.group())
                    if shoplist_item_name == "вода":
                        pass
                    elif shoplist_item_name in self.spices_list:
                        shoplist_dict["spices"].append(shoplist_item_name)
                    else:
                        shoplist_item_count = re.match("[0-9]+", shoplist_item_count).group()
                        if shoplist_item_name in shoplist_dict["ingredients"]:
                            shoplist_dict["ingredients"][shoplist_item_name] = shoplist_dict["ingredients"][shoplist_item_name] + int(shoplist_item_count)
                        else:
                            shoplist_dict["ingredients"][shoplist_item_name] = int(shoplist_item_count)
        return shoplist_dict