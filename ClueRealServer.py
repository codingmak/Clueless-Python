import socket
# Import multi-threading module
from thread import start_new_thread
import os
# Import the time module
import time
# Import command line arguments
from sys import argv
# Import logging

from ClueGui import *

import random, logging
import struct


NAME_LIST = ["Purple", "Blue", "Green", "Red", "Yellow", "White"]
random.shuffle(NAME_LIST)
SUS_PLAYER = NAME_LIST[0]
print "Suspect Player: " + SUS_PLAYER

WEAPON_LIST = ["Candlestick", "Knife", "Ropes", "Revolver", "Lead", "Wrench"]
random.shuffle(WEAPON_LIST)
SUS_WEAPON = WEAPON_LIST[0]
print "Murder Weapon: " + SUS_WEAPON

ROOMNAME_LIST = ["STUDY ROOM", "KITCHEN", "BALL ROOM", "LOUNGE", "LIBRARY", "HALL", "BILLIARDS", "CONSERVATORY", "DINING"]
random.shuffle(ROOMNAME_LIST)
SUS_ROOM = ROOMNAME_LIST[0]
print "Murder Room: " + SUS_ROOM


playercount = 0

HOST='0.0.0.0'
PORT=666

waiting_players = []


def AddPacketHeader(buf, pid):
	buf = struct.pack('!ii', len(buf), pid) + buf
	return buf

def SendPacketAll(data, pid):
	for c in waiting_players:
		c.sock.sendall(AddPacketHeader(data, pid))

#WINDOWWIDTH = 1000
#WINDOWHEIGHT = 1000
#roomscalex = WINDOWWIDTH/5
#roomscaley = WINDOWHEIGHT/5

def CheckValidMove(fromx, fromy, tox, toy):
	#temporary rescale
	#print "-before-"
	#print "fromx: " + str(fromx) + "fromy: " + str(fromy) + "tox: " + str(tox) + "toy: " + str(toy)
	fromx = fromx / 200
	fromy = fromy / 200
	tox = tox / 200
	toy = toy / 200
	#print "-after-"
	#print "fromx: " + str(fromx) + "fromy: " + str(fromy) + "tox: " + str(tox) + "toy: " + str(toy)

	difx = abs(tox - fromx)
	dify = abs(toy - fromy)
	if (difx == 0 and dify == 0):
		print "Player didn't move"
		return False
	elif (difx == 1 and dify == 0) or (difx == 0 and dify == 1):
		print "Position is close enough"
		return True
	else:
		print "Too far, checking if secret passage"

		if (fromx == 0 and fromy == 0 and tox == 4 and toy == 4): #STUDY ROOM -> KITCHEN
			return True
		if (fromx == 4 and fromy == 4 and tox == 0 and toy == 0): #KITCHEN -> STUDY ROOM
			return True

		if (fromx == 4 and fromy == 0 and tox == 0 and toy == 4): #LOUNGE -> CONSERVATORY
			return True
		if (fromx == 0 and fromy == 4 and tox == 4 and toy == 0): #CONSERVATORY -> LOUNGE
			return True

	return False


def Win(player):
	global CURRENT_PLAYER
	for p in listofplayers:
		SendPacketAll("[WIN] " + player.color, player.pid)

