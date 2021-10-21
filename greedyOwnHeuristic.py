import collections
from multiprocessing import Queue
from queue import PriorityQueue
import copy

board=[]
maxLength=0

boxRobot=[]
wallsStorageSpaces=[]
possibleMoves = {'N':[-1,0], 'E':[0,1],'S':[1,0],'W':[0,-1]}

maxRowLength = 0	
lines=0

while(1):
	line = input()
	if line!="":
		lines+=1
		board.append(line)
		if len(line)>maxRowLength:
			maxRowLength=len(line)
	else:
		break	

import time
time_start = time.time()

for i in range(0,lines):
	boxRobot.append([])
	wallsStorageSpaces.append([])
	for j in range(0,maxRowLength):
		boxRobot[-1].append('-')
		wallsStorageSpaces[-1].append('-')

for i in range(0,len(board)):
	if len(board[i])<maxRowLength:
		for j in range(len(board[i]),maxRowLength):
			board[i]+='O'

for i in range(0,len(board)):
	for j in range(0,maxRowLength):
		if board[i][j]=='B' or board[i][j]=='R':
			boxRobot[i][j]=board[i][j]
			wallsStorageSpaces[i][j]=' '
		elif board[i][j]=='S' or board[i][j]=='O':
			wallsStorageSpaces[i][j] = board[i][j]
			boxRobot[i][j] = ' '
		elif board[i][j]==' ':
			boxRobot[i][j] = ' '
			wallsStorageSpaces[i][j]=' '
		elif board[i][j] == '*':
			boxRobot[i][j] = 'B'
			wallsStorageSpaces[i][j] = 'S'
		elif board[i][j] == '.':
			boxRobot[i][j] = 'R'
			wallsStorageSpaces[i][j] = 'S'

storages = []
for i in range(0,lines):
	for j in range(0,maxRowLength):
		if wallsStorageSpaces[i][j]=='S':
			storages.append([i,j])

print(storages)
boxRobtDistance = 0
boxes=[]
storagesLeft = len(storages)
for i in range(0,lines):
	for j in range(0,maxRowLength):
		if boxRobot[i][j]=='B':
			if wallsStorageSpaces[i][j]=='S':
				print(i,j)
				storagesLeft-=1
			boxes.append([i,j])
print(storagesLeft)


for i in range(0,lines):
	for j in range(0,maxRowLength):
		if boxRobot[i][j]=='R':
			for k in boxes:
				boxRobtDistance+=abs(k[0]-i)+abs(k[1]-j)


def manhattan(state):
	distance = 0
	for i in range(0,lines):
		for j in range(0,maxRowLength):
			if state[i][j] == 'B':
				temp= 9999999
				for storage in storages:
					distanceToNearest = abs(storage[0]-i)+abs(storage[1]-j)
					if temp > distanceToNearest:
						temp = distanceToNearest

				distance+=temp
	return distance

print("Solving using Greedy search using Own heuristic\n")

movesList=[]
visitedMoves=[]

queue = PriorityQueue()
source = [boxRobot,movesList]
if boxRobot not in visitedMoves:
	visitedMoves.append(boxRobot)
queue.put((manhattan(boxRobot)+boxRobtDistance,source))

robot_x = -1
robot_y = -1
completed = 0

while not queue.empty() and completed==0:
	temp = queue.get()
	curPosition = temp[1][0]
	movesTillNow = temp[1][1]
	for i in range(0,lines):
		for j in range(0,maxRowLength):
			if curPosition[i][j]=='R':
				robot_y = j
				robot_x = i
				break
		else:
			continue
		break

	for key in possibleMoves:
		robotNew_x = robot_x+possibleMoves[key][0]
		robotNew_y = robot_y+possibleMoves[key][1] 
		curPositionCopy = copy.deepcopy(curPosition)
		movesTillNowCopy = copy.deepcopy(movesTillNow)

		if curPositionCopy[robotNew_x][robotNew_y] == 'B':
			boxNew_x = robotNew_x + possibleMoves[key][0]
			boxNew_y = robotNew_y + possibleMoves[key][1]
			if curPositionCopy[boxNew_x][boxNew_y]=='B' or wallsStorageSpaces[boxNew_x][boxNew_y]=='O':
				continue
			else:
				curPositionCopy[boxNew_x][boxNew_y]='B'
				curPositionCopy[robotNew_x][robotNew_y] = 'R'
				curPositionCopy[robot_x][robot_y] = ' '
				if curPositionCopy not in visitedMoves:
					matches= 0
					for k in range(0,lines):
						for l in range(0,maxRowLength):
							if wallsStorageSpaces[k][l]=='S':
								if curPositionCopy[k][l]!='B':
									matches=1
					movesTillNowCopy.append(key)
					if matches == 0:
						completed = 1
						print ("Number of moves : {}\n{} \n".format(len(movesTillNowCopy),movesTillNowCopy))
					else:
						boxRobtDistance = 0
						boxes=[]
						storagesLeft = len(storages)
						for i in range(0,lines):
							for j in range(0,maxRowLength):
								if curPositionCopy[i][j]=='B':
									if wallsStorageSpaces[i][j]=='S':
										storagesLeft-=1
									boxes.append([i,j])

						for i in range(0,lines):
							for j in range(0,maxRowLength):
								if curPositionCopy[i][j]=='R':
									for k in boxes:
										boxRobtDistance+=abs(k[0]-i)+abs(k[1]-j)


						queue.put((manhattan(curPositionCopy)+boxRobtDistance+storagesLeft*2,[curPositionCopy,movesTillNowCopy]))
						visitedMoves.append(curPositionCopy)
		else:
			if wallsStorageSpaces[robotNew_x][robotNew_y]=='O' or curPositionCopy[robotNew_x][robotNew_y]!=' ':
				continue
			else:
				curPositionCopy[robotNew_x][robotNew_y]='R'
				curPositionCopy[robot_x][robot_y]=' '
				if curPositionCopy not in visitedMoves:
					movesTillNowCopy.append(key)
					boxRobtDistance = 0
					boxes=[]
					storagesLeft = len(storages)
					for i in range(0,lines):
						for j in range(0,maxRowLength):
							if curPositionCopy[i][j]=='B':
								if wallsStorageSpaces[i][j]=='S':
									storagesLeft-=1
								boxes.append([i,j])

					for i in range(0,lines):
						for j in range(0,maxRowLength):
							if curPositionCopy[i][j]=='R':
								for k in boxes:
									boxRobtDistance+=abs(k[0]-i)+abs(k[1]-j)
					queue.put((manhattan(curPositionCopy)+boxRobtDistance+storagesLeft*2,[curPositionCopy,movesTillNowCopy]))
					visitedMoves.append(curPositionCopy)

if completed==0:
	print("Can't make it")
time_end = time.time()
print("Run time: "+str(time_end - time_start))
