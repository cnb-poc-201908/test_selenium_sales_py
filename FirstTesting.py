from selenium import webdriver
from time import sleep
import os

print("anakin test begin...")
driver = webdriver.Remote(
command_executor='http://10.244.2.34:5555/wd/hub',
desired_capabilities={'browserName': 'chrome'}
)
print("after remote webdriver")
driver.get('https://www.bing.com')

print("title is " + driver.title)

sleep(1)

print(os.getcwd())

driver.quit()
print("test end...")

