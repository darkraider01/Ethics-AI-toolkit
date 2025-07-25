from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv() # Load environment variables from .env file

class EthicsChatbot:
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found. Please set it as an environment variable or pass it directly.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash') # Changed model to gemini-1.5-flash
        self.chat = self.model.start_chat(history=[])

    def send_message(self, message):
        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            return f"Error: {e}"

if __name__ == "__main__":
    # Example usage (requires GEMINI_API_KEY environment variable set)
    # bot = EthicsChatbot()
    # print(bot.send_message("Hello, what is the Ethics Toolkit?"))
    pass