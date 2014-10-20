import speech
import ui
import clipboard
import console

lang = 'en-GB'
speed = 0.1

def table_action(sender):
	global lang
	selected_lang = sender.items[sender.selected_row]['title']
	if selected_lang == 'American': lang = 'en-US'
	if selected_lang == 'British': lang = 'en-GB'
	if selected_lang == 'Italian': lang = 'it-IT'
	if selected_lang == 'Spanish': lang = 'es-MX'
	if selected_lang == 'Australian': lang = 'en-AU'
	if selected_lang == 'Japanese': lang = 'ja-JP'
	if selected_lang == 'German': lang = 'de-DE'
	else:
		pass

def slider_action(sender):
	global speed
	speed = v['slider1'].value

def button_speak_action(sender):
	global speed
	text = v['user_text'].text
	if text == 'Enter your text here':
		text = 'Please tell me something to say.'
	speech.say(text, lang, speed)
	
def copy_action(sender):
	text = v['user_text'].text
	if text == 'Enter your text here':
		console.hud_alert('No text entered to copy.', 'error', 1.0)
	else:
		clipboard.set(text)
		console.hud_alert('Copied', 'success', 1.0)
		
def paste_action(sender):
	text = clipboard.get()
	console.hud_alert('Pasted', 'success', 1.0)
	v['user_text'].text = text

v = ui.load_view('speech')

speak = ui.ButtonItem()
speak.image = ui.Image.named('ionicons-ios7-volume-high-32')
speak.action = button_speak_action

copy = ui.ButtonItem()
copy.image = ui.Image.named('ionicons-ios7-copy-32')
copy.action = copy_action

paste = ui.ButtonItem()
paste.image = ui.Image.named('ionicons-clipboard-32')
paste.action = paste_action

speech.say('Greetings.', lang, 0.1)
v['languages'].scroll_enabled = False
v.right_button_items = [speak, copy, paste]
v.present(orientations=['landscape'])
