import re, pytest
from playwright.sync_api import sync_playwright, Page, expect
config_loader = __import__("config_loader")
from config_loader import get_value
from pathlib import Path
import time

def get_heading_text():
    return get_value("pages", "dragdroppage_heading")

@pytest.mark.usefixtures("page")
class TestDragDropPage:
    @pytest.fixture(autouse=True)
    def setup_page(self, page: Page):
        page.goto("/drag_and_drop", wait_until="domcontentloaded")
        page.wait_for_url("/drag_and_drop")
        self.page = page
    
    def get_drag_drop_source(self):
        return self.page.locator("#column-a")
    
    def get_drag_drop_dest(self):
        return self.page.locator("#column-b")
    
    def test_dragdrop_elements(self):
        source_element = self.get_drag_drop_source()
        source_text = self.page.get_by_text("A", exact=True)
        expect(source_text).to_be_visible()
        old_parent_source = source_text.locator("..")

        dest_element = self.get_drag_drop_dest()
        dest_text = self.page.get_by_text("B", exact=True)
        expect(dest_text).to_be_visible()
        old_parent_dest = dest_text.locator("..")
        source_element.drag_to(dest_element)
        time.sleep(5)
        new_parent_source = source_text.locator("..")
        new_parent_dest = dest_text.locator("..")

        assert old_parent_source != new_parent_source
        assert old_parent_dest != new_parent_dest
    
    def test_dragdrop_elements_reverse(self):
        drag_element = self.get_drag_drop_source()
        drag_text = self.page.get_by_text("A", exact=True)
        expect(drag_text).to_be_visible()
        old_drag_text_parent = drag_text.locator("..").get_attribute("id")

        drop_element = self.get_drag_drop_dest()
        drop_text = self.page.get_by_text("B", exact=True)
        expect(drop_text).to_be_visible()
        old_drop_text_parent = drop_text.locator("..").get_attribute("id")

        drag_element.drag_to(drop_element)
        time.sleep(2)
        drop_element.drag_to(drag_element)
        time.sleep(2)
        cur_drag_text_parent = drag_text.locator("..").get_attribute(id)
        cur_drop_text_parent = drop_text.locator("..").get_attribute(id)

        #expected this would work. Will try checking the parent countainer id
        assert old_drag_text_parent == cur_drag_text_parent
        assert old_drop_text_parent == cur_drop_text_parent

    
    def test_manual_dragdrop(self):
        drag_element = self.get_drag_drop_source()
        drag_text = self.page.get_by_text("A", exact=True)
        old_drag_parent_id = drag_text.locator("..").get_attribute("id")
        drop_element = self.get_drag_drop_dest()
        drop_text = self.page.get_by_text("B", exact=True)
        old_drop_parent_id = drop_text.locator("..").get_attribute("id")

        drag_element.hover()
        self.page.mouse.down()
        drop_element.hover()
        self.page.mouse.up()
        time.sleep(2)
        cur_drag_parent_id = drag_text.locator("..").get_attribute("id")
        cur_drop_parent_id = drop_text.locator("..").get_attribute("id")

        assert old_drag_parent_id != cur_drag_parent_id
        assert old_drop_parent_id != cur_drop_parent_id

print(f"{TestDragDropPage} tests completed")

        

