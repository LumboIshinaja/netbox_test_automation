from pages.device_type_overview_page import DeviceTypeOverview
from pages.device_type_add_page import AddDeviceType
from pages.device_add_page import AddDevice
import pytest
from faker import Faker

"""Test suite to verify the funtionality of deleting devices and device types features"""

fake = Faker()
model_text = f"Milos test {fake.word()}"
height_value = "2"
description_text = f"Milos {fake.word()} description"
linked_device_type = "AP7901" # pre-defined device type which is linked to the device for test purposes (would need more time to implement dynamic
# adding new device to link it with created device type to assert that it cannot be deleted like that :))

@pytest.fixture
def add_pages(page):
    """Logs user or creates new user entry if needed and provides pages for test suite"""
    device_type_overview_page = DeviceTypeOverview(page)
    add_device_type_page = AddDeviceType(page)
    add_device_page = AddDevice(page)
    add_device_type_page.login_or_signin()
    return add_device_type_page, device_type_overview_page, add_device_page

@pytest.mark.del_device_type
def test_delete_device_type(add_pages):
    """Verify if device type can be successfully deleted if it is not linked to any device"""
    add_device_type_page, device_type_overview_page, _ = add_pages
    # adding new device type
    add_device_type_page.goto()
    add_device_type_page.add_device_type(model_text=model_text, height_value=height_value, description_text=description_text)
    # finding created device type
    device_type_overview_page.goto()
    device_type = device_type_overview_page.find_device_type(device_type=model_text) # there was no particular need to find created device type since 
                                                                            # after new one is being created user is redirected to that device type page
                                                                            # but would be a useful logic in broad sense of things
    device_type.click()
    # deleting found device type
    device_type_overview_page.delete_device_type()
    device_type_overview_page.page.wait_for_load_state()

    # asserting if deleted device does not exist in overview anymore
    assert device_type_overview_page.find_device_type(device_type=model_text) is None

@pytest.mark.del_device_type
def test_delete_linked_device_type(add_pages):
    """Verify that device type cannot be deleted if linked to the existing device"""
    _, device_type_overview_page, _ = add_pages
    device_type_overview_page.goto()
    # finding predefined linked device type
    device_type = device_type_overview_page.find_device_type(device_type=linked_device_type)
    device_type.click()
    # attempt to delete found device type
    device_type_overview_page.delete_device_type_button.click()
    # getting alert text
    device_type_overview_page.page.locator("div[role='alert']").wait_for(state="visible", timeout=3000)
    alert_text_value = device_type_overview_page.page.locator("div[role='alert']").text_content()
    
    # assert if error message in alert is appropriate
    assert "Unable to delete" in alert_text_value

@pytest.mark.del_device_type
def test_delete_device(add_pages):
    """Verify if the device can be successfully deleted"""
    # Reported "Device cannot be deleted" bug
    _, _, add_device_page = add_pages
    # adding new device
    add_device_page.goto()
    add_device_page.add_new_device()
    add_device_page.page.wait_for_load_state() # now I use redirection instead of finding created device like I did for device type above
    # deleting created device
    add_device_page.delete_device()
    # getting alert value
    add_device_page.toast_element.wait_for(state="visible", timeout=3000)
    alert_text_value = add_device_page.toast_element.text_content()

    assert "Deleted device" in alert_text_value