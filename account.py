class AccountManager:
    def __init__(self, owner, linkedin_path):
        self.owner = owner
        self.linkedin_path = linkedin_path

    def display_account_info(self):
        print(f"Account Owner: {self.owner}")
        print(f"LinkedIn Path: {self.linkedin_path}")
