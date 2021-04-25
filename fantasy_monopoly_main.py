#Cindy Xiong (cindyxio)
#CMU 15-112 Term Project (Fantasy Monopoly against AI)

from cmu_112_graphics_cindyxiotp import *
import tkinter as tk
import random, math, time
from monopoly_classes import *

'''
AI Key Points:
- A point system: 
- will trade a property owned below a certain cutoff
- will offer trade for opponent's property above cutoff
- Points of player's prop increase when player is closer to monopoly in color
- will buy above a certain cutoff (points increase closer to monopoly)
- points decrease when AI is losing money
'''

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
    app.witch = Property('Witch Street', 220, 35, '+20*(self.level+3)', 
    'orange')
    app.mythical = Property('Mythical Road', 150, 15, '*1.5', 'orange')

    app.boardBottom = [app.dream, app.fauna, app.cecile, 'Chance', 
    'Magic Tax', 'Chance'] #right to left: green
    app.boardLeft = [app.sunset, app.deity, 'Chance', app.mythical, 
    'Magic Tax', app.witch] #down to up: orange and yellow
    app.boardTop = [app.oracle, app.seer, app.coral, 'Magic Tax', app.mermaid, 
    'Chance'] #left to right: blue and red
    app.boardRight = ['Magic Tax', 'Chance', app.fae, 'Chance', app.elven, 
    app.dragon] #up to down: purple
    app.order = ['bottom', 'left', 'top', 'right'] #order of boardSides 
    
    app.gameOver = False
    app.turn = True #is True when it's the player's turn
    app.instructions = "Press 'Space' to Roll" #holds the instructions
    app.comment = "Welcome to Fantasy Monopoly!" #holds the current comment
    app.card = None #holds the currently displayed card
    app.buy = False #is True if a buy is currently taking place
    app.trade = False #is True if a trade is currently taking place
    app.sell = False #is True if a sell is currently taking place
    app.build = False #is True if building is currently taking place
    app.cont = False #is True if player decides to buy/trade/sell a property
    app.moving = False #is True when pieces are moving across board (takes no 
    #user input then)
    app.moves = 0
    app.d1 = 0
    app.d2 = 0
    app.start = time.time()
    app.time = time.time()
    '''
    Pieces (app.player and app.ai) are dicttionaries. 

    'Position' is represented by a tuple of (boardSide, index). Note if i == 6,
    this means that i is the index of the corner piece (which is not part of 
    boardSide list): 'Go!' is the corner piece for the right side, 'Jail' for 
    the bottom, 'Free Parking' for the left, and 'Go to Jail!' for the top.

    'Jail' holds how many turns left in jail there is.

    'Monopoly' holds a list of the colors the piece has a monopoly of.

    'Money' holds the amount of money the piece has and 'Properties' holds a 
    list of properties the piece owns.
    '''
    app.player = Piece('Player')
    app.ai = Piece('AI')
    app.currentPiece = app.player
    app.currentProperty = None
    app.winner = None

def finishTurnInstructions(app):
    if app.currentPiece == app.player:
        app.instructions = "Press 'Space' to Finish Turn"
    else:
        app.instructions = "Press 'Space' to Roll"
    pass

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

def roll(app): #rolls two random die and sets up movement of piece
    app.d1 = random.randint(1, 6)
    app.d2 = random.randint(1, 6)
    app.moves = app.d1+app.d2
    app.moving = True
    app.time = time.time()

def movePiece(app, piece): #moves piece forward by one step
    side = piece.getSide()
    sideIndex = app.order.index(side)
    index = piece.getIndex()
    if index < 6:
        index += 1
    else:
        if sideIndex < 3:
            sideIndex += 1
        else:
            sideIndex = 0
        side = app.order[sideIndex]
        index = 0
    if side == 'right' and index == 6: #+$200 every time Go is passed
        piece.addMoney(200)
    piece.changePosition((side, index))

