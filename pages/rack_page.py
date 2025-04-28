from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.signin_page import SigninPage
from faker import Faker

fake = Faker()

class RackPage:
    def __init__(self, page: Page):
        self.page = page
        self.rack_url = "https://demo.netbox.dev/login/?next=/dcim/racks/39/"
        self.rack_table = page.locator("svg")
        self.device_name_field = page.get_by_role("textbox", name="Name")
        self.device_role_field = page.get_by_role("combobox", name="Device role 󰛄")
        self.device_role_option_field = page.get_by_role("option", name="Access Switch")
        self.device_type_field = page.get_by_role("combobox", name="Device type 󰛄")
        self.device_type_option = page.get_by_role("option", name="AP7901 APC")
        self.add_device_button = page.get_by_role("button", name="Create", exact=True)
        self.added_device_page_title = page.locator("h1.page-title")

        self.device_name = f"Milos Jovanovic Test {fake.word}"

    def goto(self):
        self.page.goto(self.rack_url)

    def goto_front_rack_page(self):
        self.page.goto("https://demo.netbox.dev/api/dcim/racks/39/elevation/?face=front&render=svg")

    def goto_rear_rack_page(self):
        self.page.goto("https://demo.netbox.dev/api/dcim/racks/39/elevation/?face=rear&render=svg")

    def populated_madatory_device_fields(self):
        self.device_role_field.click()
        self.device_role_option_field.click()
        self.device_type_field.click()
        self.device_type_option.click()
        self.device_name_field.fill(self.device_name)
        self.add_device_button.click()

    def login_or_signin(self):
        """Login or sign in user if login data does not exist"""
        login_page = LoginPage(self.page)
        login_page.login_user()
        if login_page.error_non_existant_user.is_visible():
            signin_page = SigninPage(self.page)
            signin_page.create_user()