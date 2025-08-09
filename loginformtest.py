import re
from playwright.sync_api import Page, expect

user_login = "tomsmith"
user_login_fail = "stevesmith"
user_password = "SuperSecretPassword!"
user_password_fail = "NotSecretPassword%"


def test_has_title(page: Page):
    page.goto("https://the-internet.herokuapp.com")

    expect(page).to_have_title(re.compile("The Internet"))


def test_get_login_link(page: Page):
    page.goto("https://the-internet.herokuapp.com")

    page.get_by_role("link", name="/login").click()

    expect(page.get_by_role("heading", name="Login Page")).to_be_visible()
    expect(page.__getattribute__("heading", e))


async def test_get_form_inputs(page: Page):
    usertextbox_locator = await page.get_by_role("username").fill(user_login)
    expect(usertextbox_locator).to_contain_text(user_login)

    passtextbox_locator = await page.get_by_role("password").fill(user_password)
    expect(passtextbox_locator).to_contain_text(user_password)

async def test_form_inputs_fail(page: Page):
    usertextinput_locator = await page.get_attribute(name="username").fill(user_login_fail)
    expect(usertextinput_locator).to_contain_text(user_login_fail)

    passtextoinput_locator = await page.get_attribute(name="password").fill(user_password_fail)
    expect(passtextoinput_locator).to_contain_text(user_password_fail)

