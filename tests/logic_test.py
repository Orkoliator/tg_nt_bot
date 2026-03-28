import logic.logic as Logic

logic = Logic.Logic()

print("### test 1: refresh the table ###")

# optional db cleaning
'''
db = SQL.SqlConnect(db_file = "notion-tg-bot.db")
db.clear_recipe_table(meal_table="TodayMeal")
db.clear_recipe_table(meal_table="TomorrowMeal")
'''

logic.update_db()

print("\n### test 2: get today's supper recipe ###\n")

image_link, message_list = logic.get_today_recipe(recipe_tag="\u0423\u0436\u0438\u043d")
print(f"IMAGE:\n{image_link}")
print(f"TEXT:")
for message_list_line in message_list:
    print(message_list_line)

print("\n### test 3: get tomorrow shoplist ###\n")

message_list = logic.get_tomorrow_shoplist()
print("TOMORROW SHOPLIST FOR SINGLE PERSON:")
print("\n> INGREDIENTS:")
for shoplist_object in message_list["ingredients"]:
    print(f">> {shoplist_object}: {message_list["ingredients"][shoplist_object]} г")
print("\n> SPICES:")
for shoplist_object in message_list["spices"]:
    print(f">> {shoplist_object}")