from datetime import date, timedelta
import time
import requests
import json

def getSession():
  with open('session.json') as f:
    data = json.load(f)

  payload = data['payload']
  cookies = data['cookies']
  actual_week = data['actual_week']

  return [payload, cookies, actual_week]

def getDates(count) :
  delta = count + 1
  today = date.today()
  dateResult = today
  weekday = today.weekday()

  while(weekday != 0) :
    dateResult -= timedelta(days=1)
    weekday = dateResult.weekday()

  return [dateResult + timedelta(days=7*count), dateResult + timedelta(days=7*delta)]

def convertDates(dates) :
  timestamp_list = [int(time.mktime(d.timetuple())) * 1000 for d in dates]
  print(timestamp_list)

  return timestamp_list

def changeJsonFile(actual_week) :
  with open('session.json', 'r') as f:
    data = json.load(f)

  data['actual_week'] = actual_week

  with open('session.json', 'w') as f:
    json.dump(data, f)

def doRequest(setOfDatesConverted, count) :
  session = getSession()
  url = "https://myges.fr/student/planning-calendar"
  headers = {
      "cache-control": "no-cache, no-store, must-revalidate",
      "pragma": "no-cache",
      "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
      "accept": "application/xml, text/xml, */*; q=0.01",
      "accept-encoding": "gzip, deflate, br",
      "accept-language": "fr-FR,fr;q=0.6",
      "referer": "https://myges.fr/student/planning-calendar",
      "origin": "https://myges.fr",
      "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
      "x-requested-with": "XMLHttpRequest",
      "sec-fetch-dest": "empty",
      "sec-fetch-site": "same-origin",
      "sec-fetch-mode": "cors",
      "sec-gpc": "1",
      "sec-ch-ua": '"Not_A Brand";v="99", "Brave";v="109", "Chromium";v="109"',
      "sec-ch-ua-mobile": "?0",
      "sec-ch-ua-platform": "Linux",
      "faces-request": "partial/ajax"
  }

  nextWeek = {
    "javax.faces.partial.ajax": "true",
    "javax.faces.source": "calendar:nextMonth",
    "javax.faces.partial.execute": "@all",
    "javax.faces.partial.render": "calendar:myschedule calendar:currentDate calendar:currentWeek calendar:campuses calendar:lastUpdate",
    "calendar:nextMonth": "calendar:nextMonth",
    "calendar": "calendar",
    "calendar:myschedule_view": "agendaWeek",
    'javax.faces.ViewState': session[0]
  }

  previousWeek = {
      "javax.faces.partial.ajax": "true",
      "javax.faces.source": "calendar:previousMonth",
      "javax.faces.partial.execute": "@all",
      "javax.faces.partial.render": "calendar:myschedule calendar:currentDate calendar:currentWeek calendar:campuses calendar:lastUpdate",
      "calendar:previousMonth": "calendar:previousMonth",
      "calendar": "calendar",
      "calendar:myschedule_view": "agendaWeek",
      'javax.faces.ViewState': session[0]
  }

  getSchedule = {
      'javax.faces.partial.ajax': 'true',
      'calendar:myschedule': 'calendar:myschedule_start calendar:myschedule_end',
      'javax.faces.source': 'calendar:myschedule',
      'javax.faces.partial.execute': 'calendar:myschedule',
      'javax.faces.partial.render': 'calendar:myschedule',
      'calendar:myschedule_start': setOfDatesConverted[0],
      'calendar:myschedule_end': setOfDatesConverted[1],
      'calendar': 'calendar',
      'calendar:myschedule_view': 'agendaWeek',
      'javax.faces.ViewState': session[0]
  }

  cookies = {
    "JSESSIONID": session[1]
  }
  print(count, session[2])
  if count < session[2] :
    for i in range(count, session[2]) :
      print("Back to " + str(i) + " weeks")
      requests.post(url, headers=headers, data=previousWeek, cookies=cookies)
  elif count > session[2] :
    for i in range(session[2], count) :
      print("Next to " + str(i) + " weeks")
      requests.post(url, headers=headers, data=nextWeek, cookies=cookies)

  changeJsonFile(count)
  response = requests.post(url, headers=headers, data=getSchedule, cookies=cookies)

  return response

def start(count):
  count = int(count)
  setOfDates = getDates(count)
  setOfDatesConverted = convertDates(setOfDates)
  response = doRequest(setOfDatesConverted, count)

  return response.text
