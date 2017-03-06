import pygame,button,xqq

class Start():
	    def initboard(self,screen):

        		# Create empty pygame surface.
        		background = pygame.image.load("menu.jpg")
        		# Fill the background white color.
        		
        		# Convert Surface object to make blitting faster.
        		self.background = background.convert()
        		# Copy background to screen (position (0, 0) is upper left corner).
        		screen.blit(self.background, (0,0))
        		self.buttons=[]

        		self.buttons.append(button.Button("start.png",self,(706+34.5,181+119),self.to_xqq))

        		print("hi")
	    def to_xqq(self):
	    	print("ahhha")
	    	xqq.game.playgame()

        		
	    def playgame(self):
	        # Initialize Pygame.
	        pygame.init()
	        # Set size of pygame window.
	        self.screen=screen=pygame.display.set_mode((1500,800))
	        self.initboard(screen)
	        clock = pygame.time.Clock()

	        mainloop = True
	        # Desired framerate in frames per second. Try out other values.              
	        FPS = 30
	        # How many seconds the "game" is played.
	        playtime = 0.0
	        key_down=None

	        while mainloop:

	            screen.blit(self.background, (0,0))
	            # Do not go faster than this framerate.
	            milliseconds = clock.tick(FPS) 
	            playtime += milliseconds / 1000.0 



	            for event in pygame.event.get():
	                # User presses QUIT-button.
	                if event.type == pygame.QUIT:
	                    mainloop = False 




	                if pygame.mouse.get_pressed() == (1,0,0):
	                	for b in self.buttons:

	                		b.on_click(pygame.mouse.get_pos())

            		for b in self.buttons:
                		b.display()


            		pygame.display.flip()

        	pygame.quit()
Start().playgame()

    	