def getSquareFromPosition(app, piece, side, i):
    if side == 'right':
        if i == 6:
            square = 'GO!'
        else:
            square = app.boardRight[i]
    if side == 'left':
        if i == 6:
            square = 'Free Parking'
        else:
            square = app.boardLeft[i]
    if side == 'top':
        if i == 6:
            square = 'Go to Jail!'
        else:
            square = app.boardTop[i]
    if side == 'bottom':
        if i == 6:
            square = 'JAIL'
        else:
            square = app.boardBottom[i]
    if isinstance(square, str):
        app.currentProperty = None
        if square == 'Chance':
            chanceCard(app, piece)
        else:
            if square == 'GO!':
                app.comment = 'Gain $200 for your Travels!'
            if square == 'JAIL' and piece.getJailTurns() == 0:
                app.comment = 'Just visiting Jail!'
            if square == 'Free Parking':
                app.comment = 'Taking a break!'
            if square == 'Go to Jail!':
                app.comment = 'Go to Jail!'
                piece.goToJail()
            if square == 'Magic Tax':
                app.comment = 'Magic Tax: $200 vanished!'
                piece.subtractMoney(200)
            finishTurnInstructions(app)
    else:
        app.currentProperty = square
        app.comment = f'Landed on {app.currentProperty.getName()}!'
        landOnProperty(app, piece, app.currentProperty)

def landOnProperty(app, piece, prop): #what happens when you land on property
    if prop in piece.getProperties():
        app.sell = True
        app.instructions = "Press 'Y' to Sell and 'N' to Pass"
    else:
        if piece == app.player:
            if prop in app.ai.getProperties():
                piece.subtractMoney(prop.getRent())
                app.comment = app.comment+f'\nPaid ${prop.getRent()} in rent!'
                app.trade = True
                app.instructions = "Press 'Y' to Trade and 'N' to Pass"
            else:
                app.buy = True
                app.instructions = "Press 'Y' to Buy and 'N' to Pass"
        elif piece == app.ai:
            if prop in app.player.getProperties():
                piece.subtractMoney(prop.getRent())
                app.comment = app.comment+f'\nPaid ${prop.getRent()} in rent!'
                app.trade = True
                app.instructions = "Press 'Y' to Trade and 'N' to Pass"
            else:
                app.buy = True
                app.instructions = "Press 'Y' to Buy and 'N' to Pass"
    pass

def buyProperty(app, piece, prop):
    if app.cont:
        piece.addProperty(prop)
        piece.subtractMoney(prop.getCost())
        checkMonopoly(app, piece)
        app.buy = False
        app.cont = False
    if app.buy == False:
        finishTurnInstructions(app)

def sellProperty(app, piece, prop):
    if app.cont:
        piece.removeProperty(prop)
        piece.addMoney(prop.getCost())
        checkMonopoly(app, piece)
        app.sell = False
        app.cont = False
    if app.sell == False:
        finishTurnInstructions(app)

def tradeProperty(app, piece, prop):
    if app.cont:
        #trade
        checkMonopoly(app, piece)
        app.trade = False
        app.cont = False
    if app.trade == False:
        finishTurnInstructions(app)

def chanceCard(app, piece): #what happens when you land on chance
    cards = ['Go to Jail', 'Materialize $50', 'Teleport to Go', 
    'Materialize $200', 'Go to Jail', 'Teleport to Witch Street', 
    'Teleport to Fauna Court', '$15 vanished', '$50 vanished']
    cardIndex = random.randint(0, len(cards)-1)
    app.comment = f'Chance: {cards[cardIndex]}!'
    if cards[cardIndex] == 'Go to Jail':
        piece.goToJail()
        finishTurnInstructions(app)
    splitCard = cards[cardIndex].split(' ')
    if splitCard[0] == 'Teleport':
        if splitCard[len(splitCard)-1] == "Go":
            piece.changePosition(('right', 6))
            piece.addMoney(200)
            finishTurnInstructions(app)
        else:
            if splitCard[len(splitCard)-2] == "Fauna":
                piece.changePosition(('bottom', 1))
                app.currentProperty = app.boardBottom[1]
                landOnProperty(app, piece, app.currentProperty)
            else:
                piece.changePosition(('left', 5))
                app.currentProperty = app.boardLeft[5]
                landOnProperty(app, piece, app.currentProperty)
    else:
        if splitCard[0] == 'Materialize':
            money = int(splitCard[1][1:])
            piece.addMoney(money)
        elif splitCard[len(splitCard)-1] == "vanished":
            money = int(splitCard[0][1:])
            piece.subtractMoney(money)
        finishTurnInstructions(app)
    pass

def checkMonopoly(app, piece):
    #checks after each play if there is all of one color in one player's 
    # possession (if getColor in monopoly)
    #now, you can choose to build after your turn
    colorDict = {}
    for prop in piece.getProperties():
        colorDict[prop.getColor()] = colorDict.get(prop.getColor(), 0) + 1
    for color in colorDict:
        if colorDict[color] >= 2:
            if color != 'green' and color != 'purple':
                piece.monopolize(color)
            else:
                if colorDict[color] == 3:
                    piece.monopolize(color)
    pass

