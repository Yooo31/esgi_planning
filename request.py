from datetime import date, timedelta
import time
import requests
import json

def getSession():
  with open('session.json') as f:
    data = json.load(f)

  payload = data['payload']
  cookies = data['cookies']

  return [payload, cookies]

def getDates() :
  today = date.today()
  dateResult = today
  weekday = today.weekday()

  while(weekday != 0) :
    dateResult -= timedelta(days=1)
    weekday = dateResult.weekday()

  return [dateResult, dateResult + timedelta(days=7)]

def convertDates(dates) :
  timestamp_list = [int(time.mktime(d.timetuple())) * 1000 for d in dates]

  return timestamp_list

def doRequest(setOfDatesConverted) :
  session = getSession()
  url = "https://myges.fr/student/planning-calendar"
  headers = {
      "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
      "accept": "application/xml, text/xml, */*; q=0.01",
      "accept-encoding": "gzip, deflate, br",
      "accept-language": "fr-FR,fr;q=0.6",
      "referer": "https://myges.fr/student/planning-calendar",
      "origin": "https://myges.fr",
      "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
      "x-requested-with": "XMLHttpRequest",
      "sec-fetch-dest": "empty",
      "sec-fetch-site": "same-origin",
      "sec-fetch-mode": "cors",
      "sec-gpc": "1",
      "sec-ch-ua": '"Chromium";v="106", "Brave Browser";v="106", "Not;A=Brand";v="99"',
      "sec-ch-ua-mobile": "?0",
      "sec-ch-ua-platform": "Linux",
      "faces-request": "partial/ajax"
  }
  payload = {
    "javax.faces.partial.ajax": "true",
    "javax.faces.source": "calendar:myschedule",
    "javax.faces.partial.execute": "calendar:myschedule",
    "javax.faces.partial.render": "calendar:myschedule",
    "calendar:myschedule": "calendar:myschedule",
    "calendar:myschedule_start": setOfDatesConverted[0],
    "calendar:myschedule_end": setOfDatesConverted[1],
    "calendar": "calendar",
    "calendar:myschedule_view": "agendaWeek",
    "javax.faces.ViewState": session[0]
  }
  cookies = {
    "JSESSIONID": session[1]
  }

  response = requests.post(url, headers=headers, data=payload, cookies=cookies)

  return response

def start():
  setOfDates = getDates()
  setOfDatesConverted = convertDates(setOfDates)
  response = doRequest(setOfDatesConverted)

  return response.text
