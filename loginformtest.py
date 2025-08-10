import re
from playwright.sync_api import Playwright, Page, expect

user_login = "tomsmith"
user_login_fail = "stevesmith"
user_password = "SuperSecretPassword!"
user_password_fail = "NotSecretPassword%"

class LoginPage:
    def _init_(self, page: Page):
        self.page = page

    def get_usernameinput(self):
        return self.page.locator("form#login").get_by_role("input", name="username")

    def get_passwordinput(self):
        return self.page.locator("form#login").get_by_role("input", name="password")

    def test_has_title(self):
        self.goto("https://the-internet.herokuapp.com")

        expect(self).to_have_title(re.compile("The Internet"))


    def test_get_login_link(self):
        self.get_by_role("link", name="/login").click()

        expect(self.get_by_role("heading", name="Login Page")).to_be_visible()
        expect(self.get_by_text("Login Page"))


    def test_get_form_inputs(page: Page):
        usertextbox_locator = get_usernameinput(page)
        usertextbox_locator.fill(user_login)
        expect(usertextbox_locator).to_contain_text(user_login)
        usertextbox_locator.clear()
        expect(usertextbox_locator).to_contain_text("")

        passtextbox_locator = get_passwordinput(page)
        usertextbox_locator.fill(user_password)
        expect(passtextbox_locator).to_contain_text(user_password)
        passtextbox_locator.clear()
        expect(passtextbox_locator).to_contain_text("")

    def test_form_inputs_fail(page: Page):
        usertextinput_locator = get_usernameinput(page)
        usertextinput_locator.fill(user_login_fail)
        expect(usertextinput_locator).to_contain_text(user_login_fail)

        passtextinput_locator = get_passwordinput(page)
        passtextinput_locator.fill(user_password_fail)
        expect(passtextinput_locator).to_contain_text(user_password_fail)


    def test_form_login(self):
        usertextbox_locator = get_usernameinput(self)
        usertextbox_locator.fill(user_login)
        
        passtextbox_locator = get_passwordinput(self)
        passtextbox_locator.fill(user_password)

        submit_btn_locator = self.get_by_role("button", name="submit")
        expect(submit_btn_locator).to_have_text("Login")
        submit_btn_locator.click()

        loggedin_heading = self.get_by_role("heading", name="Secure Area")
        expect(loggedin_heading).to_be_visible()

print(f"{LoginPage} tests completed.")
