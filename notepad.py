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

def create_file(sender):
	file_name = v['namefield'].text + '.txt'
	created_file = v['textview1'].text
	with open(file_name, 'w') as out_file:
			out_file.write(created_file)
	table_data()
	hud_alert('File successfully created!', 'success', 1.0)

v = ui.load_view('notepad')
table_data()
v.present('full_screen')
