import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.signin_page import SigninPage

@pytest.fixture
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()
