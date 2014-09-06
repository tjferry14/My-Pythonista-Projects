from collections import Counter 
import ui
	
def count_text(sender):
	counttext = v['user_text'].text
	letter = v['letter'].text
	counter = Counter(counttext)
	v['outcome'].text = ('There are %s total %s\'s') % (counter[letter], letter)

v = ui.load_view('count_text')

count_button = ui.ButtonItem()
count_button.title = 'Count'
count_button.action = count_text 
v.right_button_items = [count_button]

v.present('sheet')
