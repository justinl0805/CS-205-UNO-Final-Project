from enum import IntEnum


class Color(IntEnum):
    Red = 0
    Yellow = 1
    Green = 2
    Blue = 3
    Wild = 4


class Card():
    def __init__(self, color, symbol, action):
        """ Initializer for a Card """
        self.color = None
        self.color = Color(color)

        self.symbol = None
        self.symbol = symbol

        self.action = None
        self.action = action

    def compatible(self, card):
        """ Check if two cards match in an attribute (action, color) """
        if self.symbol == card.symbol or self.color == card.color:
            return True

        if card.action == "wild" or card.action == "wild_draw_4":
            return True

        if self.color == Color.Wild:
            return True

        return False

    def setWild(self, color):
        """ Function to change the color of a wild card """
        if Color(color):
            self.color = Color(color)
            return True
        else:
            return False

    """The following funtions were made for debugging purposes. They aren't used in the final product """

    def print(self):
        print(f"Symbol: {self.symbol}; Color: {self.color}; Action: {self.action}")

    def __str__(self):
        return f"Card color: {self.color}, symbol: {self.symbol}, action: {self.action}"

    def __repr__(self):
        return f"Card color: {self.color}, symbol: {self.symbol}, action: {self.action}"


def deckInit():
    """ Initializes the deck in the same order as the cards are in textures.png """
    deck = []

    for i in range(0, 4):
        for j in range(0, 10):
            deck.append(Card(Color(i), j, None))

        deck.append(Card(Color(i), 10, "skip"))
        deck.append(Card(Color(i), 11, "reverse"))
        deck.append(Card(Color(i), 12, "draw_2"))

    deck.append(Card(Color.Wild, "wild", "wild"))
    deck.append(Card(Color.Wild, "wild", "wild"))
    deck.append(Card(Color.Wild, "wild_draw_4", "wild_draw_4"))
    deck.append(Card(Color.Wild, "wild_draw_4", "wild_draw_4"))

    return deck
