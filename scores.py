import random
import ui
	
def get_score(sender):
	global home_score, away_score
	home_score = random.randint(0, 15)
	away_score = random.randint(0, 15)
	v['home_score'].text = str(home_score)
	v['opponents_score'].text = str(away_score)
	add_label()

def add_label():
	global home_score, away_score
	v['outcome'].font = ('DINCondensed-Bold', 25)
	if home_score == away_score: 
		v['outcome'].text = 'It\'s A Tie!'
		v['outcome'].text_color = 'black'
	if home_score > away_score:
		v['outcome'].text = 'Home wins!'
		v['outcome'].text_color = '#1D76C8'
	if away_score > home_score:
		v['outcome'].text = 'Away wins!'
		v['outcome'].text_color = '#DB1F1F'
	else:
		pass
	
v = ui.load_view('scores')
v.present('sheet')
