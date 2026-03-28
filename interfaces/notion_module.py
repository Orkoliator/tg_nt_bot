import requests
import time

class NotionConnect:

    def __init__(self, oauth_secret):
        self.oauth_secret = oauth_secret
        self.auth_string = f"Bearer {self.oauth_secret}"
        
    
    def _get_target_data(self, target_type, start_cursor=None, accumulated_result=None):

        if accumulated_result is None:
            accumulated_result = []

        headers = {
            "Authorization": self.auth_string,
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }

        if self.json_body == None:
            self.json_body = {}

        if start_cursor:
            self.json_body["start_cursor"] = start_cursor
        
        if target_type == "database":
            #print("database!")
            response = requests.post(f"https://api.notion.com/v1/databases/{self.target_id}/query", headers=headers, json=self.json_body)
        elif target_type == "page":
            #print("page!")
            response = requests.get(f"https://api.notion.com/v1/pages/{self.target_id}", headers=headers, json=self.json_body)
        elif target_type == "blocks":
            #print("blocks!")
            response = requests.get(f"https://api.notion.com/v1/blocks/{self.target_id}/children", headers=headers, json=self.json_body)
        else:
            raise Exception("Unknown target type")
        if response.status_code == 200:
            accumulated_result.extend(response.json().get("results", []))
            if "has_more" in response.json():
                if response.json()["has_more"]:
                    time.sleep(0.1)
                    return self._get_target_data(target_type, start_cursor=response.json()["next_cursor"], accumulated_result=accumulated_result)
                else:
                    return accumulated_result

        else:
            error_message = response.json()
            raise Exception(f"Status code: {response.status_code}; Error: {error_message["message"]}")


    def get_database_data(self, target_id, json_body=None):
        self.json_body = json_body
        self.target_id = target_id
        return self._get_target_data("database")


    def get_page_data(self, target_id, json_body=None):
        self.json_body = json_body
        self.target_id = target_id
        return self._get_target_data("page")


    def get_blocks_data(self, target_id, json_body=None):
        self.json_body = json_body
        self.target_id = target_id
        return self._get_target_data("blocks")