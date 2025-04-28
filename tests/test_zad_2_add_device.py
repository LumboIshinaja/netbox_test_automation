from pages.device_type_add_page import AddDeviceType
import pytest
from faker import Faker

"""Test suite to verify the funtionality of the add device type feature"""

fake = Faker()
model_text = f"Milos test {fake.word()}"
height_value = "2"
description_text = f"Milos {fake.word()} description"

@pytest.fixture
def add_device_type_page(page):
    """Logs user or creates new user entry if needed before each test run and provides add device type page"""
    add_device_type_page = AddDeviceType(page)
    add_device_type_page.login_or_signin()
    add_device_type_page.goto()
    return add_device_type_page

@pytest.mark.add_device
def test_add_new_device(add_device_type_page):
    """Verify if the new device is successfully added by checking if the input value for model is contained in device overview 
    title and toast element"""
    add_device_type_page.add_device_type(model_text=model_text, height_value=height_value, description_text=description_text)

    # Get text values
    model_text_value = add_device_type_page.overview_page_title.text_content()
    toast_text_value = add_device_type_page.toast_element.text_content().strip()

    assert model_text in model_text_value
    assert toast_text_value == f"Created device type {model_text}"

@pytest.mark.add_device
def test_no_duplicate_devices(add_device_type_page):
    """Verify if device with same input fields cannot be created"""
    add_device_type_page.add_device_type(model_text=model_text, height_value=height_value, description_text=description_text)

    # Get text value
    toast_text_value = add_device_type_page.toast_element.first.text_content().strip()

    assert toast_text_value == "Device type with this Manufacturer and Model already exists."

@pytest.mark.add_device
def test_manufacturer_required(add_device_type_page):
    """Verify if the manufacturer field is required to add new device, if not populated user stays on same page"""
    add_device_type_page.model_field.fill("Test")
    add_device_type_page.slug_field.click()
    add_device_type_page.add_device_button.click()

    # Get page title info since manufacturer field does not change class to 'ivalid form'
    page_text_value = add_device_type_page.page_title.text_content().strip()
    assert page_text_value == "Add a new device type"

@pytest.mark.add_device
def test_model_required(add_device_type_page):
    """Verify if the model field is required to add new device, field form becomes invalid"""
    add_device_type_page.manufacturer_field.click()
    add_device_type_page.drop_down_option.click()
    add_device_type_page.slug_field.fill("Test")
    add_device_type_page.add_device_button.click()

    # Get the class value
    class_value = add_device_type_page.model_field.get_attribute("class")
    assert class_value == "form-control is-invalid"

@pytest.mark.add_device
def test_slug_required(add_device_type_page):
    """Verify if the slug field is required to add new device, field form becomes invalid"""
    # Reported "Slug field copies the value set for the Model field" bug
    add_device_type_page.manufacturer_field.click()
    add_device_type_page.drop_down_option.click()
    add_device_type_page.model_field.fill("Test")
    add_device_type_page.add_device_button.click()
   
    # Get the class value
    class_value = add_device_type_page.slug_field.get_attribute("class")
    assert class_value == "form-control is-invalid"

@pytest.mark.add_device
def test_height_required(add_device_type_page):
    """Verify if the height field is required to add new device, field form becomes invalid"""
    add_device_type_page.manufacturer_field.click()
    add_device_type_page.drop_down_option.click()
    add_device_type_page.model_field.fill("Test")
    add_device_type_page.slug_field.click()
    # Clearing pre-populated heigh value
    add_device_type_page.height_field.clear()
    add_device_type_page.add_device_button.click()
   
    # Get the class value
    class_value = add_device_type_page.height_field.get_attribute("class")
    assert class_value == "form-control is-invalid"

@pytest.mark.height
@pytest.mark.parametrize("input_value, expected_form_message",
                        [
                        ("11111", "Ensure that there are no more than 4 digits in total."),
                        ("111111", "Ensure that there are no more than 4 digits in total."),
                        ("-111111", "Ensure that there are no more than 4 digits in total.")
                        ]
                    )
def test_height_invalid_values(add_device_type_page, input_value, expected_form_message):
    """Verify that inputing 5 or more digits for height value will trigger validation"""
    add_device_type_page.populate_req_except_height(height_value=height_value)
    add_device_type_page.height_field.fill(input_value)
    add_device_type_page.add_device_button.click()
    add_device_type_page.height_error_field.click()
    error_text = add_device_type_page.height_error_field.text_content().strip()
    
    assert error_text == expected_form_message
