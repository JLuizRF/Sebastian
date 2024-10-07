import time
import psutil
import os
import sys
import logging
import spacy
import random
import openai
import pyautogui
import threading
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
#logging.basicConfig(level=logging.DEBUG)


# Accounts on hold
#    
#    {   #'account_owner': 'Thea Miyakawa',
#        #'person_linkedin_path': "in/thea-miyakawa-2b20796b/",
#        #'chrome_user_data_dir': "C:\\Users\\55199\\AppData\\Local\\Google\\Chrome\\User Data",
#        #'chrome_profile_dir': "Profile 33"
#    },


# Google Sheets setup
def setup_google_sheets(sheet_name, worksheet_name):
    try:
        # Define the scope
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        # Provide the path to your credentials JSON file
        creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\55199\OneDrive\Área de Trabalho\Automations\Sebastian\credentials.json', scope)
        
        # Authorize the client
        client = gspread.authorize(creds)
        
        # Open the Google Sheet by name
        sheet = client.open(sheet_name)
        
        # Select the worksheet by name
        worksheet = sheet.worksheet(worksheet_name)
        
        return worksheet
    except Exception as e:
        print(f"Error setting up Google Sheets: {e}")
        return None

def log_message_to_sheet(worksheet, message):
        try:
            worksheet.insert_row([message], 22)  # Insert the message at the top of the sheet
            print("\n 📖✒️ Message logged to Google Sheet 📖✒️\n ")
        except Exception as e:
            print(f"An error occurred while logging the message to the sheet: {e}")

# ACCOUNTS
# List of accounts to loop through. To get Chrome person number, search for "chrome://version" in the Chrome search bar
accounts = [
     {
       'account_owner': 'José Luiz R. F.',
        'person_linkedin_path': "in/joseluizrochafilho/",
        'chrome_user_data_dir': "C:\\Users\\55199\\AppData\\Local\\Google\\Chrome\\User Data",
        'chrome_profile_dir': "Profile 1"
    },
    {   'account_owner': 'Joanne Tria Lim',
        'person_linkedin_path': "in/joanne-tria-lim-0771561b8/",
        'chrome_user_data_dir': "C:\\Users\\55199\\AppData\\Local\\Google\\Chrome\\User Data",
        'chrome_profile_dir': "Profile 40"
    },
    {   'account_owner': 'Morgan Johnson',
        'person_linkedin_path': "in/morgan-johnson-9072381bb/",
        'chrome_user_data_dir': "C:\\Users\\55199\\AppData\\Local\\Google\\Chrome\\User Data",
        'chrome_profile_dir': "Profile 39"
    }, 
    {   'account_owner': 'Andrew Reese H.',
        'person_linkedin_path': "in/andrew-reese-h-606271250/",
        'chrome_user_data_dir': "C:\\Users\\55199\\AppData\\Local\\Google\\Chrome\\User Data",
        'chrome_profile_dir': "Profile 38"
    }, 
    {   'account_owner': 'James MB',
        'person_linkedin_path': "in/james-mb-92a53820b/",
        'chrome_user_data_dir': "C:\\Users\\55199\\AppData\\Local\\Google\\Chrome\\User Data",
        'chrome_profile_dir': "Profile 37"
    }, 
    {   'account_owner': 'Brian C',
        'person_linkedin_path': "in/brian-c-4119411bb/",
        'chrome_user_data_dir': "C:\\Users\\55199\\AppData\\Local\\Google\\Chrome\\User Data",
        'chrome_profile_dir': "Profile 36"
    }, 
    {   'account_owner': 'Enio C. Borges',
        'person_linkedin_path': "in/enio-c-borges-10aa261b6/",
        'chrome_user_data_dir': "C:\\Users\\55199\\AppData\\Local\\Google\\Chrome\\User Data",
        'chrome_profile_dir': "Profile 22"
    },     
    {
        'account_owner': 'Kudzai E. Mabika',
        'person_linkedin_path': "in/kudzai-e-mabika-921063201/",
        'chrome_user_data_dir': "C:\\Users\\55199\\AppData\\Local\\Google\\Chrome\\User Data",
        'chrome_profile_dir': "Profile 10"
    }, 
    {
        'account_owner': 'Kristine V. Sade',
        'person_linkedin_path': "in/kristine-v-sade-b81963296/",
        'chrome_user_data_dir': "C:\\Users\\55199\\AppData\\Local\\Google\\Chrome\\User Data",
        'chrome_profile_dir': "Profile 30"
    },
    {
        'account_owner': 'Lee Naong',
        'person_linkedin_path': "in/lee-naong-b6aa9b212/",
        'chrome_user_data_dir': "C:\\Users\\55199\\AppData\\Local\\Google\\Chrome\\User Data",
        'chrome_profile_dir': "Profile 31"
    },
    {
        'account_owner': 'Lee Xavier Naong',
        'person_linkedin_path': "in/lee-xavier-naong-556bb81a4/",
        'chrome_user_data_dir': "C:\\Users\\55199\\AppData\\Local\\Google\\Chrome\\User Data",
        'chrome_profile_dir': "Profile 32"
    },
    {
        'account_owner': 'Thea Castro',
        'person_linkedin_path': "in/thea-castro-870609211/",
        'chrome_user_data_dir': "C:\\Users\\55199\\AppData\\Local\\Google\\Chrome\\User Data",
        'chrome_profile_dir': "Profile 25"
    },
    {
       'account_owner': 'Jose Luiz R. Filho',
        'person_linkedin_path': "in/jose-luiz-r-filho-97817021b/",
        'chrome_user_data_dir': "C:\\Users\\55199\\AppData\\Local\\Google\\Chrome\\User Data",
        'chrome_profile_dir': "Profile 42"
    },

]