def checkJail(app, piece):
    if piece.getJailTurns() == 0:
        roll(app)
        checkMonopoly(app, piece)
    else:
        piece.inJail()
        if piece.getJailTurns() == 0:
            app.comment = 'Paid $50 and left Jail!'
            piece.subtractMoney(50)
        else:
            app.comment = 'Still in Jail!'
        finishTurnInstructions(app)

def keyPressed(app, event):
    #game will be played mostly in keyPressed
    #press i for instructions to the game
    if app.gameOver or app.moving: return
    if app.buy:
        if event.key == "Y" or event.key == "y":
            app.cont = True
        if event.key == "N" or event.key == "n":
            app.buy = False
        buyProperty(app, app.currentPiece, app.currentProperty)
    elif app.sell:
        if event.key == "Y" or event.key == "y":
            app.cont = True
        if event.key == "N" or event.key == "n":
            app.sell = False
        sellProperty(app, app.currentPiece, app.currentProperty)
    elif app.trade:
        if event.key == "Y" or event.key == "y":
            app.cont = True
        if event.key == "N" or event.key == "n":
            app.trade = False
        tradeProperty(app, app.currentPiece, app.currentProperty)
        #list properties and use up and down keys
    elif ((event.key == 'b' or event.key == 'B') and 
    app.currentPiece.getMonopoly() != [] and app.build == False):
        app.build = True
        app.instructions = 'Click a Property to Build'
    elif event.key == 'Space':
        if app.turn:
            app.currentPiece = app.player
            checkJail(app, app.player)
            app.turn = False
        else:
            app.currentPiece = app.ai
            checkJail(app, app.ai)
            app.turn = True
    pass

def getPropertyFromPixels(app, x, y):
    side = None
    index = None
    if (app.height-app.margin-app.cellHeight) < y < (app.height-app.margin):
        side = app.boardBottom
        for i in range(len(app.boardBottom)):
            if ((app.height-app.margin-app.cellHeight-app.cellWidth*(i+1)) < x
            < (app.height-app.margin-app.cellHeight-app.cellWidth*(i))):
                index = i
                return side[index]
    if app.margin < y < app.margin+app.cellHeight:
        side = app.boardTop
        for i in range(len(app.boardTop)):
            if (app.margin+app.cellHeight+app.cellWidth*(i) < x 
            < app.margin+app.cellHeight+app.cellWidth*(i+1)):
                index = i
                return side[index]
    if app.margin < x < app.margin+app.cellHeight:
        side = app.boardLeft
        for i in range(len(app.boardLeft)):
            if (app.height-app.margin-app.cellHeight-app.cellWidth*(i+1) < y 
            < app.height-app.margin-app.cellHeight-app.cellWidth*(i)):
                index = i
                return side[index]
    if (app.margin+app.cellHeight+(app.cellWidth*6) < x 
    < app.margin+(app.cellHeight*2)+(app.cellWidth*6)):
        side = app.boardRight
        for i in range(len(app.boardRight)):
            if (app.margin+app.cellHeight+app.cellWidth*i < y <
            app.margin+app.cellHeight+app.cellWidth*(i+1)):
                index = i
                return side[index]
    return None

def mousePressed(app, event):
    #click on properties to view their card (and stats)
    if app.gameOver or app.moving: return
    temp = getPropertyFromPixels(app, event.x, event.y)
    if isinstance(temp, str):
        app.card = None
    if app.build: #click a property to build
        if temp.getColor() in app.currentPiece.getMonopoly():
            temp.build()
            app.build = False
            finishTurnInstructions(app)
    elif app.card == temp:
        app.card = None
    else:
        app.card = temp
    pass

def timerFired(app):
    #ends game after 20 minutes if no one has gone bankrupt yet
    if (time.time()-app.start > 1200 or app.player.getMoney() <= 0 or 
    app.ai.getMoney() <= 0):
        app.gameOver = True
        app.instructions == 'Game Over'
        if app.player.getMoney() > app.ai.getMoney():
            app.winner = app.player
        elif app.ai.getMoney() > app.player.getMoney():
            app.winner = app.ai
    elif app.moving:
        if time.time()-app.time > 0.25:
            app.time = time.time()
            if app.moves != 0:
                movePiece(app, app.currentPiece)
                app.moves -= 1
            else:
                app.moving = False
                getSquareFromPosition(app, app.currentPiece, 
                app.currentPiece.getSide(), app.currentPiece.getIndex())
    pass

