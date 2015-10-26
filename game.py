#	Messages
welcomemessage = "Welcome!"
actionmessage = "What would you like to do?"
errormessage = "Not a valid input"
successmessage = "You complete the action"
failuremessage = "You can't do that"
#	Declarations
exitinput = "x"
actions = ["move","look","talk","map"]
directions = ["up","down","right","left",None,"in"]
map_type = ["regular","wall","start"]	#	map_type[immovable[...]]
misc_message = {
	"basicsee": "You see",
	"movemap": "Which entry would you like to take?"
	}
#	Links
actions_function = {}	#	actions_function[actions[value]]=function_for_action
actions_message = {		#	actions_message[actions[value]]=message_for_action
	actions[0]:"Where would you like to move?",
	actions[1]:"You take a look around",
	actions[2]:"You look to start a conversation",
	actions[3]:"You take a look at your map"
	}
move_translate = {
	directions[0]:[-1,0],
	directions[1]:[1,0],
	directions[2]:[0,1],
	directions[3]:[0,-1],
	None:[0,0],
	directions[-1]:[0,0]
	}

#	Define classes
class recordMap:
	map = False
	recordedMap = False
	def __init__(self,map):
		self.map = map
		self.recordedMap = [["empty" for x in range(len(self.map.map))] for x in range(len(self.map.map[0]))]
	def read(self):
		list = []
		for x in range(len(self.recordedMap)):
			list.append(x)
		print(list)
		x=0
		for list in self.recordedMap:
			print(x,list)
			x += 1

class entry:
	map = False
	x = False
	y = False
	#event = False
	def __init__(self,map,xy):
		self.map = map
		self.x = xy[0]
		self.y = xy[1]
	def getLocation(self):
		return [self.x,self.y]

class player:
	name = None
	x=-1
	y=-1
	health=-1
	weapon = False
	map = False
	recordedMaps = False
	def __init__(self,name,map):
		self.name = name
		self.health=3
		self.weapon = None
		self.map = map
		self.recordedMaps = []
		self.recordedMaps.append(recordMap(self.map))
		self.moveTo(self.map.findTile(map_type[-1]))
		self.recordMap(self.getLocation())
		self.map.map[self.x][self.y][1].append(self)
	def move(self,action,entry):
		self.map.moveUnit(self,action,entry)
		self.x+=move_translate[action][0]
		self.y+=move_translate[action][1]
		self.recordMap(self.getLocation())		
	def recordMap(self,xy):
		if (xy[0] >= 0) and (xy[0] < len(self.map.map)):
				if(xy[1] >= 0) and (xy[1] < len(self.map.map[0])):
					self.getMap().recordedMap[xy[0]][xy[1]] = self.map.checkLocation(xy)[0]
					return True
		return False
	def getMap(self):
		for recordedMap in self.recordedMaps:
			if recordedMap.map == self.map:
				return recordedMap
		return False
	def getLocation(self):
		return [self.x,self.y]
	def moveTo(self,xy):
		self.x = xy[0]
		self.y = xy[1]

class overworld:
	map = [[-1 for x in range(4)] for x in range(4)]
	def __init__(self):	#	self.map[#][#] = [map_type[#],units[...],entries[]]
		self.map = [[-1 for x in range(4)] for x in range(4)]
		self.map[0][0] = [map_type[-1],[],[]]
		self.map[0][1] = [map_type[0],[],[]]
		self.map[0][2] = [map_type[0],[],[]]
		self.map[0][3] = [map_type[0],[],[]]
		self.map[1][0] = [map_type[1],[],[]]
		self.map[1][1] = [map_type[0],[],[]]
		self.map[1][2] = [map_type[1],[],[]]
		self.map[1][3] = [map_type[0],[],[]]
		self.map[2][0] = [map_type[0],[],[]]
		self.map[2][1] = [map_type[0],[],[]]
		self.map[2][2] = [map_type[1],[],[]]
		self.map[2][3] = [map_type[0],[],[]]
		self.map[3][0] = [map_type[1],[],[]]
		self.map[3][1] = [map_type[1],[],[]]
		self.map[3][2] = [map_type[0],[],[]]
		self.map[3][3] = [map_type[0],[],[]]
	def tileChange(self,xy,typeIndex):
		self.map[xy[0]][xy[1]][0] = map_type[typeIndex]
	def addEntry(self,xy,map,newxy,twoway):	#	,event
		if map.checkLocation(newxy)[0] != map_type[1]:
			self.map[xy[0]][xy[1]][2].append(entry(map,newxy))
			if twoway:
				map.map[newxy[0]][newxy[1]][2].append(entry(self,xy))
			return True
		return False
	def checkLocation(self,xy):
		if (xy[0] >= 0) and (xy[0] < len(self.map)):
			if(xy[1] >= 0) and (xy[1] < len(self.map[0])):
				return self.map[xy[0]][xy[1]]
		return [map_type[1],[],[]]
	def moveUnit(self,unit,action,entry):
		xy = unit.getLocation()
		unit.map.map[xy[0]][xy[1]][1].remove(unit)
		if entry:
			unit.map = entry.map
			xy = entry.getLocation()
			unit.moveTo(xy)
			unit.recordedMaps.append(recordMap(unit.map))
		else:
			xy[0]+=move_translate[action][0]
			xy[1]+=move_translate[action][1]
		unit.map.map[xy[0]][xy[1]][1].append(unit)
	def findTile(self,map_type):
		for x in self.map:
			for y in x:
				if y[0] == map_type:
					return [self.map.index(x),x.index(y)]

