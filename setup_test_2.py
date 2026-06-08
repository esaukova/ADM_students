from selenium import webdriver
from selenium.webdriver.chrome.options import Options


options = Options()
options.binary_location = '/usr/bin/chromium-browser' 
driver = webdriver.Chrome(options=options)

driver.get("https://adm.redsoft.test/login")
el = driver.find_element_by_class_name(" css-mn45us ")
print(el)

driver.quit()