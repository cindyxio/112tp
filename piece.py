#Cindy Xiong (cindyxio)
#Piece class for Fantasy Monopoly (aka the two players)
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