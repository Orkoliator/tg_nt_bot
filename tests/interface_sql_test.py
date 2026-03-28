import interfaces.sql_module as SQL
import config.configuration_module as Config

config = Config.Config()

db = SQL.SqlConnect(db_file = config.db_file)
db.create_tables()

meals_test_dict = [
    {
        "meal_table": "TodayMeal",
        "recipe_name_str": "test_recipe_today_breakfast",
        "recipe_id_str": "123abc",
        "recipe_tag_str": "\u0417\u0430\u0432\u0442\u0440\u0430\u043a"
    },
    {
        "meal_table": "TodayMeal",
        "recipe_name_str": "test_recipe_today_dinner",
        "recipe_id_str": "234bcd",
        "recipe_tag_str": "\u041e\u0431\u0435\u0434"
    },
    {
        "meal_table": "TodayMeal",
        "recipe_name_str": "test_recipe_today_nooning",
        "recipe_id_str": "345cde",
        "recipe_tag_str": "\u041f\u0435\u0440\u0435\u043a\u0443\u0441"
    },
    {
        "meal_table": "TodayMeal",
        "recipe_name_str": "test_recipe_today_supper",
        "recipe_id_str": "456def",
        "recipe_tag_str": "\u0423\u0436\u0438\u043d"
    },
    {
        "meal_table": "TomorrowMeal",
        "recipe_name_str": "test_recipe_tomorrow_breakfast",
        "recipe_id_str": "tmr123abc",
        "recipe_tag_str": "\u0417\u0430\u0432\u0442\u0440\u0430\u043a"
    },
    {
        "meal_table": "TomorrowMeal",
        "recipe_name_str": "test_recipe_tomorrow_dinner",
        "recipe_id_str": "tmr234bcd",
        "recipe_tag_str": "\u041e\u0431\u0435\u0434"
    },
    {
        "meal_table": "TomorrowMeal",
        "recipe_name_str": "test_recipe_tomorrow_nooning",
        "recipe_id_str": "tmr345cde",
        "recipe_tag_str": "\u041f\u0435\u0440\u0435\u043a\u0443\u0441"
    },
    {
        "meal_table": "TomorrowMeal",
        "recipe_name_str": "test_recipe_tomorrow_supper",
        "recipe_id_str": "tmr456def",
        "recipe_tag_str": "\u0423\u0436\u0438\u043d"
    }
]

table_list = ["TodayMeal", "TomorrowMeal"]
for table in table_list:
    db.clear_recipe_table(table)

for recipe in meals_test_dict:
    db.add_recipe_to_table(recipe["meal_table"], recipe["recipe_name_str"], recipe["recipe_id_str"], recipe["recipe_tag_str"])

test_req_1 = db.get_recipe_with_tag_from_table("\u0423\u0436\u0438\u043d", "TodayMeal")
test_req_2 = db.get_recipe_with_tag_from_table("\u0417\u0430\u0432\u0442\u0440\u0430\u043a", "TomorrowMeal")

print("--- req 1 ---")
print(test_req_1)
print("--- req 2 ---")
print(test_req_2)

db.clear_recipe_table("TomorrowMeal")
