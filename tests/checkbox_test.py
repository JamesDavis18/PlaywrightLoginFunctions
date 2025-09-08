import time
import re, pytest
from playwright.sync_api import sync_playwright, Page, expect
config_loader = __import__("config_loader")
from config_loader import get_value


def get_heading_text():
    return get_value("pages", "checkboxpage_heading")

@pytest.mark.usefixtures("page")
class TestCheckBoxPage:
    @pytest.fixture(autouse=True)
    def setup_page(self, page: Page):
        page.goto("/checkboxes", wait_until="domcontentloaded")
        page.wait_for_url("/checkboxes")
        self.page = page

    def get_checkbox1(self):
        return self.page.locator("#checkboxes input").get_by_role("checkbox").nth(0)

    def get_checkbox2(self):
        return self.page.locator("#checkboxes input").get_by_role("checkbox").nth(1)
    
    def test_has_title(self):
        expect(self.page).to_have_title(re.compile("The Internet"))
    
    def test_is_home(self, page):
        expect(self.page).to_have_url("/checkboxes")
        print(self.page.url)
        expect(self.page.locator("h3").get_by_role("heading"))
        assert "" in page.content()

    def test_get_checkbox_link(self):
        self.page.goto("/")
        self.page.wait_for_url("**/")
        self.page.get_by_role("link", name="Checkboxes").click()

        self.page.wait_for_load_state("domcontentloaded")
        expect(self.page.get_by_role("heading", name="Checkboxes")).to_be_visible()
        heading = self.page.locator("h3")
        assert(heading.text_content() == get_heading_text())

    def test_allCheckboxes(self):
        checkboxes = self.page.locator("#checkboxes input")
        count = checkboxes.count()

        for i in range(count):
            checkboxes.nth(i).check()
            checkboxes.nth(i).uncheck()
    
    def test_check_individual_checkboxes(self):
        #checkbox1_locator = self.get_checkbox1()
        #checkbox1_locator.first.check()
        chckbox_1 = self.page.locator("#checkboxes input").first
        expect(chckbox_1).not_to_be_checked()
        chckbox_1.check()
        expect(chckbox_1).to_be_checked()
        
        chckbox_2 = self.page.locator("#checkboxes input").nth(1)
        expect(chckbox_2).to_be_checked()
        chckbox_2.uncheck()
        expect(chckbox_2).not_to_be_checked()

        """ checkbox2_locator = self.get_checkbox2()
        checkbox2_locator.first.uncheck()
        expect(checkbox1_locator).not_to_be_checked()
        checkbox2_locator.first.check()
        expect(checkbox2_locator).to_be_checked() """
    
    def test_uncheck_individual_checkboxes(self):
        chckbox_1 = self.page.locator("#checkboxes input").first
        expect(chckbox_1).not_to_be_checked()
        chckbox_1.check(force=True)
        time.sleep(2)
        #expect(self.page.get_by_label("checkbox 1")).to_be_checked()
        chckbox_1.uncheck()
        expect(chckbox_1).not_to_be_checked()

        chckbox_2 = self.page.locator("#checkboxes input").nth(1)
        #expect(chckbox_2).to_be_checked()
        chckbox_2.uncheck()
        time.sleep(2)
        expect(chckbox_2).not_to_be_checked()
        chckbox_2.check()
        expect(chckbox_2).to_be_checked()
        
        """ checkbox1_locator = self.get_checkbox1()
        checkbox1_locator.first.uncheck()
        expect(checkbox1_locator).not_to_be_checked()
        
        checkbox2_locator = self.get_checkbox2()
        checkbox2_locator.first.uncheck()
        expect(checkbox1_locator).not_to_be_checked() """

    def test_checkbox_labels(self):
        checkbox1_label = self.page.locator("form#checkboxes").get_by_text("checkbox 1")
        expect(checkbox1_label).to_be_visible()
        expect(checkbox1_label).to_be_in_viewport()
        checkbox2_label = self.page.locator("form#checkboxes").get_by_text("checkbox 2")
        expect(checkbox2_label).to_be_visible()
        expect(checkbox2_label).to_be_in_viewport()

    def test_doubleclick_checkboxes(self):
        chckbox_1 = self.page.locator("#checkboxes input").first
        expect(chckbox_1).not_to_be_checked()
        chckbox_1.dblclick()
        expect(chckbox_1).not_to_be_checked()

        chckbox_2 = self.page.locator("#checkboxes input").nth(1)
        expect(chckbox_2).to_be_checked()
        chckbox_2.dblclick()
        expect(chckbox_2).to_be_checked()
        
"""     def test_check_individual_checkboxes(self):
        checkbox1_locator = self.get_checkbox1()
        checkbox1_locator.first.check()
        self.page.locator("form#checkboxes").get_by_role("checkbox").first.check()
        expect(self.page.get_by_role("checkbox").first).to_be_checked()
        self.page.locator("form#checkboxes").get_by_role("checkboxes").nth(1).check()
        expect(self.page.get_by_role("checkbox").nth(1)).to_be_checked()
    
    def test_uncheck_individual_checkboxes(self):
        self.page.locator("form#checkboxes").get_by_role("checkbox").first.uncheck()
        expect(self.page.get_by_role("checkbox").first).to_be_checked()
        self.page.locator("form#checkboxes")
        self.page.locator() """

print(f"{TestCheckBoxPage} tests completed")