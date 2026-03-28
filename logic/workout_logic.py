
import interfaces.googai_module as GoogAI
import interfaces.sql_module as SQL
import config.configuration_module as Config

config = Config.Config()

class WorkoutLogic:
    
    def __init__(self):
        self.db = SQL.SqlConnect(db_file = config.db_file)
        self.ai_connect = GoogAI.GoogAI(api_key = config.google_ai_api_key)
    
    def _generate_traning(self):
        return self.ai_connect.text_request(text_content = config.workout_base_prompt)