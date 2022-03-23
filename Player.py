class Player():

    def __init__(self, hand):
        """ Initializer for the Player class """
        self.hand = []
        self.hand = hand
        self.uno = False

    def addCard(self, card):
        """ Add a card to the player's hand """
        self.hand.append(card)

    def removeCard(self, card):
        """ Remove a card from the player's hand """
        self.hand.remove(card)
    
    def getHand(self):
        """ Return the player's hand """
        return self.hand

    def setUno(self, call):
        """ Change if player has called UNO """
        self.uno = call

    def getUno(self):
        """ Return if player has called UNO"""
        return self.uno