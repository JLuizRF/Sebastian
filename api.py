import openai

class OpenAIManager:
    def __init__(self, api_key):
        self.api_key = api_key

    def set_api_key(self):
        openai.api_key = self.api_key
        print("OpenAI API key has been set.")
