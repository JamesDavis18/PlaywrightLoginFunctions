import re, pytest
from playwright.sync_api import sync_playwright, Page, expect
config_loader = __import__("config_loader")
from config_loader import get_value
from pathlib import Path

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
        return self.page.locator("#drag-drop-locator")
    
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
        expect(self.page.locator("h3").get_by_role("heading", name="File Uploaded!")).to_be_visible()
        uploaded_files_area = self.page.locator("div#uploaded-files.panel.text-center").get_by_test_id("uploaded-files")
        expect(uploaded_files_area).to_be_in_viewport()
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
            file_chooser.set_files(path_two)
        drag_drop_area = self.page.locator("#drag-drop-upload")
        expect(choosefile_btn_locator).to_have_value("C:\\fakepath\\logo.jfif")
        expect(drag_drop_area).to_be_visible()
        upload_children = drag_drop_area.all_text_contents().count
        count = upload_children.count()
        assert count == 0
    
    def test_drap_drop(self):
        file_path = Path(__file__).parent.parent / "files" / "logo.png"
        with self.page.expect_file_dragdrop() as fc_upload:
            dragdrop_area = self.get_drag_drop_area()
            dragdrop_area.set_input_files(file_path)
        upload_children = dragdrop_area.all_text_contents().count
        count = upload_children.count()
        assert count == 1
        






print(f"{TestFileUploadPage} tests completed")


