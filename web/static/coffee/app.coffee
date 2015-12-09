$(document).ready(
  ()->
    console.log 'nicela!'
    source = new EventSource '/stream'
    source.onmessage = (event)->
      $('#main').append event.data
      # if make_choice was called
      if event.data[0..5] == 'CHOICE'
        console.log "CREATING A FORM"
        # choices should be divided with a |
        options = event.data[6..].split '|'
        form = "<form id=\"ch\" action=\"/choice\">"
        for a in options
          form += "<input type=\"radio\">#{a}</input>"
        form += "</form>"
        $('#main').append(form)
)
