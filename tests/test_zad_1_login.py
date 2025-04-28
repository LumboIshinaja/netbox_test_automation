import pytest
from pages.login_page import LoginPage
from pages.signin_page import SigninPage

"""Test suite to verify the funtionality of the user sign in / login features"""

@pytest.fixture
def login_page(page):
    """Provides the login page before each test run"""
    login_page = LoginPage(page)
    login_page.goto()
    return login_page

@pytest.mark.login
def test_username_required(login_page):
    """Verify if the username is required"""
    login_page.enter_password()
    login_page.click_sign_in()

    class_value = login_page.username_field.get_attribute("class")
    assert class_value == "form-control is-invalid"

@pytest.mark.login
def test_password_required(login_page):
    """Verify if the password is required"""
    login_page.enter_username()
    login_page.click_sign_in()

    class_value = login_page.password_field.get_attribute("class")
    assert class_value == "form-control is-invalid"

@pytest.mark.login
def test_credentials_required(login_page):
    """Verify if both credentials are required"""
    login_page.click_sign_in()

    user_class_value = login_page.username_field.get_attribute("class")
    pass_class_value = login_page.password_field.get_attribute("class")
    assert user_class_value == "form-control is-invalid" and pass_class_value == "form-control is-invalid"

@pytest.mark.login
def test_non_existing_user(login_page):
    """Verify if appropriate error will be displayed if user with bad credentials tries to log in"""
    login_page.username_field.fill("unknown_user")
    login_page.password_field.fill("unknown_pass")
    login_page.click_sign_in()

    assert login_page.error_non_existant_user.is_visible()

@pytest.mark.login
def test_successful_login(login_page, page):
    """Verify if the user will be successfully logged in with appropriate credentials"""
    home_url = "https://demo.netbox.dev/"
    login_page.login_user()

    # Check if current user exists and use sign in if it does not
    if login_page.error_non_existant_user.is_visible():
        signin_page = SigninPage(page)
        signin_page.create_user()
        assert login_page.page.url != signin_page.signin_url
        assert login_page.page.url == home_url 

    # Proceed with stadard assertion if it exists
    else:
        assert login_page.page.url != login_page.login_url
        assert login_page.page.url == home_url 
           