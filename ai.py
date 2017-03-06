import pygame,pygame.sprite,util,math

class Ai(object):
	def __init__(self,game,(x,y),imagedata,speed,con,is_pos_OK,side):
		self.con=con
		self.imagedata=imagedata
		image1=pygame.image.load(imagedata[0])
		image2=pygame.image.load(imagedata[1])
		
		self.x=x
		self.y=y
		self.screen=game.screen
		self.sp=speed
		self.display=(image1,image2)
		self.pick=False
		self.counter=0

		self.xx,self.yy=image1.get_rect().center
		#print (str(self.xx)+"   "+str(self.yy))
		self.game=game
		self.picked=None
		self.is_pos_OK=is_pos_OK
		self.pickdelay=pygame.time.get_ticks()
		self.angle=0
		self.debugtext=""
		self.br=98
		self.shootable=None
		self.shoot=False
		self.linelengh=0
		self.side=side
		self.moves=0







	def update(self,final_pos):
			stop=True
			newx=self.x

			newy=self.y

			x=int(final_pos[0]-(self.display[0].get_rect().width/2))
			y=int(final_pos[1]-(self.display[1].get_rect().height/2))

			#print(final_pos[0]-(self.display[0].get_rect().width/2),final_pos[1]-(self.display[1].get_rect().height/2),newx,newy)
			#import pdb;pdb.set_trace()

			if newy>y and (newy-y)>self.sp:
				newy=self.y-self.sp
				stop=False


			elif newy<y and (y-newy)>self.sp:
				newy=self.y+self.sp
				stop=False

			if newx>x and (newx-x)>self.sp:
				newx=self.x-self.sp
				stop=False

			elif newx<x and (x-newx)>self.sp:
				newx=self.x+self.sp
				stop=False


			if self.is_pos_OK(newx,newy) :
				self.x=newx
				self.y=newy
				if stop:
					if self.find_shootingangle(self.game.shooter) is None:
						self.spin()
					else:
						self.handle_shooting()
					

				
				

			if self.picked is not None:
				self.picked.x=self.x+self.xx
				self.picked.y=self.y+self.yy



	def spin(self):
		self.angle+=10
	def draw(self):
		image1=self.display[self.pick]

		image=self.rot_center(image1,self.angle)
		#image=pygame.transform.rotate(image1,self.angle)
		self.debugtext=str(image.get_rect().width)+str(image.get_rect().height)

		self.screen.blit(image,(self.x,self.y))

		self.helping_lines()


	def can_pick(self,x,y):
		if util.distance((x,y),(self.x+self.xx,self.y+self.yy)) < 15:
			return True

		else:
			return False


	def rot_center(self,image,angle):
		orig_rect = image.get_rect() 
		rot_image = pygame.transform.rotate(image, angle) 
		rot_rect = orig_rect.copy() 
		rot_rect.center = rot_image.get_rect().center 
		rot_image = rot_image.subsurface(rot_rect).copy() 
		return rot_image

	def handle_picking(self,key_down):
			if key_down==self.con["pick"] and pygame.time.get_ticks()-self.pickdelay>250:
				self.pickdelay = pygame.time.get_ticks()
				
				if self.picked is None:
					

					self.picked = self.game.chess_below_hand(self)
					#import pdb;pdb.set_trace()

				else:
					print(self.picked)
					collided=False
					for c in self.game.chesses:
						if 0<util.distance((self.picked.x,self.picked.y),(c.x,c.y))<45:
							
							
							collided=True
					if collided:
						#effect = pygame.mixer.Sound('beep.wav')
						#effect.play()
						print("bip")
					else:

							self.picked=None
							self.moves=self.moves-1
							if self.game.game_phase=="picking1":
								self.game.game_phase="picking2"
								self.pick=True
							else:
								self.game.game_phase="picking1"
								self.pick=True

					
				
			else:
				self.pick=False

	def can_shoot(self,chess):
		if self.side!=chess.side:
			
			return False

		if 30 < util.distance((chess.x,chess.y),(self.x+self.xx,self.y+self.yy)) < 90 :
			#self.shootable==True
			#import pdb;pdb.set_trace()
			return True
			
		else:
			#self.shootable==False
			
			return False
			


	def handle_shooting(self):
			
			self.shoot=True
			self.pick=True
				


	
	def drawshootline(self,chess):
		pygame.draw.line(self.screen,(100,150,20),(self.xx+self.x,self.y+self.yy),(chess.x,chess.y),2)
		self.linelengh=util.distance((self.xx+self.x,self.y+self.yy),(chess.x,chess.y))
		
	def find_shootingangle(self,chess):
		shootingangle=math.atan2(chess.y-(self.y+self.yy),chess.x-(self.x+self.xx))
		if shootingangle <0:

			shootingangle=shootingangle%(math.pi*2) 

		#print(shootingangle/(2*math.pi)*360+self.angle)
		
		upslice=self.angle*(-2*math.pi)/360+0.1+self.con["added_degree"]
		downslice=self.angle*(-2*math.pi)/360+(math.pi*2-1)+self.con["added_degree"]
		if downslice>2*math.pi:

			downslice=downslice%(math.pi*2)
		elif downslice<0:
			downslice=downslice%(math.pi*2)
		if upslice>2*math.pi:

			upslice=upslice%(math.pi*2)
		elif upslice<0:
			upslice=upslice%(math.pi*2)

		if upslice<=math.pi/2 and downslice>=math.pi*3/2:

			if upslice > shootingangle > 0 or 2*math.pi>shootingangle>downslice:

				return shootingangle
			else:
				return None
		elif upslice> shootingangle > downslice:
		
		
			return shootingangle
		else:
			

			return None

	def find_slice(self,x,y):
		pass
	def helping_lines(self):
		pygame.draw.line(self.screen,(255,0,0),(self.x,0),(self.x,300))
		pygame.draw.line(self.screen,(255,0,0),(0,self.y),(500,self.y))
		pygame.draw.line(self.screen,(255,255,0),(self.x+self.xx,0),(self.x+self.xx,300))
		pygame.draw.line(self.screen,(255,255,0),(0,self.y+self.yy),(500,self.y+self.yy))
		pygame.draw.circle(self.screen,(0,0,255),(self.x+self.xx,self.y+self.yy),90,2)
		pygame.draw.circle(self.screen,(0,255,0),(self.x+self.xx,self.y+self.yy),30,2)

		self.xxx=math.cos(self.angle*(-2*math.pi)/360+0.1+self.con["added_degree"])*self.br
		self.yyy=math.sin(self.angle*(-2*math.pi)/360+0.1+self.con["added_degree"])*self.br
		self.xxx=self.xxx+self.x+self.xx
		self.yyy=self.yyy+self.y+self.yy
		
		pygame.draw.line(self.screen,(100,30,20),(self.xx+self.x,self.y+self.yy),(int(self.xxx),int(self.yyy)),2)

		self.xxx=math.cos(self.angle*(-2*math.pi)/360-1+self.con["added_degree"])*self.br
		self.yyy=math.sin(self.angle*(-2*math.pi)/360-1+self.con["added_degree"])*self.br
		self.xxx=self.xxx+self.x+self.xx
		self.yyy=self.yyy+self.y+self.yy
		
		pygame.draw.line(self.screen,(100,150,20),(self.xx+self.x,self.y+self.yy),(int(self.xxx),int(self.yyy)),2)

	def __setattr__(self,k,v):
		if k=="angle":
			if v>360:
				v=v%360
			elif v<0:
				v=v%360

		super(Ai, self).__setattr__(k,v)


class Attr_Test(object):
	def __init__(self):
		self.a=2


	def __getattr__(self,k):

		if k=="b":
			return 7

	def __setattr__(self,k,value):

		if k=="b":
			self.a=value+1
		else:
			super(Attr_Test, self).__setattr__(k,value)

x=Attr_Test()



