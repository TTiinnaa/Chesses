import pygame
class Button(object):
	
	def __init__(self, file_name,game,(x,y),call):
		super(Button, self).__init__()
		self.screen=game.screen
		self.pic=pygame.image.load(file_name)
		self.x,self.y=self.pos=(x-(self.pic.get_rect().width/2),y-(self.pic.get_rect().height/2))
		
		self.call=call
		self.game=game
		self.game.buttons.append(self)
	def display(self):

		self.screen.blit(self.pic, self.pos)

	def on_click(self,mouse_pos):
		#print (mouse_pos)
		x=mouse_pos[0]
		y=mouse_pos[1]
		if (self.x<x<(self.x+self.pic.get_rect().width)) and (self.y<y<(self.y+self.pic.get_rect().height)):
			self.call()
			try:
				self.game.buttonstoremove.append(self)
			except:
				pass





