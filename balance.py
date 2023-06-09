import queue # TO ACCESS PRIORITY QUEUEname
import time # TO CALCULATE AMNT OF TIME PROGRAM TAKES
import copy # TO DEEP COPY LISTS OF LISTS (cannot lose values)

from log import logComment

# TO DO: MAKE GUI
# def mainMenu():
#     menu = True

#     print("Welcome to the Ship Balance Program...\n")
#     print("1. Balance Ship")
#     print("2. Log In")
#     print("Please Select one from above...\n")

class Container:
    def __init__(self, weight, name, x, y):
        self.weight = weight
        self.name = name
        self.x = x
        self.y = y
    def getName(self): return self.name
    def getX(self): return self.x
    def getY(self): return self.y
    def setX(self, x): self.x = x
    def setY(self, y): self.y = y
    def getWeight(self): return self.weight
    def __lt__(self, compare):
        if (self.weight == compare.getWeight()): return True
        else: return self.weight > compare.getWeight()

class Ship:
    def __init__(self, numContainers, containers):
        self.numContainers = numContainers
        self.containers = containers
        self.matrix = self.getmatrix() # keeps inital state
    
    def getContainers(self): return self.containers
    def getRows(self): return 8
    def getCols(self): return 12
    def getmatrix(self):
        # https://www.geeksforgeeks.org/how-to-create-an-array-of-zeros-in-python/
        matrix = [[0 for row in range(self.getRows())] for cols in range(self.getCols())]
        # -1 = NAN, 0 = UNUSED, ELSE CONTAINER
        for x in self.containers:
            matrix[int(x.getX()) - 1][int(x.getY()) - 1] = x
        return matrix
    def setmatrix(self, m): self.matrix = m

def readManifest(filepath):
    global currShip
    file = open(filepath, "r")
    containers =  []
    numContainers = 0
    for l in file:
        t = l.split(', ')
        y,x= t[0].strip("[]").split(",")
        weight = int(t[1].strip("{}"))
        name = t[2].strip("\n")
        if name == 'NAN': weight = -1
        newC = Container(weight, name, x, y)
        if (name != 'NAN') and (name != 'UNUSED'):
            numContainers = numContainers + 1
        containers.append(newC)
        
    filename = filepath.strip(".txt")
    log = 'Manifest ' + filename + ' opened, ' + str(numContainers) + ' containers loaded'
    currShip = Ship(numContainers, containers)
    logComment(log)

