""" import pytest
from playwright.sync_api import Browser
from PlaywrightLoginFunctions.conftest import browser

# Python


def test_browser_fixture_yields_browser_instance(browser):
    assert isinstance(browser, Browser)

def test_browser_can_create_context_and_page(browser):
    context = browser.new_context()
    page = context.new_page()
    assert page.url == "about:blank"
    context.close()

@pytest.mark.parametrize("browser_type", ["chromium", "firefox", "webkit"])
def test_browser_type_launch(pytestconfig, browser_type):
    pytestconfig._inicache["browser_type"] = browser_type
    with pytest.raises(ValueError) if browser_type not in ["chromium", "firefox", "webkit"] else pytest.raises(Exception) as excinfo:
        # This will only raise if browser_type is invalid
        pass """