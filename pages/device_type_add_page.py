from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.signin_page import SigninPage


class AddDeviceType:
    def __init__(self, page: Page):
        self.page = page
        self.add_device_type_url = "https://demo.netbox.dev/dcim/device-types/add/"
        self.page_title = page.locator("h1.page-title")
        self.manufacturer_field = page.get_by_role("combobox", name="Manufacturer 󰛄")
        self.drop_down_option = page.get_by_role("option", name="APC")
        self.model_field = page.get_by_role("textbox", name="Model 󰛄")        
        self.slug_field = page.get_by_role("textbox", name="Slug 󰛄")
        self.default_platform = page.get_by_role("combobox", name="Default platform")
        self.default_platform_option = page.get_by_role("option", name="Ubuntu Linux 20.04")
        self.description_field = page.get_by_role("textbox", name="Description")
        self.tags_field = page.get_by_role("combobox", name="Tags")
        self.tag_option = page.get_by_role("option", name="Alpha")
        self.height_field = page.get_by_role("spinbutton", name="Height (U) 󰛄")
        self.height_error_field = page.locator("div.form-text.text-danger")
        self.add_device_button = page.get_by_role("button", name="Create", exact=True)

        self.overview_page_title = page.locator("h1.page-title")
        self.toast_element = page.locator("div.toast-body")

    def goto(self):
        """Navigate to the add new device page"""
        self.page.goto(self.add_device_type_url)

    def add_device_type(self, model_text, height_value, description_text):
        """Add new device with pre-defined values"""
        self.manufacturer_field.click()
        self.drop_down_option.click()
        self.model_field.fill(model_text)
        self.slug_field.click()
        self.height_field.clear()
        self.height_field.fill(height_value)
        self.default_platform.click()
        self.default_platform_option.click()
        self.description_field.fill(description_text)
        self.tags_field.click()
        self.tag_option.click()
        self.add_device_button.click()

    def populate_req_except_height(self, height_value):
        """Populate Manufacturer, Model and Slug field, clear the predefined Height value"""
        self.manufacturer_field.click()
        self.drop_down_option.click()
        self.model_field.fill(height_value)
        self.slug_field.click()
        self.height_field.clear()

    def login_or_signin(self):
        """Login or sign in user if login data does not exist"""
        login_page = LoginPage(self.page)
        login_page.login_user()
        if login_page.error_non_existant_user.is_visible():
            signin_page = SigninPage(self.page)
            signin_page.create_user()
