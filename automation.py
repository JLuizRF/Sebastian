from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

class WebAutomation:
    def __init__(self, user_data_dir, profile_dir):
        self.user_data_dir = user_data_dir
        self.profile_dir = profile_dir

    def start_browser(self):
        options = Options()
        options.add_argument(f"user-data-dir={self.user_data_dir}")
        options.add_argument(f"profile-directory={self.profile_dir}")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print("Browser started.")
