import re
import time
import random
import keyboard
import requests
import openai
import pyautogui
import dateutil
import datetime
from selenium.webdriver.common.action_chains import ActionChains
from dateutil.parser import parse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from textblob import TextBlob
import spacy
from scipy.spatial.distance import cosine
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
import time
import random

# SET UP

# ACCOUNT 
# Account Owner
account_owner = 'Kristine V. Sade'
person_linkedin_path = "in/kristine-v-sade-b81963296/" 

# Chrome user data and profile directory

chrome_user_data_dir = "C:\\Users\\55199\\AppData\\Local\\Google\\Chrome\\User Data"
chrome_profile_dir = "Profile 30"

# SUPPORT
# Support email
support_email = 'research@onfrontiers.com'

# Payment support email
payment_support_email = 'yzhang@onfrontiers.com'


# API
# Set your OpenAI API key here
openai.api_key = 'sk-proj-TDNUiINov0RzlXWLX7lYT3BlbkFJWg5JUZufIndEIsl3Gse9'


# MESSAGING
# Max number of messages without a reply. 
max_follow_ups = 1

# Number of messages to check in order to reply
target_number_of_conversations = 50

# Follow-up for messages with no replies
no_reply_follow_up = f"Hey there! Just wanted to touch base since we haven't heard from you yet. Our client is eager to collaborate with you, so feel free to apply to this project through the provided link. If you have any questions, let me know. Check out OnFrontiers.com to learn more about us. Looking forward to connecting!"

# Instructions to reply
general_instructions = (f"give a general reply to the message behalf of the account_owner. Tell the expert to reach out to {support_email} for further clarifications")

# Define instructions for each category
# Interest
interested_instructions = f'''Advise the expert to apply through the project link shared in the initial message. Mention that all project details and queries about the engagement process can be addressed post-application.'''

not_interested_instructions = f'''Advise the expert to join our platform as an expert through this link (https://app.onfrontiers.com/become-an-expert) to get new projects related to their experience in the future, also ask for referrals'''

confirming_will_apply = f'''Thank the expert and inform that you are available to take any questions meanwhile. Also advise the expert to send an email to {support_email} in case they find issues with the application process.'''
# Additional information
needs_info_about_client_instructions = f'''Answer the expert's question based on the project information. 
Also, inform that if our client has allowed it, their information will be on the project page. If not, the information may be provided after the expert applies to the project.'''

needs_info_about_onfrontiers_instructions = f'''Explain that OnFrontiers is a knowledge network company that helps our clients unlock the knowledge they need to be successful.'''

needs_info_about_the_engagement_instructions = f'''Answer the question based on the information present in project description. 
If the information is not enough, advise the expert to send an email to {support_email} for more details about the engagement.'''

# Payment instructions
needs_info_about_payment_instructions = f'''Inform that the payment (if it's a consultation project) will be based on the expert's hourly rate, which can be set on their profile. 
If the project is a consulting position or job placement opportunity, the payment will be discussed during the first interview. 
If the expert needs help on how to set their hourly rate, advise them to send an email to {support_email} asking for instructions'''

How_to_get_paid_instructions = f'''Inform that our financial team will contact the expert over email to process the payment for consultations projects. 
The payment amount will be based on the expert's hourly rate and the engagement duration'''

# Updates
update_on_application_instructions = f'''Inform that if the expert completed the application, our client weill reveiw it and reach out if they decide to move forward with the expert's application. 
Advise them to keep an eye on their email for notifications.'''

update_on_completed_engagement_instructions = f'''Kindly thanks the expert for completing the engagement. Inform that our client will reachout in case they need a follow up engagement. 
Also inform that our finance team may contact the expert within the next 3 to 5 business days to process their payment (for consultations). If they need further assistance with payments, adivese them to get in touch with our finance team through this email adress {payment_support_email}'''

# Referral
update_on_shared_referral_instructions = f'''Inform that we are reaching out to the referral and will get in touch with them if our client selects their profile to move forward.'''

will_refer_an_expert_instructions = f'''Thank the expert. Advise them to share the referral email, linkedin profile or send the project link to them. Thank them again, and say that you appreciate their help sharing the referral'''

# Closed project
closed_project_instructions = f'''Inform that our client has already obtained the needed knowledge, which is why the project is closed. Advise the expert to join our platform through this link (https://app.onfrontiers.com/become-an-expert) to get new projects firsthand.'''

