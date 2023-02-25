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

    newData = [title, room, date, startTime + " - " + endTime]
    parsedEvents.append(newData)

  return parsedEvents

def redactMessage(parsedEvents) :
  message = ""

  for event in parsedEvents :
    message += "\n\n📆 " + event[2] + "\n📚 " + event[0] + "\n🏫 " + event[1] + "\n🕓 " + event[3]

  return message

def extractData(response) :
  start = response.find('<update id="calendar:myschedule">')
  end = response.find('</update>', start) + len('</update>')
  extracted = response[start:end]

  data = json.loads(extracted)
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

  return message

def start(response) :
  message = extractData(response)

  return message
