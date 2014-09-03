import ui
import webbrowser

# for some reason, this wont work with spaces in the text, need to
# figure this out

def tweet(sender):
	text = v['user_text'].text
	# text.replace(' ', '%20') # tried this but doesnt work
	webbrowser.open('twitter://post?message=' + text)

v = ui.load_view('tweetme')

tweet_button = ui.ButtonItem()
tweet_button.image = ui.Image.named('ionicons-social-twitter-32')
tweet_button.action = tweet 
v.right_button_items = [tweet_button]

v.present('sheet')
