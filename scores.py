import random
import ui
		
def get_score(sender):
	v['home_score'].text = str(random.randint(0, 15))
	v['opponents_score'].text = str(random.randint(0,15))
		
v = ui.load_view('scores')
v.present('sheet')
