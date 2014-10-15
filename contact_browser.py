import contacts
import ui

# excuse the ugly code but it works :)

class Data (ui.ListDataSource):
	def __init__(self, items=None):
		ui.ListDataSource.__init__(self, items)

	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell()
		cell.text_label.text = str(self.items[row])
		return cell

names = []
first_names = []
last_names = []
nicknames = []
people = contacts.get_all_people()
for p in people:
	names.append(p.full_name)
	first_names.append(p.first_name)
	last_names.append(p.last_name)
	nicknames.append(p.nickname)
	
def search(sender):
	query = v['search string'].text
	contacts_view = v['contactstable']
	try:
			if query in names or first_names or last_names or nicknames:
				contacts_view.data_source = Data(items=[query])
				contacts_view.reload()
			elif query == '': 
				contacts_view.data_source = Data(items=names)
				contacts_view.reload()
			else:
				contacts_view.data_source = None
				contacts_view.reload()
	except IndexError:
		pass

v = ui.load_view('contact_browser')

v['search string'].clear_button_mode = 'while_editing'

contacts_view = v['contactstable']
contacts_view.data_source = Data(items=names)

searchbut = ui.ButtonItem()
searchbut.image = ui.Image.named('ionicons-ios7-search-strong-32')
searchbut.action = search
v.right_button_items = [searchbut]

v.present('sheet')
