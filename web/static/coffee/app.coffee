$(document).ready(
  ()->
    console.log 'nicela!'
    source = new EventSource '/stream'
    source.onmessage = (event)->
      console.log event.data 
)
