import re, pytest
from playwright.sync_api import sync_playwright, Page, expect
config_loader = __import__("config_loader")
from config_loader import get_value
from pathlib import Path
import time

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
        #return self.page.locator("#file-upload").get_by_role("button", name="Choose File")
        return self.page.get_by_role("button", name="Choose File") 
    
    def get_file_upload_button(self):
        return self.page.get_by_role("button", name="Upload")
    
    def get_drag_drop_area(self):
        return self.page.query_selector("input.dz-hidden-input")
        #return self.page.locator(".dz-hidden-input[type='file']")
    
    def get_visible_dropzone(self):
        return self.page.query_selector("div.drag-drop-upload")
    
    def test_is_home(self):
        self.page.goto("/")
        self.page.wait_for_url("**/")
        self.page.get_by_role("link", name="upload").click()

        expect(self.page).to_have_url("/upload")
        print(self.page.url)
        expect(self.page.get_by_role("heading", name="File Uploader")).to_be_visible()
    
    def test_btn_file_upload(self):
        here = Path(__file__).parent
        file_path = here.parent / "files" / "code_screen.jpg"
        #self.page.on("filechooser")
        with self.page.expect_file_chooser() as fc_select:
            choosefile_btn_locator = self.get_file_choose_control()
            choosefile_btn_locator.click()
            file_chooser = fc_select.value
            file_chooser.set_files(file_path)
        #upload_btn_locator.set_input_files([".\\files\\codescreen.jpg"])
        expect(choosefile_btn_locator).to_have_value("C:\\fakepath\\code_screen.jpg")
        upload_btn_locator = self.get_file_upload_button()
        upload_btn_locator.click()
        self.page.wait_for_load_state("domcontentloaded")
        expect(self.page.get_by_role("heading", name="File Uploaded!")).to_be_visible()
        #uploaded_files_area = self.page.locator("div#uploaded-files.panel.text-center").get_by_test_id("#uploaded-files")
        uploaded_files_area = self.page.locator("")
        expect(uploaded_files_area).to_be_visible()
        expect(uploaded_files_area).to_have_text("code_screen.jpg")


    def test_multiple_upload(self):
        here = Path(__file__).parent
        path_one = here.parent / "files" / "logo.png"
        path_two = here.parent / "files" / "logo.jfif"
        with self.page.expect_file_chooser() as fc_upload:
            choosefile_btn_locator = self.get_file_choose_control()
            choosefile_btn_locator.click()
            file_chooser = fc_upload.value
            file_chooser.set_files(path_one)
        expect(choosefile_btn_locator).not_to_be_empty()
        #filename_div = self.page.locator().get_by_test_id("file-upload")
        filename_input = self.page.locator("#file-upload")
        file_value = filename_input.input_value()
        print(file_value)
        expect(filename_input).to_have_value("C:\\fakepath\\logo.png")
        time.sleep(3)
        #expect(filename_input).to_contain_text("logo.png")
        #upload_label = choosefile_btn_locator.all_text_contents()
        #assert upload_label.__contains__("logo.png")
        with self.page.expect_file_chooser() as fc_upload2:
            choosefile_btn_locator.click()
            file_chooser = fc_upload2.value
            file_chooser.set_files(path_two)
        expect(choosefile_btn_locator).not_to_be_empty()
        print(file_value)
        expect(filename_input).to_have_value("C:\\fakepath\\logo.jfif")
        #expect(filename_input).to_contain_text("logo.jfif")
        #upload_label2 = choosefile_btn_locator.all_text_contents()
        #assert upload_label.__contains__("logo.jfif")
        drag_drop_area = self.page.locator("#drag-drop-upload")
        expect(choosefile_btn_locator).to_have_value("C:\\fakepath\\logo.jfif")
        expect(drag_drop_area).to_be_visible()
        expect(drag_drop_area).to_be_in_viewport()
        self.page.wait_for_load_state("domcontentloaded")
        time.sleep(3)
        upload_children = drag_drop_area.locator("span")
        expect(upload_children).to_have_count(0)
        for i in range(upload_children.count()):
            #assert len(upload_children) == 0
            print(upload_children.nth(i).inner_text())

        upload_btn_locator = self.get_file_upload_button()
        upload_btn_locator.click()
        expect(self.page.locator("h3")).to_have_text("File Uploaded!")
        expect(self.page.get_by_role("heading", name="File Uploaded!")).to_be_visible()

    
    def test_drap_drop(self):
        file_path = Path(__file__).parent.parent / "files" / "logo.png"
        dragdrop_area = self.get_drag_drop_area()
        dragdrop_area.set_input_files(file_path)
        #expect(dragdrop_area).to_have_value("logo.png").dz-filename span

        upload_children = dragdrop_area.locator("span")
        expect(upload_children).to_have_count(1)
        for i in range(upload_children.count()):
            #assert len(upload_children).count == 1
            print(upload_children.nth(i).inner_text())
        
        upload_btn_locator = self.get_file_upload_button()
        upload_btn_locator.click()
        sucess_msg = self.page.get_by_role("heading", name="File Uploaded!")
        error_msg = self.page.locator("text=Internal Server Error")
        try:
            expect(sucess_msg).to_be_visible(timeout=3000)
            print("Upload succeeded!")
        except:
            expect(error_msg).to_be_visible(timeout=3000)
            print("Upload failed")
        finally:
            raise AssertionError("Neither success nor error message was displayed. Check format of the uploaded file")
        






print(f"{TestFileUploadPage} tests completed")


