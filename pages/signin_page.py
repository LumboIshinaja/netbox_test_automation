import os
from playwright.sync_api import Page
from dotenv import load_dotenv

# Load dotenv variables, override the system variables if set
load_dotenv(override=True)

class SigninPage:
    def __init__(self, page: Page):
        self.page = page
        self.signin_url = "https://demo.netbox.dev/plugins/demo/login/"
        self.username_field = page.get_by_role("textbox", name="Username")
        self.password_field = page.get_by_role("textbox", name="Password")
        self.signin_button = page.get_by_role("button", name="Create & Sign In")

        # Fetch the variable values from .env file
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")

    def create_user(self):
        """Create user if it does not exist"""
        self.page.goto(self.signin_url)
        self.username_field.fill(self.username)
        self.password_field.fill(self.password)
        self.signin_button.click()