# Technical issues
technical_issues_instructions = f'''Apologize for any inconvenience caused and advise the expert to send an email to {support_email} explaining the issue and requesting support. Assure them that our team will promptly assist.'''

# Reschedule call 
reschedule_need_instructions = f'''Inform that the expert can reschedule a requested call by opening the engagement link and hitting the "reschedule call" button. 
Advise the expert that in case it is an urgent rescheduling, they can request for help sending an email to {support_email} and our team will promptly provide support'''

# Problem with email or phone number
email_or_phone_issue = f'''Advise the expert to use another email or phone number in order to complete their application, or try to login with the current email or phone number and reset their password as they could already have an account on OnFrontiers.
Advise that In case the issue persists they can send an email to {support_email} and our team will promptly provide support. '''

# Conflict of interest 
possible_conflict_of_interest_instructions = f'''Assure them of our ethical commitment. 
Our platform has a thorough compliance system to prevent conflicts of interest. 
All experts and clients undergo training to ensure adherence to ethical guidelines. 
They must complete training and can step back if they identify a conflict before engaging with clients.'''

# Contract:
contract_information_instructions = f'''Kindly inform that there's no need for a separate contract because our platform automatically secures rights for both parties through the usage agreement. 
Advise that if the expert require proof of the engagement earnings to present to their country's authorities, our team can provide it after the engagement gets completed once you make a request to the this email: {payment_support_email}.'''

# Sourcing criteria 
sourcing_criteria_instructions = f'''Inform that we used their LinkedIn profile to get the information and we beliave that the expert is a good fit for the project. 
Inform that if the expert thinks otherwise, they can either refer another professional or became an expert on our platform through this link (https://app.onfrontiers.com/become-an-expert) to get new projects related to their experience in the future.'''

# Work demand 
work_demand_info = f'''Say that we have several clients from different industries and we can invite the experts for upcoming projects if they are part of our platform. They can join our platform either from the project link previously shared or through this link (https://app.onfrontiers.com/become-an-expert)'''

# Who will be on the call 
call_attendees = f'''kindly inform them that our client may invite additional team members to join the call. Their name may or may not be visible depending on their preference. Rest assured, all participants will adhere to our compliance policy and be aligned accordingly.'''

# Profile demand 
profile_demand_info = '''Inform that we work with experts from different industries, such as from the federal industry, international development area, B2B, B2C and so on. We source experts from all over the work since we have clients looking for opportunities in many countries'''

# Asking for information over email 
information_over_email = '''Inform that the expert must visit the project page through the opportunity link previously shared to check the project information and apply if interested.'''

# Expert needs more time to decide
needs_time_to_decide = '''Thank the expert for considering the opportunity, and inform that you will be waiting for their application or further questions.'''

# Completed application 

