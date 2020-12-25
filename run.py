import json
import time
import os

from dotenv import load_dotenv
from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# EMAIL, PASSWORD は .env に書く
load_dotenv(verbose=True)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
login_id = os.environ.get("EMAIL")
login_pw = os.environ.get("PASSWORD")

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory": os.path.dirname(__file__)} # this does not work currently
chromeOptions.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)
driver.get('https://anchor.fm/dashboard/episodes')


def login():

    driver.find_element_by_xpath('//*[@class="css-125l5nm jsOutboundLink"]').click()

    wait_time = 30
    login_id_xpath = '//*[@id="identifierNext"]'
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, login_id_xpath)))
    driver.find_element_by_name("identifier").send_keys(login_id)
    driver.find_element_by_xpath(login_id_xpath).click()

    login_pw_xpath = '//*[@id="passwordNext"]'
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, login_pw_xpath)))
    driver.find_element_by_name("password").send_keys(login_pw)
    time.sleep(1) 
    driver.find_element_by_xpath(login_pw_xpath).click()
    time.sleep(10)
    driver.find_element_by_xpath('//*[@class="LinkStyles__link___qLgH7"]').click()

def find_episodes():
    li_elements = driver.find_elements_by_xpath(
        '//*[@id="app-content"]/div/div/div/div[2]/ul/li')
    links = [x.find_element_by_tag_name(
        'a').get_attribute('href') for x in li_elements]
    print(f"{len(li_elements)} episodes found.")
    return links


def download_stats(link):
    driver.get(link)
    time.sleep(10)
    driver.find_element_by_xpath(
        '//*[@id="app-content"]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div').click()
    time.sleep(0.5)
    driver.find_element_by_xpath(
        '//*[@id="app-content"]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div[6]/div').click()
    time.sleep(0.5)
    driver.find_element_by_xpath(
        '//*[@id="app-content"]/div/div/div/div[3]/div[1]/div/div/div/div/div/div').click()
    time.sleep(0.5)
    driver.find_element_by_xpath(
        '//*[@id="app-content"]/div/div/div/div[3]/div[1]/div/div/div/div[2]/div/div/div[1]/div/div').click()
    time.sleep(0.5)
    driver.find_element_by_xpath(
        '//*[@id="app-content"]/div/div/div/div[3]/div[3]/div/div/div/a').click()
    time.sleep(5)


login()
time.sleep(10)
links = find_episodes()
print(links)
for l in links:
    download_stats(l)
