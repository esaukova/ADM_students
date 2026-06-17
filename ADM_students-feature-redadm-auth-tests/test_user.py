import pytest
import logging
import time
from config import ADMIN_LOGIN, ADMIN_PASSWORD
from login_page import LoginPage
from user_page import UserPage

logger = logging.getLogger(__name__)


class TestREDADMLogin:

    @pytest.mark.positive
    def test_successful_create(self, driver, base_url):
        
        login_page = LoginPage(driver)
        user_page = UserPage(driver)
        login_page.open(base_url)
        login_page.login(ADMIN_LOGIN, ADMIN_PASSWORD)

        user_page.open("https://adm.redsoft.test/directory/objectTypeExplorer/user")
        user_page.create("atu1", "autotestuser1", "Qwerty.36")
        time.sleep(3)
        user_page.redact("atu1")
        time.sleep(3)
        user_page.delete()
        time.sleep(3)