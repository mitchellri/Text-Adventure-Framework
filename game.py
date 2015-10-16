#	Fix move in and out
#	Make modifiable turn ending moves
#	Change player record map info stacks to trees
#	Make areas (sit down)

#	Messages
welcomemessage = "Welcome!"
actionmessage = "What would you like to do?"
errormessage = "Not a valid input"
successmessage = "You complete the action"
failuremessage = "You can't do that"
unitmessage = "You see "
turnovermessage = "Your turn has ended"
#	Declarations
exitinput = "x"
actions = ["move","look","talk","attack","map"]
directions = ["up","down","right","left","in","out",None]
map_type = ["regular","wall","entry","start"]	#	map_type[immovable[...]]
#	Links
actions_function = {}	#	actions_function[actions[value]]=function_for_action
actions_message = {		#	actions_message[actions[value]]=message_for_action
	actions[0]:"Where would you like to go?",
	actions[1]:"You take a look around",
	actions[2]:"You look to start a conversation",
	actions[3]:None,
	actions[4]:"You take a look at your map"
	}
move_translate = {
	directions[0]:[-1,0],
	directions[1]:[1,0],
	directions[2]:[0,1],
	directions[3]:[0,-1],
	directions[4]:[0,0],	#	in
	directions[5]:[0,0],	#	out
	None:[0,0]
	}

#	Define classes
class player:
	name = None
	x=-1
	y=-1
	health=-1
	weapon = False
	maps = False
	recordedMaps = False
	def __init__(self,name,map):
		self.name = name
		self.health=3
		self.weapon = None
		self.maps = []
		self.maps.append(map)
		self.recordedMaps = []
		self.recordedMaps.append([["empty" for x in range(len(self.maps[-1].map))] for x in range(len(self.maps[-1].map[0]))])
		self.moveTo(map_type[3])
		self.recordMap(self.getLocation())
		self.maps[-1].map[self.x][self.y][1].append(self)
	def move(self,action):
		self.maps[-1].moveUnit(self,action)
		self.x+=move_translate[action][0]	#	in -> gotostart
		self.y+=move_translate[action][1]	#	in -> 0
		self.recordMap(self.getLocation())		
	def recordMap(self,xy):
		if (xy[0] >= 0) and (xy[0] < len(self.maps[-1].map)):
				if(xy[1] >= 0) and (xy[1] < len(self.maps[-1].map[0])):
					self.recordedMaps[-1][xy[0]][xy[1]] = self.maps[-1].checkLocation([xy[0],xy[1]])
					return True
		return False
	def getLocation(self):
		return [self.x,self.y]
	def moveTo(self,map_type):
		for x in self.maps[-1].map:
			for y in x:
				if y[0] == map_type:
					self.x = self.maps[-1].map.index(x)
					self.y = x.index(y)
					return True
		return False

