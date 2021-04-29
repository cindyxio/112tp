#Cindy Xiong (cindyxio)
class Property(object):
    def __init__(self, name, cost, rent, priceChange, color):
        self.name = name
        self.rent = rent
        self.original = rent
        self.cost = cost #cost of buying the property (changes when a house is built)
        self.houseCost = cost//4 #cost of building a house
        self.priceChange = priceChange #priceChange comes in the form of a 
        #string with a math operator and price: additional price of rent every 
        # time a house is built
        self.color = color
        self.level = 0
        self.aiPoints = 0
        self.playerPoints = 0
    def getName(self):
        return self.name
    def getCost(self):
        return self.cost
    def getColor(self):
        return self.color
    def getOriginal(self):
        return self.original
    def getRent(self):
        return self.rent
    def getLevel(self):
        if 0 <= self.level < 4:
            return f'{self.level} house(s)'
        elif self.level == 4:
            return 'Hotel'
    def levelRent(self, level): #returns rent price for an integer level
        new = self.original
        for i in range(level):
            new = int(eval(str(new)+self.priceChange))
        return new
    def build(self): #note: monopoly must be True to build
        self.level += 1
        self.rent = self.levelRent(self.level)
        self.cost += self.houseCost
    def monopoly(self):
        if self.level == 0:
            self.rent = self.rent*2
    def initialPoints(self):
        ogCost = self.cost
        initRent = self.original
        hotelRent = self.levelRent(4)
        block = 2
        if self.color == 'green' or self.color == 'purple':
            block = 3
        weighted = int((initRent*2.5) + (hotelRent*0.15) + (100/block) - 
        (ogCost/4))
        if self.name == 'Fauna Court' or self.name == 'Witch Street':
            #note: this is due to Chance being able to teleport to them
            weighted += 10
        self.points = weighted
        return self.points
    def calcAiPoints(self, count): #takes how many properties of same color owned
        if count == 3:
            self.aiPoints = 50
        elif count == 2:
            self.aiPoints = 25
        elif count == 1:
            self.aiPoints = 15
        else:
            self.aiPoints = 0
    def calcPlayerPoints(self, count):
        if count == 3:
            self.playerPoints = 10
        elif count == 2:
            self.playerPoints = 30
        elif count == 1:
            self.playerPoints = 20
        else:
            self.playerPoints = 0
    def getPoints(self):
        return self.points + self.aiPoints + self.playerPoints
    def subtractPoints(self, pts):
        self.points -= pts
    def addPoints(self, pts):
        self.points += pts

class Piece(object):
    def __init__(self, name):
        self.name = name
        self.position = ('right', 6)
        self.money = 1500
        self.jailTurns = 0
        self.properties = []
        self.monopoly = []
    def getName(self):
        return self.name
    def getPosition(self):
        return self.position
    def getSide(self):
        return self.position[0]
    def getIndex(self):
        return self.position[1]
    def getMoney(self):
        return self.money
    def getJailTurns(self):
        return self.jailTurns
    def getProperties(self):
        return self.properties
    def getMonopoly(self):
        return self.monopoly
    def addMoney(self, money):
        self.money += money
    def subtractMoney(self, money):
        if self.money-money >= 0:
            self.money -= money
        else:
            self.money = 0
    def changePosition(self, newPosition):
        self.position = newPosition
    def goToJail(self):
        self.jailTurns = 1
        self.position = ('bottom', 6)
    def inJail(self):
        self.jailTurns -= 1
    def addProperty(self, prop):
        self.properties.append(prop)
    def removeProperty(self, prop):
        self.properties.remove(prop)
    def monopolize(self, color):
        self.monopoly.append(color)
    def unmonopolize(self, color):
        self.monopoly.remove(color)