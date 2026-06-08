from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = '/usr/bin/chromium-browser' 

driver = webdriver.Chrome(options=options)

driver.get("https://ya.ru")
print(driver.title)


driver.quit()