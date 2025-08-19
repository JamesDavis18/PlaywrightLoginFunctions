import re, pytest
from playwright.sync_api import Playwright, Page, expect

subheading_text = "Welcome to the Secure Area. When you are done click logout below."
user_name = "tomsmith"
user_password = "SuperSecretPassword!"

@pytest.mark.usefixtures("page")
class BaseLoggedInTest:
    @pytest.fixture(autouse=True)
    def setup_page(self, page: Page):
        page.goto("/login", wait_until="domcontentloaded")
        page.locator("form#login").get_by_role("textbox", name="Username").fill(user_name)
        page.locator("form#login").get_by_role("textbox", name="Password").fill(user_password)
        page.get_by_role("button", name="Login").click()

        page.wait_for_url("/secure")
        self.page = page
        pass

class TestLoggedInPage(BaseLoggedInTest):    
    def test_has_title(self):
        expect(self.page).to_have_title(re.compile("The Internet"))

    def test_is_loggedin(self):
        expect(self.page.get_by_role("heading", name="Secure Area", exact=True))
        expect(self.page).to_have_url("/secure")
    
    def test_is_subheading_visible(self):
        #self.goto_login_page
        subheading = self.page.get_by_role("heading", name="Welcome to the Secure Area")
        expect(subheading).to_be_visible()
        expect(subheading).to_contain_text(subheading_text)

    def test_logout(self):
        logout_btn = self.page.get_by_role("link", name="Logout")
        logout_btn.hover()
        logout_btn.click()
        
        expect(self.page.get_by_role("heading", name="Secure Area")).not_to_be_visible()

print(f"{TestLoggedInPage} tests completed")