import pytest
import re
from playwright.sync_api import sync_playwright, Page, expect
config_loader = __import__("tests.config_loader")
from tests.config_loader import get_value

user_login = "tomsmith"
user_login_fail = "stevesmith"
user_password = "SuperSecretPassword!"
user_password_fail = "NotSecretPassword%"

def get_heading_text():
    return get_value("pages", "loginpage_heading")

@pytest.mark.usefixtures("page")
class TestLoginPage:
    @pytest.fixture(autouse=True)
    def setup_page(self, page):
        self.page = page
        #self.page.goto("**/login")
        #if not self.page.url.endswith("/login"):
            #raise ValueError("Page did not navigate to the login page.")

    def setup_method(self, method):
        pass

    def get_usernameinput(self):
        return self.page.locator("form#login").get_by_role("textbox", name="Username")

    def get_passwordinput(self):
        return self.page.locator("form#login").get_by_role("textbox", name="Password")
    
    def goto_login_page(self):
        self.page.goto("/login")

    def test_has_title(self):
        expect(self.page).to_have_title(re.compile("The Internet"))

    def test_get_login_link(self):
        #self.page = page
        self.page.goto("/login", wait_until="networkidle")

        expect(self.page.get_by_role("heading", name="Login Page")).to_be_visible()
        page_heading = get_heading_text()
        expect(self.page.locator("h2")).to_have_text(page_heading)


    def test_get_form_inputs(self):
        goto_login_page = self.goto_login_page
        goto_login_page()
        usertextbox_locator = self.get_usernameinput
        print(usertextbox_locator.__name__)
        usertextbox_locator().fill(user_login)
        expect(usertextbox_locator).to_contain_text(user_login)
        usertextbox_locator.clear()
        expect(usertextbox_locator).to_contain_text("")

        passtextbox_locator = self.get_passwordinput
        passtextbox_locator().fill(user_password)
        expect(passtextbox_locator).to_contain_text(user_password)
        passtextbox_locator.clear()
        expect(passtextbox_locator).to_contain_text("")

    def test_form_inputs_fail(self):
        usertextinput_locator = self.get_usernameinput
        usertextinput_locator().fill(user_login_fail)
        expect(usertextinput_locator).to_contain_text(user_login_fail)

        passtextinput_locator = self.get_passwordinput
        passtextinput_locator().fill(user_password_fail)
        expect(passtextinput_locator).to_contain_text(user_password_fail)


    def test_form_login(self):
        usertextbox_locator = self.get_usernameinput
        usertextbox_locator().fill(user_login)
        
        passtextbox_locator = self.get_passwordinput
        passtextbox_locator().fill(user_password)

        submit_btn_locator = self.page.get_by_role("button", name="submit")
        expect(submit_btn_locator).to_have_text("Login")
        submit_btn_locator.click()

        loggedin_heading = self.page.get_by_role("heading", name="Secure Area")
        expect(loggedin_heading).to_be_visible()

print(f"{TestLoginPage} tests completed.")
