# TO DO: MAKE GUI
def mainMenu():
    menu = True

    print("Welcome to the Ship Balance Program...\n")
    print("1. Balance Ship")
    print("2. Log In")
    print("Please Select one from above...\n")

class Container:
    def __init__(self, weight, name, x, y):
        self.weight = weight
        self.name = name
        self.x = x
        self.y = y
    def getName(self): return self.name
    def getX(self): return self.x
    def getY(self): return self.y
    def getWeight(self): return self.weight

class Ship:
    def __init__(self, numContainers, containers):
        self.numContainers = numContainers
        self.containers = containers
    def getContainers(self): return self.containers

    def getLeftWeight(self):
        weight = 0
        
        for x in self.containers:
            if (int(x.getX()) <= 4):
                weight += x.getWeight()
        return weight
    def getRightWeight(self):
        weight = 0
        for x in self.containers:
            if (int(x.getX()) > 4):
                weight += x.getWeight()
        return weight
    def checkBalance(self):
        rw = self.getRightWeight()
        lw = self.getLeftWeight()
        if lw == 0 and rw == 0:
            return True
        else:
            return (min(lw, rw)/max(lw, rw)) >= 0.9

    #def balance(self):
    #   while (self.getLeftWeight )

def readManifest(filepath):
    global currShip
    file = open(filepath, "r")
    containers =  []
    containersRow = []
    numContainers = 0
    for l in file:
        t = l.split(', ')
        x,y = t[0].strip("[]").split(",")
        print(str(x) + str(y))
        weight = int(t[1].strip("{}"))
        name = t[2].strip("\n")
        newC = Container(weight, name, x, y)
        #print(name)
        if (name != 'NAN') and (name != 'UNUSED'):
            numContainers = numContainers + 1
        containers.append(newC)
        
    filename = filepath.strip(".txt")
    log = 'Manifest ' + filename + ' opened, ' + str(numContainers) + ' containers loaded'
    currShip = Ship(numContainers, containers)

    print(log)


readManifest("ShipCase1.txt")

currShip.getLeftWeight()
currShip.getRightWeight()
print(currShip.checkBalance())