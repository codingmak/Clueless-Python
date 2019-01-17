import random, pygame, sys, time, socket,logging,os,re

from ClueClient import ClueClientGame

from pygame.locals import *

import random

from thread import start_new_thread
import struct

FPS = 15

CanStart = False
gameover = False
winner = ""


STATE_WAITING = 0
STATE_MOVING = 1
STATE_SUGGESTING = 2

STATE = STATE_WAITING
TURN = 0


LocalPID = -1
CurrentPID = -1

#screen size is 1000 x 1000

WINDOWWIDTH = 1000
WINDOWHEIGHT = 1000


roomscalex = WINDOWWIDTH/5
roomscaley = WINDOWHEIGHT/5

# Color	   R	G	B
ORANGE	= (255, 165,  0)
WHITE	 = (255, 255, 255)
BLACK	 = (  0,   0,   0)
RED	   = (255,   0,   0)
YELLOW = (255, 255,	0)
PURPLE = (128, 0, 128)
BLUE	  = (0,	 0,	255)
GREEN	 = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK


ROOMS_LIST = []


s = socket.socket()

def loadandscale(path, w, h):
	img = pygame.image.load(path)
	scaledimg = pygame.transform.scale(img, (w, h))
	return scaledimg



#All the Images
teamimg = loadandscale('teamlogo.png',roomscalex, roomscaley)
#Room
ballimg = loadandscale('ballroom.png',roomscalex, roomscaley)
kitchenimg = loadandscale('kitchen.png',roomscalex, roomscaley)
studyimg = loadandscale('study.png',roomscalex, roomscaley)
loungeimg = loadandscale('lounge.png',roomscalex, roomscaley)
libraryimg = loadandscale('library.png',roomscalex, roomscaley)
hallimg = loadandscale('hall.png',roomscalex, roomscaley)
billardsimg = loadandscale('billiards_room.png',roomscalex, roomscaley)
conservatoryimg = loadandscale('conservatory.png',roomscalex, roomscaley)
diningimg = loadandscale('dining_room.png',roomscalex, roomscaley)
horiz = loadandscale('hallway_horizontal.png',roomscalex, roomscaley)
verti = loadandscale('hallway_vertical.png',roomscalex, roomscaley)

#Players

Blueimg = loadandscale('Blue.png', roomscalex, roomscaley+10)
Redimg = loadandscale('Red.png', roomscalex, roomscaley+10)
Greenimg = loadandscale('Green.png', roomscalex, roomscaley+10)
Purpleimg = loadandscale('Purple.png', roomscalex, roomscaley+10)
Whiteimg = loadandscale('White.png', roomscalex, roomscaley+10)
Yellowimg = loadandscale('Yellow.png', roomscalex, roomscaley+10)


#Weapons


Candleimg = loadandscale('CandleStick.png',roomscalex, roomscaley)
Revolverimg = loadandscale('Revolver.png',roomscalex, roomscaley)
Ropesimg = loadandscale('kitchen.png',roomscalex, roomscaley)
Leadimg = loadandscale('study.png',roomscalex, roomscaley)
Knifeimg = loadandscale('lounge.png',roomscalex, roomscaley)
Wrenchimg = loadandscale('library.png',roomscalex, roomscaley)


class Player:
#added 2 more parameters id and connection
	def __init__(self, pid, x, y, imgpath):
		#Player.count = Player.count + 1
		#self.id = Player.count;
		# Assign the corresponding connection 
		#self.connection = connection;
		# Set the player waiting status to True
		self.sock = None
		self.pid = pid
		self.is_waiting = True;
		if (imgpath):
			self.sprite = loadandscale(imgpath, roomscalex/3, roomscaley/2)
		self.x = x
		self.y = y
		self.color = "Unknown"
		self.hexcolor = (0, 0, 0)
		self.skipturns = 0

	def draw(self, room, index):
		DISPLAYSURF.blit(self.sprite, (room.tile_x*roomscalex + index*(roomscalex/7), room.tile_y*roomscaley))

	def set_pid(self,pid):
		self.pid = pid;


  

   # def list_of_rooms():




#####################################

bgimg = pygame.image.load('clue.png')


def game_over():
	print 'adf'


