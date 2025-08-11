import re, pytest
from playwright.sync_api import sync_playwright, Playwright

#Supported values "chromium", "firefox", "webkit"
BROWSER_TYPE = "firefox"

@pytest.fixture(scope="session")
def browser():
    #Launching one browser instance per test session
    with sync_playwright() as p:
        if BROWSER_TYPE == "chromium":
            browser = p.chromium.launch(headless=False)
        if BROWSER_TYPE == "firefox":
            browser = p.firefox.launch(headless=False)
        if BROWSER_TYPE == "webkit":
            browser = p.webkit.launch(headless=False)
        else:
            raise ValueError(f"Invalid browser type: {BROWSER_TYPE}")
        
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