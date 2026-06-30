import os
import pytest
from selenium import webdriver
from login_page import LoginPage


LOGIN = "Administrator"


@pytest.fixture
def driver():
    """Инициализация браузера перед тестом и закрытие после теста"""

    driver = webdriver.Chrome()
    driver.implicitly_wait(0)
    yield driver
    driver.quit()


@pytest.mark.positive
def test_success_login(driver):
    """Позитивный тест: успешная авторизация пользователя Administrator"""

    # Получение пароля из переменной окружения
    password = os.getenv("REDADM_PASSWORD")

    if not password:
        raise Exception("Переменная окружения REDADM_PASSWORD не задана")
    
    # Создание объекта страницы авторизации
    login_page = LoginPage(driver)

    login_page.open()
    login_page.login(LOGIN, password)

    # Ожидание появления имени пользователя после входа
    admin_name = login_page.get_logged_in_user()

    # Проверка отображения имени пользователя на странице
    assert admin_name.is_displayed(), "Имя пользователя Administrator не отображается после входа"
