from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.signin_page import SigninPage

class DeviceTypeOverview:
    def __init__(self, page: Page):
        self.page = page
        self.device_type_overview_url = "https://demo.netbox.dev/dcim/device-types/"
        self.delete_device_type_button = page.get_by_role("link", name="Delete")
        self.confirm_dialog_delete_button = page.locator("div[class='modal-dialog'] div[class='modal-footer'] button[type='submit']")
        self.toast_element = page.locator("div.toast-body")

    def goto(self):
        self.page.goto(self.device_type_overview_url)

    def find_device_type(self, device_type):
        # find all table's tr 
        all = self.page.locator("table.table.table-hover.object-list > :nth-child(2) > tr")
        for i in range(all.count()):
            tr_element = all.nth(i)
            # extract text from td 
            td_element_text = tr_element.locator("a").first.text_content()                
            if td_element_text == device_type:
                # return first anchor link value
                return tr_element.locator("a").first
            
    def delete_device_type(self):
        """Deletes the device type"""
        self.delete_device_type_button.click()
        self.confirm_dialog_delete_button.wait_for(state="visible", timeout=2000)
        self.confirm_dialog_delete_button.click()        

    def login_or_signin(self):
        """Login or sign in user if login data does not exist"""
        login_page = LoginPage(self.page)
        login_page.login_user()
        if login_page.error_non_existant_user.is_visible():
            signin_page = SigninPage(self.page)
            signin_page.create_user()