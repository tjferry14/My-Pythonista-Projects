import speech
import ui
		
v = ui.load_view('speech')
speech.say('Greetings!', 'en-US', 0.1) 
textfield = v['textfield1']
textfield.clear_button_mode = 'while_editing'

def button_action(sender):
    text = textfield.text
    if text == '':
        speech.say('Please tell me something to say.', 'en-US', 0.1) # speaks out the text
    else:
        speech.say(text, 'en-US', 0.1) # speaks out the text

button1 = v['button1']
button1.action = button_action
v.present('sheet')
