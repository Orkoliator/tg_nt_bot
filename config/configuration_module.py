import yaml
import os

class Config:
    
    def __init__(self):

        with open("config.yaml") as config_file:
            config = yaml.safe_load(config_file)

            self.notion_oauth = config["nt_internal_oauth_secret"]

            self.google_ai_api_key = config["google_ai_api_key"]

            self.telegram_api_id = config["telegram_api_id"]
            self.telegram_api_hash = config["telegram_api_hash"]
            self.telegram_bot_token = config["telegram_bot_token"]

            self.db_file = config["db_file"]
        with open("config/prompt.txt") as config_file:
            self.workout_base_prompt = config_file.read()
        
        if os.name != 'nt':
            app_path_divider = '/'
        else:
            app_path_divider = '\\'
        root_dir = os.path.dirname(__file__) + app_path_divider
        self.db_file = root_dir + 'db' + app_path_divider + self.db_file