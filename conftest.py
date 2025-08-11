import re, pytest
from playwright.sync_api import sync_playwright

#BROWSER_TYPE = "firefox"
def pytest_addoption(parser):
    parser.addini("browser_type", help="Browser type: chromium, firefox, webkit")
    try:
        parser.addoption("--my-browser", action="store", help="Override browser type")
    except ValueError:
        # Option already exists
        pass
    parser.addini("default_url", help="Default URL for the tests")           


@pytest.fixture(scope="session")
def browser(pytestconfig):
    browser_type = pytestconfig.getoption("browser") or pytestconfig.getini("browser_type")
    #Launching one browser instance per test session
    with sync_playwright() as p:
        if browser_type == "chromium":
            browser = p.chromium.launch(headless=False)
        elif browser_type == "firefox":
            browser = p.firefox.launch(headless=False)
        elif browser_type == "webkit":
            browser = p.webkit.launch(headless=False)
        else:
            raise ValueError(f"Invalid browser type: {browser_type}")
        
        yield browser
        browser.close()

@pytest.fixture
def page(browser, pytestconfig):
    context = browser.new_context()
    page = context.new_page()

    default_url = pytestconfig.getini("default_url")
    if default_url:
        page.goto(default_url)
    else:
        raise ValueError(f"Default URL not set in pytest.ini: {default_url}")
    page.set_default_timeout(10000)  # Set a default timeout for actions
    yield page
    context.close()


""" def run(playwright: sync_playwright):
    firefox = playwright.firefox
    browser = firefox.launch()
    page = browser.new_page()
    page.goto("https://the-internet.herokuapp.com/") """
    # other actions


""" with sync_playwright() as playwright:
    run(playwright) """