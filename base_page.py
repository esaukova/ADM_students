from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_execution.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        logger.info(f"Открываем URL: {url}")
        self.driver.get(url)

    def find_element(self, locator):
        logger.info(f"Ищем элемент по локатору: {locator}")
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        logger.info(f"Кликаем по элементу: {locator}")
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def send_keys(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        logger.info(f"Вводим текст '{text}' в элемент: {locator}")

    def is_element_visible(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            logger.info(f"Элемент {locator} виден на странице.")
            return True
        except TimeoutException:
            logger.warning(
                f"Элемент {locator} не найден на странице за {timeout} сек."
            )
            return False