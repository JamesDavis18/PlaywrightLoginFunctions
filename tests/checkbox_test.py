import re, pytest
from playwright.sync_api import sync_playwright, Page, expect
from tests.config_loader import get_value


def heading_text(pytestconfig):
    return pytestconfig.getini("checkboxpage_heading")

def get_checkbox1(self):
    return self.page.locator("form#checkboxes").get_by_role("checkbox").first

def get_checkbox2(self):
    return self.page.locator("form#checkboxes").get_by_role("checkbox").nth(1)

@pytest.mark.usefixtures("page")
class TestCheckBoxPage:
    @pytest.fixture(autouse=True)
    def setup_page(self, page):
        self.page = page
    
    def test_has_title(self):
        expect(self).to_have_title(re.compile("The Internet"))
    
    def test_is_home(self, page):
        expect(self).to_have_url("**/")
        print(page.url)
        expect(self).get_by_role("heading")
        assert "" in page.content()

    def test_get_checkbox_link(self):
        self.page.get_by_role("link", name="/Checkboxes").click()

        expect(self.page.get_by_role("heading", name="Checkboxes")).to_be_visible()
        heading = self.page.locator("h3")
        expect(heading.inner_text() == heading_text)
    
    def test_check_individual_checkboxes(self):
        checkbox1_locator = get_checkbox1()
        checkbox1_locator.first.check()
        expect(checkbox1_locator).to_be_checked()
        
        checkbox2_locator = get_checkbox2()
        checkbox2_locator.first.check()
        expect(checkbox1_locator).to_be_checked()
    
    def test_uncheck_individual_checkboxes(self):
        checkbox1_locator = get_checkbox1()
        checkbox1_locator.first.uncheck()
        expect(checkbox1_locator).not_to_be_checked()
        
        checkbox2_locator = get_checkbox2()
        checkbox2_locator.first.uncheck()
        expect(checkbox1_locator).not_to_be_checked()

    def test_checkbox_labels(self):
        checkbox1_label = self.page.locator("form#checkboxes").get_by_text("checkbox 1")
        expect(checkbox1_label).to_be_visible()
        expect(checkbox1_label).to_be_in_viewport()
        checkbox2_label = self.page.locator("form#checkboxes").get_by_text("checkbox 2")
        expect(checkbox2_label).to_be_visible()
        expect(checkbox2_label).to_be_in_viewport()
        
""" def check_individual_checkboxes(self):
        checkbox1_locator = get_checkbox1()
        checkbox1_locator.first.check()
        self.page.locator("form#checkboxes").get_by_role("checkbox").first.check()
        expect(self.page.get_by_role("checkbox").first).to_be_checked()
        self.page.locator("form#checkboxes").get_by_role("checkboxes").nth(1).check()
        expect(self.page.get_by_role("checkbox").nth(1)).to_be_checked()
    
    def uncheck_individual_checkboxes(self):
        self.page.locator("form#checkboxes").get_by_role("checkbox").first.uncheck()
        expect(self.page.get_by_role("checkbox").first).to_be_checked()
        self.page.locator("form#checkboxes")
        self.page.locator() """
print(f"{TestCheckBoxPage} tests completed")