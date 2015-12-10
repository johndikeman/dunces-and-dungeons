$(document).ready(
  ()->
    console.log 'nicela!'
    source = new EventSource '/stream'
    source.onmessage = (event)->
      $('#main').append event.data
      # if make_choice was called
      if event.data[0..5] == 'CHOICE'
        console.log "CREATING A FORM"
        make_form(event)
        # choices should be divided with a |
)

make_form = (event) ->
  options = event.data[6..].split '|'
  form = "<form id=\"ch\" action=\"/choice\">"
  for a in options
    form += "<input type=\"radio\">#{a}<br>"
  form += "<input type=\"submit\" value=\"choose!\">"
  form += "</form>"
  $('#main').append(form)
