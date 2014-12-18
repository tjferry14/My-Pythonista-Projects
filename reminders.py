# coding: utf-8
import dialogs
import reminders
import ui

v = ui.load_view('reminders')
reminders_table = v['reminders']

def picked(sender):
	item = sender.items[sender.selected_row]
	r = item['reminder']
	r.completed = True
	r.save()
	del sender.items[sender.selected_row]

def grabbed():
	global todo_items, completed_items
	todo = reminders.get_reminders(completed=False)
	todo_items = [{'title': r.title, 'reminder': r} for r in todo]
	done = reminders.get_reminders(completed=True)
	completed_items = [{'title': r.title, 'reminder': r} for r in done]
	reminders_table.data_source = ui.ListDataSource(items=todo_items)
	reminders_table.data_source.action = picked
	reminders_table.reload()

def button_action(sender):
	if segment.selected_index == 0:
		reminders_table.data_source = ui.ListDataSource(items=todo_items)
		reminders_table.data_source.action = picked
		reminders_table.reload()
	elif segment.selected_index == 1:
		reminders_table.data_source = ui.ListDataSource(items=completed_items)
		reminders_table.data_source.action = picked
		reminders_table.reload()

@ui.in_background
def but_action(sender):
	fields = [{'key' : 'name', 'type' : 'text', 'value' : 'Name your reminder'},]
	result=dialogs.form_dialog(title='Create a Reminder', fields=fields)
	r = reminders.Reminder()
	r.title = result['name']
	r.save()
	segment.selected_index = 0
	grabbed()

segment = v['segmentedcontrol1']
segment.action = button_action
reminders_table.data_source.action = picked
create_button = ui.ButtonItem()
create_button.image = ui.Image.named('ionicons-ios7-plus-empty-32')
create_button.action = but_action
grabbed()
v.right_button_items = [create_button]
v.present('sheet')
