import re, pytest
from playwright.sync_api import sync_playwright, Page, expect
from tests.config_loader import get_value
from conftest import page

def heading_text():
    return get_value("pages", "hoverpage_heading")

@pytest.mark.usefixtures("page")
class TestHoverProfilePage:
    @pytest.fixture(autouse=True)
    def navigate_before_test(self):
        self.page.goto("/hovers", wait_until="")

    def setup_page(self, page: Page):
        self.page = page
        #self.page = page

    def get_hoverelement1(self):
        return self.page.locator("#content").get_by_role("img", name="User Avatar").first

    def get_hoverelement2(self):
        return self.page.locator("#content").get_by_role("img", name="User Avatar").nth(1)

    def get_hoverelement3(self):
        return self.page.locator("#content").get_by_role("img", name="User Avatar").nth(2)

    def test_has_title(self):
        expect(self).to_have_title(re.compile("The Internet"))

    def is_home(self, page):
        expect(self).to_have_url("**/")
        expect(self).get_by_role("heading")
        assert "" in page.content()
    
    def test_get_hover_link(self):
        self.get_by_role("link", name="Hovers").click()

        expect(self.get_by_role("heading", name="Login Page")).to_be_visible()
        expect(self.page.locator("h3")).to_have_text(heading_text())
    
    def test_hover_over_elements(self, page: Page):
        hoverimg1 = self.get_hoverelement1
        expect(hoverimg1).to_be_enabled()
        hoverimg1.hover()

        userheading1 = self.get_by_role("heading", name="name: user1")
        expect(userheading1).to_be_visible()

        hoverimg2 = self.get_hoverelement2
        expect(hoverimg2).to_be_enabled()
        hoverimg2.hover()

        userheading2 = self.get_by_role("heading", name="name: user1")
        expect(userheading2).to_be_visible()

        hoverimg3 = self.get_hoverelement3()
        expect(hoverimg3).to_be_enabled()
        hoverimg3.hover()

        userheading3 = self.get_by_role("heading", name="name: user1")
        expect(userheading3).to_be_visible()

print(f"{TestHoverProfilePage} tests completed")

            
