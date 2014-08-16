import speech, ui

lang = 'en-GB'
speech.say('Greetings', lang, 0.1)

def brit_switch_action(sender):
    global lang
    lang = 'en-GB' if sender.value else 'en-US'

def button_action(sender):
    text = sender.superview['textview1'].text or 'Please tell me something to say.'
    speech.say(text, lang, 0.1) 

v = ui.load_view('speech')
# you can put the next two lines in the .pyui file instead
v['switch1'].action = brit_switch_action
v['button1'].action = button_action
v.present('sheet')
