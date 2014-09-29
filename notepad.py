# coding: utf-8
from os import listdir, getcwd
from editor import open_file
from console import hud_alert
import ui

# opening files does not work yet

def set_actions(self):
	# method 2: traversing all subviews
		for subview in self.subviews:
			if isinstance(subview, ui.TextField):
				subview.delegate = self

def textfield_did_change(self, textfield):
		query = v['searchbox'].text
		tv1 = v['file-table']
		try:
			if query in dir_items:
				tv1.data_source = ui.ListDataSource([query])
				tv1.reload()
			elif query == '': 
				tv1.data_source = ui.ListDataSource(listdir(getcwd()))
				tv1.reload()
			else:
				tv1.data_source = None
				tv1.reload()
		except IndexError:
			pass


def search_files(sender):
		query = v['searchbox'].text
		tv1 = v['file-table']
		try:
			if query in dir_items:
				tv1.data_source = ui.ListDataSource([query])
				tv1.reload()
			elif query == '': 
				tv1.data_source = ui.ListDataSource(listdir(getcwd()))
				tv1.reload()
			else:
				tv1.data_source = None
				tv1.reload()
		except IndexError:
			pass

def table_data():
	global dir_items # for search
	dir_items = listdir(getcwd())
	lst = ui.ListDataSource(dir_items)
	tv1 = v['file-table']
	tv1.data_source = lst
	tv1.reload()
	
def select(sender):
	v.close()
	#open_file("~/Notepad" + [sender.selected_row])
	print(sender, sender.selected_row, sender.items)
	
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

create = ui.ButtonItem()
create.image = ui.Image.named('ionicons-compose-32')
create.action = check
v.right_button_items = [create]

table_data()
v['searchbox'].action = search_files
v['searchbox'].clear_button_mode = 'while_editing'
v.present('full_screen')
