import re, pytest
from playwright.sync_api import sync_playwright, Page, expect
from tests.config_loader import get_value

class FileDownloadPage:
    
    def __init__(self, page: Page):
        self.page = page
    
    def test_has_title(self):
        expect(self).to_have_title(re.compile("The Internet"))
    
    def is_home(self, page):
        expect(self).to_have_url("**/")
        expect(self).get_by_role("heading")
        assert "" in page.content()
    
print(f"{FileDownloadPage} tests completed")