def getSessionValidity(response) :
  status = response.find('<update id="calendar:myschedule">')

  return status