# Idea and some code taken from group member's CS 170 Porject 1 submision
# https://github.com/hussain-adeel/170p1
# Note: matrix is 2d array of containers
class Node:
    def __init__(self, matrix, moves, hn, gn):
        self.matrix = matrix
        self.weightMatrix = self.getWeightMatrix()
        self.hn = hn
        self.gn = gn # num moves so far
        self.fn = hn + gn
        self.moves = moves
        self.prevM = []
        self.prevGns = []
    def getPrevGns(self): return self.prevGns
    def appendGn(self, g): self.prevGns.append(g)
    def getPrevMoves(self): return self.prevM
    def appendSolStep(self, m):
        self.prevM.append(m)
    def getWeightMatrix(self):
        weightMatrix = [[0 for row in range(8)] for cols in range(12)]
        for x in self.getmatrix():
            for c in x:
                weightMatrix[int(c.getX()) - 1][int(c.getY()) - 1] = c.getWeight()
        return weightMatrix
    def getMoves(self):
        return self.moves # moves taken to get to this state (in str format)
    def addMove(self, s):
        self.moves.append(s)
    def getmatrix(self):
        return self.matrix
    def updatematrix(self, newmatrix):
        self.matrix = newmatrix
    def getFn(self):
        return self.fn
    def getHn(self):
        return self.hn
    def getGn(self):
        return self.gn
    def setHn(self, new_hn):
        self.hn = new_hn
    def setGn(self, new_gn):
        self.gn = new_gn
    def updateFn(self):
        self.fn = self.hn + self.gn
    def getLeftWeight(self):
        weight = 0
        weight = 0
        for x in range(6):
            for y in range(8):
                if self.getmatrix()[x][y].getWeight() != -1: weight += self.getmatrix()[x][y].getWeight()
        return weight
    def getRightWeight(self):
        weight = 0
        for x in range(6, 12):
            for y in range(8):
                if self.getmatrix()[x][y].getWeight() != -1: weight += self.getmatrix()[x][y].getWeight()
        return weight
    def getBothWeight(self):
        return self.getLeftWeight(), self.getRightWeight()
    def checkBalance(self):
        rw = self.getRightWeight()
        lw = self.getLeftWeight()
        #print(lw)
        if lw == 0 and rw == 0:
            return True
        else:
            print(min(lw, rw)/max(lw, rw))
            return (min(lw, rw)/max(lw, rw)) >= 0.9
    def print(self):
        # TESTING PURPOSES ONLY
        for y in range(8)[::-1]:
            for x in range(12):
                print(str(self.getmatrix()[x][y].getWeight()).center(12), end='')
            print('')
    def printW(self):
        # TESTING PURPOSES ONLY
        for y in range(8)[::-1]:
            for x in range(12):
                print(str(self.weightMatrix[x][y]).center(12), end='')
            print('')
    def findValidSpaces(self, side):
        #pass in lighter side...
        spaces = []
        skip = False
        if side == 'left':
            for x in range(6)[::-1]:
                for y in range(8):
                    if self.matrix[x][y].getName() == 'UNUSED' and not skip:
                        spaces.append(x)
                        spaces.append(y)
                        skip = True
                skip = False
        if side == 'right':
            for x in range(6, 12):
                for y in range(8):
                    if self.matrix[x][y].getName() == 'UNUSED' and not skip:
                        spaces.append(x)
                        spaces.append(y)
                        skip = True
                skip = False
        return spaces
    def findValidSpace(self, side):
        #pass in lighter side...
        if side == 'left':
            for x in range(6)[::-1]:
                for y in range(0, 11):
                    if self.matrix[x][y].getName() == 'UNUSED':
                        return x, y
        if side == 'right':
            for x in range(6, 11):
                for y in range(0, 11):
                    if self.matrix[x][y].getName() == 'UNUSED':
                        return x,y
    # this is used by the priority queue to determine how to order these nodes
    def __lt__(self, compare):
        if (self.fn == compare.getFn()): return self.gn < compare.getGn()
        else: return self.fn < compare.getFn()
    
    def calcHn(self): # logic taken from Dr. Keogh's search slides
        lw, rw = self.getBothWeight()
        balanceMass = (lw + rw) / 2
        deficit = balanceMass - min(lw, rw)

        weightQ = queue.PriorityQueue() # used trick in __lt__ def to makes this a psuedo maxheap

        if lw > rw:
            for x in self.getmatrix():
                for c in x:
                    if c.getName() != 'UNUSED' and c.getName() != 'NAN' and int(c.getX()) < 6:
                        weightQ.put(c)
        else:
            for x in self.getmatrix():
                for c in x:
                    if c.getName() != 'UNUSED' and c.getName() != 'NAN' and int(c.getX()) >= 6:
                        weightQ.put(c)
        
        numCMoved = 0
        distTravel = 0
        while not weightQ.empty():
            x = weightQ.get()
            xw = x.getWeight()
            otherWeight = min(lw, rw)
            if xw <= deficit:
                otherWeight += xw

                numCMoved = numCMoved + 1
                if lw > rw:
                    x1, y1 = self.findValidSpace('right')
                else:
                    x1, y1 = self.findValidSpace('left')
                distTravel = distTravel + calcDistance(int(x.getX()) - 1, int(x.getY()) - 1, x1, y1)
            if (otherWeight / (max(lw, rw) - otherWeight) >= 0.9):
                return numCMoved + distTravel
        #print(-1)
        return numCMoved + distTravel
    
    def swap(self, c, x1, y1):
        matrix = self.getmatrix()
        x = int(c.getX()) - 1
        y = int(c.getY()) - 1
        newC = Container(c.getWeight(), c.getName(), str(x1 + 1), str(y1 + 1))


        emptyContainer = Container(0, 'UNUSED', x, y)
        matrix[x1][y1] = newC
        matrix[x][y] = emptyContainer
        self.updatematrix(matrix)


        return calcDistance(x, y, x1, y1)

def calcDistance(x, y, x1, y1):
    return abs(x - x1) + abs(y - y1)


