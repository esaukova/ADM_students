from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "http://127.0.0.1:8080/login"

        # Локатор поля ввода логина
        self.USERNAME_INPUT = (By.NAME, "username")

        # Локатор поля ввода пароля
        self.PASSWORD_INPUT = (By.NAME, "password")

        # Локатор кнопки входа
        self.SUBMIT_BUTTON = (By.XPATH, "//button[contains(., 'Войти')]")

        # Локатор имени пользователя после успешной авторизации
        self.ADMIN_NAME_LABEL = (By.XPATH, "//*[normalize-space()='Administrator']")

    def open(self):
        """Открытие страницы авторизации"""

        self.driver.get(self.url)

    def login(self, username, password):
        """Ввод логина, пароля и нажатие кнопки входа"""

        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def get_logged_in_user(self):
        """Ожидание появления имени пользователя после входа"""

        wait = WebDriverWait(self.driver, 20)
        return wait.until(
            EC.visibility_of_element_located(self.ADMIN_NAME_LABEL)
        )