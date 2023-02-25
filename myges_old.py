from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

import os
import time
from dotenv import load_dotenv


load_dotenv()
user = os.getenv("IDENTIFIANT")
password = os.getenv("PASSWORD")
result = []

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

def goToCalendar() :
  time.sleep(2)
  driver.get("https://myges.fr/student/planning-calendar")

  time.sleep(10)
  # logs = driver.get_log("performance")
  # print(logs)
  log_types = driver.execute_script("return console.getTypes();")
  print(log_types)




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
  s = Service('./chromedriver')
  driver = webdriver.Chrome(service=s, options=chrome_options)

  # Launch the process

  openMyGes()
  connexion()
  goToCalendar()

  return result

start()

