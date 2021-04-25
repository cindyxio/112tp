#Cindy Xiong (cindyxio)
class Property(object):
    def __init__(self, name, cost, rent, priceChange, color):
        self.name = name
        self.rent = rent
        self.original = rent
        self.cost = cost #cost of buying the property
        self.houseCost = cost//4 #cost of building a house
        self.priceChange = priceChange #priceChange comes in the form of a 
        #string with a math operator and price: additional price of rent every 
        # time a house is built
        self.color = color
        #other variables might needed: owner, whether monopolized...
        self.level = 0
        #self.points -> for the AI's points system
    def getName(self):
        return self.name
    def getCost(self):
        return self.cost
    def getColor(self):
        return self.color
    def getRent(self):
        return self.rent
    def getLevel(self):
        if 0 <= self.level < 4:
            return f'{self.level} house(s)'
        else:
            return 'Hotel'
    def levelRent(self, level): #returns rent price for an integer level
        new = self.original
        for i in range(level):
            new = int(eval(str(new)+self.priceChange))
        return new
    def build(self): #note: monopoly must be True to build
        self.level += 1
        self.rent = self.levelRent(self.level)
    def monopoly(self):
        if self.level == 0:
            self.rent = self.rent*2

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