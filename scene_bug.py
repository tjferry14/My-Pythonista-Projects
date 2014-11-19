from scene import *
from random import *
from sound import *
from math import sin
import ui

class MyScene(Scene):
	def setup(self):
		self.root_layer = Layer(self.bounds)
		self.org = Rect(self.bounds.x + 8, self.bounds.y + 8, self.bounds.w - 16, self.bounds.h - 16)
		self.splat = splat()
		self.splash = splash()
		pos = Point(*offset)

class SelectACharacterView(ui.View):
	def __init__(self):
		self.background_color = 'white'
		self.border_width = 0.4
		self.border_color = (0.8, 0.8, 0.8)
		self.add_subview(self.make_header())
		half = len(characters) / 2
		for i, character in enumerate(characters):
			x = 40 + i % half * 155
			y = 160 if i < half else 365
			self.add_subview(self.make_button(x, y, character))

	@classmethod
	def make_header(cls):
		header = ui.Label(frame = (40, 19.5, 700, 116.5))
		header.text_color = (0.00, 0.50, 0.00)
		header.text = 'Select A Character'
		header.font = ('AvenirNext-Heavy', 50)
		return header

	@classmethod
	def character_tapped(cls, sender):
		global game_character
		game_character = sender.name
		play_game(sender)
		sender.superview.close()

	@classmethod
	def make_button(cls, x, y, image_name = 'Frog_Face'):
		img = ui.Image.named(image_name).with_rendering_mode(ui.RENDERING_MODE_ORIGINAL)
		button = ui.Button(name=image_name, frame=(x, y, 128, 128), image=img)
		button.action=cls.character_tapped
		return button

def change_character(sender):
	SelectACharacterView().present(style='sheet', hide_title_bar=True)
	
def play_game(sender):
	root_view.add_subview(scene_view)

root_view = ui.load_view('hopper') # menu
root_view.background_color = (0.00, 0.50, 0.00)
root_view.present(orientations=['landscape'], hide_title_bar=True)
scene_view = SceneView(frame=root_view.frame)
scene_view.flex = 'WH'
scene_view.scene = MyScene()
