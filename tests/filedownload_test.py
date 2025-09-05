import re, pytest
from playwright.sync_api import sync_playwright, Page, expect
config_loader = __import__("config_loader")
from config_loader import get_value 
from pathlib import Path
import os, time

def get_heading_text():
    return get_value("pages", "filedownloadpage_heading")

@pytest.mark.usefixtures("page")
class TestFileDownloadPage:
    @pytest.fixture(autouse=True)
    def navigate_before_test(self, page: Page):
        page.goto("/download", wait_until="domcontentloaded")
        page.wait_for_url("**/download")
        
        self.page = page
        pass
        
        not_found = self.page.get_by_role("heading", name=re.compile("not found", re.IGNORECASE))
        if not_found.is_visible():
            raise ValueError("Page did not navigate to the file download page")
        #def __init__(self, page: Page):
        #self.page = page
    
    def test_has_title(self):
        expect(self.page).to_have_title(re.compile("The Internet"))

    def tmp_path(self):
        here = Path(__file__).parent
        file_path = here.parent / "downloads"
        return file_path
    
    def is_home(self, page: Page):
        expect(self).to_have_url("**/")
        expect(self).get_by_role("heading")
        assert "" in page.content()
    
    def test_get_filedownload_link(self):
        self.page.goto("/")
        self.page.wait_for_url("**/")
        self.page.get_by_role("link", name="File Download").click()
        
        self.page.wait_for_load_state("domcontentloaded")
        expect(self.get_by_role("heading", name="File Downloader")).to_be_visible()
        heading = self.page.locator("h3")
        assert(heading.text_content() == get_heading_text())
        #expect(self.page.locator("h3")).to_have_text(heading_text())

    def test_download_txt_empty(self, tmp_path):
        with self.page.expect_download() as download_txt:
            self.page.get_by_role("link", name="test.txt.txt").click()
        download = download_txt.value
        self.page.expect_download()
        time.sleep(3)

        #TODO change to use libpath
        #save_path = tmp_path / "test.txt"
        save_path = "/Users/james/source/repos/PlaywrightLoginFunctions/downloads" + download.suggested_filename
        download.save_as(save_path)

        #file_size = os.path.getsize(save_path)
        #assert file_size == 0, f"Expected empty file, but got {file_size} bytes"

        with open(save_path, "r") as dummy_file:
            content = dummy_file.read()
        assert content == "Sample", f"Expected 'Sample' text in file, but found {content} in file"
        #download.delete()   

        #dummy_file = "Users/Source/repos/PlaywrightLoginFunctions/dummy.txt"

        """ try:
            file_size = os.path.getsize(dummy_file)
            
            if file_size == 0:
                print("file is empty")
            else:
                print("File is not empty")
        except FileNotFoundError as e:
            print(f"Downloaded file not found {e}") """
    
    def test_download_txt_filled(self, tmp_path):
        with self.page.expect_download() as pytest_text:
            self.page.get_by_role("link", name="tmpdey056iz.txt")
        download = pytest_text.value
        self.page.expect_download()
        time.sleep(3)

        #save_path = tmp_path / "playwright-test-file.txt"
        save_path = "/Users/james/source/repos/PlaywrightLoginFunctions/downloads" + download.suggested_filename
        download.save_as(save_path)

        with open(save_path, "r") as pytest_txt:
            content = pytest_txt.read()
        assert content != ""
        pytest_sample = "hello from pytest"
        assert content == pytest_sample





    

    
print(f"{TestFileDownloadPage} tests completed")