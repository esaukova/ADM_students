import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)


# РЕГИСТРАЦИЯ ОПЦИЙ КОМАНДНОЙ СТРОКИ
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
        default="https://adm.redsoft.test/login",
        help="Базовый URL для тестирования"
    )


# ФИКСТУРА КОНФИГУРАЦИИ
@pytest.fixture(scope="session")
def config(request):
    return {
        'headless': request.config.getoption("--headless"),
        'base_url': request.config.getoption("--base-url")
    }


# ОСНОВНАЯ ФИКСТУРА ДРАЙВЕРА
@pytest.fixture(scope="function")
def driver(config):
    headless = config['headless']

    chrome_options = ChromeOptions()
    chrome_options.accept_insecure_certs = True
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-insecure-localhost')
    
    chrome_options.add_argument('--lang=ru')
    
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    # Headless режим (если включен)
    if headless:
        chrome_options.add_argument('--headless=new')
        # Дополнительные опции для headless режима
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-software-rasterizer')

    try:
        # Используем webdriver-manager для автоматической установки chromedriver
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )
    except Exception as e:
        logger.error(f"Ошибка при инициализации Chromium через webdriver-manager: {e}")
        # Пробуем без webdriver-manager (если chromedriver уже установлен)
        driver = webdriver.Chrome(options=chrome_options)

    # Устанавливаем неявное ожидание
    driver.implicitly_wait(10)
    
    # Максимизируем окно
    driver.maximize_window()

    yield driver

    # Закрываем браузер после теста
    driver.quit()


# ФИКСТУРА ДЛЯ БАЗОВОГО URL
@pytest.fixture(scope="function")
def base_url(config):
    return config['base_url']


# РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЬСКИХ МАРКЕРОВ (для устранения предупреждений)
def pytest_configure(config):
    config.addinivalue_line("markers", "positive: маркер для позитивных тестов")
    config.addinivalue_line("markers", "negative: маркер для негативных тестов")