import sqlite3, os

class SqlConnect:

    def __init__(self, db_file):
        self.db_file =  db_file
        self.meal_by_days = ["TodayMeal", "TomorrowMeal"]
        self.possible_tables = ["Subscribers"]
        self.possible_tables.extend(self.meal_by_days)
        self.possible_tags = [
            "\u0417\u0430\u0432\u0442\u0440\u0430\u043a",
            "\u041e\u0431\u0435\u0434",
            "\u041f\u0435\u0440\u0435\u043a\u0443\u0441",
            "\u0423\u0436\u0438\u043d"]
        # decode:
        #   - breakfast
        #   - dinner
        #   - nooning
        #   - supper
        self.subscription_types = ["Recipes", "Workout"]

    def create_tables(self):
        try:
            sqliteConnection = sqlite3.connect(self.db_file)
            cursor = sqliteConnection.cursor()
            sql_query_list = []
            for table_name in self.possible_tables:
                if table_name in self.meal_by_days:
                    table_structure = "(Meal VARCHAR(255), PageId VARCHAR(255), PageTag VARCHAR(255) PRIMARY KEY)"
                else:
                    table_structure = "(ChatID INT PRIMARY KEY, Recipes TINYINT(1), Workout TINYINT(1))"
                sql_query_list.append(f"CREATE TABLE IF NOT EXISTS {table_name} {table_structure}")
            for query in sql_query_list:
                cursor.execute(query)
        except sqlite3.Error as error:
            print(f"[DEBUG] {error}")
        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def add_subscriber(self, chat_id_int):
        sqliteConnection = sqlite3.connect(self.db_file)
        cursor = sqliteConnection.cursor()
        sql_query = f"SELECT ChatID FROM Subscribers WHERE ChatID = {chat_id_int} LIMIT 1;"
        cursor.execute(sql_query)
        sql_answer = cursor.fetchone()
        if sql_answer is None:
            sql_query = f"INSERT INTO Subscribers (ChatID, Recipes, Workout) VALUES ({chat_id_int}, 0, 0)"
                # 0 stays for False
                # 1 stays for True
            cursor.execute(sql_query)
            sqliteConnection.commit()
        sqliteConnection.close()

    def remove_subscriber(self, chat_id_int):
        sqliteConnection = sqlite3.connect(self.db_file)
        cursor = sqliteConnection.cursor()
        sql_query = f"DELETE FROM Subscribers WHERE ChatID = {chat_id_int}"
        cursor.execute(sql_query)
        sqliteConnection.commit()
        sqliteConnection.close()

    def update_subscribtion_type(self, chat_id_int, subscription_type, subscription_status):
        if subscription_type not in self.subscription_types:
            pass # type error
        else:
            sqliteConnection = sqlite3.connect(self.db_file)
            cursor = sqliteConnection.cursor()
            if subscription_status == False:
                subscription_status = 0
            else:
                subscription_status = 1
            sql_query = f"UPDATE Subscribers SET {subscription_type} = {subscription_status} WHERE ChatID = {chat_id_int}"
            cursor.execute(sql_query)
            sqliteConnection.commit()
            sqliteConnection.close()

    def check_if_table_empty(self, meal_table):
        sqliteConnection = sqlite3.connect(self.db_file)
        cursor = sqliteConnection.cursor()
        sql_query = f"SELECT Meal, PageId FROM {meal_table}"
        cursor.execute(sql_query)
        sqliteConnection.commit()
        result = cursor.fetchone()
        sqliteConnection.close()
        if result is None:
            return True
        else:
            return False

    def get_recipe_with_tag_from_table(self, recipe_tag_str, meal_table):
        if meal_table in self.meal_by_days:
            sqliteConnection = sqlite3.connect(self.db_file)
            cursor = sqliteConnection.cursor()
            sql_query = f"SELECT Meal, PageId FROM {meal_table} WHERE PageTag = \'{recipe_tag_str}\'"
            cursor.execute(sql_query)
            sqliteConnection.commit()
            recipe = cursor.fetchone()
            sqliteConnection.close()
            return {
                "meal_name": recipe[0],
                "meal_page": recipe[1]
            }
            
        else:
            print(f"[WARNING] wrong table, check if {meal_table} is a meal table")

    def add_recipe_to_table(self, meal_table, recipe_name_str, recipe_id_str, recipe_tag_str):
        if meal_table in self.meal_by_days:
            if recipe_tag_str in self.possible_tags:
                sqliteConnection = sqlite3.connect(self.db_file)
                cursor = sqliteConnection.cursor()
                sql_query = f"INSERT INTO {meal_table} (Meal,PageId,PageTag) VALUES (?, ?, ?)"
                recipe_tuple = (recipe_name_str, recipe_id_str, recipe_tag_str)
                cursor.execute(sql_query, recipe_tuple)
                sqliteConnection.commit()
                sqliteConnection.close()
            else:
                print(f"[WARNING] wrong tag, won't add recipe {recipe_name_str} to {meal_table}")
        else:
            print(f"[WARNING] wrong table, won't add recipe {recipe_name_str} to {meal_table}")

    def clear_recipe_table(self, meal_table):
        if meal_table in self.meal_by_days:
            sqliteConnection = sqlite3.connect(self.db_file)
            cursor = sqliteConnection.cursor()
            sql_query = f"DELETE FROM {meal_table}"
            cursor.execute(sql_query)
            sqliteConnection.commit()
            sqliteConnection.close()
        else:
            print(f"[WARNING] wrong table, won't clear table {meal_table}")
            