def drawPressKeyMsg():
	ST_FADEIN = 0
	ST_FADEOUT = 1

	state = ST_FADEIN
	last_state_change = time.time()

	

	pressKeySurf = BASICFONT.render('Press any key to play or ESC to quit', True, RED)
	pressKeyRect = pressKeySurf.get_rect()
	pressKeyRect.topleft = (WINDOWWIDTH - 480, WINDOWHEIGHT - 30)
	DISPLAYSURF.fill(BGCOLOR, pressKeyRect)

	DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
	if len(pygame.event.get(QUIT)) > 0:
		terminate()
	keyUpEvents = pygame.event.get(KEYUP)
	if len(keyUpEvents) == 0:
		return None
	if keyUpEvents[0].key == K_ESCAPE:
		terminate()
	return keyUpEvents[0].key


def showStartScreen():
	titleFont = pygame.font.Font('freesansbold.ttf', 100)
	#titleSurf2 = titleFont.render('CLUE', True, WHITE)
	scaledimg1 = pygame.transform.scale(bgimg,(WINDOWWIDTH,WINDOWHEIGHT))
	scaledimg2 = pygame.transform.scale(teamimg,(100,100))
		
	
	degrees1 = 0
	degrees2 = 0
	while True:
		DISPLAYSURF.fill(BGCOLOR)
		DISPLAYSURF.blit(scaledimg1, (0, 0))
		w,h = scaledimg2.get_size()
		DISPLAYSURF.blit(scaledimg2, (WINDOWWIDTH - w, 0))
	   # rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
		#rotatedRect2 = rotatedSurf2.get_rect()
		#rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
	   # DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)
		
		drawPressKeyMsg()
		if checkForKeyPress():
			pygame.event.get() # clear event queue
			return
		pygame.display.update()
		FPSCLOCK.tick(FPS)


def terminate():
	s.shutdown(socket.SHUT_RDWR)
	s.close()
	pygame.quit()
	sys.exit()






#Slecting for characters
def Lobby():

	global LocalPID
	global CanStart

   #implement the start button here.
		

	myfont = pygame.font.SysFont('Comic Sans MS', 40)

	label_title = myfont.render("Lobby",False,ORANGE)
	textRect = label_title.get_rect()

	label_start = myfont.render("START",False,ORANGE)
	if LocalPID != 0:
		label_start = myfont.render("[Waiting for host]",False,ORANGE)

	startRect = label_start.get_rect()

	textRect.centerx = DISPLAYSURF.get_rect().centerx	   


	label_red = myfont.render("Red",False,(255,0,0))



	label_blue =  myfont.render("Blue",False,(0,0,255))
	label_green =  myfont.render("Green",False,(0,255,0))
	label_white = myfont.render("White",False,(0,0,0))
	label_yellow =  myfont.render("Yellow",False,(255,255,0))
	label_purple = myfont.render("Purple",False,(128,0,128))


	


	while True:

		DISPLAYSURF.fill(BGCOLOR)


		DISPLAYSURF.blit(label_title, textRect)

		#DISPLAYSURF.blit(label_red, textRect)
#
		DISPLAYSURF.blit(Redimg, (roomscalex * 0.25 , roomscaley * 1.25))

		DISPLAYSURF.blit(Blueimg, (roomscalex*0.5, roomscaley*2))


		DISPLAYSURF.blit(Yellowimg,(roomscalex*1, roomscaley * 2.5))


		DISPLAYSURF.blit(Purpleimg, (roomscalex*1.5, roomscaley * 3))


		DISPLAYSURF.blit(Whiteimg, (roomscalex*2, roomscaley * 3.5))


		DISPLAYSURF.blit(Greenimg, (roomscalex*2.5, roomscaley* 4))

		DISPLAYSURF.fill(GREEN, startRect)
		DISPLAYSURF.blit(label_start, startRect)

		x,y = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminate()
			elif event.type == MOUSEBUTTONDOWN:
				if LocalPID == 0 and startRect.collidepoint(x, y):
					print "START!"
					s.sendall("[START]")

		if checkForKeyPress() or CanStart:
			pygame.event.get() # clear event queue
			return
		pygame.display.update()
		FPSCLOCK.tick(FPS)


   # NextScreen()



	
