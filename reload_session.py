from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

import json
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

def findJSessionId(cookies) :
  jsessionid_cookie = None
  for cookie in cookies:
    if cookie['name'] == 'JSESSIONID':
      jsessionid_cookie = cookie
      break

  if jsessionid_cookie is not None:
    jsessionid_value = jsessionid_cookie['value']
  else:
    print("Le cookie JSESSIONID n'a pas été trouvé.")
    jsessionid_value = None

  return jsessionid_value

def changeJsonFile(cookie, payload) :
  with open('session.json', 'r') as f:
    data = json.load(f)

  data['payload'] = payload
  data['cookies'] = cookie
  data['actual_week'] = 0

  with open('session.json', 'w') as f:
    json.dump(data, f)

def getSessionValue() :
  time.sleep(2)
  driver.get("https://myges.fr/student/planning-calendar")

  time.sleep(10)

  cookies = driver.get_cookies()
  jsessionid = findJSessionId(cookies)

  viewstate_element = driver.find_element("name", "javax.faces.ViewState")
  viewstate_value = viewstate_element.get_attribute("value")

  changeJsonFile(jsessionid, viewstate_value)

def start() :
  chrome_options = Options()

  # Options to run without interface
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--headless")

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
  getSessionValue()

  return result
