from time import time
import pytest
import re
import random
import string
from playwright.sync_api import sync_playwright, Page, expect
config_loader = __import__("config_loader")
from config_loader import get_value

user_login = "tomsmith"
user_login_fail = "stevesmith"
user_password = "SuperSecretPassword!"
user_password_fail = "NotSecretPassword%"

def get_heading_text():
    return get_value("pages", "loginpage_heading")

def get_random_login_string(length):
    result_str = ''.join(random.choice(string.ascii_letters + string.digits) for i in range (length))
    return result_str

@pytest.mark.usefixtures("page")
class TestLoginPage:
    @pytest.fixture(autouse=True)
    def setup_page(self, page: Page):
        page.goto("/login", wait_until="domcontentloaded")
        page.wait_for_url("/login")

        self.page = page
        pass
        #self.page.goto("**/login")
        if not self.page.url.endswith("/login"):
            raise ValueError("Page did not navigate to the login page.")

    def get_usernameinput(self):
        return self.page.locator("form#login").get_by_role("textbox", name="Username")
    
    def get_usernameinput_name(self, element):
        return element.get_attribute("name")

    def get_passwordinput(self):
        return self.page.locator("form#login").get_by_role("textbox", name="Password")
    
    def get_passwordinput_name(self, element):
        return element.get_attribute("name")
    
    def goto_login_page(self):
        self.page.goto("/login")

    def test_has_title(self):
        expect(self.page).to_have_title(re.compile("The Internet"))

    def test_get_login_link(self):
        #self.page = page
        self.page.goto("/login", wait_until="domcontentloaded")

        expect(self.page.get_by_role("heading", name="Login Page")).to_be_visible()
        page_heading = get_heading_text()
        expect(self.page.locator("h2")).to_have_text(page_heading)


    def test_get_form_inputs(self):
        #goto_login_page = self.goto_login_page
        usertextbox_locator = self.get_usernameinput()
        usertextbox_locator_name = self.get_usernameinput_name(usertextbox_locator)
        print(f"Username input field found: {usertextbox_locator_name}")
        field_type = usertextbox_locator.get_attribute("type")
        expect(field_type).to_be("text")
        usertextbox_locator.fill(user_login)
        usertextbox_locator.all_text_contents()
        expect(usertextbox_locator).to_have_text(user_login).use_inner_text()
        usertextbox_locator.clear()
        expect(usertextbox_locator).to_have_text("").use_inner_text()

        passtextbox_locator = self.get_passwordinput()
        passtextbox_locator_name = self.get_passwordinput_name(passtextbox_locator)
        print(f"Password input field found: {passtextbox_locator_name}")
        field_type = passtextbox_locator.get_attribute("type")
        expect(field_type).to_be("password")
        passtextbox_locator.fill(user_password)
        passtexts = passtextbox_locator.all_inner_texts()
        expect(passtexts).to_have_text(user_password).use_inner_text()
        passtextbox_locator.clear()
        expect(passtextbox_locator).to_have_text("").use_inner_text()

    def test_form_inputs_fail(self):
        usertextinput_locator = self.get_usernameinput()
        usertextinput_locator.fill(user_login_fail)
        expect(usertextinput_locator).to_have_value(user_login_fail)

        passtextinput_locator = self.get_passwordinput()
        passtextinput_locator.fill(user_password_fail)
        expect(passtextinput_locator).to_have_value(user_password_fail)


    def test_form_login(self):
        usertextbox_locator = self.get_usernameinput()
        usertextbox_locator.fill(user_login)
        
        passtextbox_locator = self.get_passwordinput()
        passtextbox_locator.fill(user_password)

        submit_btn_locator = self.page.get_by_role("button", name=" Login")
        #button_type = submit_btn_locator.get_attribute(type)
        expect(submit_btn_locator).to_have_attribute("type", "submit")
        #expect(submit_btn_locator).to_contain_text("Login")
        submit_btn_locator.click()
        self.page.wait_for_load_state('domcontentloaded')  # Wait for the page to load after clicking the button
        expect(self.page).to_have_title("/secure")

        loggedin_heading = self.page.get_by_role("heading", name="Secure Area")
        expect(loggedin_heading).to_be_visible()
        print("Login successful!")
        #logic to navigate back to login page

    def test_form_login_fail(self):
        usertextbox_locator = self.get_usernameinput()
        usertextbox_locator.fill(user_login_fail)

        passtextbox_locator = self.get_passwordinput()
        passtextbox_locator.fill(user_password_fail)

        submit_btn_locator = self.page.get_by_role("button", name=" Login")
        expect(submit_btn_locator).to_have_text("Login")
        submit_btn_locator.click()

        fail_alert = self.page.locator("#flash-messages").get_by_text("Your username is invalid! ×")
        expect(fail_alert).to_be_visible()
        expect(fail_alert).to_have_css("background-color", "rgb(198, 15, 19)")
        
        fail_alert.filter(
            has=self.page.get_by_role("link", name="×").click()
        )
        #fail_alert_close.click()
        expect(fail_alert).not_to_be_visible()

    def test_random_login_fails(self):
        usertextbox_locator = self.get_usernameinput()
        usertextbox_locator.fill(get_random_login_string(10))
        expect(usertextbox_locator).to_have_value(re.compile(r"^[a-zA-Z0-9]{10}$"))

        passtextbox_locator = self.get_passwordinput()
        passtextbox_locator.fill(get_random_login_string(10))
        expect(usertextbox_locator).to_have_value(re.compile(r"^[a-zA-z0-9]{10}$"))

        submit_btn_locator = self.get

    
    #Other tests that would go here include: test for uppercase, special characters number requirements etc. 


print(f"{TestLoginPage} tests completed.")
