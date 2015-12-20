$(document).ready(
  ()->
    # first bind the jquery draggable thingy to the movable elements.
    $('.movable').draggable(
      # whenever we stop dragging, send the positions to the server
      stop: (()-> send_positions())
    )
    $('.bar').progressbar()
    # window.positions will be the same string we sent to the server
    reset_movables window.positions
    process_output window.messages
)

reset_movables = (positions) ->
  console.log positions
  if positions != null
    ind = 0
    for a in positions.split('%')
      if a != ''
        l = a.split '|'
        element = $ "\##{l[0]}"
        element.offset(top:l[1],left:l[2])




send_positions = () ->
  # select all the elements that are movable
  movable = $('.movable')
  payload = ''
  for a in [0...movable.length]
    # this is one movable jquery selector
    one_movable_object = $(movable[a])
    pos = one_movable_object.position()
    # only send the id as a payload
    payload += "#{one_movable_object[0].id}|#{pos.top}|#{pos.left}%"
  # send the position string to the server
  $.post('/positioning',payload)


is_choice = (data) ->
  return yes if data[0..5] == 'CHOICE'
  no

make_choice_form = (data) ->
  console.log window.choiceskips
  if window.choiceskips == 0
    options = data[6..].split('|')
    # console.log options
    # options = options[1..options.length-2]
    # console.log options
    form = "<form id=\"ch\" action=\"/choice\" method='post'>"
    for a in options
      # make sure the option is in fact an option
      if a != '' and a != undefined
        # add a radio button to the string
        form += "<input type=\"radio\" name='makechoice' value=\"#{data}%#{a[0]}\">#{a[1..]}<br>"
    form += "<input type=\"submit\" value=\"choose!\">"
    form += "</form>"
    # add the form to the main div
    $('#choiceholder').append(form)
  else
    window.choiceskips -= 1

is_input = (message) ->
  # console.log message[0..4]
  if message[0..4] == 'INPUT' then yes else no

make_input_form = (message) ->
  if window.choiceskips == 0
    form = "<a>#{message[5..]}</a><form id=\"ch\" action=\"/input\" method='post'>"
    form += "<input type=\"text\" name='input'><br><input type=\"submit\" value=\"choose!\"></form>"
    $('#choiceholder').append(form)
  else
    window.choiceskips -= 1

is_player_info = (message) ->
  if message[0..9] == 'PLAYERINFO' then yes else no

update_player_ui = (message) ->
  player_data = $.parseJSON(message[10..])
  console.log player_data
  $('#healthbar').html("health: #{player_data.hp}")
  $('#xpbar').html("xp: #{player_data.xp}")
  $('#playername').html("#{player_data.name}'s stats")
  $('#action_points').html("action points: #{player_data.action_points}")
  #(player_data.max_health / player_data.health)*100)

process_output = (message) ->
  for mes in message
    # console.log "#{typeof(mes)},#{mes}"
    if is_choice(mes)
      make_choice_form(mes)
    else if is_input(mes)
      make_input_form(mes)
    else if is_player_info(mes)
      update_player_ui(mes)
    else
      $('#main').append("#{mes}<br>")

fix = () ->
  alert 'dicks'
