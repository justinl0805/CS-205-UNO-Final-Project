import enum
import math 
import pygame
from Card import Color

class game_event(enum.Enum): 
    game_quit = 0
    card_click = 1
    draw = 2
    user_scroll = 3
    uno = 4

WHITE=(255,255,255)
BLACK=(0,0,0)
BLUE=(0,0,255)

class View():
    def __init__(self):
        pygame.init()
        self.display_width = 1200
        self.display_height = 625 
        self.display = pygame.display.set_mode((self.display_width,self.display_height))
        self.display.fill(WHITE)
        self.player_hand_onscreen = [] 
        self.player_hand_onscreen = []
        # Set by makeCards
        self.card_width = 80
        self.card_height = 125
        self.offset_level = 0
        self.possible_cards_onscreen  = (self.display_width - (self.card_width * 2)) // self.card_width
        self.player_hand_offset_max = 0

        # Load images
        self.background = pygame.image.load('wood_background.jpg')
        self.background.convert()

        all_card_textures = pygame.image.load('textures.png')
        all_card_textures.convert()
        all_card_images = self.makeCards(all_card_textures)

        back_img = pygame.image.load('uno_back.png')
        back_img.convert()

        arrow_img = pygame.image.load('leftrightarrow.png')
        arrow_img.convert()

        inverted_arrow_img = pygame.image.load('inverted_arrows.png')
        inverted_arrow_img.convert()

        self.uno_button_img = pygame.image.load('uno_button.png')
        self.uno_button_img.convert()

        self.start_menu_background = pygame.image.load('uno_background.jpg')
        self.start_menu_background.convert()

        self.uno_rules_img = pygame.image.load('uno_rules.png')
        self.uno_rules_img.convert()
        
        # Load the images
        self.red_card_images    = [] 
        self.blue_card_images   = []
        self.yellow_card_images = []
        self.green_card_images  = []
        self.game_card_images   = []

        self.red_card_images    = all_card_images[0:10]
        self.red_card_images = self.red_card_images[-1:] + self.red_card_images[:-1] ## Move 0 card to front 
        self.yellow_card_images = all_card_images[10:20]
        self.yellow_card_images = self.yellow_card_images[-1:] + self.yellow_card_images[:-1]
        self.green_card_images  = all_card_images[20:30]
        self.green_card_images = self.green_card_images[-1:] + self.green_card_images[:-1]
        self.blue_card_images   = all_card_images[30:40]
        self.blue_card_images = self.blue_card_images[-1:] + self.blue_card_images[:-1]

        self.red_card_images = self.red_card_images + all_card_images[40:44]
        self.yellow_card_images = self.yellow_card_images + all_card_images[43:47]
        self.green_card_images = self.green_card_images + all_card_images[46:50]
        self.blue_card_images = self.blue_card_images + all_card_images[49:53]

        self.game_card_images   = all_card_images[53:56] # Avoiding duplicas in quad total image
        
        self.game_card_images.append(back_img)

        self.wild_card_textures = []
        wildcard = self.game_card_images[0]
        colors = [(255,0,0),(255,255,0),(0,255,0),(0,0,255)]
        for i in range(4):
            surface = pygame.Surface((self.card_width + 10, self.card_height + 10))
            surface.fill(colors[i])
            rect = wildcard.get_rect()
            rect.center = (self.card_width + 10) // 2, (self.card_height + 10) // 2
            surface.blit(wildcard,rect)
            self.wild_card_textures.append(surface)
        self.wild_card_textures.append(wildcard)

        self.drawfour_card_textures = []
        drawfour = self.game_card_images[1]
        for i in range(4):
            surface = pygame.Surface((self.card_width + 10, self.card_height + 10))
            surface.fill(colors[i])
            rect = drawfour.get_rect()
            rect.center = (self.card_width + 10) // 2, (self.card_height + 10) // 2
            surface.blit(drawfour,rect)
            self.drawfour_card_textures.append(surface)
        self.drawfour_card_textures.append(drawfour)

        arrow_width = arrow_img.get_width() // 2
        arrow_height = arrow_img.get_height()
        self.left_arrow_img = arrow_img.subsurface(pygame.Rect(0,0,arrow_width,arrow_height))
        self.right_arrow_img = arrow_img.subsurface(pygame.Rect(arrow_width,0,arrow_width,arrow_height))
        
        self.inverted_left_arrow_img = inverted_arrow_img.subsurface(pygame.Rect(0,0,arrow_width,arrow_height))
        self.inverted_right_arrow_img = inverted_arrow_img.subsurface(pygame.Rect(arrow_width,0,arrow_width,arrow_height))


    def showRules(self):
        """ Display the rules, return on any user click """ 
        w, h = self.display.get_width(), self.display.get_height()
        rect = self.start_menu_background.get_rect()
        rect.center = w // 2, h // 2
        self.display.blit(self.start_menu_background,rect)

        rules_rect = self.uno_rules_img.get_rect()
        rules_rect.center = w // 2, h // 2
        self.display.blit(self.uno_rules_img,rules_rect)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return True


    def promptForRestart(self,did_user_win):
        """ Display a 'sorry' or 'congrats' screen, with an option to replay. """ 
        w, h = self.display.get_width(), self.display.get_height()
        rect = self.start_menu_background.get_rect()
        rect.center = w // 2, h // 2
        self.display.blit(self.start_menu_background,rect)

        menu_height = 500
        menu_width  = 400
        menu = pygame.Surface((menu_width,menu_height))
        menu.fill(BLACK)
        menu_rect = menu.get_rect()
        menu_rect.center = w // 2, h // 2
        self.display.blit(menu,menu_rect)

        # Title text
        font = pygame.font.SysFont('arial',30)
        text = font.render("UNO",True,WHITE,BLACK)
        textRect = text.get_rect()
        textRect.center = w // 2, (h // 2) - ((1/2) * menu_height) + ((1/2) * text.get_height()) + 10
        self.display.blit(text,textRect)

        # Print status
        result_text_raw = "Congrats!" if did_user_win else "Sorry"
        result_text = font.render(result_text_raw,True,BLACK,WHITE)
        result_text_rect = text.get_rect()
        result_text_rect.center = w // 2, (h // 2) 
        self.display.blit(result_text,result_text_rect)

        ## Play Button
        play_font = pygame.font.SysFont("arial",30)
        play_text = play_font.render("Play",True,WHITE,BLUE)
        rect_play_text = play_text.get_rect()
        rect_play_text.center = (w // 2), (h // 2) + (menu_height // 2) - (play_text.get_height() // 2) - 10
        self.display.blit(play_text,rect_play_text)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if rect_play_text.collidepoint(pos):
                        return True

        
    def startMenu(self):
        """ Display start screen, accept configuration inputs, returns when user clicks play button"""
        w, h = self.display.get_width(), self.display.get_height()
        rect = self.start_menu_background.get_rect()
        rect.center = w // 2, h // 2
        self.display.blit(self.start_menu_background,rect)

        # Layout configuration options
        menu_height = 500
        menu_width  = 400
        menu = pygame.Surface((menu_width,menu_height))
        menu.fill(BLACK)
        menu_rect = menu.get_rect()
        menu_rect.center = w // 2, h // 2
        self.display.blit(menu,menu_rect)

        # Title text
        font = pygame.font.SysFont('arial',30)
        text = font.render("UNO",True,WHITE,BLACK)
        textRect = text.get_rect()
        textRect.center = w // 2, (h // 2) - ((1/2) * menu_height) + ((1/2) * text.get_height()) + 10
        self.display.blit(text,textRect)

        # Buttons
        opponent_selection_buttons = []
        hardness_selection_buttons = []
        button_font = pygame.font.SysFont('arial',20)
        ## Players
        opponent_text_y = (h // 2) - ((1/4) * menu_height)
        
        one_opponent_text = button_font.render("1 Opponent",True,BLACK,WHITE)
        rect_one_opponent_text = one_opponent_text.get_rect()
        rect_one_opponent_text.center = (w // 2) - ((1/2) * menu_width) + ((1/2) * one_opponent_text.get_width()) + 10, opponent_text_y
        self.display.blit(one_opponent_text,rect_one_opponent_text)
        opponent_selection_buttons.append(["1 Opponent",rect_one_opponent_text,1])
                          
        two_opponent_text = button_font.render("2 Opponents",True,WHITE,BLACK)
        rect_two_opponent_text = two_opponent_text.get_rect()
        rect_two_opponent_text.center = (w // 2) - ((1/2) * menu_width) + ((3/2) * two_opponent_text.get_width()) + 10, opponent_text_y
        self.display.blit(two_opponent_text,rect_two_opponent_text)
        opponent_selection_buttons.append(["2 Opponents",rect_two_opponent_text,2])
        
        three_opponent_text = button_font.render("3 Opponents",True,WHITE,BLACK)
        rect_three_opponent_text = three_opponent_text.get_rect()
        rect_three_opponent_text.center = (w // 2) - ((1/2) * menu_width) + ((5/2) * three_opponent_text.get_width()) + 20, opponent_text_y
        self.display.blit(three_opponent_text,rect_three_opponent_text)
        opponent_selection_buttons.append(["3 Opponents",rect_three_opponent_text,3])

        ## Hardness
        hardness_text_y = opponent_text_y + (4 * one_opponent_text.get_height())
        one_hardness_text = button_font.render("Easy",True,BLACK,WHITE)
        rect_one_hardness_text = one_hardness_text.get_rect()
        rect_one_hardness_text.center = (w // 2) - ((1/2) * menu_width) + ((1/2) * one_opponent_text.get_width()) + 10, hardness_text_y
        self.display.blit(one_hardness_text,rect_one_hardness_text)
        hardness_selection_buttons.append(["Easy",rect_one_hardness_text,1])

        two_hardness_text = button_font.render("Medium",True,WHITE,BLACK)
        rect_two_hardness_text = two_hardness_text.get_rect()
        rect_two_hardness_text.center = (w // 2) - ((1/2) * menu_width) + ((3/2) * two_opponent_text.get_width()) + 10, hardness_text_y
        self.display.blit(two_hardness_text,rect_two_hardness_text)
        hardness_selection_buttons.append(["Medium",rect_two_hardness_text,2])

        three_hardness_text = button_font.render("Hard",True,WHITE,BLACK)
        rect_three_hardness_text = three_hardness_text.get_rect()
        rect_three_hardness_text.center = (w // 2) - ((1/2) * menu_width) + ((5/2) * three_opponent_text.get_width()) + 20, hardness_text_y
        self.display.blit(three_hardness_text,rect_three_hardness_text)
        hardness_selection_buttons.append(["Hard",rect_three_hardness_text,3])

        ## Play Button
        play_font = pygame.font.SysFont("arial",30)
        play_text = play_font.render("Play",True,WHITE,BLUE)
        rect_play_text = play_text.get_rect()
        rect_play_text.center = (w // 2), (h // 2) + (menu_height // 2) - (play_text.get_height() // 2) - 10
        self.display.blit(play_text,rect_play_text)

        ## Rules
        rules_button = play_font.render("Rules",True,WHITE,BLUE)
        rect_rules_button = rules_button.get_rect()
        rect_rules_button.center = (w // 2), (h // 2) + (menu_height // 2) - play_text.get_height() - 20 - (rules_button.get_height() // 2)
        self.display.blit(rules_button,rect_rules_button)
        
        
        pygame.display.update()
        opponents = 1
        hardness = 1 
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()

                    if rect_play_text.collidepoint(pos):
                        return (opponents,hardness)
                    elif rect_rules_button.collidepoint(pos):
                        self.showRules()
                        return self.start_menu()
                    
                    opponent_selected_button = None
                    hardness_selected_button = None
                    
                    for button in opponent_selection_buttons:
                        if button[1].collidepoint(pos):
                            opponent_selected_button = button
                            break

                    for button in hardness_selection_buttons:
                        if button[1].collidepoint(pos):
                            hardness_selected_button = button
                            break

                    # Repaint opponent buttons 
                    if opponent_selected_button is not None: 
                        for opponent_button in opponent_selection_buttons:
                            updated_text = button_font.render(opponent_button[0],True,WHITE,BLACK)
                            updated_text_rec = updated_text.get_rect()
                            updated_text_rec.center = opponent_button[1].center
                            self.display.blit(updated_text,updated_text_rec)

                        opponents = opponent_selected_button[2]
                        updated_text = button_font.render(opponent_selected_button[0],True,BLACK,WHITE)
                        updated_text_rec = updated_text.get_rect()
                        updated_text_rec.center = opponent_selected_button[1].center
                        self.display.blit(updated_text,updated_text_rec)
                        opponent_selected_button[1] = updated_text_rec

                    # Repaint hardness buttons
                    if hardness_selected_button is not None: 
                        for button in hardness_selection_buttons:
                            updated_text = button_font.render(button[0],True,WHITE,BLACK)
                            updated_text_rec = updated_text.get_rect()
                            updated_text_rec.center = button[1].center
                            self.display.blit(updated_text,updated_text_rec)

                        hardness = hardness_selected_button[2]
                        updated_text = button_font.render(hardness_selected_button[0],True,BLACK,WHITE)
                        updated_text_rec = updated_text.get_rect()
                        updated_text_rec.center = hardness_selected_button[1].center
                        self.display.blit(updated_text,updated_text_rec)
                        hardness_selected_button[1] = updated_text_rec

            pygame.display.update()


    def getWildColorSelection(self):
        """ Display a color selector for wildcards, returning the color clicked on. If the user clicks anywhere besides the selector, return None """ 
        # Render the selector
        selector_rectangle_width = (4 * self.card_width) + 30
        selector_rectangle_height = self.card_height + 10 
        selector_rectangle = pygame.Surface((selector_rectangle_width,selector_rectangle_height))
        selector_rectangle.fill(BLACK)
        selector_rect = selector_rectangle.get_rect()
        selector_rect.center = self.display.get_width() // 2, self.display.get_height() // 2
        self.display.blit(selector_rectangle,selector_rect)
        
        # Blit the colors onto the selector
        rect_list = [] 
        starting_x = (self.display.get_width() // 2) - self.card_width - (self.card_width // 2) - 9 
        width = self.card_width + 6
        # Red, Yellow, Green, Blue 
        colors = [(255,0,0),(255,255,0),(0,255,0),(0,0,255)]
        for i, color  in enumerate(colors):
            color_surface = pygame.Surface((width,self.card_height))
            color_rect = color_surface.get_rect()
            color_rect.center = starting_x + (i * width), (self.display.get_height() // 2)
            color_surface.fill(color)
            self.display.blit(color_surface,color_rect)
            rect_list.append(color_rect)

        pygame.display.update()

        # Listen for color selection
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for i, color_rect in enumerate(rect_list):
                        if color_rect.collidepoint(pos):
                            return Color(i) # This should correspond to the color
                    return None # If the player has clicked anywhere besides the colors, we take that to mean they don't want to play the wildcard


    def handle_event(self,event):
        """ Take a pygame event, detect collision with onscreen semantic objects, return a game_event sum type """ 
        if event.type == pygame.QUIT:
            return (game_event.game_quit,0)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            # Check for collision with scroll buttons, issue player_scroll_{left,right} event
            # return (game_event.player_scroll_left,0)
            if self.left_arrow_rect.collidepoint(pos):
                self.offset_level = max(0,(self.offset_level - 1))
                return (game_event.user_scroll,0)
            elif self.right_arrow_rect.collidepoint(pos):
                if (self.offset_level + 1) <= self.player_hand_offset_max:
                    self.offset_level += 1
                else:
                    pass
                return (game_event.user_scroll,0)
            elif self.uno_button_rect.collidepoint(pos):
                return (game_event.uno,0)
            for index, card in enumerate(self.player_hand_onscreen):
                if card.collidepoint(pos):
                    actual_index = index + (self.offset_level * self.possible_cards_onscreen)
                    return (game_event.card_click,actual_index)
            if self.deck_onscreen.collidepoint(pos):
                    return (game_event.draw,0)
        else:
            return None
                

    def mapCardToCardTexture(self,card):
        """ Map card object to corresponding texture """
        if card.action == "wild":
            card_texture = self.wild_card_textures[int(card.color)]
            return card_texture
        elif card.action == "wild_draw_4":
            card_texture = self.drawfour_card_textures[int(card.color)]
            return card_texture 
        
        if card.color == Color.Red:
            card_texture = self.red_card_images[card.symbol]
        elif card.color == Color.Yellow: 
            card_texture = self.yellow_card_images[card.symbol]
        elif card.color == Color.Green:
            card_texture = self.green_card_images[card.symbol]
        elif card.color == Color.Blue:
            card_texture = self.blue_card_images[card.symbol]
        
        return card_texture


    def render(self,hand,opponent_hands,discard,turn, suppress_update=False):
        """ Render updated playscreen given model data. When passed optional suppress_update flag, the render is done but the gamescreen is not updated, to allow further rendering to happen in the same tick"""
        if len(hand) == 0: # game is over, nothing to render
            return None
        
        display = self.display
        self.player_hand_onscreen = list(map(self.mapCardToCardTexture,hand))
        hand = self.player_hand_onscreen
        display_width, display_height = display.get_width(), display.get_height()
        card_width = hand[0].get_width() # Get surface width for card[0]
        card_height = hand[0].get_height()

        # Render over past move
        self.display.fill(WHITE)
        background_rect = self.background.get_rect()
        background_rect.center = display_width // 2, display_height // 2 
        self.display.blit(self.background,background_rect)

        # Draw the opponent hand(s)
        image = self.game_card_images[3]
        rect = self.game_card_images[3].get_rect()

        opponent_hand_size_block = (3 * card_width) + ((1/2) * card_width)
        opponent_x = card_width // 2
        opponent_y = card_height //2
        for j in range(min(opponent_hands[0],13)):
            x = opponent_x + (j * (card_width * (1/4)))
            rect.center = x, opponent_y
            display.blit(image,rect)

        if len(opponent_hands) > 1: 
            opponent_x = (display_width // 2) - ((1/2) * opponent_hand_size_block)
            for j in range(min(opponent_hands[1],13)):
                x = opponent_x + (j * (card_width * (1/4)))
                rect.center = x, opponent_y
                display.blit(image,rect)

        if len(opponent_hands) > 2:
            opponent_x = display_width - opponent_hand_size_block
            for j in range(min(opponent_hands[2],13)):
                x = opponent_x + (j * (card_width * (1/4)))
                rect.center = x, opponent_y
                display.blit(image,rect)

        # Print UNO Button
        self.uno_button_rect = self.uno_button_img.get_rect()
        self.uno_button_rect.center = (self.uno_button_img.get_width() // 2) + ((1/4) * card_width), display_height // 2
        display.blit(self.uno_button_img,self.uno_button_rect)
        
        # Print discard
        discard_img = self.mapCardToCardTexture(discard)
        rect = discard_img.get_rect()
        rect.center = display_width // 2, display_height // 2
        display.blit(discard_img,rect)

        # Print the turn
        font = pygame.font.SysFont('arial',30)
        text = font.render(turn.upper(),True,WHITE,BLACK)
        textRect = text.get_rect()
        textRect.center = (display_width // 2), ((display_height // 2) - (card_height * 3/4))
        display.blit(text,textRect)
                
        # Print deck
        deck_img = self.game_card_images[3]
        rect = deck_img.get_rect()
        rect.center = (display_width // 2) + (2 * card_width), (display_height // 2)
        display.blit(deck_img,rect)
        self.deck_onscreen = rect

        arrow_height = self.right_arrow_img.get_height()
        arrow_width  = self.right_arrow_img.get_width()
        possible_number_of_cards = (self.display_width - (arrow_width * 2)) // card_width 

        # Print arrows
        if len(hand) > possible_number_of_cards:
            inv_left_arrow_rect = self.inverted_left_arrow_img.get_rect()
            self.left_arrow_rect = inv_left_arrow_rect 
            inv_left_arrow_rect.center = arrow_width // 2, self.display_height - (arrow_height // 2)
            display.blit(self.inverted_left_arrow_img,inv_left_arrow_rect)

            inv_right_arrow_rect = self.inverted_right_arrow_img.get_rect()
            self.right_arrow_rect = inv_right_arrow_rect
            inv_right_arrow_rect.center = self.display_width - (arrow_width // 2), self.display_height - (arrow_height // 2)
            display.blit(self.inverted_right_arrow_img,inv_right_arrow_rect)
        else:
            left_arrow_rect = self.left_arrow_img.get_rect()
            self.left_arrow_rect = left_arrow_rect 
            left_arrow_rect.center = arrow_width // 2, self.display_height - (arrow_height // 2)
            display.blit(self.left_arrow_img,left_arrow_rect)

            right_arrow_rect = self.right_arrow_img.get_rect()
            self.right_arrow_rect = right_arrow_rect
            right_arrow_rect.center = self.display_width - (arrow_width // 2), self.display_height - (arrow_height // 2)
            display.blit(self.right_arrow_img,right_arrow_rect)

        # Print player hand
        rect_list = [] 
        starting_y = display_height - (card_height // 2)
        starting_x = (card_width // 2) + arrow_width
        # hand slice offset * hand_width
        card_offset = possible_number_of_cards * self.offset_level
        # Take slice of hand based on offset
        hand_offset = hand[card_offset:]
        if len(hand_offset) == 0 and self.offset_level > 0:
            self.offset_level -= 1
        else:
            hand = hand_offset
            
        for i, card in enumerate(hand):
            if i >= possible_number_of_cards: 
                break
            rect = card.get_rect()
            x = starting_x + (i * card_width)
            rect.center = x, starting_y
            display.blit(card,rect)
            rect_list.append(rect)
        
        self.player_hand_offset_max = math.ceil(len(hand) / possible_number_of_cards)
        self.player_hand_onscreen = rect_list

        if not suppress_update:
            pygame.display.update()


    def animateDrawCard(self,hand,opponent_hands,discard,turn):
        """ Animate an UNO card moving from the top of the deck to the last available spot in the player's hand, or offscreen if their onscreen hand is full """ 
        w, h = self.display.get_width(), self.display.get_height()
        # First, we re-render the whole screen
        self.render(hand,opponent_hands,discard,turn)
        # Get the card set up to move on top of the deck
        moving_card_img = self.game_card_images[3]
        moving_card_rect = moving_card_img.get_rect()
        moving_card_rect.center = (w // 2) + (2 * self.card_width), (h // 2)
        self.display.blit(moving_card_img,moving_card_rect)
        # Figure out the target
        user_hand_length = len(hand)
        card_offset = self.possible_cards_onscreen * self.offset_level
        hand_offset = hand[card_offset:]
        if len(hand_offset) > self.possible_cards_onscreen: # We have a full page, we want to just shoot the draw offscreen
            target = ((w + 10), (h  - self.card_height // 2))
        else: # Our target is going to be at the end of the current hand, in the spot where the next card would go
            target = (((len(hand_offset) + 1) * self.card_width + (self.card_width // 2)), (self.display_height - (self.card_height // 2)))
        
        target_x, target_y = target
        prev_x, prev_y = moving_card_rect.center
        x_delta = 3
        y_delta = 3
        if target_x >= prev_x: # Destination is to the right, add delta_x
            while target_x > prev_x or target_y > prev_y:
                moving_card_rect.center = min(target_x,prev_x + x_delta), min(target_y,prev_y + y_delta)
                prev_x, prev_y = moving_card_rect.center
                self.render(hand,opponent_hands,discard,turn,suppress_update=True)
                self.display.blit(moving_card_img,moving_card_rect)
                pygame.display.update()
        else: # Destination is left, subtract delta_x
            while prev_x > target_x or prev_y < target_y:
                moving_card_rect.center = max(target_x,prev_x - x_delta), min(target_y,prev_y + y_delta)
                prev_x, prev_y = moving_card_rect.center
                self.render(hand,opponent_hands,discard,turn,suppress_update=True)
                self.display.blit(moving_card_img,moving_card_rect)
                pygame.display.update()



    def animatePlayCard(self,card,hand,opponent_hands,discard,turn):
        w, h = self.display.get_width(), self.display.get_height()
        # First, we re-render the whole screen
        self.render(hand,opponent_hands,discard,turn)
        # Then, we re-draw the card
        moving_card_img = self.mapCardToCardTexture(card)
        moving_card_rect = moving_card_img.get_rect()
        moving_card_rect.center = w // 2, h - (moving_card_img.get_height()) - (moving_card_img.get_height() // 2) # Start card right above hand
        x = w // 2 
        y_delta = 2
        while moving_card_rect.center[1] > (h // 2): # We don't want to check strict equality because that could result in misalignment 
            prev_y = moving_card_rect.center[1]
            moving_card_rect.center = x, prev_y - y_delta
            self.render(hand,opponent_hands,discard,turn,suppress_update=True)
            self.display.blit(moving_card_img,moving_card_rect)
            pygame.display.update()



    def makeCards(self,image):
        """ Given total texture image, provides 2D list of subsurface indexes corresponding to cards """ 
        cards = [] 
        for i in range(6): # rows
            top = i * self.card_height
            row = []
            for j in range(10): # columns
                left = j * self.card_width
                cards.append(image.subsurface(pygame.Rect(left,top,self.card_width,self.card_height)))

        return cards