class Rooms():

	#DISPLAYSURF.blit(studyimg, (0, 0))
	#creates a room instance

	def __init__(self,tile_x,tile_y, name,imgpath,color,ishallway=False):
		self.PLAYER_LIST = []
		self.img = loadandscale(imgpath, roomscalex, roomscaley)
		#which room the player is in.
		self.tile_x = tile_x
		self.tile_y = tile_y

		self.name=name
		self.color=color
		self.ishallway = ishallway
		ROOMS_LIST.append(self)

	def PlayerCount(self):
		return self.PLAYER_LIST.__len__()
   
	def AddPlayer(self,player):
		if (self.ishallway and (self.PlayerCount() > 0)):


			return False
		else:
			#Remove player from any room it was in before
			for rem in ROOMS_LIST:
				if player in rem.PLAYER_LIST:
					rem.RemovePlayer(player)
			self.PLAYER_LIST.append(player)

			return True

	def RemovePlayer(self,player):
		if (player in self.PLAYER_LIST):
			self.PLAYER_LIST.remove(player)

	def RoomLocation(self,x,y):
		lx = self.x
		ly = self.y 
		return lx,ly


	def InsideRoom(self, x, y):
		rx = self.tile_x * roomscalex
		ry = self.tile_y * roomscaley

	  
		if (x >= rx and y >= ry and x <= rx + self.img.get_width() and y <= ry + self.img.get_height()):
			
			return True

	  
		return False

  #  def CheckPlayer(self,player):
	  #  if(player in self.PLAYER_LIST and player in ROOMS_LIST):


	def draw(self):
		myfont = pygame.font.SysFont('Comic Sans MS', 20,True)

		label_title = myfont.render(self.name,False,self.color)
		textRect = label_title.get_rect()

		DISPLAYSURF.blit(self.img,(self.tile_x * roomscalex , self.tile_y * roomscaley))

		for i, p in enumerate(self.PLAYER_LIST):
			p.draw(self, i)

		DISPLAYSURF.blit(label_title,((self.tile_x * roomscalex) + (roomscalex/2 - textRect.width/2), (self.tile_y * roomscaley) + roomscaley - textRect.height))



studyroom = Rooms(0,0,"STUDY ROOM", 'study.png',BLACK) 
kitchenroom = Rooms(4,4,"KITCHEN", 'kitchen.png', BLACK)
ballroom =  Rooms(2,4,"BALL ROOM", 'ballroom.png', BLACK) 
loungeroom = Rooms(4,0,"LOUNGE", 'lounge.png',BLACK) 
libraryroom = Rooms(0,2,"LIBRARY", 'library.png',BLACK)
hallroom	= Rooms(2,0,"HALL", 'hall.png',BLACK) 
billiardroom   = Rooms(2,2,"BILLIARDS", 'billiards_room.png',BLACK) 
conservatoryroom   = Rooms(0,4,"CONSERVATORY", 'conservatory.png',BLACK) 
diningroom	   = Rooms(4,2,"DINING", 'study.png',BLACK) 

_1x_horizroom = Rooms(1,0," ", 'hallway_horizontal.png',BLUE, True) 
_1x2y_horizroom = Rooms(1,2," ", 'hallway_horizontal.png',BLUE, True)
_3x_horizroom = Rooms(3,0," ", 'hallway_horizontal.png',BLUE, True) 
_3x2y_horizroom = Rooms(3,2," ", 'hallway_horizontal.png',BLUE, True) 
_1x4y_horizroom = Rooms(1,4," ", 'hallway_horizontal.png',BLUE, True) 
_3x4y_horizroom = Rooms(3,4," ", 'hallway_horizontal.png',BLUE, True)  

_0x1y_vertroom = Rooms(0,1," ", 'hallway_vertical.png',BLUE, True)
_2x1y_vertroom = Rooms(2,1," ", 'hallway_vertical.png',BLUE, True)
_4x1y_vertroom = Rooms(4,1," ", 'hallway_vertical.png',BLUE, True)
_0x3y_vertroom = Rooms(0,3," ", 'hallway_vertical.png',BLUE, True)
_4x3y_vertroom = Rooms(4,3," ", 'hallway_vertical.png',BLUE, True)
_2x3y_vertroom = Rooms(2,3," ", 'hallway_vertical.png',BLUE, True)

Purple = Player(-1, 0, 0, 'Purple.png')
Purple.color = "Purple"
Purple.hexcolor = Purple

Blue = Player(-1, 0, 0, 'Blue.png') 
Blue.color = "Blue" 
Blue.hexcolor = Blue

