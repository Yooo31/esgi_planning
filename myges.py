from datetime import date, timedelta, datetime
import time
import requests
import json

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
    "javax.faces.ViewState": "-4496979502816867172:5112411270531609037"
  }
  cookies = {
    "JSESSIONID": "7535A052388A9941FE4EF371FA56C6F7"
  }

  response = requests.post(url, headers=headers, data=payload, cookies=cookies)

  return response

def convertData(allEvents):
  parsedEvents = []

  for event in allEvents :
    title, room = event[0].split('\n')

    date = event[1][:10]
    startTime = event[1][11:16]

    endTime = event[2][11:16]

    date = date[8:]+"/"+date[5:7]+"/"+date[:4]

    startTime = startTime[:2] + "h" + startTime[3:]
    endTime = endTime[:2] + "h" + endTime[3:]

    newData = [title, room, date, startTime + " - " + endTime]
    parsedEvents.append(newData)

  return parsedEvents

def redactMessage(parsedEvents) :
  message = ""

  for event in parsedEvents :
    message += "\n\n📆 " + event[2] + "\n📚 " + event[0] + "\n🏫 " + event[1] + "\n🕓 " + event[3]

  return message

def extractData(response) :
  start = response.text.index("CDATA[") + 6
  end = response.text.index("]]></update>")
  json_string = response.text[start:end]

  data = json.loads(json_string)
  events = data['events']

  allEvents = []

  for event in events:
    newEvent = []

    newEvent.append(event['title'])
    newEvent.append(event['start'])
    newEvent.append(event['end'])

    allEvents.append(newEvent)

  allEvents.sort(key=lambda x: x[1])

  parsedEvents = convertData(allEvents)
  message = redactMessage(parsedEvents)

  return message

def errorMessage(response) :
  message = "Une erreur provenant du site est survenue\n\nCODE :" +response.status_code + '\n\nVeuillez rééssayer plus tars avec la commande "!planning"'

def start() :
  setOfDates = getDates()
  setOfDatesConverted = convertDates(setOfDates)

  response = doRequest(setOfDatesConverted)
  message = extractData(response) if response.status_code == 200 else errorMessage(response)

  print(message)