def rgbString(r, g, b):
    #from: https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
    return f'#{r:02x}{g:02x}{b:02x}'

def drawSide(app, canvas, square, side, x1, y1, x2, y2):
    canvas.create_rectangle(x1, y1, x2, y2, width=3)
    if square == 'Chance':
        canvas.create_text((x1+x2)/2, (y1+y2)/2, anchor='center', text="CHANCE",
        font=f'Courier {app.text}')
    elif square == "Magic Tax":
        canvas.create_text((x1+x2)/2, (y1+y2)/2, anchor='center', 
        text="Magic\nTax", font=f'Courier {app.text}')
    else:
        propertyName = square.getName()
        propertyName = propertyName.replace(' ', '\n')
        canvas.create_text((x1+x2)/2, (y1+y2)/2, anchor='center', 
        text=propertyName, font=f'Courier {app.text}')
        color = square.getColor()
        if side == 'left':
            canvas.create_rectangle(x2-app.margin, y1, x2, y2, fill = color)
            if square in app.player.getProperties():
                canvas.create_rectangle(x1, y1, x1+app.margin, y2, 
                fill = 'white')
            elif square in app.ai.getProperties():
                canvas.create_rectangle(x1, y1, x1+app.margin, y2, 
                fill = 'black')
        elif side == 'right':
            canvas.create_rectangle(x1, y1, x1+app.margin, y2, fill = color)
            if square in app.player.getProperties():
                canvas.create_rectangle(x2-app.margin, y1, x2, y2, 
                fill = 'white')
            elif square in app.ai.getProperties():
                canvas.create_rectangle(x2-app.margin, y1, x2, y2, 
                fill = 'black')
        elif side == 'top':
            canvas.create_rectangle(x1, y2-app.margin, x2, y2, fill = color)
            if square in app.player.getProperties():
                canvas.create_rectangle(x1, y1, x2, y1+app.margin, 
                fill = 'white')
            elif square in app.ai.getProperties():
                canvas.create_rectangle(x1, y1, x2, y1+app.margin, 
                fill = 'black')
        else:
            canvas.create_rectangle(x1, y1, x2, y1+app.margin, fill = color)
            if square in app.player.getProperties():
                canvas.create_rectangle(x1, y2-app.margin, x2, y2, 
                fill = 'white')
            elif square in app.ai.getProperties():
                canvas.create_rectangle(x1, y2-app.margin, x2, y2, 
                fill = 'black')
        

def drawBoard(app, canvas):
    monopolyGreen = rgbString(204, 255, 204)

    canvas.create_rectangle(app.margin, app.margin, app.height-app.margin,
    app.height-app.margin, width = 5, fill = monopolyGreen)

    canvas.create_rectangle(app.cellHeight+app.margin, 
    app.cellHeight+app.margin, app.height-app.cellHeight-app.margin, 
    app.height-app.cellHeight-app.margin, width = 3)

    canvas.create_text(app.height/2, app.height/2-app.margin, 
    text = "FANTASY  MONOPOLY", anchor = "center", 
    font = f"Helectiva {int(app.text*5/2)} bold", fill = 'purple4')

    for i in range(len(app.boardBottom)):
        drawSide(app, canvas, app.boardBottom[i], 'bottom',
        app.height-app.margin-app.cellHeight-app.cellWidth*(i+1), 
        app.height-app.margin-app.cellHeight, 
        app.height-app.margin-app.cellHeight-app.cellWidth*(i), 
        app.height-app.margin)
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
    playerSide = app.player.getSide()
    playerIndex = app.player.getIndex()
    x1, y1, x2, y2 = getPixelsFromPosition(app, playerSide, playerIndex)
    canvas.create_oval(x1, y1, x1+2*app.radius, y1+2*app.radius, fill = 'white')
    aiSide = app.ai.getSide()
    aiIndex = app.ai.getIndex()
    v1, w1, v2, w2 = getPixelsFromPosition(app, aiSide, aiIndex)
    canvas.create_oval(v2, w2, v2-2*app.radius, w2-2*app.radius, fill = 'black')

def drawGameOver(app, canvas):
    if app.gameOver:
        color = 'red'
        if app.winner == None:
            canvas.create_text(app.height/2, app.height/2+int(app.text*2), 
            text = "Tie!", anchor = "n", 
            font = f"Helectiva {int(app.text*2)}", fill = color)
        else:
            canvas.create_text(app.height/2, app.height/2+int(app.text*2), 
            text = f"{app.winner.getName()} Wins!", anchor = "n", 
            font = f"Helectiva {int(app.text*2)}", fill = color)