Green = Player(-1, 0, 0, 'Green.png')
Green.color = "Green"
Green.hexcolor = Green

Red = Player(-1, 0, 0, 'Red.png')
Red.color = "Red"
Red.hexcolor = Red

White = Player(-1, 0, 0, 'White.png')
White.color = "White"
White.hexcolor = White

Yellow = Player(-1, 0, 0, 'Yellow.png')
Yellow.color = "Yellow"
Yellow.hexcolor = Yellow

listofplayers = [Purple,Blue,Green,Red,White,Yellow]


def move(x, y, player):
	#print "move() " + str(player.pid)
   
	for radd in ROOMS_LIST:
		#If mouse is inside room
		if radd.InsideRoom(x, y):
		
			
	
		  
			if (radd.AddPlayer(player)):
				
				break



#remove player from list
#hallroom.RemovePlayer(Purple)
#should not appear again
#conservatoryroom.AddPlayer(Purple)





#################################################################################################


def SocketThread():
  
	global LocalPID, CurrentPID, CanStart, gameover, winner
	#global pid



	while True:

		header = s.recv(8)





		#print(header)
		packetsize, pid = struct.unpack('!ii', header)
		#print "Packet size: " + str(packetsize)
		data = s.recv(packetsize)
		print(data)
		#print "Message from PID: " + str(pid)

		if "START" in data:
			print "Server is starting the game"
			CanStart = True

		elif "PID" in data:
			LocalPID = pid
			print "LocalPID: " + str(LocalPID)
	 
		elif "NEW" in data:
			for p in listofplayers:
				if p.color in data:
					#p.set_pid(pid)
					p.pid = pid
					color = str(p.color)
					if p.color == "Purple":
						_0x1y_vertroom.AddPlayer(p)
					  
					if p.color == "Yellow":
						_0x3y_vertroom.AddPlayer(p)
					  
					if p.color == "Blue":
						_2x1y_vertroom.AddPlayer(p)
					  
					if p.color == "Green":
						_1x4y_horizroom.AddPlayer(p)
					  
					if p.color == "Red":
						
						_1x2y_horizroom.AddPlayer(p)
					if p.color == "White":
					  
						_3x4y_horizroom.AddPlayer(p)
					
		elif "MOV" in data:
			#global pid
			#holds all the pids

			print "From PID: " + str(pid)

			x, y = struct.unpack('!ii', data[6:])
			print "Move: [" + str(x) + "," + str(y) + "]"
			print "Searching for PID: " + str(pid)
			for player in listofplayers:
				print "LIST OF ALL THE PLAYER IN THE PLAYER_LIST: " + str(player.pid)
				print "This is the color:" + player.color

				if player.pid == -1:
					print "PID: Not connected"
				else:
					print "PID: " + str(player.pid)

				#something is wrong here
				if player.pid == pid:
					print("matched pid")
					print 'Moving: ' + str(player.pid) + " color: " + player.color
					move(x, y, player)
					print("Moved function used")
					#player.tile_x = x
					#player.tile_y = y
					#CURRENT_PLAYER.x???????
					#NOT UPDATING THE MOVE LOCATION OF THE SUGGESTED PLAYER
					break



		


		elif "TRN" in data:
		
			print "This is TRN data coming in : " + data
			CurrentPID = pid

		elif "WIN" in data:
			for p in listofplayers:
				if p.color in data:
					print "WINNER: " + str(p.color)
					gameover = True
					winner = p.color
					s.close()
					break

 
