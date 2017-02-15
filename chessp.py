import pygame,math
from sets import Set

class Chess(object):
	def __init__(self,game,(x,y),r,img,speed,side,number):
		self.x=x
		self.y=y
		self.xx=img.get_rect().width/2
		self.yy=img.get_rect().height/2
		self.r=r
		self.img=img
		self.speed=speed
		self.side=side
		self.screen=game.screen
		self.game=game
		self.shot=False
		self.angle=None
		self.v=0
		self.colors=[(255,0,0),(0,0,255)]
		self.col_with={}
		self.number=number



	def is_out(self):
		if self.xx<-22.5:
			return True
		if self.xx>game.screen.get_rect().width+22.5:
			return True
		if self.yy<-22.5:
			return True
		if self.yy>game.screen.get_rect().hight+22.5:
			return True




	def movechess(self,t):

		if self.shot and self.angle is not None:
			t=t/10.0
			distance=self.v*t+0.5*t*t*self.game.a

			self.xxx=math.cos(self.angle)*distance
			self.yyy=math.sin(self.angle)*distance
			self.x=self.x+self.xxx
			self.y=self.y+self.yyy
			self.v=self.v+self.game.a*t

			if self.v<0:
				self.v=0
				self.shot=False	




	def draw(self):
		pygame.font.init()
		myfont = pygame.font.SysFont("Comic Sans MS", 30)
		textsurface = myfont.render(str(self.number), False, (0,0,0))
		
		

		if self.game.game_phase!="shooting1" and self.game.game_phase!="shooting2":
			if self.game.can_i_be_picked(self):
				pygame.draw.circle(self.screen,(0,255,0),(int(self.x),int(self.y)),27,6)
			if self.game.am_i_picked(self):
				pygame.draw.circle(self.screen,(0,0,255),(int(self.x),int(self.y)),27,6)

		self.screen.blit(self.img,(self.x-self.xx,self.y-self.yy))

		pygame.draw.circle(self.screen,self.colors[self.side],(int(self.x),int(self.y)),6)

		self.screen.blit(textsurface,(int(self.x-self.xx),int(self.y-self.yy)))