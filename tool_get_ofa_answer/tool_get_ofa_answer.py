from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup_selenium_firefox():
    ser = Service("driverbrowser/geckodriver.exe")
    firefox_options = FirefoxOptions()
    firefox_options.set_preference("media.volume_scale", "0.0")
    firefox_options.set_preference('devtools.jsonview.enabled', False)
    firefox_options.set_preference('dom.webnotifications.enabled', False)
    firefox_options.add_argument("--test-type")
    firefox_options.add_argument('--ignore-certificate-errors')
    firefox_options.add_argument('--disable-extensions')
    firefox_options.add_argument('disable-infobars')
    firefox_options.add_argument("--incognito")
    # firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(service=ser, options=firefox_options)
    return driver


def get_ofa_answer(driver, question, dir_image):
    start = time.time()
    send_question = driver.find_element(By.CSS_SELECTOR, value=".input-text")
    send_question.send_keys(question)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.upload')))
    send_image = driver.find_element(By.CSS_SELECTOR, value=""".upload""")
    image = dir_image.replace("/", "\\")
    send_image.click()
    time.sleep(1)
    os.system("auto_send_images.exe {0}".format(image))
    submit_button = driver.find_element(By.XPATH, value="/html/body/div/div/div/div[1]/div/div[1]/div[1]/div[2]/button[2]")
    submit_button.click()
    driver.find_element(By.CSS_SELECTOR, value=".input-text").clear()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.duration')))
    result = driver.find_element(By.CSS_SELECTOR, value=".output-text")
    print(result.text)
    print(time.time() - start)
    driver.find_element(By.XPATH, value="""/html/body/div/div/div/div[1]/div/div[1]/div[1]/div[1]/div[1]/div[2]/div/div/button[2]""").click()
    return result.text




driver = setup_selenium_firefox()
driver.get("https://hf.space/embed/OFA-Sys/OFA-vqa/+")
get_ofa_answer(driver, "what color is skirt", "E:/test_shopee_ver3/shopee/shopee/Váy/image/000f0dd3c08cee5f8c4b4e8a79aaa8b2/1.jpg")
get_ofa_answer(driver, "what color is shirt", "E:/test_shopee_ver3/shopee/shopee/Váy/image/000f0dd3c08cee5f8c4b4e8a79aaa8b2/2.jpg")
driver.close()