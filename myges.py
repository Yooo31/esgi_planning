from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import os
import time
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("IDENTIFIANT")
password = os.getenv("PASSWORD")

def openMyGes() :
  print('Opening myges website')

  driver.get("https://myges.fr/student/planning-calendar")
  time.sleep(1)

def loginForm(inputType, value) :
  driver.find_element(By.ID, inputType).send_keys(os.getenv(value))

def connexion() :
  print('Connect me')
  loginForm('username', 'IDENTIFIANT')
  time.sleep(1)
  loginForm('password', 'PASSWORD')
  time.sleep(1)
  driver.find_element(By.CSS_SELECTOR, 'input.input_submit').click()


def start() :
  chrome_options = Options()

  # Options to run without interface

  # chrome_options.add_argument("--no-sandbox")
  # chrome_options.add_argument("--headless")

  # Bypass the anti bot

  chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
  chrome_options.add_experimental_option('useAutomationExtension', False)
  chrome_options.add_argument("--disable-blink-features=AutomationControlled")

  # Create the driver

  global driver
  driver = webdriver.Chrome(executable_path="./chromedriver", options=chrome_options)

  # Launch the process

  openMyGes()
  connexion()
