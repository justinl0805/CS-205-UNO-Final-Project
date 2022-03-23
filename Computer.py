from typing import List, Dict

from Player import *
from Card import *
import random


class Computer(Player):
    def __init__(self, hand):
        self.chain_cards = False
        super().__init__(hand)
        self.difficulty = 1

    def play(self, discard, next_hand, num_players):
        """ Loops through the Computer's hand and plays the first compatible card """
        playable = []
        for card in self.hand:
            if discard.compatible(card):
                playable.append(card)

        if self.difficulty == 3:  # Hard, Monte Carlo tree traversal
            """
            Hard Difficulty AI: [Monte Carlo Tree Traversal]
            Build a tree given the current playable card options, which are root nodes for the trees
            The root nodes predict what cards will be played after it, and then those even further after it
            For each tree, choose the one that the computer finds most beneficial (ie. has the most cards for)

            Example Scenario:
            The computer chooses r0 from their playable cards
            The possible following cards are r0-9, r-action, wild, and any color with 9
            The computer predicts which card will be played for each option, thereby simulating all the choices
            The computer aggregates which cards will be played into a single value
            Repeat for all playable cards in the computer's hand
            Computer compares the value of each playable card and chooses the highest one
            """

            def monteCarloTreeSearch(hand: List[Card]):
                # No playable cards
                if len(hand) == 0:
                    return None

                options: Dict[Card, int] = {}
                # Loop through each playable card in the hand
                # We set up a dictionary to keep track of the "values" each card possesses
                # The optimal play will be the one with the highest simulated value from the dictionary
                # That is, the card gives us the most flexibility in terms of cards we have in our hand
                for card in hand:
                    options[card] = traverse(card)

                # Return the best option
                return bestChild(options)

            # Function for node traversal
            def traverse(node):
                # Create a deck of all the cards
                all_cards = deckInit()

                # This is the value that this particular node holds
                value = 0

                # Loop through every possible card in the game
                # This is the opponent's card that they play in response to our card
                for card in all_cards:
                    # If the card is compatible with the node we are traversing,
                    # Expand the node, counting how many playable cards we have for it
                    if card.compatible(node):
                        # Add to the current value after expanding the current node
                        value += expand(card)

                return value

            # Function for the result of the simulation
            def expand(node):
                value = 0

                # We simulate the opponent's card (node) and see how many compatible cards we have
                # Each compatible card increments a value
                for card in playable:
                    if card.compatible(node):
                        value += 1

                return value

            # Function for selecting the best child
            # The node with highest number of values
            def bestChild(node: Dict[Card, int]):
                max_val: int = 0
                best_card: Card = None
                for key, value in node.items():
                    # Compare the value points given by each node
                    if value > max_val:
                        best_card = key
                        max_val = value

                return best_card

            return monteCarloTreeSearch(playable)
        elif self.difficulty == 2:  # Medium, handle card priority logic
            """
            Medium Difficulty AI:
            The AI tries to chains as many moves as possible when it reaches a threshold of action cards, otherwise
            it checks if the next player's hand is below a threshold and tries to add more cards to their hand, 
            if both conditions are unsatisfied (next player's hand is high and the computer has low action cards),
            we play our cards in the priority of: (9-0 cards, draw-2, skip, reverse, wild, wild draw-4)
            """

            # Loop through every single card and add each playable card into a list
            # We also check for the number of action cards we can play
            action = 0

            for card in playable:
                if card.action == "skip" or card.action == "draw_2" or card.action == "reverse" or card.action == "wild_draw_4" or card.action == "wild":
                    action += 1

            # Bool to chain cards together is flagged
            # With more than 1 opponent, this is never true
            if self.chain_cards:
                for card in playable:
                    if card.action == "reverse":
                        return card

                for card in playable:
                    if card.action == "skip":
                        return card

                for card in playable:
                    if card.action == "wild":
                        return card

                for card in playable:
                    if card.action == "wild_draw_4":
                        return card

                for card in playable:
                    if card.action == "draw_2":
                        return card

                # We have no action cards left that we can chain
                if action == 0:
                    self.chain_cards = False
            else:
                # Check the size of the next player's hand, if its lower than the threshold, try to delay their win
                if len(next_hand) <= 5:

                    # Single player priority
                    # Play a color skip, color draw +2 card, otherwise play +4 wild card
                    if num_players == 2:
                        for card in playable:
                            # Card priority tries to keep as many wild cards
                            if card.action == "skip":
                                return card

                        for card in playable:
                            if card.action == "draw_2":
                                return card

                        for card in playable:
                            if card.action == "wild_draw_4":
                                return card
                    else:
                        # Play +4 wild card, color draw +2 card, or color skip
                        # Since we cannot chain actions, we use the card that delays the opponent the longest
                        for card in playable:
                            # Card priority tries to keep as many wild cards
                            if card.action == "wild_draw_4":
                                return card

                        for card in playable:
                            if card.action == "draw_2":
                                return card

                        for card in playable:
                            if card.action == "skip":
                                return card

                # Hand has more action cards than the threshold
                # Action card priority (reverse, skip, wild, wild draw-4, draw-2)

                # This only activates when there is only one computer player
                # Chaining doesnt work since playing skip action cards will move to the next player in the list
                if num_players == 2:
                    if action >= 3:
                        # Flag the boolean
                        # This boolean does repeated actions if it is single player

                        self.chain_cards = True

                        # Play the action cards in succession
                        for card in playable:
                            if card.action == "reverse":
                                return card

                        for card in playable:
                            if card.action == "skip":
                                return card

                        for card in playable:
                            if card.action == "wild":
                                return card

                        for card in playable:
                            if card.action == "wild_draw_4":
                                return card

                        for card in playable:
                            if card.action == "draw_2":
                                return card

                # Both checks failed, priority is: (9-0 cards, draw-2, skip, reverse, wild, wild draw-4)
                # This ensures the computer saves up their action cards
                for card in playable:
                    if card.action == None:
                        return card

                for card in playable:
                    if card.action == "draw_2":
                        return card

                for card in playable:
                    if card.action == "skip":
                        return card

                for card in playable:
                    if card.action == "reverse":
                        return card

                for card in playable:
                    if card.action == "wild":
                        return card

                for card in playable:
                    if card.action == "wild_draw_4":
                        return card

        elif self.difficulty == 1:  # Easy, play the first compatible card
            random.shuffle(self.hand)
            for card in self.hand:
                if discard.compatible(card):
                    return card
        return None

    def chooseColor(self):
        """ Chooses a random color for the Computer """
        # If difficulty is medium/hard, make it so it picks the color most beneficial
        # Loop through the hand of the computer and count card colors
        if self.difficulty == 2 or self.difficulty == 3:
            colors = {
                "red": 0,
                "yellow": 0,
                "green": 0,
                "blue": 0
            }

            for card in self.hand:
                if card.color == Color.Red:
                    colors["red"] += 1
                elif card.color == Color.Yellow:
                    colors["yellow"] += 1
                elif card.color == Color.Green:
                    colors["green"] += 1
                elif card.color == Color.Blue:
                    colors["blue"] += 1

            max_num = 0
            max_key = ""
            for key, value in colors.items():
                if colors[key] > max_num:
                    max_num = colors[key]
                    max_key = key

            if max_key == "red":
                return 0
            elif max_key == "yellow":
                return 1
            elif max_key == "green":
                return 2
            elif max_key == "blue":
                return 3
        else:
            # Difficulty is easy, choose a random color
            return random.randrange(0, 4)

    def setDifficulty(self, diff):
        self.difficulty = diff

    def compCallUno(self):
        if len(self.hand) != 1:
            return False
        prob = random.random()
        if self.difficulty == 1:
            if prob>.5:
                return True
            return False
        elif self.difficulty == 2:
            if prob>.3:
                return True
            return False
        elif self.difficulty == 3:
            if prob>.1:
                return True
            return False