from datetime import date, timedelta
import time
import requests

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
    "javax.faces.ViewState": "5924194908406122877:1760918383373028995"
  }
  cookies = {
    "JSESSIONID": "2F474BCD53CF04BA2D34595EE85D154B"
  }

  response = requests.post(url, headers=headers, data=payload, cookies=cookies)

  return response

def start():
  setOfDates = getDates()
  setOfDatesConverted = convertDates(setOfDates)
  response = doRequest(setOfDatesConverted)

  return response