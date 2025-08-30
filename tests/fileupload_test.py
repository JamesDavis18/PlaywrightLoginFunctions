import re, pytest
from playwright.sync_api import sync_playwright, Page, expect
config_loader = __import__("config_loader")
from config_loader import get_value

def get_heading_text():
    return get_value("pages", "fileupload_heading")

@pytest.mark.usefixtures("page")
class TestFileUploadPage:
    @pytest.fixture(autouse=True)
    def setup_page(self, page: Page):
        page.goto("/upload", wait_until="domcontentloaded")
        page.wait_for_url("/upload")
        self.page = page
    
    def get_file_choose_control(self):
        return self.page.locator("#button").get_by_role("button", name="Choose File")
    
    def get_file_upload_button(self):
        return self.page.locator("#button").get_by_role("button", name="Upload")
    
    def test_is_home(self):
        self.page.goto("/")
        self.page.wait_for_url("**/")
        self.page.get_by_role("link", name="upload").click()

        expect(self.page).to_have_url("/upload")
        print(self.page.url)
        expect(self.page.get_by_role("heading", name="File Uploader")).to_be_visible()
    
    def test_btn_file_upload(self):
        upload_btn_locator = self.get_file_choose_control()
        upload_btn_locator.click()
        upload_btn_locator.set_input_files(["./files/codescreen.jpg"])
        expect(upload_btn_locator).to_have_value("C:\\fakepath\\code_screen.jpg")

print(f"{TestFileUploadPage} tests completed")


