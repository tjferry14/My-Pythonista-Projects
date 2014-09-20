from collections import Counter
from console import hud_alert
import ui

def check(sender):
	counttext = v['user_text'].text
	letter = v['letter'].text
	if letter == '':
		hud_alert('Please enter a letter or number to count.', 'error', 1.0)
	else: 
		count_text()	
	
def count_text():
	counttext = v['user_text'].text
	letter = v['letter'].text
	counter = Counter(counttext)
	hud_alert(('There are %s total %s\'s') % (counter[letter], letter), 'success', 3)

v = ui.load_view('count_text')

count_button = ui.ButtonItem()
count_button.title = 'Count'
count_button.action = check 
v.right_button_items = [count_button]

v.present('sheet')
