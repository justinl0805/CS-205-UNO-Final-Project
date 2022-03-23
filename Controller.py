import sys
import time
import View
import Model
from Model import game_event
import pygame
from Card import Color

class Controller:
    def __init__(self):
        pygame.init()
        self.view  = View.View()
        self.model = Model.Model()
        self.clock = pygame.time.Clock()

    def run(self):
        options = self.view.startMenu()
        
        print(options)
        num_players, difficulty = options
        if num_players > 1:
            self.model.addPlayers(num_players - 1)

        self.model.setGameDifficulty(difficulty)
        self.view.render(self.model.player.getHand(),self.model.getComputerHands(),self.model.discard[0],self.model.getPlayer())
        
        exit = False
        while not exit:
            turn = self.model.getPlayer()
            if turn == "computer_won" or turn == "user_won":
                exit = True
                break
            
            if turn == "human":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                        pygame.quit()
                        sys.exit(0)
                        exit = True
                        break
                    
                    handled_event = self.view.handle_event(event)
                    if handled_event == None: # Non-event, skip this loop
                        break
                    action, idx = handled_event
                    card = self.model.player.getHand()[idx]
                    discard = self.model.discard[0]
                    if action == game_event.game_quit:
                        print("QUIT")
                        exit = True
                        pygame.quit()
                        sys.exit(1)
                        break
                    elif action == game_event.uno:
                        self.model.callUno(self.model.player)
                    elif action == game_event.user_scroll:
                        # Just skip the loop and re-render
                        pass 
                    elif action == game_event.draw:
                        self.view.animateDrawCard(self.model.player.getHand(),self.model.getComputerHands(),self.model.discard[0],turn) 
                        self.model.checkMove(action)
                    elif card.color == Color.Wild:
                        color = self.view.getWildColorSelection()
                        if color is None: # Player has clicked away from wildcard, they no longer want to play it
                            break
                        card.color = color
                        legal = self.model.checkMove(card)
                        if legal:
                            self.view.animatePlayCard(card,self.model.player.getHand(),self.model.getComputerHands(),discard,turn)
                    else:
                        legal = self.model.checkMove(card)
                        if legal:
                                self.view.animatePlayCard(card,self.model.player.getHand(),self.model.getComputerHands(),discard,turn)
            elif turn == "computer":
                self.view.render(self.model.player.getHand(),self.model.getComputerHands(),self.model.discard[0],turn) #Gives you time to see "computer"'s turn indicator flash onscreen
                time.sleep(1)
                self.model.computerTurn()
            else:
                exit = True
                break

            self.view.render(self.model.player.getHand(),self.model.getComputerHands(),self.model.discard[0],turn)
            self.clock.tick(20)

        did_user_win = (turn == "user_won")
        restart = self.view.promptForRestart(did_user_win)
        if restart:
            self.model = Model.Model() # Make a new model
            self.run()
        else:
            print("Goodbye!")
            pygame.quit()

            
            
        
