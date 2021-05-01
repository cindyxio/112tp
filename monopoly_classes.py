#Cindy Xiong (cindyxio)
class Property(object):
    def __init__(self, name, cost, rent, priceChange, color):
        self.name = name
        self.rent = rent
        self.originalRent = rent
        self.originalCost = cost
        self.cost = cost #cost of buying the property (changes when a house is built)
        self.houseCost = cost//4 #cost of building a house
        self.priceChange = priceChange #priceChange comes in the form of a 
        #string with a math operator and price: additional price of rent every 
        # time a house is built
        self.color = color
        self.level = 0
        self.propertyPoints = 0 #points calculated based off of property status
        self.aiPoints = 0 #points calculated based off of properties AI owns
        self.playerPoints = 0 #points calc based off properties player owns
        self.changingPoints = 0 #points that change due to other factors in game
        self.points = (self.propertyPoints + self.aiPoints + self.playerPoints 
        + self.changingPoints)
    def getName(self):
        return self.name
    def getCost(self):
        return self.cost
    def getColor(self):
        return self.color
    def getOriginalRent(self):
        return self.originalRent
    def getRent(self):
        return self.rent
    def getLevel(self):
        if 0 <= self.level < 4:
            return f'{self.level} house(s)'
        elif self.level == 4:
            return 'Hotel'
    def levelRent(self, level): #returns rent price for an integer level
        new = self.originalRent
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
    def calcPropertyPoints(self):
        hotelRent = self.levelRent(4)
        block = 2
        if self.color == 'green' or self.color == 'purple':
            block = 3
        weighted = int((self.rent*2) + (hotelRent*0.25) + (100/block) - 
        (self.originalCost/3))
        if self.name == 'Fauna Court' or self.name == 'Witch Street':
            #note: this is due to Chance being able to teleport to them
            weighted += 20
        if self.color == "green" or self.color == "orange":
            #note: this is due to the advantage of Fauna and Witch
            weighted += 10
        self.propertyPoints = weighted
        return self.propertyPoints
    def calcAiPoints(self, count): 
        #takes in how many properties of same color owned
        if count == 2:
            self.aiPoints = 100
        elif count == 1:
            self.aiPoints = 75
        else:
            self.aiPoints = 0
    def calcPlayerPoints(self, count):
        #takes in how many properties of same color owned
        if count == 2:
            self.playerPoints = 20
        elif count == 1:
            self.playerPoints = 70
        else:
            self.playerPoints = 0
    def getPoints(self):
        self.points = (self.propertyPoints + self.aiPoints + self.playerPoints 
        + self.changingPoints)
        return self.points
    def subtractPoints(self, pts):
        self.changingPoints -= pts
    def addPoints(self, pts):
        self.changingPoints += pts

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