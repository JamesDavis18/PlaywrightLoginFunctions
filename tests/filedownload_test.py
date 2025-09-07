import re, pytest
from playwright.sync_api import sync_playwright, Page, expect
config_loader = __import__("config_loader")
from config_loader import get_value 
from pathlib import Path
import os, time, json, subprocess
from PIL import Image

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
        self.page.get_by_role("link", name="File Download", exact=True).click()
        
        self.page.wait_for_load_state("domcontentloaded")
        expect(self.page.get_by_role("heading", name="File Downloader")).to_be_visible()
        heading = self.page.locator("h3")
        assert(heading.text_content() == get_heading_text())
        #expect(self.page.locator("h3")).to_have_text(heading_text())

    def test_download_txt_filled(self, downloads_dir):
        with self.page.expect_download() as download_txt:
            self.page.get_by_role("link", name="test.txt", exact=True).click()
        download = download_txt.value
        time.sleep(3)

        #save_path = tmp_path / "test.txt"
        save_path = os.path.join(downloads_dir, download.suggested_filename)
        #save_path = "/Users/james/source/repos/PlaywrightLoginFunctions/downloads" + download.suggested_filename
        download.save_as(save_path)

        file_size = os.path.getsize(save_path)
        assert file_size != 0, f"Expected file with content, but received empty file. {file_size} in bytes"

        with open(save_path, "r") as txt_download:
            content = txt_download.read()
        assert content == re.compile(r"test/n"), f"Expected 'test' text in file, but found {content} in file"
        txt_download.close()
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
    
    def test_download_txt_empty(self, downloads_dir):
        with self.page.expect_download() as dummy_text:
            self.page.get_by_role("link", name="dummy.txt").click()
        download = dummy_text.value
        time.sleep(3)

        #save_path = tmp_path / "playwright-test-file.txt"
        save_path = os.path.join(downloads_dir, download.suggested_filename)
        download.save_as(save_path)

        with open(save_path, "r") as pytest_txt:
            content = pytest_txt.read()
        assert content == ""

        file_size = os.path.getsize(save_path)
        assert file_size == 0, f"Expected empty file, but recieved file with a size of {file_size} bytes "

        pytest_txt.close()
        #pytest_sample = "hello from pytest"
        #assert content == pytest_sample

    def test_download_json(self, downloads_dir):
        with self.page.expect_download() as download_json:
            self.page.get_by_role("link", name="package.json").click()
        download = download_json.value
        time.sleep(3)

        save_path = os.path.join(downloads_dir, download.suggested_filename)
        download.save_as(save_path)
        
        #json_file = open(save_path)
        #data = json.load(json_file)
        with open(save_path, "r") as json_file:
            data = json.load(json_file)
        assert data != "", f"Data from JSON returned null {data}"

        dev_deps = data.get("devDependencies", {})
        scripts = data.get("scripts", {})

        for p in dev_deps:
            print (p)
        
        for p in scripts:
            print (p)
        
        requiredDeps = [
            "name",
            "type"
        ]

        for dep in requiredDeps:
            assert dep in requiredDeps, f"Missing required dependency: {dep}"

        requiredVers = [
            "@wdio/cli",
            "@wdio/local-runner",
            "@wdio/mocha-framework",
            "@wdio/spec-reporter"
        ]

        for dep in requiredVers:
            assert dep in requiredVers, f"Missing required dependency runner: {dep}"
        
        requiredScripts = [
            "wdio"
        ]

        for dep in requiredScripts:
            assert dep in requiredScripts, f"Missing required script key: {dep}"

        json_file.close()

    def test_download_jpg(self, downloads_dir):
        try:
            with self.page.expect_download() as download_jpg:
                self.page.get_by_role("link", name="megadyneBladeHero.jpg").click()
            download = download_jpg.value
        except Exception:
            with self.page.expect_download() as download_jpg:
                #self.page.get_by_role("link", name="megadyneBladeHero.jpg").click()
                self.page.get_by_role("link", name="4scr-73419325.jpg").click()
            download = download_jpg.value
        time.sleep(3)

        save_path = os.path.join(downloads_dir, download.suggested_filename)
        download.save_as(save_path)

        download_jpg, file_extension = os.path.splitext(save_path)
        assert file_extension == ".jpg"

        try:
            with Image.open(save_path) as im:
                im.show()
                print(save_path, im.format, f"{im.size}x{im.mode}")
                im.close()
                subprocess.call("TASKKILL /F /IM photos.exe", shell=True)
                time.sleep(10)
        except IOError as e:
            print(f"File is not a valid image file: {e}")
            pass

    def test_download_png(self, downloads_dir):
        try:   
            with self.page.expect_download() as download_png:
                self.page.get_by_role("link", name="sample_media_file.png").click()
                download = download_png.value
        except Exception:
            with self.page.expect_download() as download_png:
                self.page.get_by_role("link", name="selenium-snapshot.png").click()
                download = download_png.value
        time.sleep(3)

        saved_path = os.path.join(downloads_dir, download.suggested_filename)
        download.save_as(saved_path)

        download_png, file_extension = os.path.splitext(saved_path)
        assert file_extension == ".png"

        try:
            with Image.open(saved_path) as img:
                img.show()
                print(saved_path, img.format, f"{img.size}x{img.mode}")
                img.close()
                subprocess.call("TASKKILL /F /IM photos.exe", shell=True)
                time.sleep(10)
        except IOError as e:
            print(f"File is not a valid image file: {e}")

    def test_download_csv(self, downloads_dir):



    



print(f"{TestFileDownloadPage} tests completed")