#Cindy Xiong (cindyxio)
#The Additional Rules and Game Notes strings for Fantasy Monopoly

def rulesText():
    text = ''''Go!': Passing Go will cause the player to gain $200.
    \n\n'Jail':  If a player is sent to Jail, they will spend one turn 
    \nthere and then pay $50 to leave.
    \n\n'Magic Tax':  Landing on a magic tax square will cause $200 to vanish.
    \n\n'Chance':  Landing on a chance square will randomly pick 
    \nbetween a series of events.
    \n\n'Instructions':  The Instructions box tells the player what 
    \nthey should do next.
    \n\n'Comment':  The Comment box is below the Instructions and is 
    \ntitled with the current piece’s turn. It displays the current 
    \nhappenings of the game.
    \n\n'Game Notes/Card Display':  The Game Notes in the bottom right corner 
    \nwill always display useful information for the player to know.
    \nThe Game Notes will be replaced with the display of a Title Deed card 
    \nif a property is clicked. Clicking off the property or clicking 
    \nthe property again will cause Game Notes to reappear.
    \n\n'Buying':  To buy, you can press either “Y” or “N” to accept or 
    \ndecline when you land on an unowned property.
    \n\n'Rent':  Landing on someone else’s property will automatically 
    \ncause the current player to pay rent to the owner.'''
    return text

def gameNotesText():
    text = '''\nThe game ends in 20 minutes, \nor when a player goes bankrupt.
    \nClick on a property to view \nits information.
    \nBefore you finish your turn, you can:
    \n  - Press 's' to sell a property \n   (at half-price of original)\n   if you own properties.
    \n  - Press 't' to trade a property \n   if both players own properties.
    \n  - Press 'b' to build on a property \n   if you have a color monopoly.
    \nPress 'r' to view additional rules \nand features.'''
    return text