def runGame():
	#This should be 600 x 600
	#DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	global LocalPID, CurrentPID, gameover, winner
	
	#speed of game
	clock = pygame.time.Clock()


	
	#global PlayerState

	#SocketThread()
  
	FADETIME = 1.0
	endtime = time.time() + FADETIME
	winfont = pygame.font.SysFont('Comic Sans MS', 100)

	myfont = pygame.font.SysFont('Comic Sans MS', 40)

	label_suggest = myfont.render("Suggest",False,ORANGE)
	suggestRect = label_suggest.get_rect()
	suggestRect.x = roomscalex * 1
	suggestRect.y = roomscaley * 1
	
	w = roomscalex / 3
	h = roomscaley / 2
	
	redlbl = myfont.render("R",False,BLACK)
	purplelbl = myfont.render("P",False,BLACK)
	greenlbl = myfont.render("G",False,BLACK)
	yellowlbl = myfont.render("Y",False,BLACK)
	whitelbl = myfont.render("W",False,BLACK)
	bluelbl = myfont.render("B",False,BLACK)
	
	redrect = pygame.Rect(roomscalex + w*0, roomscaley, w, h)
	purplerect = pygame.Rect(roomscalex + w*1, roomscaley, w, h)
	greenrect = pygame.Rect(roomscalex + w*2, roomscaley, w, h)
	yellowrect = pygame.Rect(roomscalex + w*0, roomscaley + h, w, h)
	whiterect = pygame.Rect(roomscalex + w*1, roomscaley + h, w, h)
	bluerect = pygame.Rect(roomscalex + w*2, roomscaley + h, w, h)



	label_accuse = myfont.render("Accuse",False,ORANGE)
	accuseRect = label_accuse.get_rect()
	accuseRect.x = roomscalex * 1
	accuseRect.y = roomscaley * 3
	
	redrect2 = pygame.Rect(roomscalex + w*0, roomscaley * 3, w, h)
	purplerect2 = pygame.Rect(roomscalex + w*1, roomscaley * 3, w, h)
	greenrect2 = pygame.Rect(roomscalex + w*2, roomscaley * 3, w , h)
	yellowrect2 = pygame.Rect(roomscalex + w*0, h + roomscaley * 3, w, h)
	whiterect2 = pygame.Rect(roomscalex + w*1, h + roomscaley * 3, w, h)
	bluerect2 = pygame.Rect(roomscalex + w*2, h + roomscaley * 3, w, h)

	showcolors = False
	while True:
		x,y = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminate()
			elif event.type == MOUSEBUTTONDOWN:
				s.sendall("[MOV] " + struct.pack('!ii', x, y))
				if showcolors == 0:
					if suggestRect.collidepoint(x, y):
						showcolors = 1
						break
					elif accuseRect.collidepoint(x, y):
						showcolors = 2
						break
				else:
					if showcolors == 1:
						if redrect.collidepoint(x, y):
							print "Suggesting Red!"
							s.sendall("[SGST] Red")
							showcolors = 0
						elif yellowrect.collidepoint(x, y):
							print "Suggesting Yellow!"
							s.sendall("[SGST] Yellow")
							showcolors = 0
						elif greenrect.collidepoint(x, y):
							print "Suggesting Green!"
							s.sendall("[SGST] Green")
							showcolors = 0
						elif purplerect.collidepoint(x, y):
							print "Suggesting Purple!"
							s.sendall("[SGST] Purple")
							showcolors = 0
						elif bluerect.collidepoint(x, y):
							print "Suggesting Blue!"
							s.sendall("[SGST] Blue")
							showcolors = 0
						elif whiterect.collidepoint(x, y):
							print "Suggesting White!"
							s.sendall("[SGST] White")
							showcolors = 0
						#else:
							#s.sendall("[MOV] " + struct.pack('!ii', x, y))
					elif showcolors == 2:
						if redrect2.collidepoint(x, y):
							print "Accusing Red!"
							s.sendall("[ACC] Red")
							showcolors = 0
						elif yellowrect2.collidepoint(x, y):
							print "Accusing Yellow!"
							s.sendall("[ACC] Yellow")
							showcolors = 0
						elif greenrect2.collidepoint(x, y):
							print "Accusing Green!"
							s.sendall("[ACC] Green")
							showcolors = 0
						elif purplerect2.collidepoint(x, y):
							print "Accusing Purple!"
							s.sendall("[ACC] Purple")
							showcolors = 0
						elif bluerect2.collidepoint(x, y):
							print "Accusing Blue!"
							s.sendall("[ACC] Blue")
							showcolors = 0
						elif whiterect2.collidepoint(x, y):
							print "Accusing White!"
							s.sendall("[ACC] White")
							showcolors = 0
						#else:
							#s.sendall("[MOV] " + struct.pack('!ii', x, y))

		DISPLAYSURF.fill(BGCOLOR)

	 

		for i in ROOMS_LIST:
			i.draw()

	  


		#pl.draw(DISPLAYSURF)


		#Fade Start#
		timedif = endtime - time.time()
		if timedif < FADETIME:


			label = myfont.render("START",False,(255,0,0))
			w,h = label.get_size()
			label.set_alpha(255 * timedif)
			DISPLAYSURF.blit(label,(WINDOWWIDTH/2 - w/2 ,WINDOWHEIGHT/2 - h/2))

		if CurrentPID == LocalPID:
			if showcolors == 1:
				DISPLAYSURF.fill(GREEN, greenrect)
				DISPLAYSURF.fill(RED, redrect)
				DISPLAYSURF.fill(YELLOW, yellowrect)
				DISPLAYSURF.fill(PURPLE, purplerect)
				DISPLAYSURF.fill(WHITE, whiterect)
				DISPLAYSURF.fill(BLUE, bluerect)
				
				DISPLAYSURF.blit(greenlbl, greenrect)
				DISPLAYSURF.blit(redlbl, redrect)
				DISPLAYSURF.blit(yellowlbl, yellowrect)
				DISPLAYSURF.blit(bluelbl, bluerect)
				DISPLAYSURF.blit(whitelbl, whiterect)
				DISPLAYSURF.blit(purplelbl, purplerect)
			elif showcolors == 2:
				DISPLAYSURF.fill(GREEN, greenrect2)
				DISPLAYSURF.fill(RED, redrect2)
				DISPLAYSURF.fill(YELLOW, yellowrect2)
				DISPLAYSURF.fill(PURPLE, purplerect2)
				DISPLAYSURF.fill(WHITE, whiterect2)
				DISPLAYSURF.fill(BLUE, bluerect2)
				
				DISPLAYSURF.blit(greenlbl, greenrect2)
				DISPLAYSURF.blit(redlbl, redrect2)
				DISPLAYSURF.blit(yellowlbl, yellowrect2)
				DISPLAYSURF.blit(bluelbl, bluerect2)
				DISPLAYSURF.blit(whitelbl, whiterect2)
				DISPLAYSURF.blit(purplelbl, purplerect2)
			else:
				DISPLAYSURF.fill(GREEN, suggestRect)
				DISPLAYSURF.blit(label_suggest, suggestRect)
				DISPLAYSURF.fill(GREEN, accuseRect)
				DISPLAYSURF.blit(label_accuse, accuseRect)

		turnlabel = myfont.render("Your turn!",False,ORANGE)
		if CurrentPID != LocalPID:
			for p in listofplayers:
				if p.pid == CurrentPID:
					turnlabel = myfont.render("Waiting on player: ",False,ORANGE)
					turnlabel2 = myfont.render(p.color,False,ORANGE)
					DISPLAYSURF.blit(turnlabel2,(roomscalex * 3, (roomscaley * 1)+turnlabel.get_rect().height))
		DISPLAYSURF.blit(turnlabel,(roomscalex * 3, roomscaley * 1))
		
		
		
		for p in listofplayers:
			if p.pid == LocalPID:
				melabel = myfont.render("My Color: ",False,ORANGE)
				DISPLAYSURF.blit(melabel,(roomscalex * 3, roomscaley * 3))
				melabel = myfont.render(p.color,False,ORANGE)
				DISPLAYSURF.blit(melabel,(roomscalex * 3, (roomscaley * 3)+melabel.get_rect().height))

		if gameover:
			wintext = "WINNER: " + winner
			label_win = winfont.render(wintext,False, RED)
			winrect = label_win.get_rect()
			winrect.centerx  = WINDOWWIDTH / 2
			DISPLAYSURF.blit(label_win, winrect)
		

		pygame.display.update()
		FPSCLOCK.tick(FPS)
		checkForKeyPress()


def main():

	global FPSCLOCK, DISPLAYSURF, BASICFONT
	#global PlayerState


	pygame.init()

	FPSCLOCK = pygame.time.Clock()

	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

	pygame.display.set_caption('CLUE')


	showStartScreen()

	


		
	s.connect(('localhost',666))


   

	start_new_thread(SocketThread, ())

	#s.sendall('Im in the lobby')
	#data = s.recv(1024)

	#print "Lobby: " + data
	Lobby()  
	#s.sendall('Im in the game')
	#data = s.recv(1024)
	#print "Ingame: " + data  

	runGame()

	#s.shutdown(socket.SHUT_RDWR)
	s.close()
	print "Disconnected"


	   

	   # showGameOverScreen()









if __name__ == '__main__':

	main()