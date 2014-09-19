from os import listdir, getcwd
from editor import open_file
from console import hud_alert
import ui

def table_data():
	dir_items = listdir(getcwd())
	lst = ui.ListDataSource(dir_items)
	tv1 = v['file-table']
	tv1.data_source = lst
	tv1.reload()
	
def select(sender):
	v.close()
	#open_file("~/Notepad" + [sender.selected_row])
	print (sender, sender.selected_row, sender.items)
	
def make_file():
	global file_name, created_file
	with open(file_name, 'w') as out_file:
			out_file.write(created_file)
	table_data()
	hud_alert('File successfully created!', 'success', 1.0)

def check(sender):
	global file_name, created_file
	file_name = v['namefield'].text + '.txt'
	if file_name == '.txt':
		file_name = 'Untitled' + '.txt'
	else: 
		pass
	created_file = v['textview1'].text
	if created_file == '':
		hud_alert('No text entered.', 'error', 1.0)
	else:	
		make_file()

v = ui.load_view('notepad')
table_data()
v.present('full_screen')
