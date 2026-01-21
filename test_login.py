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
        """Тест успешной авторизации с правильными учетными данными"""
        logger.info("Запуск теста: Успешная авторизация в RED ADM")

        try:
            login_page = LoginPage(driver)

            # Открываем страницу логина
            logger.info(f"Открываем страницу логина: {base_url}")
            login_page.open(base_url)

            # Упрощенная проверка загрузки страницы
            assert "login" in driver.current_url.lower() or driver.current_url == base_url, \
                f"Не загрузилась страница логина. URL: {driver.current_url}"

            logger.info(f"Страница логина загружена. Заголовок: '{driver.title}'")
            driver.save_screenshot("screenshot_before_login.png")

            # Выполняем вход
            logger.info(f"Пытаемся войти с логином: {ADMIN_LOGIN}")
            login_page.login(ADMIN_LOGIN, ADMIN_PASSWORD)

            # Даем время для обработки
            time.sleep(3)

            # Проверяем успешность входа
            dashboard_page = DashboardPage(driver)

            # Проверяем, что мы покинули страницу логина
            assert "login" not in driver.current_url.lower(), \
                "Остались на странице логина после ввода правильных данных"

            # Проверяем наличие элемента дашборда
            assert dashboard_page.verify_login_success(), \
                "Вход не выполнен успешно - не удалось найти подтверждение"

            driver.save_screenshot("screenshot_after_successful_login.png")
            logger.info("✓ Тест успешной авторизации пройден")

        except Exception as e:
            logger.error(f"Ошибка в тесте успешной авторизации: {e}")
            driver.save_screenshot("error_successful_login.png")
            raise

    @pytest.mark.negative
    @pytest.mark.parametrize("username,password", [
        ("wrong_user", ADMIN_PASSWORD),
        (ADMIN_LOGIN, "wrong_password"),
        ("", ""),
    ])
    def test_failed_login(self, driver, base_url, username, password):
        """Тест неудачной авторизации с неправильными учетными данными"""
        logger.info(f"Запуск теста: Неудачная авторизация - {username}/{password}")

        try:
            login_page = LoginPage(driver)
            login_page.open(base_url)

            login_page.login(username, password)
            time.sleep(2)

            error_displayed = login_page.is_element_visible(login_page.ERROR_MESSAGE, timeout=5)

            driver.save_screenshot(f"screenshot_failed_login_{username}.png")

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

        except Exception as e:
            logger.error(f"Ошибка в тесте неудачной авторизации: {e}")
            driver.save_screenshot("error_failed_login.png")
            raise