# Shuffle the accounts list to process them in random order each time the script runs
random.shuffle(accounts)


# MOTHER FUNCTION
def perform_actions_for_account(account, worksheet):    
    
    #SET UP

    # Support email
    support_email = 'research@onfrontiers.com'
    
    # API
    openai.api_key = 'The Key'

    # Max number of messages without a reply. 
    max_follow_ups = 1

    # Number of messages to check
    target_number_of_conversations = 9999

    # Follow-up for messages with no replies
    no_reply_follow_up = f"Hi! Just following up to let you know that our client is eager to collaborate with you. Please apply through the provided link. If you have questions about this opportunity, kindly check the shared link to learn more. Also, feel free to visit https://try.onfrontiers.com/knowledge to learn more about us or https://www.onfrontiers.com/policies/expert-participation-agreement to understand more about our policies. Looking forward to connecting!"

    # Variables for the accounts
    account_owner = account['account_owner']
    person_linkedin_path = account['person_linkedin_path']
    chrome_user_data_dir = account['chrome_user_data_dir']
    chrome_profile_dir = account['chrome_profile_dir']

# FUNCTIONS

    def click_random_position_within_area(top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        random_x = random.randint(top_left_x, bottom_right_x)
        random_y = random.randint(top_left_y, bottom_right_y)
        pyautogui.moveTo(random_x, random_y)
        pyautogui.click()

    # Check batery status and shut down if needed 
    def check_battery_and_shutdown():
        battery = psutil.sensors_battery()
        if battery is not None:
            battery_percent = battery.percent
            if battery_percent <= 19 and not battery.power_plugged:
                print(f"Battery is at {battery_percent}%. Shutting down the computer...")
                # Windows shutdown command
                if sys.platform == 'win32':
                    os.system("shutdown /s /t 1")
            else:
                print(f"\n 🔋🔋🔋 Battery is at {battery_percent}%. No need to shut down.🔋🔋🔋\n ")

    # Archive conversation card
    def archive_conversation(driver):
        try:
            print("\nAttempting to archive the conversation...\n")
            # Try to locate the first type of dropdown button
            try:
                dropdown_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.msg-thread-actions__control.artdeco-button.artdeco-button--circle.artdeco-button--2.artdeco-button--muted.artdeco-button--tertiary.artdeco-dropdown__trigger.artdeco-dropdown__trigger--placement-bottom.ember-view'))
                )
                print("First type of dropdown button found and clickable.")
            except:
                print("First type of dropdown button not found. Trying the second type.")
                try:
                    # If the first type is not found, try to locate the second type of dropdown button
                    dropdown_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.msg-thread-actions__control.artdeco-button.artdeco-button--circle.artdeco-button--1.artdeco-button--muted.artdeco-button--tertiary.artdeco-dropdown__trigger.artdeco-dropdown__trigger--placement-bottom.ember-view'))
                    )
                    print("Second type of dropdown button found and clickable.")
                except:
                    print("Second type of dropdown button not found. Trying the third type.")
                    # If the first and second types are not found, try to locate the third type of dropdown button
                    dropdown_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.msg-thread-actions__control artdeco-button artdeco-button--circle artdeco-button--1 artdeco-button--muted artdeco-button--tertiary artdeco-dropdown__trigger artdeco-dropdown__trigger--placement-bottom ember-view'))
                    )
                    print("Third type of dropdown button found and clickable.")

            # Click on the dropdown button to reveal the archive option
            dropdown_button.click()
            time.sleep(random.uniform(1, 3))  # Wait for the dropdown options to appear
            print("\n⏰ Dropdown menu clicked, waiting for options to appear⏰\n")

            # Locate the dropdown container
            dropdown_container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.artdeco-dropdown__content-inner'))
            )
            print("Dropdown container located.")

            # Locate and click the archive button within the dropdown menu
            archive_button = WebDriverWait(dropdown_container, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.msg-thread-actions__dropdown-option[role="button"][data-view-name="message-toolbar-dropdown-toggle-archive"]'))
            )
            print("Archive button located.")
            driver.execute_script("arguments[0].click();", archive_button)
            print("\n ✅ Archive button clicked. Conversation archived successfully.✅ \n")

            # Add a random delay after archiving to ensure UI updates
            time.sleep(random.uniform(1, 5))  # Added delay after archiving

        except Exception as e:
            print(f"\nError archiving conversation: {e}")



    # Generate a reply with GPT 
    def get_reply_from_gpt(account_owner, support_email, conversation_context, temperature=0.5, max_tokens=250):
    # General behavior and guidelines
        system_instructions = f'''
        - You are an assistant replying on behalf of {account_owner}.
        - You are writing a real message, not a template, write something that makes real sense.
        - Don't be lazy; think it through and write something that really addresses the last message based on the {conversation_context}.
        - You are inviting experts to apply to projects, not the other way around.
        - Refer to the projects as "opportunities" and use the project link for invitations.
        - Keep replies short, direct, and conversational.
        - When sharing the project link, get it from the first message. The project link will usually start with "https://link.onfrontiers.com/". Add the correct link.
        - Do not promise new opportunities; instead, guide experts to join the platform.
        - Do not agree to send emails, join calls, or set up meetings.
        - Only write the message in other language if the expert replied to you if the whole last message is in another language.
        - Make the messages simple and not like an email. Make it as short as needed when needed, write just the necessary.
        '''

        # Specific instructions for common scenarios
        specific_instructions = f'''
        If experts are:
        - having questions about our platform, inform them that we are a knowledge network platform and we match specific experts with specific clients so that experts can share knowledge with our clients.
        - interested and didn't inform that they have already applied, invite them to apply.
        - not interested, ask for referrals, and always advise them to share the project link with the referral, also and advise them to become an expert by visiting: https://app.onfrontiers.com/become-an-expert to get new project opportunities.
        - saying that they are not interested in a new role or new job but the project is a consultation opportunity. Advise them that it is a consultation opportunity which should take 30 to 60 minutes to be completed and there is no need for long-term engagement. 
        - wanting more information about the client or the project, tell them to check the project page; the information they are seeking is there.
        - saying that the project is closed, inform them that our client already got the needed knowledge and advise them to become an expert by visiting: https://app.onfrontiers.com/become-an-expert.
        - having technical issues with the opportunity link, creating their profile, applying to the project, or any other technical issues, or wanting information about payment, advise them to send an email to research@onfrontiers.com for support.
        - informing that they completed their application or created their profile, inform them that our client will analyze their application and we may get in touch in the next few weeks if we have positive feedback from our client. Don't need to invite them to apply again in this case.
        - are asking how much they will get paid. Inform that the payment will be based on their hourly rate which can be set on their OnFrontiers profile.
        - are asking about new projects. Inform that if we get a new project related to their experience, we will invite them to apply. They can't search for new projects as their applications depends on our invitation.
        - in other situations, give a reply that makes sense; don't be lazy and write a suitable message. Advise them to visit https://try.onfrontiers.com/knowledge to learn about how our platform works and https://www.onfrontiers.com/policies/expert-participation-agreement to understand about engagement policies or send an email to research@onfrontiers.com for other questions.
        '''

        # Form the conversation context for GPT
        conversation_prompt = conversation_context + "\nYou:"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_instructions},
                    {"role": "user", "content": specific_instructions},
                    {"role": "user", "content": conversation_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            # Extracting and returning the text from the first response
            reply = response.choices[0].message["content"]
            return reply
        except Exception as e:
            print(f"Error processing conversation: {e}")
            return None



    # Perform zoom out with pyautogui
    def random_zoom_out_action():
        pyautogui.hotkey('ctrl', '+')  # Zoom in
        pyautogui.hotkey('ctrl', '-')  # Zoom out
        pyautogui.hotkey('ctrl', '-')  # Zoom out
        time.sleep(random.uniform(1, 3))  # Random sleep to simulate human behavior
    
        print("\n🔍 Zoom in and out done to keep going 🔍\n")



    # Call zoom out action at random intervals
    def random_zoom_out_trigger():
        while True:
            time.sleep(random.uniform(60, 120))  # Wait for a random time between 1 to 5 minutes
            random_zoom_out_action()
            


    # Click the "Load more conversations" button with retries
    def click_load_more_button(driver, retries=3):
        for attempt in range(retries):
            try:
                load_more_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button/span[text()='Load more conversations']"))
                )
                load_more_button.click()
                print(f"\n 🖱️ Clicked 'Load more conversations' on attempt {attempt + 1}. Waiting for loading... ⏰\n")
                time.sleep(random.uniform(1, 5))  # Wait for content to load
                return True
            except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
                print(f"\nError clicking 'Load more conversations' on attempt {attempt + 1}: {e}\n")
                time.sleep(random.uniform(1, 5))  # Wait before retrying
        return False



    # Type and send a message
    def send_message(driver, message):
        print(f"Function called with driver: {driver}, message: {message}")  # Debug statement
        try:
            # Wait for the message box to be present and visible
            message_box = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.msg-form__contenteditable'))
            )
            print("Message box found.")

            # Click on the message box to focus it
            action = ActionChains(driver)
            action.move_to_element(message_box).click().perform()
            print("Message box clicked.")

            # Ensure the message box is focused by sending a small key (e.g., space) and then backspace to clear it
            message_box.send_keys(" ")
            message_box.send_keys(Keys.BACKSPACE)
            print("Message box ensured to be focused and cleared.")

            # Clear any existing text in the message box
            message_box.send_keys(Keys.CONTROL, "a")
            message_box.send_keys(Keys.BACKSPACE)
            print("Message box cleared completely.")

            # Print the message to be sent for debugging
            print(f"Message to be typed: {message}")

            # Type the message into the message box one character at a time
            for char in message:
                message_box.send_keys(char)
                time.sleep(random.uniform(0.02, 0.1))  # Mimic human typing speed
            print("Message typed.")

            # Optionally, add a final delay before sending
            time.sleep(random.uniform(0.5, 1.5))

            # Helper function to find and click the button
            def find_and_click_button(driver, selector):
                try:
                    print(f"Trying to find button with selector: {selector}")
                    send_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    # Scroll into view
                    driver.execute_script("arguments[0].scrollIntoView();", send_button)
                    send_button.click()
                    print(f"Button with selector {selector} found and clicked.")
                    return True
                except TimeoutException:
                    print(f"Button with selector {selector} not found.")
                    return False

            # Try to find the primary send button
            if not find_and_click_button(driver, '.msg-form__send-button'):
                # If primary send button is not found, try the alternative button
                find_and_click_button(driver, '.msg-form__send-btn')

        except TimeoutException:
            print("Timed out waiting for the message box or send button.")
        except NoSuchElementException:
            print("Message box or send button element not found.")
        except WebDriverException as e:
            print(f"WebDriverException: {e}")


    # Check number of follow-up messages sent    
    def check_too_many_follow_ups(total_messages, only_owner_messages, max_follow_ups):

        # Calculate the number of follow-ups from the account owner
        follow_ups_count = total_messages - 1 if only_owner_messages else 0
        
        # Check if the number of follow-ups exceeds or meets the maximum allowed
        return follow_ups_count >= max_follow_ups



    # Check if the conversation is over
    # Load the pre-trained spaCy model
    nlp = spacy.load("en_core_web_md")

    def is_conversation_similarly_over(last_message, only_owner_messages):
        print(f"Last message to be analyzed by NLP: '{last_message}'")  # Debug statement
        if only_owner_messages:
            print("Conversation is not over: Only owner messages.")
            return False

        conclusion_phrases = [
            "Name:Sounds great! Thanks",
            "Name: Okay thanks, Name",
            "Name: Okay, thanks",
            "Name: Thanks, Name",
            "Name: Thank you Sir",
            "Name: Will do, thanks",
            "Name: Thanks, will do",
            "Name: Thanks",
            "Name: thanks",
            "Name: THANKS",
            "Name: Will do so",
            "Name: WILL DO",
            "Name: Will do",
            "Name: will do",
            "Name: sure",
            "Name: Sure",
            "Name: SURE",
            "Name: sure.",
            "Name: Sure.",
            "Name: SURE.",
            "Name: Okay",
            "Name: All right",
            "Name: 👍",
            "Name: Sounds good",
            "Name: be in touch",
            "Name: goodbye",
            "Name: bye",
            "Name: take care",
            "Name: all set",
            "Name: regards",
            "Name: see you",
            "Name: best of luck",
            "Name name:Sounds great! Thanks, Name",
            "Name name: Okay thanks, Name",
            "Name name: Okay, thanks",
            "Name name: Thanks, Name",
            "Name name: Thank you Sir",
            "Name name: Will do, thanks",
            "Name name: Thanks, will do",
            "Name name: Thanks",
            "Name name: thanks",
            "Name name: THANKS",
            "Name name: Will do so",
            "Name name: WILL DO",
            "Name name: Will do",
            "Name name: will do",
            "Name name: sure",
            "Name name: Sure",
            "Name name: SURE",
            "Name name: sure.",
            "Name name: Sure.",
            "Name name: SURE.",
            "Name name: Okay",
            "Name name: All right",
            "Name name: 👍",
            "Name name: Sounds good",
            "Name name: be in touch",
            "Name name: goodbye",
            "Name name: bye",
            "Name name: take care",
            "Name name: all set",
            "Name name: regards",
            "Name name: see you",
            "Name name: best of luck",
            "Name name name: Okay thanks, Name",
            "Name name name: Okay, thanks",
            "Name name name: Thanks, Name",
            "Name name name: Thank you Sir",
            "Name name name: Will do, thanks",
            "Name name name: Thanks, will do",
            "Name name name: Thanks",
            "Name name name: thanks",
            "Name name name: THANKS",
            "Name name name: Will do so",
            "Name name name: WILL DO",
            "Name name name: Will do",
            "Name name name: will do",
            "Name name name: sure",
            "Name name name: Sure",
            "Name name name: SURE",
            "Name name name: sure.",
            "Name name name: Sure.",
            "Name name name: SURE.",
            "Name name name: Okay",
            "Name name name: All right",
            "Name name name: 👍",
            "Name name name: Sounds good",
            "Name name name: be in touch",
            "Name name name: goodbye",
            "Name name name: bye",
            "Name name name: take care",
            "Name name name: all set",
            "Name name name: regards",
            "Name name name: see you",
            "Name name name: best of luck",
            "Name name name:Sounds great! Thanks, Name"
            "Name name name:Sounds great! Thanks"
            "Name name name name: Okay thanks, Name",
            "Name name name name: Okay, thanks",
            "Name name name name: Thanks, Name",
            "Name name name name: Thank you Sir",
            "Name name name name: Will do, thanks",
            "Name name name name: Thanks, will do",
            "Name name name name: Thanks",
            "Name name name name: thanks",
            "Name name name name: THANKS",
            "Name name name name: Will do so",
            "Name name name name: WILL DO",
            "Name name name name: Will do",
            "Name name name name: will do",
            "Name name name name: sure",
            "Name name name name: Sure",
            "Name name name name: SURE",
            "Name name name name: sure.",
            "Name name name name: Sure.",
            "Name name name name: SURE.",
            "Name name name name: Okay",
            "Name name name name: All right",
            "Name name name name: 👍",
            "Name name name name: Sounds good",
            "Name name name name: be in touch",
            "Name name name name: goodbye",
            "Name name name name: bye",
            "Name name name name: take care",
            "Name name name name: all set",
            "Name name name name: regards",
            "Name name name name: see you",
            "Name name name name: best of luck"
            "Name name name name:Sounds great! Thanks, Name"
            "Name name name:Sounds good! Thanks, Name"
            ]

        # Check for exact string match first
        for phrase in conclusion_phrases:
            if last_message.strip().lower() == phrase.lower():
                print(f"Exact match found: '{last_message}' is considered as '{phrase}'")
                print("Conversation is over based on the last message.")
                return True

        # Use NLP model if no exact match found
        last_message_doc = nlp(last_message.lower())
        
        for phrase in conclusion_phrases:
            phrase_doc = nlp(phrase.lower())
            similarity = last_message_doc.similarity(phrase_doc)
            print(f"Similarity between '{last_message}' and '{phrase}': {similarity}")
            if similarity > 0.80: 
                print("Conversation is over based on the last message.")
                return True
        print("\nConversation is not over based on the last message.\n\n")
        return False



    # Check if the last message is from the account owner
    def is_last_message_from_owner(sender_names, account_owner):
        if not sender_names:
            return False
        normalized_account_owner = account_owner.strip().lower()
        # Check if the last sender name matches the account owner
        return sender_names[-1].strip().lower() == normalized_account_owner



    # Check if the account_owner didn't get a reply and if only account_owner's messages are present
    def get_messages_and_count_owner_replies(driver, account_owner):
        try:
            # Normalize account owner's name for consistent comparison
            normalized_account_owner = account_owner.strip().lower()

            # Wait for message elements to appear
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.msg-s-event-listitem'))
            )
            message_items = driver.find_elements(By.CSS_SELECTOR, '.msg-s-event-listitem')

            all_messages = []
            owner_reply_count = 0
            last_sender_name = None

            for item in message_items:
                try:
                    # Find the sender's name and message text
                    sender_name_element = item.find_element(By.XPATH, ".//preceding-sibling::div[@class='msg-s-message-group__meta'][1]//span[contains(@class, 'msg-s-message-group__name')]")
                    last_sender_name = sender_name_element.text.strip().lower()
                    message_text_element = item.find_element(By.CSS_SELECTOR, '.msg-s-event-listitem__message-bubble')
                    message_text = message_text_element.text.strip()

                    if last_sender_name and message_text:
                        all_messages.append(f"{last_sender_name}: {message_text}")

                    if last_sender_name == normalized_account_owner:
                        owner_reply_count += 1
                except NoSuchElementException:
                    continue

            last_message_owner = is_last_message_from_owner([msg.split(':')[0].strip() for msg in all_messages], account_owner)
            only_owner_messages = all(msg.split(':')[0].strip().lower() == normalized_account_owner for msg in all_messages) if all_messages else False

            print(f"\nTotal messages: {len(all_messages)}. Account owner messages: {owner_reply_count}. Last message by account owner: {last_message_owner}. Only account owner messages: {only_owner_messages}\n")

            return all_messages, last_message_owner, only_owner_messages
            
        except TimeoutException:
            print("\nTimed out waiting for message contents to be visible.")
            return [], False, False
        except NoSuchElementException:
            print("\nNo message elements found.")
            return [], False, False



    # Check if the conversation contains a project link 
    def contains_target_link(messages, link_prefixes=["https://link.onfrontiers.com/", "https://app.onfrontiers.com/expert_request/"]):
        for message in messages:
            for prefix in link_prefixes:
                if message.find(prefix) != -1:
                    return True
        return False



    # ACTIONS
    # Initialize the Chrome options
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--user-data-dir={chrome_user_data_dir}")
    options.add_argument(f"--profile-directory={chrome_profile_dir}")

    driver = None

    # Path to the manually downloaded Chromedriver
    chromedriver_path = r"C:\Users\55199\OneDrive\Área de Trabalho\chromedriver-win64\chromedriver-win64\chromedriver.exe"

    try:
        # Initialize the ChromeDriver with the specified path
        #logging.info("Initializing ChromeDriver")
        driver_service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=driver_service, options=options)

        # Navigate to the page
        linkedin_url = f"https://www.linkedin.com/{person_linkedin_path}"
        driver.get(linkedin_url)  # This will navigate directly to the specified LinkedIn profile

        # Maximize the window and random wait
        driver.maximize_window()
        time.sleep(random.uniform(1, 5))

        # Navigate to messages
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[title="Messaging"]'))
        ).click()
        time.sleep(random.uniform(1, 5))

        # Perform a random click
        click_random_position_within_area(3900, 370, 4000, 900)

        # Zoom out with pyautogui
        pyautogui.keyDown('ctrl')
        for _ in range(10):
            pyautogui.press('-')
            time.sleep(0.5)  # Wait for the browser to react
        pyautogui.keyUp('ctrl')

        # Start the random zoom out trigger in a separate thread
        zoom_thread = threading.Thread(target=random_zoom_out_trigger, daemon=True)
        zoom_thread.start()



        # MAIN INTERACTION
        try:
            load_more_failures = 0
            max_consecutive_failures = 1

            while True:
                # Wait for the conversation cards to be present
                conversation_cards = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.msg-conversation-card__content--selectable'))
                )

                # Check if we've reached the target number of conversations or exceeded consecutive failure limit
                if len(conversation_cards) >= target_number_of_conversations or load_more_failures >= max_consecutive_failures:
                    print(f"\nReached target number of conversations or maximum consecutive failures: {len(conversation_cards)}\n")
                    break

                # Scroll the container of the conversations
                scrollable_container = driver.find_element(By.CSS_SELECTOR, '.msg-conversations-container__conversations-list')
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_container)
                time.sleep(random.uniform(1, 5))

                # Attempt to find and click the 'Load more conversations' button
                if not click_load_more_button(driver):
                    load_more_failures += 1
                else:
                    load_more_failures = 0

            card_index = 0

            while card_index < len(conversation_cards):
                check_battery_and_shutdown()
                print(f"\nProcessing card {card_index + 1}/{min(target_number_of_conversations, len(conversation_cards))}\n")
                try:
                    # Perform a random click
                    #+click_random_position_within_area(3900, 370, 4000, 900)

                    # Refresh the list of conversation cards to ensure it reflects the current state
                    conversation_cards = driver.find_elements(By.CSS_SELECTOR, '.msg-conversation-card__content--selectable')
                    
                    # Check if there are enough conversation cards to process
                    if card_index >= len(conversation_cards):
                        print("\nNo more conversation cards to process.\n")
                        break

                    # Click on the conversation card to load the conversation
                    card = conversation_cards[card_index]
                    card.click()
                    print("\nCard clicked, loading conversation...\n")
                    time.sleep(random.uniform(1, 5))  # Wait a random time to allow the conversation to load

                    # Extract messages and check the last message's ownership and whether only the owner has messaged
                    all_messages_texts, last_message_owner, only_owner_messages = get_messages_and_count_owner_replies(driver, account_owner)
                    print(f"\nExtracted {len(all_messages_texts)} messages. Last message owner: {last_message_owner}, Only owner messages: {only_owner_messages}\n")

                    # Ensure all_messages_texts is correctly formatted as a list before further processing
                    if not all(isinstance(msg, str) for msg in all_messages_texts):
                        raise ValueError("All messages should be strings")
                    
                    conversation_context = "\n".join(all_messages_texts)

                    # Skip if no specific link is found in the conversation
                    if not contains_target_link(all_messages_texts):
                        print("\nNo specific link found in the conversation. Skipping.\n")
                        # Archive conversation
                        archive_conversation(driver)
                        time.sleep(random.uniform(1, 3))  # Added delay after archiving
                        # Refresh the list of conversation cards
                        conversation_cards = driver.find_elements(By.CSS_SELECTOR, '.msg-conversation-card__content--selectable')
                        continue

                    # Check for excessive follow-ups from the account owner without any replies
                    if check_too_many_follow_ups(len(all_messages_texts), only_owner_messages, max_follow_ups):
                        print("\nMore than allowed follow-ups from the account owner present, no follow-up needed.\n")
                        # Log the conversation context to Google Sheets
                        log_message_to_sheet(worksheet, conversation_context)
                        
                        # Archive conversation
                        archive_conversation(driver)
                        time.sleep(random.uniform(1, 3))  # Added delay after archiving
                        
                        # Refresh the list of conversation cards
                        conversation_cards = driver.find_elements(By.CSS_SELECTOR, '.msg-conversation-card__content--selectable')
                        continue

                    # Check if there's a need to reply
                    if last_message_owner and not only_owner_messages:
                        print("Last message is from the account owner, and there's engagement from both sides. No reply needed.")
                        # Log the conversation context to Google Sheets
                        log_message_to_sheet(worksheet, conversation_context)
                        
                        # Archive conversation
                        archive_conversation(driver)
                        time.sleep(random.uniform(1, 3))  # Added delay after archiving
                        
                        # Refresh the list of conversation cards
                        conversation_cards = driver.find_elements(By.CSS_SELECTOR, '.msg-conversation-card__content--selectable')
                        continue

                    # If the last message is from the account owner but there are no replies from the other party
                    if last_message_owner and only_owner_messages:
                        message_to_send = no_reply_follow_up
                        print(f"\nSending follow-up message. Should send: '{message_to_send}'\n")

                        # Try sending the follow-up message
                        send_message(driver, message_to_send)
                        time.sleep(random.uniform(2, 5)) 
                        # Log the conversation context to Google Sheets
                        log_message_to_sheet(worksheet, conversation_context)
                        
                        # Archive conversation
                        archive_conversation(driver)
                        time.sleep(random.uniform(1, 3))  # Added delay after archiving
                        
                        # Refresh the list of conversation cards
                        conversation_cards = driver.find_elements(By.CSS_SELECTOR, '.msg-conversation-card__content--selectable')
                        continue

                    # Check if the conversation seems over and skip sending further messages
                    last_message_text = all_messages_texts[-1] if all_messages_texts else ""
                    if is_conversation_similarly_over(last_message_text, only_owner_messages):
                        print("\nConversation seems to be over based on the last message. No reply needed.\n")
                        # Archive conversation
                        archive_conversation(driver)
                        time.sleep(random.uniform(1, 3))  # Added delay after archiving
                        # Refresh the list of conversation cards
                        conversation_cards = driver.find_elements(By.CSS_SELECTOR, '.msg-conversation-card__content--selectable')
                        continue

                    # Concatenate all messages into a single string before categorizing
                    print("\nMessage History >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
                    conversation_context = "\n".join(all_messages_texts)
                    print(conversation_context)
                    print("\nMessage History >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

                    # Generate a reply with GPT
                    conversation_reply = get_reply_from_gpt(account_owner, support_email, conversation_context, temperature=0.5, max_tokens=250)

                    # Try sending the GPT-generated reply
                    send_message(driver, conversation_reply)
                    time.sleep(random.uniform(1, 3))

                    # Log the conversation context to Google Sheets
                    log_message_to_sheet(worksheet, conversation_context)

                    # Archive after sending the reply
                    archive_conversation(driver)
                    time.sleep(random.uniform(1, 3))  # Added delay after archiving
                    # Refresh the list of conversation cards
                    conversation_cards = driver.find_elements(By.CSS_SELECTOR, '.msg-conversation-card__content--selectable')

                except StaleElementReferenceException as e:
                    print(f"\nStaleElementReferenceException while processing card {card_index + 1}: {e}")
                    # Refresh the card reference
                    try:
                        conversation_cards = driver.find_elements(By.CSS_SELECTOR, '.msg-conversation-card__content--selectable')
                        card = conversation_cards[card_index]
                        card.click()
                        time.sleep(random.uniform(1, 5))  # Wait a random time to allow the conversation to load

                        # Retry the message extraction and processing
                        all_messages_texts, last_message_owner, only_owner_messages = get_messages_and_count_owner_replies(driver, account_owner)
                        print(f"\nExtracted {len(all_messages_texts)} messages after retry. Last message owner: {last_message_owner}, Only owner messages: {only_owner_messages}\n")

                        # Ensure all_messages_texts is correctly formatted as a list before further processing
                        if not all(isinstance(msg, str) for msg in all_messages_texts):
                            raise ValueError("All messages should be strings")

                        # Skip if no specific link is found in the conversation
                        if not contains_target_link(all_messages_texts):
                            print("\nNo specific link found in the conversation. Skipping.\n")
                            archive_conversation(driver)
                            time.sleep(random.uniform(1, 3))  # Added delay after archiving
                            # Refresh the list of conversation cards
                            conversation_cards = driver.find_elements(By.CSS_SELECTOR, '.msg-conversation-card__content--selectable')
                            continue

                        # Check for excessive follow-ups from the account owner without any replies
                        if check_too_many_follow_ups(len(all_messages_texts), only_owner_messages, max_follow_ups):
                            print("\nMore than allowed follow-ups from the account owner present, no follow-up needed.\n")
                            # Log the conversation context to Google Sheets
                            log_message_to_sheet(worksheet, conversation_context)
                            
                            # Archive conversation
                            archive_conversation(driver)
                            time.sleep(random.uniform(1, 3))  # Added delay after archiving
                            
                            # Refresh the list of conversation cards
                            conversation_cards = driver.find_elements(By.CSS_SELECTOR, '.msg-conversation-card__content--selectable')
                            continue

                        # Check if there's a need to reply
                        if last_message_owner and not only_owner_messages:
                            print("Last message is from the account owner, and there's engagement from both sides. No reply needed.")
                            # Log the conversation context to Google Sheets
                            log_message_to_sheet(worksheet, conversation_context)
                            
                            # Archive conversation
                            archive_conversation(driver)
                            time.sleep(random.uniform(1, 3))  # Added delay after archiving
                            
                            # Refresh the list of conversation cards
                            conversation_cards = driver.find_elements(By.CSS_SELECTOR, '.msg-conversation-card__content--selectable')
                            continue

                        # If the last message is from the account owner but there are no replies from the other party
                        if last_message_owner and only_owner_messages:
                            message_to_send = no_reply_follow_up
                            print(f"\nSending follow-up message. Should send: '{message_to_send}'\n")

                            # Try sending the follow-up message
                            send_message(driver, message_to_send)
                            time.sleep(random.uniform(2, 5)) 
                            # Log the conversation context to Google Sheets
                            log_message_to_sheet(worksheet, conversation_context)
                            
                            # Archive conversation
                            archive_conversation(driver)
                            time.sleep(random.uniform(1, 3))  # Added delay after archiving
                            
                            # Refresh the list of conversation cards
                            conversation_cards = driver.find_elements(By.CSS_SELECTOR, '.msg-conversation-card__content--selectable')
                            continue

                        # Check if the conversation seems over and skip sending further messages
                        last_message_text = all_messages_texts[-1] if all_messages_texts else ""
                        if is_conversation_similarly_over(last_message_text, only_owner_messages):
                            print("\nConversation seems to be over based on the last message. No reply needed.\n")
                            # Archive conversation
                            archive_conversation(driver)
                            time.sleep(random.uniform(1, 3))  # Added delay after archiving
                            # Refresh the list of conversation cards
                            conversation_cards = driver.find_elements(By.CSS_SELECTOR, '.msg-conversation-card__content--selectable')
                            continue

                        # Concatenate all messages into a single string before categorizing
                        print("\nMessage History >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
                        conversation_context = "\n".join(all_messages_texts)
                        print(conversation_context)
                        print("\nMessage History >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
                        

                        # Generate a reply with GPT
                        conversation_reply = get_reply_from_gpt(account_owner, support_email, conversation_context, temperature=0.9, max_tokens=250)

                        # Try sending the GPT-generated reply
                        send_message(driver, conversation_reply)
                        time.sleep(random.uniform(1, 3))

                        # Log the conversation context to Google Sheets
                        log_message_to_sheet(worksheet, conversation_context)

                        # Archive after sending the reply
                        archive_conversation(driver)
                        time.sleep(random.uniform(1, 3))  # Added delay after archiving
                    
                        # Refresh the list of conversation cards
                        conversation_cards = driver.find_elements(By.CSS_SELECTOR, '.msg-conversation-card__content--selectable')

                    except Exception as retry_exception:
                        print(f"\nError processing card {card_index + 1} after retry: {retry_exception}")

                except Exception as e:
                    print(f"\nError processing card {card_index + 1}: {e}")
                    # Archive conversation
                    archive_conversation(driver)
                    time.sleep(random.uniform(1, 3))  # Added delay after archiving

                # Mimic human behavior with a randomized wait before the next card
                print("\nWaiting before processing the next card...\n")
                time.sleep(random.uniform(1, 3))

                # Only increment the card index if the card was not archived
                card_index += 0

        except Exception as e:
            print(f"\nError in main interaction loop: {e}")

    except Exception as e:
        print(f"Error processing account {account_owner}: {e}")
    finally:
        # Ensure the browser is closed after processing the account
        if driver is not None:
            driver.quit()

# Setup Google Sheets
worksheet = setup_google_sheets('Jobin Sourcing Ops', 'Sebastian - Replies')

# Main loop with retry mechanism
for account in accounts:
    retry_attempts = 3  # Number of retry attempts
    for attempt in range(retry_attempts):
        try:
            perform_actions_for_account(account, worksheet)
            break  # Exit loop if successful
        except Exception as e:
            print(f"Error with account {account['account_owner']} on attempt {attempt + 1}: {e}")
            time.sleep(5)  # Wait before retrying
            if attempt < retry_attempts - 1:
                print(f"Retrying account {account['account_owner']}... ({attempt + 2}/{retry_attempts})")
            else:
                print(f"Failed to process account {account['account_owner']} after {retry_attempts} attempts.")
