from Card import *
from Player import *
from Computer import *
from View import game_event
import random


class Model():
    def __init__(self):
        """ initializes deck, user and computer players, discard pile and sets reverse and turn to default values """
        self.deck = deckInit()
        self.discard = []
        self.reverse = False

        player_hand = []
        computer_hand = []
        random.shuffle(self.deck)
        for i in range(7):
            player_hand.append(self.deck.pop(0))
            computer_hand.append(self.deck.pop(0))
        self.player = Player(player_hand)
        self.computer = Computer(computer_hand)
        self.players = [self.player, self.computer]
        self.turn = 0

        self.discard.append(self.deck.pop(0))
        self.top_card = self.discard[0]

    def getComputerHands(self):
        """ returns list of number of cards the computer players have """
        return_list = []
        for player in self.players:
            if isinstance(player, Computer):
                return_list.append(len(player.getHand()))
        return return_list

    def addPlayers(self, num_computer_players):
        """ add 1 or 2 computer players """
        new_hand = []
        for i in range(7):
            new_hand.append(self.deck.pop(0))
        computer1 = Computer(new_hand)
        self.players.append(computer1)
        if num_computer_players == 2:
            new_hand = []
            for i in range(7):
                new_hand.append(self.deck.pop(0))
            computer2 = Computer(new_hand)
            self.players.append(computer2)

    def setGameDifficulty(self, diff):
        """ sets difficulty of the computer player(s) """
        for p in self.players:
            if p != self.player:
                p.setDifficulty(diff)

    def getPlayer(self):
        """ returns value that tells controller if the game is over (who won) or whose turn it is """
        for i in self.players:
            if len(i.getHand()) == 0:
                if i == self.player:
                    return "user_won"
                else:
                    return "computer_won"
        if self.turn == 0:
            return "human"
        else:
            return "computer"

    def nextPlayer(self):
        """ computes whose turn it is next, reverse means it is going backward through the list """
        curr = self.turn
        if self.reverse:
            if curr == 0:
                self.turn = len(self.players) - 1
            else:
                self.turn = curr - 1
        else:
            if curr == len(self.players) - 1:
                self.turn = 0
            else:
                self.turn = curr + 1

    def callUno(self, curr_player):
        """ if player calls uno, determines validity of call """
        if len(curr_player.getHand()) == 1:
            curr_player.setUno(True)
        else:
            self.checkDeck()
            curr_player.addCard(self.deck.pop(0))
            curr_player.addCard(self.deck.pop(0))
            self.nextPlayer()

    def checkDeck(self):
        """ if the deck is less than four cards, it shuffles the discard into the bottom of the deck """
        if len(self.deck) < 4:
            self.discard.remove(self.top_card)
            if len(self.deck) + len(self.discard) < 4:
                new_deck = deckInit()
                if len(self.discard) > 0:
                    self.discard = self.discard + new_deck
                else:
                    self.discard = new_deck
            random.shuffle(self.discard)
            for card in self.discard:
                if card.action == "wild" or card.action == "wild_draw_4":
                    card.color = Color.Wild
            if len(self.deck) > 0:
                self.deck = self.deck + self.discard
            else:
                self.deck = self.discard
            self.discard = [self.top_card]

    def checkMove(self, card):
        """ verifies a user choice of card, returns True if it can be played or False if it can't, it also handles cards with actions"""
        self.checkDeck()
        if card is game_event.draw:
            self.player.addCard(self.deck.pop(0))
            self.player.setUno(False)
            return True

        if self.top_card.compatible(card):
            if len(self.player.getHand()) == 1 and not self.player.getUno():
                self.player.addCard(self.deck.pop(0))
                self.player.addCard(self.deck.pop(0))
                if card.action == "wild" or card.action == "wild_draw_4":
                    card.setWild(4)
                self.nextPlayer()
                return False
            self.discard.insert(0,card)
            self.player.removeCard(card)
            self.top_card = self.discard[0]
            if card.action == "wild":
                self.nextPlayer()
                return True
            elif card.action == "wild_draw_4":
                self.nextPlayer()
                for i in range(4):
                    self.players[self.turn].addCard(self.deck.pop(0))
                self.nextPlayer()
                return True
            elif card.action == "reverse":
                if len(self.players) > 2:
                    self.reverse = not self.reverse
                    self.nextPlayer()
                return True
            elif card.action == "draw_2":
                card1 = self.deck.pop(0)
                card2 = self.deck.pop(0)
                self.nextPlayer()
                self.players[self.turn].addCard(card1)
                self.players[self.turn].addCard(card2)
                self.nextPlayer()
                return True
            elif card.action == "skip":
                self.nextPlayer()
                self.nextPlayer()
                return True
            else:
                self.nextPlayer()
                return True
        else:
            return False

    def computerTurn(self):
        """ takes card from computer function and handles action cards """
        curr_player = self.players[self.turn]
        self.checkDeck()
        card = curr_player.play(self.top_card, self.nextPlayerHand(), len(self.players))
        if card is None:
            curr_player.addCard(self.deck.pop(0))
            curr_player.setUno(False)
        else:
            if curr_player.compCallUno():
                self.callUno(curr_player)
            if len(curr_player.getHand()) == 1 and not curr_player.getUno():
                curr_player.addCard(self.deck.pop(0))
                curr_player.addCard(self.deck.pop(0))
                self.nextPlayer()
                return True
            self.discard.insert(0, card)
            curr_player.hand.remove(card)
            self.top_card = self.discard[0]
            if card.action == "wild":
                color = Color(curr_player.chooseColor())
                card.color = color
                self.nextPlayer()
                return True
            elif card.action == "wild_draw_4":
                color = Color(curr_player.chooseColor())
                card.color = color
                self.nextPlayer()
                for i in range(4):
                    self.players[self.turn].addCard(self.deck.pop(0))
                self.nextPlayer()
                return True
            elif card.action == "reverse":
                if len(self.players) > 2:
                    self.reverse = not self.reverse
                    self.nextPlayer()
                return True
            elif card.action == "draw_2":
                self.nextPlayer()
                self.players[self.turn].addCard(self.deck.pop(0))
                self.players[self.turn].addCard(self.deck.pop(0))
                self.nextPlayer()
                return True
            elif card.action == "skip":
                self.nextPlayer()
                self.nextPlayer()
                return True
            else:
                self.nextPlayer()
                return True

    def nextPlayerHand(self):
        """ Returns how many cards the next player has """
        curr = self.turn
        if self.reverse:
            if curr == 0:
                return self.players[len(self.players) - 1].getHand()
            else:
                return self.players[curr - 1].getHand()
        else:
            if curr == len(self.players) - 1:
                return self.players[0].getHand()
            else:
                return self.players[curr + 1].getHand()
