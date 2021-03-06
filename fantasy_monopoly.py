#Cindy Xiong (cindyxio)
#CMU 15-112 Term Project (Monopoly (Fantasy ver.)) Main File

from cmu_112_graphics_monopoly import *
import tkinter as tk
import random, math, time
from piece import *
from property import *
from words import *

def appStarted(app):
    app.margin = 20
    app.cellHeight = (app.height-2*app.margin)/6
    app.cellWidth = app.cellHeight*2/3
    app.text = int(app.height//60)
    app.radius = app.text
    app.fauna = Property('Fauna Court', 150, 17, '+100', 
    'green')
    app.cecile = Property('Cecile Circle', 70, 5, '+50', 'green')
    app.dream = Property("Dream Loop", 314, 13, '*2.5', 'green')
    app.dragon = Property('Dragon Trail', 400, 25, '*2', 'purple')
    app.fae = Property('Fae Avenue', 100, 15, '*1.75', 'purple')
    app.elven = Property('Elven Place', 500, 50, '*1.9', 'purple')
    app.seer = Property('Seer Terrace', 220, 35, '+60', 'red')
    app.oracle = Property('Oracle Way', 150, 15, '*1.5', 'red')
    app.mermaid = Property('Mermaid Beach', 50, 10, '+15', 'blue')
    app.coral = Property('Coral Lane', 150, 15, '*1.5', 'blue')
    app.deity = Property('Deity Run', 400, 25, '*2', 'yellow')
    app.sunset = Property('Sunset Drive', 220, 35, '+60', 
    'yellow')
    app.witch = Property('Witch Street', 220, 35, '+60', 
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
    app.properties = [app.dream, app.fauna, app.cecile, app.sunset, app.deity,
    app.mythical, app.witch, app.oracle, app.seer, app.coral, app.mermaid, 
    app.fae, app.elven, app.dragon]
    for prop in app.properties:
        prop.calcPropertyPoints()

    app.gameOver = False
    app.turn = False #is True when it's the player's turn
    app.instructions = "Press 'Space' to Roll" #holds the instructions
    app.comment = "Welcome to Fantasy Monopoly!" #holds the current comment
    app.card = None #holds the currently displayed card
    app.buy = False #is True if a buy is currently taking place
    app.trade = False #is True if a trade is currently taking place
    app.offer = 0 #the offering price for a trade
    app.offerPending = False #is True if trade offer is being considered
    app.trading = [] #the two properties being traded
    app.sell = False #is True if a sell is currently taking place
    app.build = False #is True if building is currently taking place
    app.cont = False #is True if player decides to act on a property
    app.moving = False #is True when pieces are moving across board (takes no 
    #user input then)
    app.rules = False #is True when you want to view the rules
    app.moves = 0
    app.d1 = 0
    app.d2 = 0
    app.start = time.time()
    app.count = 1200 - int(time.time()-app.start)
    app.time = time.time()
    app.player = Piece('Player')
    app.ai = Piece('AI')
    app.aiMoney = app.ai.getMoney()
    app.currentPiece = app.player
    app.currentProperty = None
    app.winner = None

def finishTurnInstructions(app):
    if app.currentPiece == app.player:
        app.instructions = "Press 'Space' to Finish Turn"
    else:
        app.instructions = "Press 'Space' to Roll"
        
def aiBuy(app):
    if app.currentProperty.getPoints() > 35:
        if (len(app.ai.getProperties()) < 3 or 
        app.currentProperty.getPoints() > 70) and (app.currentProperty.getCost() 
        < app.aiMoney):
            app.ai.addProperty(app.currentProperty)
            app.ai.subtractMoney(app.currentProperty.getCost())
            app.comment += f'\nAI bought {app.currentProperty.getName()}!'
            return True
    app.comment += f'\nAI passed on {app.currentProperty.getName()}!'
    return False

def aiTrade(app):
    if app.player.getProperties() != [] and app.ai.getProperties() != []:
        if app.trade:
            if app.trading[0] in app.ai.getProperties():
                ownProp = app.trading[0]
                oppProp = app.trading[1]
            else:
                ownProp = app.trading[1]
                oppProp = app.trading[0]
            if ownProp.getPoints() < (oppProp.getPoints()+app.offer/10):
                app.cont = True
                app.comment = "Trade completed!"
            else:
                app.comment = "Trade declined..."
            tradeProperty(app) 
        else: #should enter this first when aiTrade is called
            for playerOwn in app.player.getProperties():
                if playerOwn.getPoints() > 100:
                    worstPoints = 300
                    worstProp = None
                    for aiOwn in app.ai.getProperties():
                        if worstPoints > aiOwn.getPoints():
                            worstPoints = aiOwn.getPoints()
                            worstProp = aiOwn
                    if worstPoints+50 < playerOwn.getPoints():
                        app.trading.append(playerOwn)
                        app.trading.append(worstProp)
                        app.offer = playerOwn.getPoints()-worstPoints
                        if app.aiMoney-app.offer <= 100:
                            app.offer = 0
                        app.currentPiece = app.player
                        app.trade = True
                        app.turn = True
                        tradeOffer(app)
                        return True
        return False

def tradeOffer(app): #called for player to view trade offer by AI
    app.offerPending = True
    ownProp = None
    oppProp = None
    if app.trading[0] in app.currentPiece.getProperties():
        ownProp = app.trading[0]
        oppProp = app.trading[1]
    else:
        ownProp = app.trading[1]
        oppProp = app.trading[0]
    app.instructions = "Press 'Y' to Accept and 'N' to Decline Offer"
    app.comment += f"\nOffer of ${app.offer} and {oppProp.getName()} for {ownProp.getName()}."
    #goes to keyPressed

def aiSell(app):
    if app.ai.getProperties() != []:
        if app.aiMoney < 250:
            worstPoints = 300
            worstProp = None
            for aiOwn in app.ai.getProperties():
                if worstPoints > aiOwn.getPoints():
                    worstPoints = aiOwn.getPoints()
                    worstProp = aiOwn
            app.ai.removeProperty(worstProp)
            app.ai.addMoney(worstProp.getCost()//2)
            app.comment += f"\nAI sold {worstProp.getName()}!"
            return True
        for aiOwn in app.ai.getProperties():
            if aiOwn.getPoints() < -20:
                app.ai.removeProperty(aiOwn)
                app.ai.addMoney(aiOwn.getCost()//2)
                app.comment += f"\nAI sold {aiOwn.getName()}!"
                return True
    return False

def aiBuild(app):
    if app.ai.getMonopoly() != []:
        color  = random.choice(app.ai.getMonopoly())
        for aiOwn in app.ai.getProperties():
            bestPoints = -300
            bestProp = None
            if (bestProp == None and aiOwn.getColor() == color 
            and aiOwn.getLevel() != 'Hotel'):
                bestPoints = aiOwn.getPoints()
                bestProp = aiOwn
            elif (aiOwn.getColor() == color and aiOwn.getPoints() > bestPoints 
            and aiOwn.getLevel() != 'Hotel'):
                bestPoints = aiOwn.getPoints()
                bestProp = aiOwn
        if (bestProp.getPoints() > 50 and bestProp.getLevel() != 'Hotel' and 
        bestProp.houseCost < app.aiMoney-50):
            bestProp.build()
            app.ai.subtractMoney(bestProp.houseCost)
            app.comment += f"\nAI built on {bestProp.getName()}!"
            return True
    return False

def aiDecisionMaker(app):
    if app.currentPiece == app.player: return 
    if app.buy:
        buy = aiBuy(app)
        if buy:
            checkMonopoly(app, app.currentPiece)
            checkPropertyState(app)
        app.buy = False
    #Note: AI can only choose to sell/trade/build once per turn
    sell = aiSell(app)
    checkMonopoly(app, app.ai)
    if sell == False: 
        build = aiBuild(app)
    if (sell == False and build == False):
        trade = aiTrade(app)
    if app.trade == False:
        finishTurnInstructions(app)

def checkPropertyState(app): 
    #checks which properties are owned by who and adjusts all points that 
    # let AI make its decisions
    for prop in app.properties:
        prop.calcPropertyPoints()
        c1 = 0
        for aiOwn in app.ai.getProperties():
            if aiOwn.getColor() == prop.getColor() and aiOwn != prop:
                c1 += 1
        prop.calcAiPoints(c1)
        c2 = 0
        for playerOwn in app.player.getProperties():
            if playerOwn.getColor() == prop.getColor() and playerOwn != prop:
                c2 += 1
        prop.calcPlayerPoints(c2)

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

def getSquareFromPixels(app, x, y): #identifies the square
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

def getSquareFromPosition(app): #identifies the square and calls appropriate results
    side = app.currentPiece.getSide()
    i = app.currentPiece.getIndex()
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
    if isinstance(square, Property) == False:
        app.currentProperty = None
        if square == 'Chance':
            chanceCard(app)
        else:
            if square == 'GO!':
                app.comment = 'Gain $200 for your Travels!'
            if square == 'JAIL' and app.currentPiece.getJailTurns() == 0:
                app.comment = 'Just visiting Jail!'
            if square == 'Free Parking':
                app.comment = 'Taking a break!'
            if square == 'Go to Jail!':
                app.comment = 'Go to Jail!'
                app.currentPiece.goToJail()
            if square == 'Magic Tax':
                app.comment = 'Magic Tax: $200 vanished!'
                app.currentPiece.subtractMoney(200)
            if app.currentPiece == app.ai:
                aiDecisionMaker(app)
            else:
                finishTurnInstructions(app)
    else:
        app.currentProperty = square
        app.card = square
        app.comment = f'Landed on {app.currentProperty.getName()}!'
        landOnProperty(app, app.currentProperty)

def roll(app): #rolls two random die and sets up movement of piece
    app.d1 = random.randint(1, 6)
    app.d2 = random.randint(1, 6)
    app.moves = app.d1+app.d2
    app.moving = True
    app.time = time.time()

def movePiece(app): #moves piece forward by one step
    side = app.currentPiece.getSide()
    sideIndex = app.order.index(side)
    index = app.currentPiece.getIndex()
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
        app.currentPiece.addMoney(200)
    app.currentPiece.changePosition((side, index))

def landOnProperty(app, prop): #what happens when you land on property
    if prop in app.currentPiece.getProperties():
        if app.currentPiece == app.ai:
            aiDecisionMaker(app)
        finishTurnInstructions(app)
    else:
        if app.currentPiece == app.player:
            if prop in app.ai.getProperties():
                app.player.subtractMoney(prop.getRent())
                app.ai.addMoney(prop.getRent())
                app.comment = app.comment+f'\nPaid ${prop.getRent()} in rent!'
            else:
                app.buy = True
                app.instructions = "Press 'Y' to Buy and 'N' to Pass"
        elif app.currentPiece == app.ai:
            if prop in app.player.getProperties():
                app.ai.subtractMoney(prop.getRent())
                app.player.addMoney(prop.getRent())
                app.comment = app.comment+f'\nPaid ${prop.getRent()} in rent!'
                aiDecisionMaker(app)
            else:
                app.buy = True
                aiDecisionMaker(app)

def buyProperty(app, prop): #called to buy property
    if app.cont:
        app.currentPiece.addProperty(prop)
        app.currentPiece.subtractMoney(prop.getCost())
        checkMonopoly(app, app.currentPiece)
        app.buy = False
        app.cont = False
    if app.buy == False:
        finishTurnInstructions(app)

def tradeProperty(app): #called to trade properties
    ownProp = None
    oppProp = None
    if app.trading[0] in app.currentPiece.getProperties():
        ownProp = app.trading[0]
        oppProp = app.trading[1]
    else:
        ownProp = app.trading[1]
        oppProp = app.trading[0]
    if app.cont:
        app.offerPending = False
        app.cont = False
        app.currentPiece.addMoney(app.offer)
        app.currentPiece.addProperty(oppProp)
        app.currentPiece.removeProperty(ownProp)
        if app.currentPiece == app.ai:
            oppPiece = app.player
        else:
            oppPiece = app.ai
        oppPiece.subtractMoney(app.offer)
        oppPiece.addProperty(ownProp)
        oppPiece.removeProperty(oppProp)
    if app.offerPending == False:
        if app.currentPiece == app.ai:
            app.currentPiece = app.player
            app.turn = True
        else:
            app.currentPiece = app.ai
            app.turn = False
        app.offer = 0
        app.trade = False
        app.trading = []
        finishTurnInstructions(app)

def chanceCard(app): #what happens when you land on chance
    cards = ['Go to Jail', 'Materialize $50', 'Teleport to Go', 
    'Materialize $200', 'Go to Jail', 'Teleport to Witch Street', 
    'Teleport to Fauna Court', '$15 vanished', '$50 vanished']
    cardIndex = random.randint(0, len(cards)-1)
    app.comment = f'Chance: {cards[cardIndex]}!'
    if cards[cardIndex] == 'Go to Jail':
        app.currentPiece.goToJail()
        finishTurnInstructions(app)
    splitCard = cards[cardIndex].split(' ')
    if splitCard[0] == 'Teleport':
        if splitCard[len(splitCard)-1] == "Go":
            app.currentPiece.changePosition(('right', 6))
            app.currentPiece.addMoney(200)
            finishTurnInstructions(app)
        else:
            if splitCard[len(splitCard)-2] == "Fauna":
                app.currentPiece.changePosition(('bottom', 1))
                app.currentProperty = app.boardBottom[1]
                landOnProperty(app, app.currentProperty)
            else:
                app.currentPiece.changePosition(('left', 5))
                app.currentProperty = app.boardLeft[5]
                landOnProperty(app, app.currentProperty)
    else:
        if splitCard[0] == 'Materialize':
            money = int(splitCard[1][1:])
            app.currentPiece.addMoney(money)
        elif splitCard[len(splitCard)-1] == "vanished":
            money = int(splitCard[0][1:])
            app.currentPiece.subtractMoney(money)
        finishTurnInstructions(app)
    if app.currentPiece == app.ai:
        aiDecisionMaker(app)

def checkTradingIsLegal(app):
    if app.trading[0] in app.player.getProperties():
        if app.trading[1] in app.ai.getProperties():
            return True
    if app.trading[1] in app.player.getProperties():
        if app.trading[0] in app.ai.getProperties():
            return True
    else:
        app.trading = []
        return False

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
    for color in piece.getMonopoly():
        if colorDict[color] <= 2:
            if color == 'green' and color == 'purple':
                piece.unmonopolize(color)
            else:
                if colorDict[color] < 2:
                    piece.unmonopolize(color)

def checkJail(app):
    if app.currentPiece.getJailTurns() == 0:
        roll(app)
        checkMonopoly(app, app.currentPiece)
    else:
        app.currentPiece.inJail()
        if app.currentPiece.getJailTurns() == 0:
            app.comment = 'Paid $50 to leave Jail!'
            app.currentPiece.subtractMoney(50)
        else:
            app.comment = 'Still in Jail!'
        finishTurnInstructions(app)

def keyPressed(app, event):
    #press t to trade
    #press b to build
    #press s to sell
    #press r to view Monopoly Rules
    if app.moving: return
    if app.gameOver:
        if event.key == "Space":
            appStarted(app)
    else:
        if event.key == "R" or event.key == "r": #additional rules appear
            app.rules = not app.rules
        if app.buy and app.turn: #player chooses whether to buy
            if event.key == "Y" or event.key == "y":
                app.cont = True
            if event.key == "N" or event.key == "n":
                app.buy = False
            buyProperty(app, app.currentProperty)
        elif ((event.key == "S" or event.key == "s") and 
        app.currentPiece.getProperties() != None and app.sell == False 
        and app.turn): #player initiates sell
            app.sell = True
            app.instructions = "Click a Property to Sell"
        elif ((event.key == "T" or event.key == "t") and 
        app.ai.getProperties() != [] and app.player.getProperties() != [] 
        and app.trade == False and app.turn): #player initiates trade
            app.trade = True
            app.instructions = "Click Properties to Trade"
        elif app.trade and app.cont and app.turn: #player chooses additional offer
            if event.key == "Enter":
                app.currentPiece = app.ai
                app.cont = False
                aiTrade(app)
            elif event.key == "Up" or event.key == "Right" and (app.offer <= 
            app.player.getMoney()):
                app.offer += 10
                app.comment = f"How much will you offer in addition? ${app.offer}"
            elif (event.key == "Down" or event.key == "Left") and app.offer > 0:
                app.offer -= 10
                app.comment = f"How much will you offer in addition? ${app.offer}"
        elif app.offerPending and app.turn: #when player is given offer by AI
            if event.key == "Y" or event.key == "y":
                app.cont = True
                app.comment = "Trade completed!"
            if event.key == "N" or event.key == "n":
                app.offerPending = False
                app.comment = "Trade declined..."
            tradeProperty(app)
        elif ((event.key == 'b' or event.key == 'B') and 
        app.currentPiece.getMonopoly() != [] and app.build == False 
        and app.turn): #initiates build
            app.build = True
            app.instructions = 'Click a Property to Build'
        elif event.key == 'Space':
            app.card = None
            if app.turn == False:
                app.turn = True
                app.currentPiece = app.player
                checkJail(app)
            else:
                app.turn = False
                app.currentPiece = app.ai
                checkJail(app)

def mousePressed(app, event):
    #click on properties to view their card (and stats)
    if app.gameOver or app.moving: return None
    temp = getSquareFromPixels(app, event.x, event.y)
    if isinstance(temp, Property) == False:
        app.card = None
        return None
    if app.build: #click a property to build
        if (temp.getColor() in app.currentPiece.getMonopoly() and 
        temp.getLevel() != 'Hotel'):
            temp.build()
            app.currentPiece.subtractMoney(temp.houseCost)
            app.build = False
            finishTurnInstructions(app)
    if app.sell: #click a property to sell
        if temp in app.currentPiece.getProperties():
            app.currentPiece.removeProperty(temp)
            app.currentPiece.addMoney(temp.getCost()//2)
            checkMonopoly(app, app.currentPiece)
            app.sell = False
            finishTurnInstructions(app)
    if app.trade and (app.cont == False): #click two properties to sell
        if temp in app.ai.getProperties() or temp in app.player.getProperties():
            app.trading.append(temp)
            if len(app.trading) == 1:
                app.comment = f"Trading... {app.trading[0].getName()}"
            if len(app.trading) == 2:
                check = checkTradingIsLegal(app)
                if check:
                    app.cont = True
                else:
                    app.instructions = "Try Again"
            if app.cont: #goes to keyPressed
                app.instructions = "Change Offer With Arrows; Press 'Enter' when Done"
                app.comment = f"How much will you offer in addition? ${app.offer}"
    if app.card == temp:
        app.card = None
    else:
        app.card = temp

def timerFired(app):
    #ends game after 20 minutes if no one has gone bankrupt yet
    if (time.time()-app.start > 1200 or app.player.getMoney() <= 0 or 
    app.ai.getMoney() <= 0):
        app.instructions == 'Game Over!'
        app.count = 0
        app.rules = False
        if app.player.getMoney() > app.ai.getMoney():
            app.winner = app.player
        elif app.ai.getMoney() > app.player.getMoney():
            app.winner = app.ai
        if app.winner == None:
            app.comment = 'Tie!'
        else:
            app.comment = f'{app.winner.getName()} Wins!'
        app.gameOver = True
        app.instructions = "Press 'Space' to Restart Game!"
    #moves the piece the rolled amount of times on the board
    elif app.moving:
        if time.time()-app.time > 0.25:
            app.time = time.time()
            if app.moves != 0:
                movePiece(app)
                app.moves -= 1
            else:
                app.moving = False
                getSquareFromPosition(app)
    else:
        app.count = int(1200-(time.time()-app.start))
    #checks the AI's money to adjust points
    if app.ai.getMoney() != app.aiMoney:
        diff = app.ai.getMoney()-app.aiMoney
        pts = diff//10 #1 AI point = $10 of AI money
        for prop in app.properties:
            prop.addPoints(pts)
        app.aiMoney = app.ai.getMoney()
    #calls function to check state of each property and adjust points
    checkPropertyState(app)

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

def drawMoneyAndTime(app, canvas):
    if app.rules: return
    playerMoney = str(app.player.getMoney())
    aiMoney = str(app.ai.getMoney())
    canvas.create_text((app.width-app.height)/2+app.height, app.margin*2, 
    font = f"Courier {int(app.text*2)}", anchor = 'c',
    text = f'Player: ${playerMoney}', fill = 'purple4')
    canvas.create_text((app.width-app.height)/2+app.height, 
    app.margin*2+int(app.text*3), 
    font = f"Courier {int(app.text*2)}", anchor = 'c',
    text = f'AI: ${aiMoney}', fill = 'purple4')
    canvas.create_text((app.width-app.height)/2+app.height, 
    app.margin*2+int(app.text*6), 
    font = f"Courier {int(app.text*1.5)}", anchor = 'c',
    text = f'Time: {app.count}s', fill = 'red')
    
def drawInstructions(app, canvas):
    if app.rules: return
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
    app.margin*2+int(app.text*14), font = f"Helectiva {int(app.text*1.25)}",
    anchor = 'c', text = app.instructions)

def drawComment(app, canvas):
    if app.rules: return
    piece = app.currentPiece.getName()
    canvas.create_rectangle(app.margin*4+app.height, 
    app.margin*2+int(app.text*18),
    app.width-app.margin*4, app.margin*2+int(app.text*20), fill = 'black',
    width = 2)
    canvas.create_text((app.width-app.height)/2+app.height, 
    app.margin*2+int(app.text*19), font = f"Courier {int(app.text*1.5)}",
    anchor = 'c', text = f"{piece}'s Turn", fill = 'white')
    canvas.create_rectangle(app.margin*4+app.height, 
    app.margin*2+int(app.text*20),
    app.width-app.margin*4, app.margin*2+int(app.text*26), width = 2)
    if app.moving == True:
        canvas.create_text((app.width-app.height)/2+app.height, 
        app.margin*2+int(app.text*23), 
        font = f"Helectiva {int(app.text*1.25)}",
        anchor = 'c', text = f'{piece} rolled a {app.d1} and {app.d2}!')
    elif app.comment != None:
        if app.gameOver:
            color = 'red'
        else:
            color = 'black'
        canvas.create_text((app.width-app.height)/2+app.height, 
        app.margin*2+int(app.text*23), 
        font = f"Helectiva {int(app.text*1.25)}",
        anchor = 'c', text = app.comment, fill = color)

def drawGameNotes(app, canvas):
    if app.rules: return
    canvas.create_rectangle(app.margin*4+app.height, app.height/2, 
    app.width-app.margin*4, app.height-app.margin, width = 2,
    fill = 'white smoke')
    canvas.create_rectangle(app.margin*4+app.height, app.height/2, 
    app.width-app.margin*4, app.height/2+3*app.margin, width = 2, 
    fill = 'black')
    canvas.create_text((app.height+app.width)/2,
    app.height/2+1.5*app.margin, text = "Game Notes", 
    font = f"Helectiva {int(app.text*2)} bold", fill = 'white')
    canvas.create_text((app.height+app.width)/2,
    app.height/2+3*app.margin, anchor = 'n',
    text = gameNotesText(), 
    font = f'Courier {int(app.text)}')

def drawCardDisplay(app, canvas):
    if app.gameOver == False and app.rules == False:
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
            canvas.create_text((app.height+app.width)/2,
            app.height/2+1.5*app.margin, text = app.card.getName(), 
            font = f"Helectiva {int(app.text*2)} bold", fill = nameColor)

            canvas.create_text((app.height+app.width)/2,
            app.height/2+4*app.margin, anchor = 'n',
            text = f'''Rent: ${str(app.card.getOriginalRent())}
            \nWith 1 House: ${str(app.card.levelRent(1))}
            \nWith 2 Houses: ${str(app.card.levelRent(2))}
            \nWith 3 Houses: ${str(app.card.levelRent(3))}
            \nWith a Hotel: ${str(app.card.levelRent(4))}
            \n\nCost of Property: ${str(app.card.getCost())}
            \nCost of Building: ${str(app.card.houseCost)}
            \nCurrent Level: {app.card.getLevel()}''',
            #+ f'\nAI Points: {app.card.getPoints()}',
            #^ to view AI points for each property
            font = f'Courier {int(8*app.text/7)}')

def drawRules(app, canvas):
    if app.rules == False: return
    canvas.create_text((app.width-app.height)/2+app.height, app.margin*2, 
    font = f"Courier {int(app.text*2)} bold", anchor = 'c',
    text = f'Additional Rules and Features', fill = 'purple4')
    canvas.create_text((app.width-app.height)/2+app.height, app.margin*4, 
    font = f"Courier {int(app.text)}", anchor = 'n',
    text = rulesText())
    pass

def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawPieces(app, canvas)
    drawMoneyAndTime(app, canvas)
    drawInstructions(app, canvas)
    drawComment(app, canvas)
    drawGameNotes(app, canvas)
    drawCardDisplay(app, canvas)
    drawRules(app, canvas)

def runMonopoly():
    runApp(width=1255, height=725)
    
runMonopoly()