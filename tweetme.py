import console
import ui
import webbrowser

def tweet(sender):
	tweet_text = v['user_text']
	text = tweet_text.text.strip().replace(' ', '%20')
	if len(text) < 140:
		webbrowser.open('twitter://post?message=' + text)
	else:
		console.hud_alert('Exceeded Character Limit', 'error', 1.5)

v = ui.load_view('tweetme')

tweet_button = ui.ButtonItem()
tweet_button.image = ui.Image.named('ionicons-social-twitter-32')
tweet_button.action = tweet 
v.right_button_items = [tweet_button]

v.present('sheet')
