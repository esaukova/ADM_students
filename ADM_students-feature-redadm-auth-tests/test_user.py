import pytest
import logging
import time
from config import ADMIN_LOGIN, ADMIN_PASSWORD, USER_NAME, USER_PASSWORD
from login_page import LoginPage
from user_page import UserPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)


class TestREDADMLogin:

    @pytest.mark.positive
    def test_successful_create(self, driver, base_url):
        
        login_page = LoginPage(driver)
        user_page = UserPage(driver)

        login_page.open(base_url)
        login_page.login(ADMIN_LOGIN, ADMIN_PASSWORD)
        WebDriverWait(driver, 5).until(EC.url_changes(base_url))
        user_page.open("https://adm.redsoft.test/directory/objectTypeExplorer/user")
        user_page.create(USER_NAME, USER_PASSWORD)
        assert user_page.is_user_present(USER_NAME), f"Пользователь {USER_NAME} не появился"

    @pytest.mark.negative
    @pytest.mark.parametrize("username, password, description", [
        ("", "", "Пустые поля"),
        ("Administrator", "Qwerty.36", "Пользователь с таким логином уже существует"),
        ("weak_user", "1", "Слишком короткий пароль")
    ])
    def test_failed_user_creation(self, driver, base_url, username, password, description):
        login_page = LoginPage(driver)
        user_page = UserPage(driver)
        
        login_page.open(base_url)
        login_page.login(ADMIN_LOGIN, ADMIN_PASSWORD)
        WebDriverWait(driver, 5).until(EC.url_changes(base_url))
        user_page.open("https://adm.redsoft.test/directory/objectTypeExplorer/user")
        user_page.create(username, password)
        assert user_page.is_element_visible(user_page.ERROR_MESSAGE, timeout=5), f"Ошибка не появилась для кейса: '{description}'"
        
    
    @pytest.mark.positive
    def test_successful_redact(self, driver, base_url):
        
        login_page = LoginPage(driver)
        user_page = UserPage(driver)

        login_page.open(base_url)
        login_page.login(ADMIN_LOGIN, ADMIN_PASSWORD)
        WebDriverWait(driver, 5).until(EC.url_changes(base_url))
        user_page.open("https://adm.redsoft.test/directory/objectTypeExplorer/user")
        user_page.redact(USER_NAME)
        assert user_page.is_user_present(USER_NAME), f"Пользователь {USER_NAME} не найден"



    @pytest.mark.positive
    def test_successful_delete(self, driver, base_url):
        
        login_page = LoginPage(driver)
        user_page = UserPage(driver)

        login_page.open(base_url)
        login_page.login(ADMIN_LOGIN, ADMIN_PASSWORD)
        WebDriverWait(driver, 5).until(EC.url_changes(base_url))
        user_page.open("https://adm.redsoft.test/directory/objectTypeExplorer/user")
        user_page.delete(USER_NAME)
        assert user_page.is_user_absent(USER_NAME), f"Пользователь {USER_NAME} не удалился"