def drawStats(app, canvas):
    piece = app.currentPiece.getName()

    #draw Money
    playerMoney = str(app.player.getMoney())
    aiMoney = str(app.ai.getMoney())
    canvas.create_text((app.width-app.height)/2+app.height, app.margin*2, 
    font = f"Courier {int(app.text*2)}", anchor = 'c',
    text = f'Player: ${playerMoney}', fill = 'purple4')
    canvas.create_text((app.width-app.height)/2+app.height, 
    app.margin*2+int(app.text*4), 
    font = f"Courier {int(app.text*2)}", anchor = 'c',
    text = f'AI: ${aiMoney}', fill = 'purple4')
    
    #draw Instructions
    canvas.create_rectangle(app.margin*4+app.height, 
    app.margin*2+int(app.text*10),
    app.width-app.margin*4, app.margin*2+int(app.text*12), fill = 'red4',
    width = 2)
    canvas.create_text((app.width-app.height)/2+app.height, 
    app.margin*2+int(app.text*11), font = f"Courier {int(app.text*1.5)}",
    anchor = 'c', text = 'Instructions', fill = 'white')
    canvas.create_rectangle(app.margin*4+app.height, 
    app.margin*2+int(app.text*12),
    app.width-app.margin*4, app.margin*2+int(app.text*16), width = 2)
    canvas.create_text((app.width-app.height)/2+app.height, 
    app.margin*2+int(app.text*14), font = f"Helectiva {int(app.text*1.5)}",
    anchor = 'c', text = app.instructions)

    #draw Comments
    canvas.create_rectangle(app.margin*4+app.height, 
    app.margin*2+int(app.text*18),
    app.width-app.margin*4, app.margin*2+int(app.text*20), fill = 'black',
    width = 2)
    canvas.create_text((app.width-app.height)/2+app.height, 
    app.margin*2+int(app.text*19), font = f"Courier {int(app.text*1.5)}",
    anchor = 'c', text = f"{piece}'s Turn", fill = 'white')
    canvas.create_rectangle(app.margin*4+app.height, 
    app.margin*2+int(app.text*20),
    app.width-app.margin*4, app.margin*2+int(app.text*24), width = 2)
    if app.moving == True:
        canvas.create_text((app.width-app.height)/2+app.height, 
        app.margin*2+int(app.text*22), 
        font = f"Helectiva {int(app.text*1.5)}",
        anchor = 'c', text = f'{piece} rolled a {app.d1} and {app.d2}!')
    elif app.comment != None:
        canvas.create_text((app.width-app.height)/2+app.height, 
        app.margin*2+int(app.text*22), 
        font = f"Helectiva {int(app.text*1.5)}",
        anchor = 'c', text = app.comment)

def drawCardDisplay(app, canvas):
    if app.card != None:
        canvas.create_rectangle(app.margin*4+app.height, app.height/2, 
        app.width-app.margin*4, app.height-app.margin, width = 2,
        fill = 'white smoke')
        canvas.create_rectangle(app.margin*4+app.height, app.height/2, 
        app.width-app.margin*4, app.height/2+3*app.margin, width = 2,
        fill = app.card.getColor())
        if app.card.getColor() in ['blue', 'purple', 'green']:
            nameColor = 'white'
        else:
            nameColor = 'black'
        canvas.create_text((app.margin*4+app.height+app.width-app.margin*4)/2,
        app.height/2+1.5*app.margin, text = app.card.getName(), 
        font = f"Helectiva {int(app.text*2)} bold", fill = nameColor)

        canvas.create_text((app.margin*4+app.height+app.width-app.margin*4)/2,
        app.height/2+4*app.margin, anchor = 'n',
        text = f'''Rent: ${str(app.card.original)}
        \nWith 1 House: ${str(app.card.levelRent(1))}
        \nWith 2 Houses: ${str(app.card.levelRent(2))}
        \nWith 3 Houses: ${str(app.card.levelRent(3))}
        \nWith a Hotel: ${str(app.card.levelRent(4))}
        \n\nCost of Property: ${str(app.card.cost)}
        \nCost of Building: ${str(app.card.houseCost)}
        \nCurrent Level: {app.card.getLevel()}''', 
        font = f'Courier {int(8*app.text/7)}')

def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawPieces(app, canvas)
    drawStats(app, canvas)
    drawCardDisplay(app, canvas)
    drawGameOver(app, canvas)

def runMonopoly():
    runApp(width=1255, height=725)
    
runMonopoly()