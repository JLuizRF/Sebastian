
# README

## Introduction
This script automates LinkedIn messaging for the account owner "Kristine V. Sade". It uses various Python libraries and APIs to interact with LinkedIn, send messages based on specific criteria, and categorize responses using OpenAI's GPT-3. The script is designed to ensure that experts are engaged effectively and receive appropriate follow-ups.

## Prerequisites
- Python 3.x
- Chrome browser
- A LinkedIn account
- Necessary Python libraries (see Installation section)

## Installation
1. **Install Python Packages:**
   ```sh
   pip install re time random keyboard requests openai pyautogui dateutil datetime selenium webdriver_manager textblob spacy scipy
   ```

2. **Set Up Chrome Driver:**
   ```sh
   pip install webdriver-manager
   ```

3. **Download spaCy Model:**
   ```sh
   python -m spacy download en_core_web_md
   ```

## Configuration
1. **Account Details:**
   Set the account owner's name and LinkedIn profile path.
   ```python
   account_owner = 'Kristine V. Sade'
   person_linkedin_path = "in/kristine-v-sade-b81963296/"
   ```

2. **Chrome User Data:**
   Set the path to Chrome user data and profile directory.
   ```python
   chrome_user_data_dir = "C:\Users\55199\AppData\Local\Google\Chrome\User Data"
   chrome_profile_dir = "Profile 30"
   ```

3. **Support Emails:**
   ```python
   support_email = 'research@onfrontiers.com'
   payment_support_email = 'yzhang@onfrontiers.com'
   ```

4. **OpenAI API Key:**
   ```python
   openai.api_key = 'sk-proj-TDNUiINov0RzlXWLX7lYT3BlbkFJWg5JUZufIndEIsl3Gse9'
   ```

5. **Messaging Configuration:**
   ```python
   max_follow_ups = 1
   target_number_of_conversations = 50
   ```

6. **Instruction Templates:**
   Modify the instruction templates for various messaging scenarios as needed.

## Running the Script
1. **Initialize WebDriver:**
   The script uses ChromeDriver with specified options.
   ```python
   options = Options()
   options.add_experimental_option("detach", True)
   options.add_argument("--disable-gpu")
   options.add_argument("--no-sandbox")
   options.add_argument("--disable-dev-shm-usage")
   options.add_argument(f"--user-data-dir={chrome_user_data_dir}")
   options.add_argument(f"--profile-directory={chrome_profile_dir}")
   driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
   ```

2. **Navigate and Interact:**
   The script navigates to LinkedIn, accesses messages, scrolls through conversations, categorizes responses, and sends appropriate replies.
   ```python
   linkedin_url = f"https://www.linkedin.com/{person_linkedin_path}"
   driver.get(linkedin_url)
   driver.maximize_window()
   time.sleep(random.uniform(1, 5))
   ```

3. **Main Interaction Loop:**
   The script processes each conversation card, categorizes the conversation, and generates a reply based on the categorization.
   ```python
   while True:
       # Process logic here...
   ```

## Notes
- Ensure that your LinkedIn account is logged in and has necessary permissions.
- The script relies on specific CSS selectors and may need adjustments if LinkedIn's interface changes.
- The OpenAI API key should be kept secure and not shared publicly.

## Troubleshooting
- **Timeouts:** Increase the wait times in WebDriverWait statements if elements are not loading in time.
- **Selectors:** Verify and update CSS selectors if elements are not found.
- **API Errors:** Ensure the OpenAI API key is valid and has sufficient credits.

## License
This script is for personal and educational use only. Make sure to comply with LinkedIn's terms of service and usage policies.
