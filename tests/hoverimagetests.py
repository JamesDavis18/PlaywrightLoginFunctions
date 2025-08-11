import re, pytest
from playwright.sync_api import sync_playwright, Page, expect

class HoverProfilePage:
    def __init__(self, page: Page):
        self.page = page
    