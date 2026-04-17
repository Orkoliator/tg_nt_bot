import yaml
import os

class Config:
    
    def __init__(self):

        if os.name != 'nt':
            app_path_divider = '/'
        else:
            app_path_divider = '\\'
        self.root_dir_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
        self.db_dir_path = self.root_dir_path + app_path_divider + "db"

        if os.path.exists(f"{self.root_dir_path}{app_path_divider}config.yaml"):
            with open("config.yaml") as config_file:
                config = yaml.safe_load(config_file)

                self.notion_oauth = config["nt_internal_oauth_secret"]

                self.google_ai_api_key = config["google_ai_api_key"]

                self.telegram_api_id = config["telegram_api_id"]
                self.telegram_api_hash = config["telegram_api_hash"]
                self.telegram_bot_token = config["telegram_bot_token"]

                self.db_file = self.root_dir_path + app_path_divider + config["db_file"]

        else:
            self.notion_oauth = os.getenv("NT_INTERNAL_OAUTH_SECRET")
            
            self.google_ai_api_key = os.getenv("GOOGLE_AI_API_KEY")

            self.telegram_api_id = os.getenv("TELEGRAM_API_ID")
            self.telegram_api_hash = os.getenv("TELEGRAM_API_HASH")
            self.telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

            print(f"self.root_dir_path: {self.root_dir_path}\napp_path_divider: {app_path_divider}\nDB_FILE: {os.getenv("LOCAL_DB_FILE")}")
            self.db_file = self.root_dir_path + app_path_divider + os.getenv("LOCAL_DB_FILE")


        with open("config/prompt.txt") as config_file:
            self.workout_base_prompt = config_file.read()