from selenium.webdriver.common.by import By
from base_page import BasePage
import logging

logger = logging.getLogger(__name__)

class UserPage(BasePage):
    FULLNAME_INPUT = (By.NAME, "name")
    USERNAME_INPUT = (By.NAME, "sAMAccountName")
    REDACTED_NAME_INPUT = (By.XPATH, "//div[label[text()='Имя']]//input")
    PASSWORD_INPUT = (By.NAME, "password")
    CONFIRM_PASSWORD_INPUT = (By.NAME, "confirmPassword")
    CREATE_BUTTON = (By.XPATH, "//button[contains(., 'Создать')]")
    CONFIRM_CREATE_BUTTON = (By.XPATH, "//div[contains(@class, 'DialogActions')]//button[contains(., 'Создать')]")
    DELETE_BUTTON = (By.XPATH, "//button[contains(., 'Удалить')]")
    CONFIRM_DELETE_BUTTON = (By.XPATH, "//*[@role='dialog']//button[contains(., 'Удалить')]")
    BLANK_CLICK = (By.XPATH, "//body")
    USER_SAVE_BUTTON = (By.XPATH, "//button[@data-tooster-action='save']")
    REDACT_EXIT_BUTTON = (By.XPATH, "//button[@aria-label='Назад']")
    ERROR_MESSAGE = (By.XPATH, "//*[@role='alert'] | //*[contains(@class, 'error')]") 

    def __init__(self, driver):
        super().__init__(driver)

    def create(self,username, password):
        self.click(self.CREATE_BUTTON)
        self.send_keys(self.FULLNAME_INPUT, username)
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.send_keys(self.CONFIRM_PASSWORD_INPUT, password)
        self.click(self.CONFIRM_CREATE_BUTTON)
        self.click(self.BLANK_CLICK)
    
    def redact(self, username):
        user_button = (By.XPATH, f"//a[span[text()='{username}']]") 
        self.click(user_button) 
        self.send_keys(self.REDACTED_NAME_INPUT, username)
        self.click(self.USER_SAVE_BUTTON)
        self.click(self.REDACT_EXIT_BUTTON)

    def delete(self, username):
        user_select_button = (By.XPATH, f"//div[@data-field='objectDisplayName' and contains(., '{username}')]")
        self.click(user_select_button)
        self.click(self.DELETE_BUTTON)
        self.click(self.CONFIRM_DELETE_BUTTON)
        self.click(self.BLANK_CLICK)
    
    def is_user_present(self, username):
        locator = (By.XPATH, f"//div[@data-field='objectDisplayName' and contains(., '{username}')]")
        return self.is_element_visible(locator)

    def is_user_absent(self, username):
        locator = (By.XPATH, f"//div[@data-field='objectDisplayName' and contains(., '{username}')]")
        return self.is_element_invisible(locator)