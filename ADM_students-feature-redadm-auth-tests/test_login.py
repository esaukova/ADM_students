import pytest
import logging
import time
from config import ADMIN_LOGIN, ADMIN_PASSWORD
from login_page import LoginPage
from dashboard_page import DashboardPage

logger = logging.getLogger(__name__)


class TestREDADMLogin:

    @pytest.mark.positive
    def test_successful_login(self, driver, base_url):
        """Тест успешной авторизации"""
        logger.info("Запуск теста: Успешная авторизация в RED ADM")
        
        login_page = LoginPage(driver)
        login_page.open(base_url)
        
        assert "login" in driver.current_url.lower() or driver.current_url == base_url, \
            f"Не загрузилась страница логина. URL: {driver.current_url}"
        
        login_page.login(ADMIN_LOGIN, ADMIN_PASSWORD)
        time.sleep(2)
        
        dashboard_page = DashboardPage(driver)
        
        assert "login" not in driver.current_url.lower(), \
            "Остались на странице логина после ввода правильных данных"
        
        assert dashboard_page.verify_login_success(), \
            "Вход не выполнен успешно"
        
        logger.info("✓ Тест успешной авторизации пройден")

    @pytest.mark.negative
    @pytest.mark.parametrize("username,password", [
        ("wrong_user", ADMIN_PASSWORD),
        (ADMIN_LOGIN, "wrong_password"),
        ("", ""),
    ])
    def test_failed_login(self, driver, base_url, username, password):
        """Тест неудачной авторизации"""
        logger.info(f"Запуск теста: Неудачная авторизация - {username}/{password}")
        
        login_page = LoginPage(driver)
        login_page.open(base_url)
        
        login_page.login(username, password)
        time.sleep(2)
        
        error_displayed = login_page.is_element_visible(login_page.ERROR_MESSAGE, timeout=2)
        
        if error_displayed:
            logger.info("✓ Сообщение об ошибке отображено корректно")
            assert True
        else:
            current_url = driver.current_url
            if "login" in current_url or base_url in current_url:
                logger.info("✓ Остались на странице логина")
                assert True
            else:
                assert False, f"Не удалось обнаружить ошибку"
        
        logger.info("✓ Тест неудачной авторизации пройден")