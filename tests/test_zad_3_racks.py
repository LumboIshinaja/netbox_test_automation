import pytest
from pages.rack_page import RackPage

"""Below is explained the attempt to get to the list of all available rack slots to add new device, unfortunatelly I never got to that list
In case the list is available following scenarios would make sense regarding to defined task"""
"""
1. Add new device if there is a free rack slot, after the device is created assert if the number of free slots has -1 element
2. Try to add device on occupied rack slot, assert if user is redirected to existing device page
3. If all slots are taken, assert the error (assuming in toast element)
"""

@pytest.fixture
def rack_page(page):
    """Logs user or creates new user entry if needed before each test run and provides rack page"""
    rack_page = RackPage(page)
    rack_page.login_or_signin()
    return rack_page

@pytest.mark.racks
def test_find_elements_on_main_racks_page(rack_page):
    """Tryin to locate elements on https://demo.netbox.dev/dcim/racks/{39} page""" 
    rack_page.goto()
    table = rack_page.page.locator("object[data='/api/dcim/racks/39/elevation/?face=front&render=svg']")
    table_class_value = table.get_attribute("class")
    print(f"Table object: {table.count()}, class value from table: {table_class_value}") # Printed value (1, rack_elevation), table element found
    table_children = rack_page.page.locator("object[data='/api/dcim/racks/39/elevation/?face=front&render=svg'] > *")
    print(f"All table children: {table_children.count()}") # Printed value 0, no children elements found for table element
    table_svg = rack_page.page.locator("svg")
    print(f"SVG table children: {table_svg.count()}") # Printed value 0, no 'svg' element found on page 

@pytest.mark.racks
def test_find_elements_on_linked_front_rack_page(rack_page):
    """Tryin to locate elements on linked https://demo.netbox.dev/api/dcim/racks/39/elevation/?face=front&render=svg page"""
    rack_page.goto_front_rack_page()
    table = rack_page.page.locator("svg")
    print(f"SVG items on linked page: {table.count()}") # Printed value 1, found svg item (table)
    table_all_children = rack_page.page.locator("svg > *")
    print(f"All SVG item children: {table_all_children.count()}") # Printed value 89
    table_a_children = table_all_children = rack_page.page.locator("svg > a")
    print(f"All SVG anchor type children {table_a_children.count()}") # Printed value 45 anchor child elements found

    anchor_with_add_device_text = []
    for i in range(table_a_children.count()):
        element = table_a_children.nth(i)
        if element.text_content().strip() == "add device":
            anchor_with_add_device_text.append(element)
    print(f"All anchor children with 'add device' text: {len(anchor_with_add_device_text)}") # Printed value 42. I expected
    # to have here filtered only free slots but that wasnt the case

    # tryin to clear the group of elements from the ones that have 'title' value, which is the case only for taken slots
    table_a_children_with_title = rack_page.page.locator("svg > a > title")
    print(f"All anchor 'add device' children with title: {table_a_children_with_title.count()}") # Printed value 3, which at 
    # the time of executing matches the number of taken slots
     
    table_a_children_without_title = rack_page.page.locator("svg > a > :scope > :not(title)")
    print(f"All anchor 'add device' children without title: {table_a_children_without_title.count()}") # Printed value 0
    # for some reason this wont work and it should be :(
    
@pytest.mark.racks
def test_find_elements_on_linked_rear_rack_page(rack_page):
    """Tryin to locate elements on linked https://demo.netbox.dev/api/dcim/racks/39/elevation/?face=rear&render=svg page"""
    # Basicaly same thing as the scenario above
    rack_page.goto_rear_rack_page()
    table = rack_page.page.locator("svg")
    print(f"SVG items on linked page: {table.count()}") 
    table_all_children = rack_page.page.locator("svg > *")
    print(f"All SVG item children: {table_all_children.count()}") 
    table_a_children = table_all_children = rack_page.page.locator("svg > a")
    print(f"All SVG anchor type children {table_a_children.count()}") 

    anchor_with_add_device_text = []
    for i in range(table_a_children.count()):
        element = table_a_children.nth(i)
        if element.text_content().strip() == "add device":
            anchor_with_add_device_text.append(element)
    print(f"All anchor children with 'add device' text: {len(anchor_with_add_device_text)}")

    table_a_children_with_title = rack_page.page.locator("svg > a > title")
    print(f"All anchor 'add device' children with title: {table_a_children_with_title.count()}")

    table_a_children_without_title = rack_page.page.locator("svg > a > :scope > :not(title)")
    print(f"All anchor 'add device' children without title: {table_a_children_without_title.count()}")