def expand(Node, repeatStates):
    lw, rw = Node.getBothWeight()

    nodes_to_expand = []

    if lw > rw: # left side heavier - find node(s) to expand...
        for x in range(6):
            for y in range(8)[::-1]:
                # take top node from each stack (only ones that can move..., if hit NAN go to next)
                cn = Node.getmatrix()[x][y]
                if cn.getName() == 'NAN': break
                elif cn.getName() == 'UNUSED': continue
                else:
                    nodes_to_expand.append(cn)
                    #print('found node l: ' + cn.getName() + ' ' + cn.getX() + ' ' + cn.getY())
                    break
    else: # right side heavier
        for x in range(6, 12):
            for y in range(8)[::-1]:
                # take top node from each stack (only ones that can move..., if hit NAN go to next)
                cn = Node.getmatrix()[x][y]
                if cn.getName() == 'NAN': break
                elif cn.getName() == 'UNUSED': continue
                else:
                    nodes_to_expand.append(cn)
                    #print('found node r: ' + cn.getName() + ' ' + cn.getX() + ' ' + cn.getY())
                    break
    
    nodes_return = []

    for n in nodes_to_expand: 
        if lw > rw:
            spaces = Node.findValidSpaces('right')
            while (spaces):
                newNode = copy.deepcopy(Node)
                x1 = spaces.pop(0)
                y1 = spaces.pop(0)
                if (x1 == int(n.getX()) -1 and y1 == int(n.getY())):
                    continue
                c = newNode.swap(n, x1, y1)
                newNode.calcHn()
                newNode.appendSolStep(Node.getmatrix())
                newNode.appendGn(Node.getGn())
                newNode.setGn(Node.getGn() + c)
                newNode.updateFn()
                newNode.addMove('Move container ' + n.getName() + ' from ' + n.getX() + ',' + n.getY() + ' to ' + str("{:02d}".format(x1 + 1)) + ',' + str("{:02d}".format(y1 + 1)))
                if repeatStates.get(tuple(tuple(s) for s in newNode.getWeightMatrix())) != 'R':
                    nodes_return.append(newNode)
        else:
            spaces = Node.findValidSpaces('right')
            while (spaces):
                newNode = copy.deepcopy(Node)
                x1 = spaces.pop(0)
                y1 = spaces.pop(0)
                if (x1 == int(n.getX())-1 and y1 == int(n.getY())):
                    #print('skipped')
                    continue
                c = newNode.swap(n, x1, y1)
                newNode.appendSolStep(Node.getmatrix())
                newNode.calcHn()
                newNode.setGn(Node.getGn() + c)
                newNode.updateFn()
                newNode.addMove('Move container ' + n.getName() + ' from ' + n.getX() + ',' + n.getY() + ' to ' + str(x1 + 1) + ',' + str(y1 + 1))
                if repeatStates.get(tuple(tuple(s) for s in newNode.getWeightMatrix())) != 'R':
                    nodes_return.append(newNode)
    return nodes_return

def m(nodes, moves):
    new_nodes = nodes
    for node in moves:
        new_nodes.put(node)
    
    return new_nodes



def search(): # can only have 1 manifest / ship at once - so no need for parameter when alr global var

    nodes = queue.PriorityQueue()
    repeatStates = {}

    initalNode = Node(currShip.getmatrix(), [], Node(currShip.getmatrix(), [], 0, 0).calcHn(), 0)
    nodes.put(initalNode)

    stateTuple = tuple(tuple(s) for s in initalNode.getWeightMatrix())
    repeatStates[stateTuple] = "R"

    while(1):
        # no solution and no nodes left, search failed...
        if (nodes.empty()):
            print('Failed, need to use SIFT')
            return "failed" # use SIFT

        # pop current node off PQ
        currNode = nodes.get()
        # check if goal state reached
        if (currNode.checkBalance()):
            print(currNode.getLeftWeight())
            print(currNode.getRightWeight())

            print("----------------\n")
            print("\n!!! REACHED GOAL STATE !!!")
            print("----------------")
            currNode.print()
            currShip.setmatrix(currNode.getmatrix())
            print('minutes taken: ' + str(currNode.getGn()))
            for x in currNode.getMoves(): print(x)
            return currNode
        
        
        # If not goal, then we need to expand it
        print("The best state to expand with a g(n) = " + str(currNode.getGn()) + " and h(n) = " + str(currNode.getHn()) + " is...")
        currNode.print()
        
        # EXPAND to find new moves (need to do this sep. becasuse of how my repeat check works)
        new_nodes = expand(currNode, repeatStates)
        
        # Need to sure no repeats of moves we already found through expanding
        for n in new_nodes:
            t = tuple(tuple(x) for x in n.getWeightMatrix())
            repeatStates[t] = 'R'
        
        # Use queueing function selected to order PQ to better come up with solution
        nodes = m(nodes, new_nodes)