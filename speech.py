import speech
import ui

v = ui.load_view('speech')
speech.say('Greetings!', 'en-GB', 0.1) 
textview = v['textview1']
switch1 = v['switch1']

def brit_switch_action(sender):
    global lang
    lang = 'en-GB' if sender.value else 'en-US'

def button_action(sender):
    global lang
    v['switch1'].action = brit_switch_action
    text = textview.text
    if text == '':
        speech.say('Please tell me something to say.', lang, 0.1) 
    else:
        speech.say(text, lang, 0.1) 

button1 = v['button1']
button1.action = button_action
v.present('sheet')
