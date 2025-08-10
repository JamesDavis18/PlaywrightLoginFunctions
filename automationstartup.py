import re
from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    firefox = playwright.firefox
    browser = firefox.launch()
    page = browser.new_page()
    page.goto("https://the-internet.herokuapp.com")
    # other actions
    browser.close()
