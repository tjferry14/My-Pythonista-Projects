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

def create_note(sender):
	namefile = v['namefield'].text + '.txt'
	txtfile = v['textview1'].text
	with open(namefile, 'w') as out_file:
			out_file.write(txtfile)
	table_data()
	hud_alert('File successfully created!', 'success', 1.0)

v = ui.load_view('notepad')
table_data()
v.present('full_screen')
