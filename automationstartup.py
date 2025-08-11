import re, pytest, configparser
from playwright.sync_api import sync_playwright, Playwright

#BROWSER_TYPE = "firefox"
def pytest_browser_source(parser):
    parser.addini("browser_type", help="Browser type: chromium, firefox, webkit")
    parser.addoption("--browser", action="store", help="Override browser type")

@pytest.fixture(scope="session")
def browser(pytestconfig):
    browser_type = pytestconfig.getini("browser_type") or pytestconfig.getoption("browser")

    #Launching one browser instance per test session
    with sync_playwright() as p:
        if browser_type == "chromium":
            browser = p.chromium.launch(headless=False)
        if browser_type == "firefox":
            browser = p.firefox.launch(headless=False)
        if browser_type == "webkit":
            browser = p.webkit.launch(headless=False)
        else:
            raise ValueError(f"Invalid browser type: {browser_type}")
        
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


def run(playwright: sync_playwright):
    firefox = playwright.firefox
    browser = firefox.launch()
    page = browser.new_page()
    page.goto("https://the-internet.herokuapp.com")
    # other actions

#def close(playwright: Playwright):    
    #browser.close()

with sync_playwright() as playwright:
    run(playwright)