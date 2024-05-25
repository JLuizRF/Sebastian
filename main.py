from config import *
from account import AccountManager
from api import OpenAIManager
from messaging import MessageHandler
from automation import WebAutomation

def main():
    # Initialize components
    account_manager = AccountManager(account_owner, person_linkedin_path)
    openai_manager = OpenAIManager(openai.api_key)
    message_handler = MessageHandler(max_follow_ups, target_number_of_conversations, no_reply_follow_up)
    web_automation = WebAutomation(chrome_user_data_dir, chrome_profile_dir)

    # Example usage
    account_manager.display_account_info()
    openai_manager.set_api_key()
    message_handler.check_messages()
    web_automation.start_browser()

if __name__ == "__main__":
    main()
