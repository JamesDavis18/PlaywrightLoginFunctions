import re, pytest
from playwright.sync_api import sync_playwright, Page, expect

def heading_text(pytestconfig):
    return pytestconfig.getini("filedownloadpage_heading")

class FileDownloadPage:
    
    def __init__(self, page: Page):
        self.page = page
    
    def test_has_title(self):
        expect(self).to_have_title(re.compile("The Internet"))
    
    def is_home(self, page):
        expect(self).to_have_url("**/")
        expect(self).get_by_role("heading")
        assert "" in page.content()
    
