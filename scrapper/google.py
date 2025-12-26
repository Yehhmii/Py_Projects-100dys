from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import lxml
import requests
import random

google_form = "https://docs.google.com/forms/d/e/1FAIpQLSfp2CHmt6tlUIElQpU9IJkc33Adbomauh5sUK1y1nEeKI-AQg/formResponse"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

# for n in range(0, 2):
driver.get(google_form)
time.sleep(5)

btn_next = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div/div[1]/div/span/span').click()
time.sleep(5)

# def select_random_dropdown():
dropdown = driver.find_element(By.CLASS_NAME, "e2CuFe.eU809d").click()
options = dropdown.find_elements(By.TAG_NAME, "div")
options[random.randint(1, len(options)-1)].click()

# Click on the dropdown to reveal options
dropdown_elements = driver.find_elements(By.CLASS_NAME, "MocG8c.HZ3kWc.mhLiyf.OIC90c.LMgvRb")
for dropdown in dropdown_elements:
    dropdown.click()
    time.sleep(1)
    # select_random_dropdown()
    time.sleep(1)
