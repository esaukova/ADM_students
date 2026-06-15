from selenium.webdriver.common.by import By
from base_page import BasePage
import logging

logger = logging.getLogger(__name__)

class DashboardPage(BasePage):
    SETTINGS_MENU_ITEM = (By.XPATH, "//span[text()='Настройки']")

    def __init__(self, driver):
        super().__init__(driver)

    def verify_login_success(self):
        logger.info("Проверяем успешность входа, ищем пункт меню 'Настройки'...")
        return self.is_element_visible(self.SETTINGS_MENU_ITEM)