# Categorize using GPT-3 
def categorize_with_gpt3(text):
    print("Categorizing the message with GPT")
    if isinstance(text, list):
        text = "\n".join(text)
    prompt = f"""Categorize the expert's reply (Not just based on {account_owner} messages) in the scenarios below using the examples provided for each category. Check all possible scenarios before defining the category. The conversation is an interaction between {account_owner} and an expert.
        "interested": Experts (not {account_owner}) may say something along the lines of ["I'm interested", "sounds interesting", "looks like a fit for me", "I want to apply"] / Cases that shouldn't not be considered ["I did", "completed my application", "done with the application"]
        "not interested": Experts may (not {account_owner}) say something along the lines of ["can't help you", "no thanks", "not interested", "I'll pass", "not for me", "not my area", "I don't have the knowledge", "know nothing about", "I'm not from this area", "I'm not from this industry"],
        "needs info about the client": Experts (not {account_owner}) may say something along the lines of ["client information", "who is the client", "client details", "client background"],
        "needs info about OnFrontiers": Experts (not {account_owner}) may say something along the lines of ["what is OnFrontiers", "OnFrontiers details", "how does OnFrontiers works", "about OnFrontiers"],
        "needs info about the engagement": Experts (not {account_owner}) may say something along the lines of ["project details", "engagement information", "project specifics", "more information about the project"],
        "needs info about payment": Experts (not {account_owner}) may say something along the lines of ["my hourly rate is", "payment", "compensation", "how much", "paid"],
        "update on application": Experts (not {account_owner}) may say something along the lines of ["application status", "I applied", "application completed", "application update", "status of application", "I applied to the project", "completed my application", "sent my application", "I did", "completed it"],
        "update on shared referral": Experts (not {account_owner}) may say something along the lines of ["referral status", "I shared referral", "referral update", "referral progress"],
        "closed project": Experts (not {account_owner}) may say something along the lines of ["project closed", "no longer available", "project completed", "project finished"]
        "technical issue": Experts (not {account_owner}) may say something along the lines of ["can't complete my application", "there is a problem with the link", "can't create my profile", "the page is not opening", "can't update my profile", "having issues logging in"]   
        "how to get paid": Experts (not {account_owner}) may say something along the lines of ["from where will you pay me", "when do I get paid", "should I send you my bank details", "who will pay me for that"]
        "will refer an expert": FYI - This won't apply if {account_owner} is one talking about refer an expert. Experts (not {account_owner}) may say something along the lines of ["I will search on my network for someone", "let me think about someone", "I will share it with my colleague", "I will try to figure any useful resource persons you can interact with"]   
        "reschedule need": Experts (not {account_owner}) may say something along the lines of ["Need to reschedule my call", "won't be able to join the confirmed call", "My availability has changed", "I need to reschedule", "can't make to the call"]
        "email or phone issue": Experts (not {account_owner}) may say something along the lines of ["Can't use my email to create an account", "Can't use my phone number to create an account", "It says that my email is already in use", "It says that my phone is already in use"]
        "possible conflict of interest": Experts (not {account_owner}) may say something along the lines of ["Would that be a conflict of interest", "can you confirm that I will not have any restrictions or limitations with my own client?", "what if this is a conflict of interest?"]
        "update on completed engagement": Experts (not {account_owner}) may say something along the lines of ["I completed the call", "I completed the engagement", "the call went well"] 
        "contract information": Experts (not {account_owner}) may say something along the lines of "Could you send me a contract via email for this engagement?", "can you give me a proof of earnings from the engagement", "I need an invoice", "I need to have a paper contract"]
        "sourcing criteria": Experts (not {account_owner}) may say something along the lines of ["Why you think I'm a good fit?", "from where did you get my information", "how did you find my profile"]
        "work demand info": Experts (not {account_owner}) may say something along the lines of ["How often do you have these projects", "how many projects can I get", "what is the project demand"]
        "call attendees info": Experts (not {account_owner}) may say something along the lines of ["Would you be able to share who will be on the call?", "Is there any other client on the call or is that just one?", "Who will be joining the call"]
        "profile demand info": Experts (not {account_owner}) may say something along the lines of ["How diverse are the profiles that you usually work with or look for?", "what kind of profiles do you source", "is OnFrontiers focused on a specific industry or country?"]
        "information over email": Experts (not {account_owner}) may say something along the lines of ["Please share the details on my mail", "Can you send me an email with the information", "Can you reach me out on my email"]
        "needs time to decide": Experts (not {account_owner}) may say something along the lines of ["Let me think", "will get back to you soon", "let me review it first", "give me some days to review it", "give me some time".]
    Conversation: "{text}"
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Please categorize the conversation."}
            ],
        )
        category = response.choices[0].message['content'].strip()
        print(f"GPT-3 categorization result: {category}")
        return category
    except Exception as e:
        print(f"Error accessing GPT-3 API: {e}")
        return "Error"

# Generate a reply based on the category using the correct GPT-3 chat model
def generate_reply_with_gpt3(category, conversation_context):
    print(f"Generating reply with GPT-3 for category: {category}")
    if isinstance(conversation_context, list):
        conversation_context = "\n".join(conversation_context)
    if category == "interested":
        instructions = interested_instructions
    elif category == "confirming will apply":
        instructions = confirming_will_apply
    elif category == "needs time to decide":
        instructions = needs_time_to_decide
    elif category == "information over email":
        instructions = information_over_email
    elif category == "profile demand info":
        instructions = profile_demand_info
    elif category == "call attendees info":
        instructions = call_attendees
    elif category == "work demand info":
        instructions = work_demand_info
    elif category == "sourcing criteria":
        instructions = sourcing_criteria_instructions
    elif category == "contract information":
        instructions = contract_information_instructions
    elif category == "update on completed engagement":
        instructions = update_on_completed_engagement_instructions
    elif category == "possible conflict of interest":
        instructions = possible_conflict_of_interest_instructions
    elif category == "email or phone issue":
        instructions = email_or_phone_issue
    elif category == "reschedule need":
        instructions = reschedule_need_instructions
    elif category == "will refer an expert":
        instructions = will_refer_an_expert_instructions
    elif category == "not interested":
        instructions = not_interested_instructions
    elif category == "how to get paid":
        instructions = How_to_get_paid_instructions
    elif category == "technical issue":
        instructions = technical_issues_instructions
    elif category == "needs info about the client":
        instructions = needs_info_about_client_instructions
    elif category == "needs info about OnFrontiers":
        instructions = needs_info_about_onfrontiers_instructions
    elif category == "needs info about the engagement":
        instructions = needs_info_about_the_engagement_instructions
    elif category == "needs info about payment":
        instructions = needs_info_about_payment_instructions
    elif category == "update on application":
        instructions = update_on_application_instructions
    elif category == "update on shared referral":
        instructions = update_on_shared_referral_instructions
    elif category == "closed project":
        instructions = closed_project_instructions
    else:
        instructions = "Please provide general assistance."

    # GPT model
    role = f'''You are replying as {account_owner}. 
    Your role is to help experts with questions related to projects opportunities from OnFrontiers clients'''
    system = f'''
    Always strictly follow the instructions to generate a message.
    Don't write your message as an email, make the conversation natural. 
    Copy and past the opportunity/project link in your messages when inviting the expert to apply.
    Don't agree on sending emails, don't agree on joining or calling experts, don't set up meetings.
    Don't be too long and use a daily vocabulary.
    Add the Expert name to your message when needed. Your are writing a real message, not a template.
    Your answers should always be related to the project information shared.
    Projects can be either consultations or job placement, check the project description to write your reply.
    Your response should be clear, friendly and be related to the project description and instructions.
    Your response shouldn't go over 300 characters.'''

    prompt = f'''Conversation context: {conversation_context}\n\nInstructions: {instructions}\n\nPlease craft a suitable response to the expert based on the instructions and conversation context:'''

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": role,
            },
            {
                "role": "system",
                "content": system,
            },
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    final_reply = response.choices[0].message['content'].strip()
    print(f"Generated Reply: {final_reply}")
    return final_reply

# Function to scroll through the messages in a conversation
def scroll_through_conversation(driver):
    try:
        # Wait for the message list to be present
        message_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".msg-s-message-list.full-width.scrollable"))
        )

        # Find a target element within the conversation box (e.g., the first message bubble)
        target_element = message_list.find_element(By.CSS_SELECTOR, '.msg-s-event-listitem__message-bubble')

        # Get the location of the target element
        location = target_element.location
        size = target_element.size

        # Calculate the center point of the target element
        center_x = location['x'] + size['width'] / 2
        center_y = location['y'] + size['height'] / 2

        # Move the mouse to the center of the target element
        pyautogui.moveTo(center_x, center_y, duration=1)

        # Perform scrolling actions
        for _ in range(3):  # Scroll down 3 times
            pyautogui.scroll(-1000)  # Scroll down
            time.sleep(1)  # Wait for a second to load more messages

        for _ in range(3):  # Scroll up 3 times
            pyautogui.scroll(1000)  # Scroll up
            time.sleep(1)  # Wait for a second to load more messages

        print("Scrolled through the conversation to ensure all messages are loaded.")

    except TimeoutException:
        print("Timed out waiting for the message list to be present.")
    except NoSuchElementException:
        print("Message list element not found.")
    except Exception as e:
        print(f"Error during scrolling: {e}")


# Function to send message
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
        print("Message box cleared.")

        # Type the message into the message box one character at a time
        for char in message:
            message_box.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))  # Mimic human typing speed
        print("Message typed.")

        # Optionally, add a final delay before sending
        time.sleep(random.uniform(0.5, 1.5))

        # Find the send button and click it
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.msg-form__send-button'))
        )
        send_button.click()
        print("Message sent by clicking the send button.")

    except TimeoutException:
        print("Timed out waiting for the message box or send button.")
    except NoSuchElementException:
        print("Message box or send button element not found.")
    except WebDriverException as e:
        print(f"WebDriverException: {e}")


def type_message_like_human(message):
    """
    Types out a message in the currently focused input field, mimicking human typing behavior.

    :param message: The message to type out.
    """
    # Loop through each character in the message
    for char in message:
        # Type out the character
        pyautogui.typewrite(char)
        # Wait for a random short interval to mimic human typing speed
        time.sleep(random.uniform(0.05, 0.2))
    
    # Optionally, add a final delay before sending
    time.sleep(random.uniform(0.5, 1.5))
    
    # Press 'Enter' to send the message (ensure this is appropriate for the input field)
    pyautogui.press('enter')

def check_too_many_follow_ups(total_messages, only_owner_messages, max_follow_ups):
    """
    Determine if there are too many follow-ups from the account owner without a reply from the other party.
    
    :param total_messages: The total number of messages in the conversation.
    :param only_owner_messages: A boolean indicating if only the account owner has messaged.
    :param max_follow_ups: The maximum allowed number of follow-ups without a reply.
    :return: A boolean indicating whether another follow-up message should be sent.
    """
    # Calculate the number of follow-ups from the account owner
    follow_ups_count = total_messages - 1 if only_owner_messages else 0
    
    # Check if the number of follow-ups exceeds or meets the maximum allowed
    return follow_ups_count >= max_follow_ups

# Check if the conversation is over (Natural Language Processing)
# Load the pre-trained spaCy model
nlp = spacy.load("en_core_web_md")

# Load the pre-trained spaCy model
nlp = spacy.load("en_core_web_md")

def is_conversation_similarly_over(last_message, only_owner_messages):
    print(f"Last message to be analyzed by NLP: '{last_message}'")  # Debug statement
    if only_owner_messages:
        print("Conversation is not over: Only owner messages.")
        return False

    conclusion_phrases = [
        "Thank you dear", "Okay, thanks", "humm", "Hmm", "thanks", "Okay, thanks", 'Thanks, you too', "have a good day", 
        "goodbye", "bye", "take care", "all set", "best regards", "kind regards", "regards", "see you", "looking forward", 
        "appreciate it", "grateful", 'thanks', "cheers", "no further questions", "resolved", "all good", "sincerely", 
        "yours faithfully", "best wishes", "warm regards", "cordially", "catch you later", "see ya", "peace out", 
        "take it easy", "much appreciated", "thanks a lot", "thanks for your help", "got it", "understood", 
        "makes sense", "I see", "that's all for now", "we're done here", "that wraps it up", "nothing more to add", 
        "let me know if you have any questions", "sounds great", "sounds good", "talk to you later", "thank you for your time",
        "it was nice talking to you", "have a great day", "have a great evening", "all the best", "best of luck"
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
        print(f"Similarity between '{last_message}' and '{phrase}': {similarity}")  # Debug statement
        if similarity > 0.65:  # Adjusted threshold for stricter comparison
            print("Conversation is over based on the last message.")
            return True
    print("Conversation is not over based on the last message.")
    return False

# Function to check if the last message is from the account owner
def is_last_message_from_owner(sender_names, account_owner):
    if not sender_names:
        return False
    normalized_account_owner = account_owner.strip().lower()
    # Check if the last sender name matches the account owner
    return sender_names[-1].strip().lower() == normalized_account_owner


# Check if the account_owner didn't get a reply and if only account_owner's messages are present
import re  # Regular expressions

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
        print(f"All Messages: {all_messages}")

        return all_messages, last_message_owner, only_owner_messages
        
    except TimeoutException:
        print("\nTimed out waiting for message contents to be visible.")
        return [], False, False
    except NoSuchElementException:
        print("\nNo message elements found.")
        return [], False, False

# Check if the conversation contains a project link 
def contains_target_link(messages, link_prefixes=["https://link.onfrontiers.com/", "https://app.onfrontiers.com/expert_request/"]):
    """Check if any of the messages contain a link starting with the specified prefix."""
    for message in messages:
        for prefix in link_prefixes:
            if message.find(prefix) != -1:
                return True
    return False

# WEB DRIVER 

# Initialize the Chrome options
options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(f"--user-data-dir={chrome_user_data_dir}")
options.add_argument(f"--profile-directory={chrome_profile_dir}")

# Initialize the ChromeDriver with the specified options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# ACTIONS

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

# Zoom out with pyautogui
pyautogui.keyDown('ctrl')
for _ in range(10):
    pyautogui.press('-')
    time.sleep(0.5)  # Wait for the browser to react
pyautogui.keyUp('ctrl')

# Find the 'My Connections' button by its visible text and click it
#my_connections_button = driver.find_element(By.XPATH, "//button[normalize-space()='My Connections']")
#my_connections_button.click()
#time.sleep(random.uniform(1, 5))

# Unselect URL 
# Coordinates for the top-left corner and bottom-right corner of the target area
top_left_x = 4800
top_left_y = 370
bottom_right_x = 5100
bottom_right_y = 900

# Generate a random position within the defined area
random_x = random.randint(top_left_x, bottom_right_x)
random_y = random.randint(top_left_y, bottom_right_y)

# Move the mouse to the random position
pyautogui.moveTo(random_x, random_y)

# Perform the click
pyautogui.click()

# Function to click the "Load more conversations" button with retries
def click_load_more_button(driver, retries=3):
    for attempt in range(retries):
        try:
            load_more_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button/span[text()='Load more conversations']"))
            )
            load_more_button.click()
            print(f"\nClicked 'Load more conversations' on attempt {attempt + 1}. Waiting for loading...\n")
            time.sleep(random.uniform(1, 5))  # Wait for content to load
            return True
        except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
            print(f"\nError clicking 'Load more conversations' on attempt {attempt + 1}: {e}\n")
            time.sleep(random.uniform(1, 5))  # Wait before retrying
    return False

# Main interaction
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
            load_more_failures = 0  # Reset failures if the button is successfully clicked

    # Process each conversation card up to the specified number of conversations to process
    for card_index, card in enumerate(conversation_cards[:target_number_of_conversations]):
        print(f"\nProcessing card {card_index + 1}/{min(target_number_of_conversations, len(conversation_cards))}\n")
        try:
            # Click on the conversation card to load the conversation
            card.click()
            print("\nCard clicked, loading conversation...\n")
            time.sleep(random.uniform(1, 5))  # Wait a random time to allow the conversation to load

            # Scroll through the conversation to ensure all messages are loaded
            scroll_through_conversation(driver)

            # Extract messages and check the last message's ownership and whether only the owner has messaged
            all_messages_texts, last_message_owner, only_owner_messages = get_messages_and_count_owner_replies(driver, account_owner)
            print(f"\nExtracted {len(all_messages_texts)} messages. Last message owner: {last_message_owner}, Only owner messages: {only_owner_messages}\n")
            
            # Ensure all_messages_texts is correctly formatted as a list before further processing
            if not all(isinstance(msg, str) for msg in all_messages_texts):
                raise ValueError("All messages should be strings")

            # Skip if no specific link is found in the conversation
            if not contains_target_link(all_messages_texts):
                print("\nNo specific link found in the conversation. Skipping.\n")
                continue

            # Check for excessive follow-ups from the account owner without any replies
            too_many_follow_ups = check_too_many_follow_ups(len(all_messages_texts), only_owner_messages, max_follow_ups)
            if too_many_follow_ups:
                print("\nMore than allowed follow-ups from the account owner present, no follow-up needed.\n")
                continue

            # Check if there's a need to reply
            if last_message_owner and not only_owner_messages:
                print("Last message is from the account owner, and there's engagement from both sides. No reply needed.")
                continue

            # If the last message is from the account owner but there are no replies from the other party
            if last_message_owner and only_owner_messages:
                message_to_send = no_reply_follow_up
                print(f"\nCondition met for sending follow-up message. Should send: '{message_to_send}'\n")

                # Try sending the follow-up message
                send_message(driver, message_to_send)
                time.sleep(2)  # Ensure the message is sent before moving to the next conversation
                continue

            # Check if the conversation seems over and skip sending further messages
            last_message_text = all_messages_texts[-1] if all_messages_texts else ""
            conversation_over = is_conversation_similarly_over(last_message_text, only_owner_messages)
            if conversation_over:
                print("\nConversation seems to be over based on the last message. No reply needed.\n")
                continue

            # Concatenate all messages into a single string before categorizing
            conversation_context = "\n".join(all_messages_texts)

            # Categorize the conversation based on the entire message history
            conversation_category = categorize_with_gpt3(conversation_context)

            # Generate a reply based on the categorized conversation if not concluded
            conversation_reply = generate_reply_with_gpt3(conversation_category, conversation_context)
            print(f"\nGPT's reply to the conversation: '{conversation_reply}'\n")

            # Try sending the GPT-generated reply
            send_message(driver, conversation_reply)
            time.sleep(2)  # Ensure the message is sent before moving to the next conversation

        except Exception as e:
            print(f"\nError processing card {card_index + 1}: {e}")

        # Mimic human behavior with a randomized wait before the next card
        print("\nWaiting before processing the next card...\n")
        time.sleep(random.uniform(1, 3))

except Exception as e:
    print(f"\nError in main interaction loop: {e}")
