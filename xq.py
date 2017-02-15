import pygame
import hand,chessp,math,util
from sets import Set
def deg(num):
    return(num/(2*math.pi)*360)




class Xiangqi():
    def collide(self,c1,c2):
            if c1 is c2:
                return False

            if 0<util.distance((c1.x,c1.y),(c2.x,c2.y))<45:
                
                return True
            else:
                return False

    def initboard(self,screen):

        # Create empty pygame surface.
        background = pygame.Surface(screen.get_size())
        # Fill the background white color.
        background.fill((255, 255, 255))
        # Convert Surface object to make blitting faster.
        self.background = background.convert()
        # Copy background to screen (position (0, 0) is upper left corner).
        screen.blit(self.background, (0,0))

        self.chesspic=pygame.image.load("xqz.png")

        handimg={"white":("handcenter2.png","handcenter.png"),"black":("hand2center.png","hand2center2.png")}
        handcon1={"up":pygame.K_w,"down":pygame.K_s,"left":pygame.K_a,"right":pygame.K_d,"pick":pygame.K_SPACE,"counter_c":pygame.K_g,"clock":pygame.K_h,"added_degree":-2.2}
        handcon2={"up":pygame.K_UP,"down":pygame.K_DOWN,"left":pygame.K_LEFT,"right":pygame.K_RIGHT,"pick":pygame.K_RETURN,"counter_c":pygame.K_COMMA,"clock":pygame.K_PERIOD,"added_degree":0}

        self.hands=hand.Hand(self,(400,120),handimg["white"],5,handcon1,self.posOK1,0)
        self.handt=hand.Hand(self,(900,20),handimg["black"],5,handcon2,self.posOK2,1)
        self.allhand=[self.hands,self.handt]
        self.chesses=[]

        self.game_phase="picking1"  
        self.a=-0.25
        self.font=pygame.font.Font(None,30)
        for s in range(0,2):
            for i in range(0,12):
                self.chesses.append(chessp.Chess(self,(s*1450+20,100+i*50),5,self.chesspic,5,s,i))

        self.testpos=[(1220, 200,840, 172,1175,100),(200,100,300,250,-80,-80),(200,200,300,300,250,260)]
        
    def is_pick(self):
        return self.game_phase == "picking1" or self.game_phase == "picking2"


            
    def can_i_be_shot(self,hand):
        lines=0
        inrange=[]
        for c in self.chesses:

                if hand.can_shoot(c):
                    hand.drawshootline(c)
                    c.angle=hand.find_shootingangle(c)
                        #print(c.angle)
                    if c.angle!=None:
                        

                        inrange.append(c)
        if hand.shoot and inrange:
            closer=inrange[0]
            closerdis=0
            for cc in inrange:
                if (hand.angle-cc.angle)*(hand.angle-cc.angle)>closerdis:
                    closer=cc
                    closerdis=(hand.angle-cc.angle)*(hand.angle-cc.angle)
                    #print((hand.angle-cc.angle)*(hand.angle-cc.angle),closerdis)

            hand.drawshootline(closer)
            closer.v=int(1/hand.linelengh*800)

            closer.shot=True
            print("shoot hand chess",hand.x,hand.y,closer.x,closer.y,hand,self.game_phase)

            if self.game_phase=="shooting1":

                self.game_phase="shooting2"
            elif self.game_phase=="shooting2":

                self.game_phase="shooting1"
                #import pdb;pdb.set_trace()
            inrange=[]
            return "hah"

    def can_i_be_picked(self,chess):
        if self.hands.can_pick(chess.x,chess.y):
            return True
        
        elif self.handt.can_pick(chess.x,chess.y):
            return True
        else:
            return False
    def am_i_picked(self,chess):
        for hand in self.allhand:
            if hand.picked is chess:
                return True
        return False
    def chess_below_hand(self,hand):
        for chess in self.chesses:
            if hand.can_pick(chess.x,chess.y):
                return chess

    def posOK1(self,x,y):
        if self.game_phase=="shooting1":
            return True
        return x<self.screen.get_rect().width/2-45
    def posOK2(self,x,y):
        if self.game_phase=="shooting2":
            return True
        return x>self.screen.get_rect().width/2+45

    def display_score(self):

        lab=self.font.render(self.game_phase,1,(0,0,0))
        self.screen.blit(lab,(self.screen.get_rect().width/2,0))

    def bounce(self,c1,c2):
        #print("c1 cordinante",c1.x,c1.y,c1.angle,c1.v,"c2 cordinate",c2.x,c2.y,c2.angle,c2.v)
        #import pdb;pdb.set_trace()


        try:
                x=math.cos(c1.angle)
                y=math.sin(c1.angle)
        except:
            import pdb;pdb.set_trace()
        k1=y/x
        x2=c1.x-c2.x+0.0
        y2=c1.y-c2.y+0.0
        if x2==0:
            if c1.angle>math.pi/2*3:
                c1.angle=c1.angle-(math.pi*2)
            the_angle=(math.pi/2)-c1.angle
        else:
            k2=y2/x2
            the_angle=-math.atan((k1-k2)/(1+k1*k2)) 
        xx=math.cos(c1.angle+the_angle)
        yy=math.sin(c1.angle+the_angle)
        newc2angle=the_angle+c1.angle

        if the_angle<0:
            newc1angle=c1.angle+((math.pi/2)+the_angle)
        else:
            newc1angle=c1.angle-((math.pi/2)-the_angle)
        newc1x=math.cos(newc1angle)
        newc1y=math.sin(newc1angle)
        
        pygame.draw.line(self.screen,(100,150,20),(c1.x,c1.y),(c2.x,c2.y),2)
        pygame.draw.line(self.screen,(200,100,50),(c1.x,c1.y),(c1.x+x*100,c1.y+y*100),3)
        #pygame.draw.line(self.screen,(0,10,100),(c1.x,c1.y),(c1.x+xx*100,c1.y+yy*100),3)
        pygame.draw.line(self.screen,(0,10,100),(c1.x,c1.y),(c1.x+newc1x*100,c1.y+newc1y*100),5)
        c2.v=c1.v*math.cos(the_angle)
        c1.v=c1.v*math.sin(the_angle)
        #print(c1.v,c2.v)
        c1.angle=newc1angle
        c2.angle=newc2angle
        c1.shot=True
        c2.shot=True
        #import pdb;pdb.set_trace()
        if util.distance((c1.x,c1.y),(c2.x,c2.y))<45:
            #import pdb;pdb.set_trace()
            shiftx=46*math.cos(c2.angle)
            shifty=46*math.sin(c2.angle)
            c2.x=c1.x+shiftx
            c2.y=c1.y+shifty
            #print("The chesses that are too close should be seperated",c1.number,c2.number)
            
            #import pdb;pdb.set_trace()
        c1.col_with[c2]=5
        c2.col_with[c1]=5
        #print(c1.number,c2.number,"c1 cordinante",c1.x,c1.y,c1.angle,c1.v,"c2 cordinate",c2.x,c2.y,c2.angle,c2.v)
        #print("------------------------------------------------------------------")
        return(the_angle/(2*math.pi)*360,newc1angle/(2*math.pi)*360,newc2angle/(2*math.pi)*360)

    def forget_bounced(self):

        for c in self.chesses:
            toremove=[]
            for cc,b in c.col_with.iteritems():
                b=b-1
                if b==0:
                    toremove.append(cc)
                else:
                      c.col_with[cc]=b
            for cc in toremove:
                del c.col_with[cc]

        #import pdb;pdb.set_trace()

    def find_collide(self):
        for c in self.chesses:
            if c in self.calledc:
                continue
            for cc in self.chesses:
                if cc in self.calledc:
                    continue
                if self.collide(c,cc):
                    self.calledc.add(c)
                    self.calledc.add(cc)
                    
                    return c,cc
        #import pdb;pdb.set_trace()
        return None


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
        """
        c1=self.chesses[9]
        c2=self.chesses[10]
        c1.x,c1.y,c2.x,c2.y,self.handt.x,self.handt.y=self.testpos[0]
        """
        
        self.hands.x,self.hands.y=-80,-80
        while mainloop:

            screen.blit(self.background, (0,0))
            # Do not go faster than this framerate.
            milliseconds = clock.tick(FPS) 
            playtime += milliseconds / 1000.0 



            for event in pygame.event.get():
                # User presses QUIT-button.
                if event.type == pygame.QUIT:
                    mainloop = False 
                elif event.type == pygame.KEYDOWN:
                    # User presses ESCAPE-Key
                    if event.key == pygame.K_ESCAPE:
                        mainloop = False
                    key_down=event.key
                    if event.key == pygame.K_F1:
                        self.game_phase="shooting1"


                elif event.type == pygame.KEYUP:
                    key_down=None

            # Print framerate and playtime in titlebar.
            text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)+"hello world   "+str(self.handt.debugtext)
            pygame.display.set_caption(text)            
            
            if self.game_phase=="picking1" or self.game_phase=="shooting1":
                self.hands.update(key_down)
            if self.game_phase=="picking2" or self.game_phase=="shooting2":
                self.handt.update(key_down)

            self.hands.draw()
            self.handt.draw()

            self.forget_bounced()
            if self.game_phase=="shooting1":
                self.can_i_be_shot(self.hands)

            elif self.game_phase=="shooting2":
                self.can_i_be_shot(self.handt)

            
            for c in range(10):
                for i in self.chesses:
                    i.movechess(milliseconds/10.0)
                self.calledc=Set()

                if self.game_phase=="shooting2" or self.game_phase=="shooting1":
                        printed = False
                        
                        self.tocollide=self.find_collide()
                        while self.tocollide is not None:
                            #print(tocollide[0].number,self.tocollide[1].number)
                            if self.tocollide[0].v>self.tocollide[1].v:
                                self.bounce(self.tocollide[0],self.tocollide[1])
                            else:
                                self.bounce(self.tocollide[1],self.tocollide[0])
                            self.tocollide=self.find_collide()




            for i in self.chesses:
             #   i.movechess(milliseconds)

                i.draw()
            self.display_score()

            if self.handt.moves==0 and self.hands.moves==0 and self.game_phase=="picking1":

                self.game_phase="shooting1"

            
            pygame.display.flip()

        # Finish Pygame.  
        pygame.quit()

        # At the very last:
        print("This game was played for {0:.2f} seconds".format(playtime))

game=Xiangqi()

game.playgame()

