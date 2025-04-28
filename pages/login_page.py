import os
from playwright.sync_api import Page
from dotenv import load_dotenv

# Load dotenv variables, override the system variables if set
load_dotenv(override=True)

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.login_url = "https://demo.netbox.dev/login/?next=/"
        self.username_field = page.get_by_role("textbox", name="Username")
        self.password_field = page.get_by_role("textbox", name="Password")
        self.sign_in_button = page.get_by_role("button", name="Sign In")
        self.error_non_existant_user = page.get_by_text("Errors Please enter a correct")

        # Fetch the variable values from .env file
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")

    def goto(self):
        """Navigate to the login page"""
        self.page.goto(self.login_url)

    def enter_username(self):
        """Enter username"""
        self.username_field.fill(self.username)

    def enter_password(self):
        """Enter password"""
        self.password_field.fill(self.password)

    def click_sign_in(self):
        "Click sign in button"
        self.sign_in_button.click()

    def login_user(self):
        """Login user to application"""
        self.page.goto(self.login_url)
        self.username_field.fill(self.username)
        self.password_field.fill(self.password)
        self.sign_in_button.click()
