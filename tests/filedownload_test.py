import re, pytest
from playwright.sync_api import sync_playwright, Page, expect
from tests.config_loader import get_value

def heading_text():
    return get_value("pages", "hfiledownloadpage_heading")

class TestFileDownloadPage:
    
    #def __init__(self, page: Page):
        #self.page = page
    
    def test_has_title(self, page: Page):
        expect(self).to_have_title(re.compile("The Internet"))
    
    def is_home(self, page: Page):
        expect(self).to_have_url("**/")
        expect(self).get_by_role("heading")
        assert "" in page.content()
    
    def test_get_login_link(self, page: Page):
        self.get_by_role("link", name="File Download").click()

        expect(self.get_by_role("heading", name="Login Page")).to_be_visible()
        expect(self.page.locator("h3")).to_have_text(heading_text())
    
print(f"{TestFileDownloadPage} tests completed")