class overworld:
	map = [[-1 for x in range(4)] for x in range(4)]
	def __init__(self):	#	self.map[#][#] = [map_type[#],units[...],map]
		self.map[0][0] = [map_type[3],[],None]
		self.map[0][1] = [map_type[0],[],None]
		self.map[0][2] = [map_type[0],[],None]
		self.map[0][3] = [map_type[0],[],None]
		self.map[1][0] = [map_type[1],[],None]
		self.map[1][1] = [map_type[0],[],None]
		self.map[1][2] = [map_type[1],[],None]
		self.map[1][3] = [map_type[0],[],None]
		self.map[2][0] = [map_type[0],[],None]
		self.map[2][1] = [map_type[0],[],None]
		self.map[2][2] = [map_type[1],[],None]
		self.map[2][3] = [map_type[0],[],None]
		self.map[3][0] = [map_type[1],[],None]
		self.map[3][1] = [map_type[1],[],None]
		self.map[3][2] = [map_type[2],[],None]
		self.map[3][3] = [map_type[0],[],None]
	def tileChange(self,xy,typeIndex):
		self.map[xy[0]][xy[1]][0] = map_type[typeIndex]
	def addEntry(self,xy,map):
		if self.checkLocation(xy) == map_type[2]:
			self.map[xy[0]][xy[1]][2]=map
			return True
		else:
			return False
	def checkLocation(self,xy):
		if (xy[0] >= 0) and (xy[0] < len(self.map)):
			if(xy[1] >= 0) and (xy[1] < len(self.map[0])):
				return self.map[xy[0]][xy[1]][0]
		return map_type[1]
	def checkUnits(self,xy):
		if (xy[0] >= 0) and (xy[0] < len(self.map)):
			if(xy[1] >= 0) and (xy[1] < len(self.map[0])):
				return self.map[xy[0]][xy[1]][1]
		return []
	def moveUnit(self,unit,action):
		xy = unit.getLocation()
		unit.maps[-1].map[xy[0]][xy[1]][1].remove(unit)
		if action == directions[4]:
			unit.maps.append(unit.maps[-1].map[xy[0]][xy[1]][2])
			unit.recordedMaps.append([["empty" for x in range(len(unit.maps[-1].map))] for x in range(len(unit.maps[-1].map[0]))])
		elif action == directions[5]:
			unit.maps.pop()
			unit.recordedMaps.pop()
		xy[0]+=move_translate[action][0]
		xy[1]+=move_translate[action][1]
		unit.maps[-1].map[xy[0]][xy[1]][1].append(unit)

#	Define action functions
def basicAction(message,player):
	while(True):
		action = input(message).split(" ")
		if len(action) > 1:
			command = action[1]
		else:
			command = None
		action = action[0]
		if action in actions:
			return actions_function[action](actions_message[action],command,player)
		else:
			print(errormessage)

def basicMove(message,action,player):
	while True:
		if action == None:
			action=input(message)
		if action in directions:
			x = player.x + move_translate[action][0]
			y = player.y + move_translate[action][1]
			loc = player.maps[-1].checkLocation([x,y])
			if loc != map_type[1]:
				print(successmessage)
				player.move(action)
				return True
			else:
				print(failuremessage)
				print("It's a " + loc)
				player.recordMap([x,y])
				return False
		elif action == exitinput:
			break;
		else:
			print(errormessage)
			action = None

def basicLook(message,action,player):
	if action in directions:
		print(message)
		x = player.x + move_translate[action][0]
		y = player.y + move_translate[action][1]
		print([x,y],player.maps[-1].checkLocation([x,y]))
		action = player.maps[-1].checkUnits([x,y])
		for unit in action:
			if unit != player:
				print(unitmessage + unit.name)
		player.recordMap([x,y])
	else:
		print(errormessage)

def basicTalk(message,action,player):
	if len(player.maps[-1].map[player.x][player.y][1])>1:
		print(message)
		return True
	else:
		print(failuremessage)
		return False

def basicMap(message,action,player):
	print(message)
	list = []
	for x in range(len(player.recordedMaps[-1])):
		list.append(x)
	print(list)
	list = 0
	for x in player.recordedMaps[-1]:
		print(list,x)
		list += 1

#	Define misc functions

#	Link functions
actions_function[actions[0]] = basicMove
actions_function[actions[1]] = basicLook
actions_function[actions[2]] = basicTalk
actions_function[actions[3]] = None
actions_function[actions[4]] = basicMap

#	---	/	FRAMEWORK END	\	---

#	Game variables and libraries
import time
over_world = overworld()
underworld = overworld()
over_world.addEntry([3,2],underworld)
player1 = player("Mitchell", over_world)
player2 = player("Ryan", over_world)
players=[player1,player2]
turns = 10

print(welcomemessage)
while True:
	for x in players:
		taken = 0
		while(taken<turns):
			basicAction(actionmessage+x.name,x)
			taken += 1
		print(turnovermessage)
		time.sleep(1)