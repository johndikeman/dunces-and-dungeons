



$(document).ready(
  ()->
    console.log "new print #{window.messages}"
    process_output(window.messages)
    # console.log 'nicela!'
    source = new EventSource '/stream'
    source.onmessage = (event)->
      # $('#main').append event.data
      # if make_choice was called
      if is_choice(event.data)
        make_choice_form(event)
        # choices should be divided with a |
      else
        # only process output if nobody else has done anything with it
        # process_output takes a list only
        document.location.reload yes
)

is_choice = (data) ->
  return yes if data[0..5] == 'CHOICE'
  no

make_choice_form = (event) ->
  options = event.data[6..].split('|')
  # console.log options
  # options = options[1..options.length-2]
  # console.log options
  form = "<form id=\"ch\" action=\"/choice\" method='post'>"
  for a in options
    # make sure the option is in fact an option
    if a != '' and a != undefined
      # add a radio button to the string
      form += "<input type=\"radio\" name='makechoice' value=\"#{a[0]}\">#{a[1..]}<br>"
  form += "<input type=\"submit\" value=\"choose!\">"
  form += "</form>"
  # add the form to the main div
  $('#choiceholder').append(form)

process_output = (message) ->
  for mes in message
    if not is_choice(mes)
      $('#main').append("#{mes}<br>")
