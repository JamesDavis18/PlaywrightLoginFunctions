import re
from playwright.sync_api import Playwright, Page, expect

subheading_text = "Welcome to the Secure Area. When you are done click logout below."

class TestLoggedInPage:

    #def _init_(self, page: Page):
        #self.page = page
    
    def test_has_title(self, page: Page):
        expect(self).to_have_title(re.compile("The Internet"))

    def test_is_loggedin(self, page: Page):
        expect(self).get_by_role("heading", name="Secure Area", exact=True)
        expect(self).to_have_url("**/")
    
    def test_is_subheading_visible(self, page: Page):
        subheading = self.page.get_by_role("heading", name="Welcome to the Secure Area")
        expect(subheading).to_be_visible()
        expect(subheading).to_contain_text(subheading_text)

    def test_logout(self, page: Page):
        logout_btn = self.page.get_by_role("link", name="Logout")
        logout_btn.hover()
        logout_btn.click()
        
        expect(self.page.get_by_role("heading", name="Secure Area")).not_to_be_visible()

print(f"{TestLoggedInPage} tests completed")