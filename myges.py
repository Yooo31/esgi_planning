import request as Request

import datetime
import json

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

    newData = [title, room, date, startTime + " - " + endTime, event[3]]
    parsedEvents.append(newData)

  return parsedEvents

def concatenatePlanning(events) :
  finalEvents = []
  while len(events) != 1 :
    nameMatch = events[0][0] == events[1][0]
    classMatch = events[0][1] == events[1][1]
    dateMatch = events[0][2] == events[1][2]
    firstSchedule = events[0][3].split(" - ")
    secondSchedule = events[1][3].split(" - ")

    firstMinutes = datetime.datetime.strptime(firstSchedule[1], "%Hh%M").time()
    firstMinutesMore15 = datetime.datetime.combine(datetime.date.today(), firstMinutes) + datetime.timedelta(minutes=15)
    isScheduleMatch15 =  firstMinutesMore15.strftime("%Hh%M") == secondSchedule[0]
    firstMinutesMore60 = datetime.datetime.combine(datetime.date.today(), firstMinutes) + datetime.timedelta(minutes=60)
    isScheduleMatch60 =  firstMinutesMore60.strftime("%Hh%M") == secondSchedule[0]

    if nameMatch and classMatch and dateMatch :
      if isScheduleMatch15 or isScheduleMatch60 :
        finalSchedule = firstSchedule[0] + " - " + secondSchedule[1]
        events[0][3] = finalSchedule
        del events[1]
    else :
      finalEvents.append(events[0])
      del events[0]

  finalEvents.append(events[0])
  del events[0]

  return finalEvents

def redactMessage(parsedEvents) :
  message = ""
  concatenatedEvents = concatenatePlanning(parsedEvents)

  for event in concatenatedEvents :
    courseId = event[4]
    detailedCourse = Request.getDetailedValue(courseId)

    event[0] = detailedCourse[0]
    teacher = detailedCourse[1]
    message += "\n\n📆 " + event[2] + "\n📚 " + event[0] + "\n🏫 " + event[1] + "\n🎓 " + teacher + "\n🕓 " + event[3]

  return message

def extractData(response) :
  start = response.find('<update id="calendar:myschedule"><![CDATA[')
  end = response.find(']]></update>', start)
  extracted = response[start:end].replace('<update id="calendar:myschedule"><![CDATA[', '')

  data = json.loads(extracted)
  events = data['events']

  allEvents = []

  for event in events:
    newEvent = []

    newEvent.append(event['title'])
    newEvent.append(event['start'])
    newEvent.append(event['end'])
    newEvent.append(event['id'])

    allEvents.append(newEvent)

  allEvents.sort(key=lambda x: x[1])

  parsedEvents = convertData(allEvents)
  message = redactMessage(parsedEvents)

  return message

def errorMessage(response) :
  message = "Une erreur provenant du site est survenue\n\nCODE :" +response.status_code + '\n\nVeuillez rééssayer plus tars avec la commande "!planning"'

  return message

def start(response) :
  message = extractData(response)

  return message
