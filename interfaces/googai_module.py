from google import genai

class GoogAI:

    def __init__(self, api_key):
        self.client = genai.Client(
            api_key=api_key
        )

    def text_request(self, text_content):
        response = self.client.models.generate_content(
            model="gemini-3-flash-preview", contents=text_content
        )
        return response.text