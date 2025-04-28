from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.signin_page import SigninPage


class AddDevice:
    def __init__(self, page: Page):
        self.page = page
        self.add_device_url = "https://demo.netbox.dev/dcim/devices/add/"
        self.device_name_field = page.get_by_role("textbox", name="Name")
        self.device_role_field = page.get_by_role("combobox", name="Device role 󰛄")
        self.device_role_option_field = page.get_by_role("option", name="Access Switch")
        self.device_type_field = page.get_by_role("combobox", name="Device type 󰛄")
        self.device_type_option = page.get_by_role("option", name="AP7901 APC")
        self.device_site_field = page.get_by_role("combobox", name="Site 󰛄")
        self.device_site_option = page.get_by_role("option", name="Butler Communications")
        self.add_device_button = page.get_by_role("button", name="Create", exact=True)
        self.added_device_page_title = page.locator("h1.page-title")
        self.delete_device_button = page.get_by_role("link", name="Delete")
        self.confirm_dialog_delete_button = page.locator("div[class='modal-dialog'] div[class='modal-footer'] button[type='submit']")
        self.toast_element = page.locator("div.toast-body")

    def goto(self):
        self.page.goto(self.add_device_url)

    def add_new_device(self):
        """Adding new device with the text value for type drop-down option"""
        self.device_role_field.click()
        self.device_role_option_field.click()
        self.device_type_field.click()
        self.device_type_option.click()
        self.device_site_field.click()
        self.device_site_option.click()
        self.add_device_button.click()

    def delete_device(self):
        """Deletes the device"""
        self.delete_device_button.click()
        self.confirm_dialog_delete_button.wait_for(state="visible", timeout=2000)
        self.confirm_dialog_delete_button.click()

    def login_or_signin(self):
        """Login or sign in user if login data does not exist"""
        login_page = LoginPage(self.page)
        login_page.login_user()
        if login_page.error_non_existant_user.is_visible():
            signin_page = SigninPage(self.page)
            signin_page.create_user()