#	Define action functions
def basicAction(message,player):
	turnOver = False
	while not turnOver:
		action = input(message).split(" ")
		if len(action) > 1:
			command = action[1]
		else:
			command = None
		action = action[0]
		if action in actions:
			turnOver = actions_function[action](actions_message[action],command,player)
		else:
			print(errormessage)

def basicMove(message,action,player):
	while True:
		if action == None:
			action=input(message)
		if action in directions:
			x = player.x + move_translate[action][0]
			y = player.y + move_translate[action][1]
			tile = player.map.checkLocation([x,y])
			if tile[0] != map_type[1]:
				if action == directions[-1]:
					if len(tile[2])>0:
						entry = basicMoveMap(misc_message["movemap"],tile[2],player)
						if not entry:
							break
					else:
						print(failuremessage)
						return True
				else:
					entry = None
				print(successmessage)
				player.move(action,entry)
				return True
			else:
				print(failuremessage)
				print("It's a " + tile[0])
				player.recordMap([x,y])
				return True
		elif action == exitinput:
			break
		else:
			print(errormessage)
			action = None

def basicLook(message,action,player):
	if action in directions:
		print(message)
		x = player.x + move_translate[action][0]
		y = player.y + move_translate[action][1]
		tile = player.map.checkLocation([x,y])
		print([x,y],tile[0])
		for unit in tile[1]:
			if unit != player:
				print(misc_message["basicsee"], unit.name)
		for entry in tile[2]:
			print(misc_message["basicsee"], entry.getLocation(), entry.map.checkLocation(entry.getLocation())[0])
		player.recordMap([x,y])
		return True
	print(errormessage)

def basicTalk(message,action,player):
	if len(player.map.checkLocation(player.getLocation())[1])>1:
		print(message)
		return True
	print(failuremessage)
	return True

def basicMap(message,action,player):
	print(message)
	player.getMap().read()
	return True

#	Define misc functions
def basicMoveMap(message,entries,player):
	while True:
		x=0
		print("Index","Coordinates","Type","Different")
		for entry in entries:
			print(x,entry.getLocation(), entry.map.checkLocation(entry.getLocation())[0],entry.map!=player.map)
			x+=1
		x = input(message)
		if x.isdigit():
			x=int(x)
			if x in range(len(entries)):
				return entries[x]
		elif x == exitinput:
			return None
		print(errormessage)

#	Link functions
actions_function[actions[0]] = basicMove
actions_function[actions[1]] = basicLook
actions_function[actions[2]] = basicTalk
actions_function[actions[3]] = basicMap

#	---	/	FRAMEWORK END	\	---

#	Game variables and libraries
import time
turnovermessage = "Your turn has ended"
moveovermessage = "Time has passed"
over_world = overworld()
underworld = overworld()
over_world.addEntry([2,1],over_world,[3,2],False)
over_world.addEntry([3,2],underworld,[2,0],True)
player1 = player("Mitchell", underworld)
player2 = player("Ryan", over_world)
players=[player1,player2]
turns = 100

print(welcomemessage)
while True:
	for x in players:
		taken = 0
		while(taken<turns):
			basicAction(actionmessage+x.name,x)
			print(moveovermessage)
			taken += 1
		print(turnovermessage)
		time.sleep(1)