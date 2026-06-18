from selenium.webdriver.common.by import By
from base_page import BasePage
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")
    ERROR_MESSAGE = (By.XPATH, "//*[contains(text(), 'Неверные учётные данные')]")

    def __init__(self, driver):
        super().__init__(driver)

    def login(self, username, password):
        logger.info("Начало процедуры входа.")
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        logger.info("Процедура входа завершена.")