def clientthread(conn,pid):
	global TURN, waiting_players
	#a = " hello dsfg"
	#onn.send(a.encode())

	CURRENT_PLAYER = waiting_players[TURN % waiting_players.__len__()]
	SendPacketAll("[TRN] " + str(CURRENT_PLAYER.pid), CURRENT_PLAYER.pid)

	while(1):

		if gameover:
			break
		
		data = conn.recv(1024)
	
		print "Sent packet from PID: " + str(pid)
		CURRENT_PLAYER = waiting_players[TURN % waiting_players.__len__()]

		if CURRENT_PLAYER.skipturns == 1:
			CURRENT_PLAYER.skipturns -= 1
			TURN += 1
			CURRENT_PLAYER = waiting_players[TURN % waiting_players.__len__()]

		if "START" in data and pid == 0:
			print "Host requesting start game"
			SendPacketAll("[START]", pid)

		if pid == CURRENT_PLAYER.pid:
			if "MOV" in data:
				x, y = struct.unpack('!ii', data[6:])
				if (CheckValidMove(CURRENT_PLAYER.x, CURRENT_PLAYER.y, x, y)):

					CURRENT_PLAYER.x = x
					CURRENT_PLAYER.y = y
					SendPacketAll(data,pid)					
					TURN = TURN + 1
					CURRENT_PLAYER = waiting_players[TURN % waiting_players.__len__()]
					SendPacketAll("[TRN] " + str(CURRENT_PLAYER.pid), CURRENT_PLAYER.pid)

				else:
					print "Invalid move"
			elif "ACC" in data:
				for p in listofplayers:
					if p.color in data:
						print p.color + " == " + SUS_PLAYER
						if p.color == SUS_PLAYER:
							print "Correct suspect"
							Win(CURRENT_PLAYER)
							break
						else:
							print "Wrong suspect, next player's turn"
							#CURRENT_PLAYER.skipturns += 1
							break

				TURN = TURN + 1
				CURRENT_PLAYER = waiting_players[TURN % waiting_players.__len__()]
				SendPacketAll("[TRN] " + str(CURRENT_PLAYER.pid), CURRENT_PLAYER.pid)
					
			elif "SGST" in data:
				roomx = CURRENT_PLAYER.x 
				roomy = CURRENT_PLAYER.y 
				#print "This is roomx x" + str(roomx)
				#print "This is roomx y" + str(roomy)
				x=roomx
				y=roomy
				print "Suggesting player: " + str(roomx) + "," + str(roomy)
				for p in listofplayers:
					if p.color in data and p.pid >= 0:

						print "This is server getting the color " + str(p.color)
						SendPacketAll("[MOV] " + struct.pack('!ii', x, y), p.pid)
						print "Moving player: " + p.color + ":" + str(p.pid)
						CURRENT_PLAYER = waiting_players[TURN % waiting_players.__len__()]
						SendPacketAll("[TRN] " + str(CURRENT_PLAYER.pid), CURRENT_PLAYER.pid)

			
		else:
			print("Not your turn!")

		if len(data) == 0:
			break

		#print(reply)
		#conn.sendall(reply)

	#conn.shutdown(socket.SHUT_RDWR)
	conn.close()

     
  

try:
	s=socket.socket()
	s.bind((HOST,PORT))
	s.listen(1)
	print 'Socket established'
	
	


	#print NAME_LIST



	#logging.info("Received connection from " + str(addr));

	# Initialize a new Player object to store all the client's infomation

	# Push this new player object into the players array
	
	#conn.sendall(chosen)

	#Server still needs to stay up even if client disconnected and also only allow up to 6 and no more than  6

	while True:
	#if NAME_LIST.__len__() <= 6:
		if STATE == STATE_WAITING:
			print NAME_LIST.__len__()
			conn, addr = s.accept()

	#		print "Room is Full"
			chosen = NAME_LIST.pop()
			print chosen
			x = 0
			y = 0

			if chosen == "Purple":
				x = 0
				y = 1
			elif chosen == "Blue":
				x = 2
				y = 1
			elif chosen == "Green":
				x = 1
				y = 4
			elif chosen == "Red":
				x = 1
				y = 2
			elif chosen == "Yellow":
				x = 0
				y = 3
			elif chosen == "White":
				x = 3
				y = 4
			else:
				print("If we see this, bad things happened")

			#temporary rescaling
			x = x * 200
			y = y * 200

			new_player = Player(playercount, x, y, None)	
			playercount += 1
			new_player.sock = conn
			new_player.color = chosen
			conn.sendall(AddPacketHeader("[PID] " + new_player.color, new_player.pid))

			for p in listofplayers:
				if p.color == chosen:
					p.pid = new_player.pid
					break

			#print "New: " + "Color: " +  new_player.color + "PID: " + new_player.pid 

			# = data[6];


			for player in waiting_players: 
				print "Color: " + player.color
				print "Sending waiting player to new player pid: " + str(player.pid)
				#print "This is what we are testing " + str(player)
				conn.sendall(AddPacketHeader("[NEW] " + player.color, player.pid)) 

			waiting_players.append(new_player)


			for player in waiting_players: 
				print "Color: " + player.color
				print "Sending new player to waiting player pid: " + str(player.pid)
				#print "This is what we are testing " + str(player)
				player.sock.sendall(AddPacketHeader("[NEW] " + new_player.color, new_player.pid))

			#waiting_players.append(new_player)

			for i in waiting_players:
				print "PID: " + str(i.pid)
			
			start_new_thread(clientthread, (conn, new_player.pid))
		'''-------------------------------------------------------------------------------------------------------------'''

except socket.error:
	print "Doesn't work"
