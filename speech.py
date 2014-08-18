import speech, ui

lang = 'en-GB'

def brit_switch_action(sender):
    global lang
    lang = 'en-GB' if sender.value else 'en-US'

def button_speak_action(sender):
    text = sender.superview['user_text'].text or 'Please tell me something to say.'
    speech.say(text, lang, 0.1) 

ui.load_view('speech').present('sheet')
speech.say('Greetings!', lang, 0.1)
