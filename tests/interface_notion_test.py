import random

import interfaces.notion_module as Notion
import config.configuration_module as Config

config = Config.Config()

nt_connect = Notion.NotionConnect(
    oauth_secret = config.notion_oauth
    )

def test_get_database_data():
    meal_dict = [
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
    for meal in meal_dict:
        database_request_body = {
            "filter": {
                "property": "Tags",
                "multi_select": {
                    "contains": meal["name"]
                }
            }
        }
        nt_database_output = nt_connect.get_database_data(target_id = "0eb3f467210247428ddf6513dc38e1b8", json_body=database_request_body)
        random_meal = nt_database_output[random.randrange(len(nt_database_output))]
        assert isinstance(random_meal["properties"]["Name"]["title"][0]["text"]["content"], str)
        assert random_meal["properties"]["Tags"]["multi_select"][0]["name"] == meal["name"]
        print(f"tag: {random_meal["properties"]["Tags"]["multi_select"][0]["name"]}")