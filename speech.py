import speech, ui

lang = 'en-GB'
speech.say('Greetings', lang, 0.1)

def brit_switch_action(sender):
    global lang
    lang = 'en-GB' if sender.value else 'en-US'

def button_speak_action(sender):
    text = sender.superview['user_text'].text or 'Please tell me something to say.'
    speech.say(text, lang, 0.1) 

v = ui.load_view('speech')
# I have put the next two lines in the .pyui file instead
#v['brit_switch'].action = brit_switch_action
#v['button_speak'].action = button_speak_action
v.present('sheet')
