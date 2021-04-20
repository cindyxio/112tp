#Cindy Xiong (cindyxio)
#CMU 15-112 Term Project (Fantasy Monopoly against AI)

from cmu_112_graphics_cindyxiotp import *
import tkinter as tk
import random, math, time
from time import sleep

class Property(object):
    #priceChange comes in the form of a string with a math operator and price
    def __init__(self, name, cost, rent, priceChange, color):
        self.name = name
        self.rent = rent
        self.cost = cost
        self.priceChange = priceChange
        self.color = color
        #other variables might needed: owner, whether monopolized...
        self.level = 0
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
            return f'{self.level} houses'
        else:
            return 'Hotel'
    def build(self): #note: monopoly must be True to build
        self.rent = eval(str(self.rent)+self.priceChange)
        self.level += 1
    def monopoly(self):
        if self.level == 0:
            self.rent = self.rent*2

def appStarted(app):
    app.margin = 20
    app.cellHeight = (app.height-2*app.margin)/6
    app.cellWidth = app.cellHeight*2/3
    app.text = int(app.height//60)
    app.radius = app.text
    app.fauna = Property('Fauna Court', 150, 17, '+100*(self.level+1)', 
    'green')
    app.cecile = Property('Cecile Circle', 70, 5, '+50', 'green')
    app.dream = Property("Dream Loop", 314, 13, '*1.3', 'green')
    app.dragon = Property('Dragon Trail', 400, 25, '*2', 'purple')
    app.fae = Property('Fae Avenue', 100, 11, '*1.5', 'purple')
    app.elven = Property('Elven Place', 500, 50, '*2.1', 'purple')
    app.seer = Property('Seer Terrace', 220, 35, '+20*(self.level+3)', 'red')
    app.oracle = Property('Oracle Way', 150, 15, '*1.5', 'red')
    app.mermaid = Property('Mermaid Beach', 50, 10, '+15', 'blue')
    app.coral = Property('Coral Lane', 150, 15, '*1.5', 'blue')
    app.deity = Property('Deity Run', 400, 25, '*2', 'yellow')
    app.sunset = Property('Sunset Drive', 220, 35, '+20*(self.level+3)', 
    'yellow')
    app.magic = Property('Magic Street', 220, 35, '+20*(self.level+3)', 
    'orange')
    app.mythical = Property('Mythical Road', 150, 15, '*1.5', 'orange')
    app.boardBottom = [app.dream, app.fauna, app.cecile, 'Chance', 'Income Tax', 
    'Chance'] #right to left: green
    app.boardLeft = [app.sunset, app.deity, 'Chance', app.mythical, 
    'Income Tax', app.magic] #down to up: orange and yellow
    app.boardTop = [app.oracle, app.seer, app.coral, 'Income Tax', app.mermaid, 
    'Chance'] #left to right: blue and red
    app.boardRight = ['Income Tax', 'Chance', app.fae, 'Chance', app.elven, 
    app.dragon] #up to down: purple
    app.order = ['bottom', 'left', 'top', 'right'] #order of boardSides
    app.turn = True
    app.gameOver = False
    '''
    Pieces are dicttionaries. 

    'Position' is represented by a tuple of (boardSide, index). Note if i == 6,
    this means that i is the index of the corner piece (which is not part of 
    boardSide list): 'Go!' is the corner piece for the right side, 'Jail' for 
    the bottom, 'Free Parking' for the left, and 'Go to Jail!' for the top.

    'Jail' holds how many turns left in jail there is.

    'Monopoly' holds a list of the colors the piece has a monopoly of.

    'Money' holds the amount of money the piece has and 'Properties' holds a 
    list of properties the piece owns.
    '''
    app.player = {'Position': ('right', 6),'Money': 1500, 'Jail': 0,
    'Properties': None, 'Monopoly': None}
    app.ai = {'Position': ('right', 6),'Money': 1500, 'Jail': 0,
    'Properties': None, 'Monopoly': None}

def getPixelsFromPosition(app, side, i):
    if side == 'right':
        x1 = app.margin+app.cellHeight+(app.cellWidth*6)
        y1 = app.margin+app.cellHeight+app.cellWidth*i
        x2 = app.margin+(app.cellHeight*2)+(app.cellWidth*6)
        y2 = app.margin+app.cellHeight+app.cellWidth*(i+1)
        if i == 6:
            y2 = app.height-app.margin
    if side == 'left':
        x1 = app.margin
        y1 = app.height-app.margin-app.cellHeight-app.cellWidth*(i+1) 
        x2 = app.margin+app.cellHeight
        y2 = app.height-app.margin-app.cellHeight-app.cellWidth*(i)
        if i == 6:
            y1 = app.margin
    if side == 'top':
        x1 = app.margin+app.cellHeight+app.cellWidth*(i)
        y1 = app.margin
        x2 = app.margin+app.cellHeight+app.cellWidth*(i+1) 
        y2 = app.margin+app.cellHeight
        if i == 6:
            x2 = app.height-app.margin
    if side == 'bottom':
        x1 = app.height-app.margin-app.cellHeight-app.cellWidth*(i+1) 
        y1 = app.height-app.margin-app.cellHeight
        x2 = app.height-app.margin-app.cellHeight-app.cellWidth*(i)
        y2 = app.height-app.margin
        if i == 6:
            x1 = app.margin
    return x1, y1, x2, y2

def roll(app, piece):
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    moves = d1+d2
    for move in range(moves):
        movePiece(app, piece)
    #getSquareFromPosition(app, piece, newSide, newIndex)

def movePiece(app, piece):
    sideIndex = app.order.index(piece['Position'][0])
    side = app.order[sideIndex]
    index = piece['Position'][1]
    if index < 6:
        index += 1
    else:
        if sideIndex < 3:
            sideIndex += 1
        else:
            sideIndex = 0
        side = app.order[sideIndex]
        index = 0
    piece['Position'] = (side, index)

def getSquareFromPosition(app, piece, side, i):
    if side == 'right':
        if i == 6:
            square = 'GO!'
        else:
            square = app.boardRight[i]
    if side == 'left':
        if i == 6:
            square = 'Free\nParking'
        else:
            square = app.boardLeft[i]
    if side == 'top':
        if i == 6:
            square = 'Go to\nJail!'
        else:
            square = app.boardTop[i]
    if side == 'bottom':
        if i == 6:
            square = 'JAIL'
        else:
            square = app.boardBottom[i]
    if isinstance(square, str):
        if square == 'GO!':
            piece['Money'] += 200
        if square == 'Jail':
            piece['Jail'] -= 1
            if piece['Jail'] == 0:
                piece['Money'] -= 50
        if square == 'Go to\nJail!':
            piece['Jail'] = 2
        if square == 'Chance':
            chanceCard(app)
        if square == 'Income Tax':
            piece['Money'] -= 200
    else:
        landOnProperty(app, square)

def landOnProperty(app, property): #what happens when you land on property
    pass

def chanceCard(app): #what happens when you land on chance
    pass

def keyPressed(app, event):
    if app.gameOver: return
    if event.key == 'Space':
        if app.turn:
            roll(app, app.player)
            app.turn = False
        else:
            roll(app, app.ai)
            app.turn = True
    pass

def mousePressed(app, event):
    pass

def timerStarted(app, event):
    
    pass

def rgbString(r, g, b):
    #from: https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
    return f'#{r:02x}{g:02x}{b:02x}'

def drawSide(app, canvas, square, side, x1, y1, x2, y2):
    canvas.create_rectangle(x1, y1, x2, y2, width=3)
    if square == 'Chance':
        canvas.create_text((x1+x2)/2, (y1+y2)/2, anchor='center', text="CHANCE",
        font=f'Courier {app.text}')
    elif square == "Income Tax":
        canvas.create_text((x1+x2)/2, (y1+y2)/2, anchor='center', 
        text="Income\nTax", font=f'Courier {app.text}')
    else:
        propertyName = square.getName()
        propertyName = propertyName.replace(' ', '\n')
        canvas.create_text((x1+x2)/2, (y1+y2)/2, anchor='center', 
        text=propertyName, font=f'Courier {app.text}')
        color = square.getColor()
        if side == 'left':
            canvas.create_rectangle(x2-app.margin, y1, x2, y2, fill = color)
        elif side == 'right':
            canvas.create_rectangle(x1, y1, x1+app.margin, y2, fill = color)
        elif side == 'top':
            canvas.create_rectangle(x1, y2-app.margin, x2, y2, fill = color)
        else:
            canvas.create_rectangle(x1, y1, x2, y1+app.margin, fill = color)

def drawBoard(app, canvas):
    monopolyGreen = rgbString(204, 255, 204)
    canvas.create_rectangle(app.margin, app.margin, app.height-app.margin,
    app.height-app.margin, width = 5, fill = monopolyGreen)
    canvas.create_rectangle(app.cellHeight+app.margin, 
    app.cellHeight+app.margin, app.height-app.cellHeight-app.margin, 
    app.height-app.cellHeight-app.margin, width = 3)
    canvas.create_text(app.height/2, app.height/2-app.margin, 
    text = "FANTASY  MONOPOLY", anchor = "center", 
    font = f"Helectiva {int(app.text*5/2)} bold")
    for i in range(len(app.boardBottom)):
        drawSide(app, canvas, app.boardBottom[i], 'bottom',
        app.height-app.margin-app.cellHeight-app.cellWidth*(i+1), 
        app.height-app.margin-app.cellHeight, 
        app.height-app.margin-app.cellHeight-app.cellWidth*(i), app.height-app.margin)
    for i in range(len(app.boardTop)):
        drawSide(app, canvas, app.boardTop[i], 'top',
        app.margin+app.cellHeight+app.cellWidth*(i), 
        app.margin, app.margin+app.cellHeight+app.cellWidth*(i+1), 
        app.margin+app.cellHeight)
    for i in range(len(app.boardLeft)):
        drawSide(app, canvas, app.boardLeft[i], 'left', app.margin, 
        app.height-app.margin-app.cellHeight-app.cellWidth*(i+1), 
        app.margin+app.cellHeight,
        app.height-app.margin-app.cellHeight-app.cellWidth*(i))
    for i in range(len(app.boardRight)):
        drawSide(app, canvas, app.boardRight[i], 'right',
        app.margin+app.cellHeight+(app.cellWidth*6), 
        app.margin+app.cellHeight+app.cellWidth*i, 
        app.margin+(app.cellHeight*2)+(app.cellWidth*6),
        app.margin+app.cellHeight+app.cellWidth*(i+1))
    canvas.create_text(app.margin+app.cellHeight/2, app.margin+app.cellHeight/2,
    text = 'Free\nParking', font = f'Courier {int(4*app.text/3)}')
    canvas.create_text(app.height-app.margin-app.cellHeight/2,
    app.margin+app.cellHeight/2, text = 'Go to\nJail!', 
    font = f'Courier {int(4*app.text/3)}')
    canvas.create_text(app.margin+app.cellHeight/2, 
    app.height-app.margin-app.cellHeight/2, text = "JAIL", 
    font = f'Courier {int(4*app.text/3)}')
    canvas.create_text(app.height-app.margin-app.cellHeight/2,
    app.height-app.margin-app.cellHeight/2, text = 'GO!', 
    font = f'Courier {int(4*app.text/3)}')

def drawPieces(app, canvas):
    playerSide = app.player['Position'][0]
    playerIndex = app.player['Position'][1]
    x1, y1, x2, y2 = getPixelsFromPosition(app, playerSide, playerIndex)
    canvas.create_oval(x1, y1, x1+2*app.radius, y1+2*app.radius, fill = 'white')
    aiSide = app.ai['Position'][0]
    aiIndex = app.ai['Position'][1]
    v1, w1, v2, w2 = getPixelsFromPosition(app, aiSide, aiIndex)
    canvas.create_oval(v2, w2, v2-2*app.radius, w2-2*app.radius, fill = 'black')

def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawPieces(app, canvas)

def runMonopoly():
    runApp(width=1255, height=725)
    
runMonopoly()