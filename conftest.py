import pytest
import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запуск в headless режиме"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="http://0.0.0.0:8000/login",  # ИЗМЕНЕНО на ваш URL
        help="Базовый URL для тестирования"
    )


@pytest.fixture(scope="session")
def config(request):
    return {
        'headless': request.config.getoption("--headless"),
        'base_url': request.config.getoption("--base-url")
    }


@pytest.fixture(scope="function")
def driver(config):
    headless = config['headless']

    firefox_options = FirefoxOptions()

    # Локализация для русского языка
    firefox_options.set_preference('intl.accept_languages', 'ru')

    # Отключение автоматизации detection
    firefox_options.set_preference('dom.webdriver.enabled', False)
    firefox_options.set_preference('useAutomationExtension', False)

    if headless:
        firefox_options.add_argument('--headless')

    try:
        # Используем webdriver-manager для автоматической установки geckodriver
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=firefox_options
        )
    except Exception as e:
        logger.error(f"Ошибка при инициализации Firefox через webdriver-manager: {e}")
        # Пробуем без webdriver-manager
        driver = webdriver.Firefox(options=firefox_options)

    driver.maximize_window()
    driver.implicitly_wait(10)

    yield driver

    driver.quit()


@pytest.fixture(scope="function")
def base_url(config):
    return config['base_url']