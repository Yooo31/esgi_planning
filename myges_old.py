from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
  delay = 10 # seconds
  try:
      myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'calendar')))
      isClass()
  except TimeoutException:
      print("Loading took too much time!")
      driver.close()

def isClass() :
  try:
    classes = driver.find_element(By.CLASS_NAME, 'reservation-TOULOUSE')
    if classes:
      print("Y a cours")
      checkClass()
  except:
    print("Y a pas cours")
    result = "Pas de cours :)"

def checkClass() :
  classesCount = driver.find_elements(By.CLASS_NAME, 'reservation-TOULOUSE')
  lastElement = classesCount[-1]
  classesCount.append(lastElement)

  for i in classesCount :
    i.click()
    element = driver.find_element(By.ID, "dlg1").text
    result.append(element)
    time.sleep(3)

  result.pop(0)
  return result


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
  driver = webdriver.Chrome(executable_path="./chromedriver", options=chrome_options)

  # Launch the process

  openMyGes()
  connexion()
  goToCalendar()

  return result


