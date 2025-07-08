from ai import AI
from card import Card
from itertools import combinations
from json import dump
from PyQt6.QtCore import QRect, Qt, QTimer
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtWidgets import QLabel
from random import choice
from ui import Button, CallSetButton, GameOver, InfoPanelBorder, PauseButton, ScorePanelBorder


class Board:

    def add_cards(self):

        # Draw more cards
        for i in range(len(self.current_board), len(self.current_board) + self.num_variations):
            self.draw_card(i)
        self.add_cards_btn.setEnabled(False)
        
        self.update_board()
        
    def apply_penalty(self):
        
        # Apply score penalty if in score mode
        if self.mode in ["recycle", "xs", "ai"] and self.player_score_card.text() != "0":
            self.player_score_card.setText(str(int(self.player_score_card.text()) - 1))

        # Apply time penalty if in time mode, amount based on settings
        elif self.mode in ["time_trial", "xl"]:
            self.elapsed_time += self.num_variations ** self.num_traits
        
    def call_set(self):

        # Change cursor icon to pointing hand over cards when clickable
        for card in self.current_board:
            card.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        # Styling is updated over 10 seconds at 10 updates/sec
        if not self.call_set_btn.called:
            self.call_set_btn.called = True
            self.call_set_btn.timer.start(100)

            # Pause AI
            if self.mode == "ai":
                self.ai.stop()

    def call_set_reset(self, remove_cards, is_set, source):

        self.selection_delay_timer.stop()
        self.selection_delay_timer_active = False
        if self.mode in ["recycle", "xl", "time_trial"]:
            self.timer.start()

        # Reset button
        self.call_set_btn.setText("Call SET")
        self.call_set_btn.time_left = 100
        self.call_set_btn.setStyleSheet(f"""
            background-color: {self.call_set_btn.color};
            border: {self.call_set_btn.height() // 15}px solid {self.call_set_btn.shift_color_lightness(self.call_set_btn.color, -60)};
        """)
        
        # Unselect all selected cards
        if remove_cards:
            while self.selected_cards:
                card = self.selected_cards.pop()
                card.has_border = not card.has_border
                card.update()

            # Resume AI
            if self.mode == "ai":
                self.ai.start()
        
        else:
            self.process_cards(is_set, source)
            
    def call_set_stop_timer(self, remove_cards = False, is_set = None, source = "player"):
        
        # Stop timer
        self.call_set_btn.timer.stop()
        if self.mode in ["recycle", "xl", "time_trial"]:
            self.timer.stop()

        # Update button text based on called condition, pause, then continue
        self.call_set_btn.called = False
        if source == "player":
            if is_set == True:
                self.call_set_btn.setText("SET!")
            elif is_set == False:
                self.call_set_btn.setText("Not a SET!")
            elif remove_cards:
                self.call_set_btn.setText("Time's Up!")

        # Delay before processing selected cards
        self.selection_delay_timer.timeout.disconnect()
        self.selection_delay_timer.timeout.connect(lambda: self.call_set_reset(remove_cards, is_set, source))
        self.selection_delay_timer.start(1000 * self.main.settings["selection_delay"])
        self.selection_delay_timer_active = True
            
    def call_set_update_button(self):
        
        # Stop updates after 100 total
        if self.call_set_btn.time_left == 0:
            self.apply_penalty()
            self.call_set_stop_timer(remove_cards = True)
        
        # Update "Call Set" button styling based on time_left value
        else:
        
            if self.call_set_btn.time_left % 10 == 0:
                self.call_set_btn.setText(str(self.call_set_btn.time_left // 10))
            self.call_set_btn.setStyleSheet(f"""
                background-color: qlineargradient(
                    x1: 0,
                    x2: 1,
                    stop: {(self.call_set_btn.time_left - 1) / 100} {self.call_set_btn.color},
                    stop: {self.call_set_btn.time_left / 100} #f3eef6
                );
                border: {self.call_set_btn.height() // 15}px solid {self.call_set_btn.shift_color_lightness(self.call_set_btn.color, -60)};
            """)
            self.call_set_btn.time_left -= 1
        
    def card_clicked(self, card, source):

        # Toggle card selection border
        card.has_border = not card.has_border
        card.update()

        if card in self.selected_cards:
            self.selected_cards.remove(card)
        else:
            self.selected_cards.append(card)
            if len(self.selected_cards) == self.num_variations:
                
                # Stop "Call Set" timer
                self.call_set_stop_timer(source = source, is_set = self.is_set(self.selected_cards))

    def count_sets(self, board, traits_step_1_3, traits_step_2):

        # Step 1: if there is any trait with less than max variations, search each variation of that trait
        for trait in traits_step_1_3:

            # Count number of variations of current trait on the board
            variations = set()
            for card in board:
                variations.add(getattr(card, trait))
                if len(variations) == self.num_variations:
                    break

            # Call search if less than max
            if len(variations) < self.num_variations:

                # If trait with less than max variations already searched, then no SETs exist
                if trait in traits_step_1_3 and trait not in traits_step_2:
                    return

                for variation in variations:
                    next_board = [card for card in board if getattr(card, trait) == variation] # Filter board to only include cards with current variation

                    # If exactly num_variations cards, check if they form a SET
                    if len(next_board) == self.num_variations and self.is_set(next_board):
                        self.sets.append(tuple(next_board))

                    # If more than num_variations cards, search
                    elif len(next_board) > self.num_variations:
                        next_traits_1_3 = traits_step_1_3.copy()
                        next_traits_1_3.remove(trait)
                        next_traits_2 = traits_step_2.copy()
                        if trait in next_traits_2:
                            next_traits_2.remove(trait)
                        self.count_sets(next_board, next_traits_1_3, next_traits_2)
                        
                return

        # Step 2: search each variation of each trait
        prev_searched_same = [] # Traits already searched on the same level
        next_traits_2 = traits_step_2.copy()
        while next_traits_2:
            trait = next_traits_2.pop(0)
            
            variations = self.all_properties[trait]
            for variation in variations:

                next_board = [card for card in board if getattr(card, trait) == variation] # Filter board to only include cards with current variation

                # If exactly num_variations cards, check if they form a SET
                if len(next_board) == self.num_variations and self.is_set(next_board):
                    prev_searched_diff = [t for t in traits_step_1_3 if t not in traits_step_2] # Traits already searched on higher levels

                    # If cards share any previously searched trait, then SET has already been found
                    prev_searched = set(prev_searched_same) | set(prev_searched_diff)
                    if not any(len(set(getattr(card, prev_trait) for card in next_board)) == 1 for prev_trait in prev_searched):
                        self.sets.append(tuple(next_board))

                # If more than num_variations cards, search
                elif len(next_board) > self.num_variations:
                    next_traits_1_3 = traits_step_1_3.copy()
                    next_traits_1_3.remove(trait)
                    self.count_sets(next_board, next_traits_1_3, next_traits_2)

            prev_searched_same.append(trait)

        # Step 3: brute force search
        for cards in combinations(board, 2):
            
            # Check if any 2 cards have different traits
            if all(getattr(cards[0], trait) != getattr(cards[1], trait) for trait in traits_step_1_3):

                for card3 in board:

                    # Check every card after the 2nd if its traits are all different
                    if card3.card_pos > cards[1].card_pos and all(getattr(card3, trait) != getattr(cards[0], trait) and getattr(card3, trait) != getattr(cards[1], trait) for trait in traits_step_1_3):
                        
                        # If 3 cards per SET, then SET found
                        if self.num_variations == 3:
                            self.sets.append((cards[0], cards[1], card3))
                        else:

                            # Check every card after the 3rd if its traits are all different
                            for card4 in board:
                                if card4.card_pos > card3.card_pos and all(getattr(card4, trait) != getattr(cards[0], trait) and getattr(card4, trait) != getattr(cards[1], trait) and getattr(card4, trait) != getattr(card3, trait) for trait in traits_step_1_3):
                                    
                                    # If 4 cards per SET, then SET found
                                    if self.num_variations == 4:
                                        self.sets.append((cards[0], cards[1], card3, card4))
                                    else:

                                        # Check every card after the 4th if its traits are all different
                                        for card5 in board:
                                            if card5.card_pos > card4.card_pos and all(getattr(card5, trait) != getattr(cards[0], trait) and getattr(card5, trait) != getattr(cards[1], trait) and getattr(card5, trait) != getattr(card3, trait) and getattr(card5, trait) != getattr(card4, trait) for trait in traits_step_1_3):
                                                self.sets.append((cards[0], cards[1], card3, card4, card5))

        return
    
    def destroy(self):
        for card in self.current_board:
            card.deleteLater()
        if self.show_num_sets:
            self.show_num_sets.deleteLater()
        if self.show_cards_left_in_deck:
            self.show_cards_left_in_deck.deleteLater()
        self.info_panel_border.destroy()
        self.score_panel_border.destroy()
        self.add_cards_btn.deleteLater()
        self.call_set_btn.destroy()
        self.pause_game_btn.destroy()
        self.quit_game_btn.deleteLater()
        self.quit_game_text.deleteLater()
        self.quit_game_yes.deleteLater()
        self.quit_game_no.deleteLater()
        self.show_settings_btn.deleteLater()
        for tile in self.settings_name_tiles:
            tile.deleteLater()
        for tile in self.settings_values_tiles:
            tile.deleteLater()
        if self.enable_hints:
            self.enable_hints.deleteLater()
            if self.color_hint:
                self.color_hint.deleteLater()
        self.player_score_card.deleteLater()
        self.player_score_text.deleteLater()
        if self.mode in ["time_trial", "xl", "recycle"]:
            self.timer.deleteLater()
            self.display_time.deleteLater()
            self.final_time.deleteLater()
        if self.mode == "ai":
            self.ai.destroy()
            self.ai_score_card.deleteLater()
            self.ai_score_text.deleteLater()
        self.game_over_text.deleteLater()
        self.game_over.destroy()
        self.selection_delay_timer.deleteLater()
        self.main.board = None
    
    def draw_card(self, card_pos):
        card_id = choice(self.deck)
        self.deck.remove(card_id)
        self.current_board.append(Card(
            card_id["color"],
            card_id["shape"],
            card_id["number"],
            card_id["fill"],
            card_id["corner"],
            card_pos,
            self
        ))

    def end_game(self):
            
        # Hide cards
        for card in self.current_board:
            card.hide()

        # Disable buttons
        self.pause_game_btn.setEnabled(False)
        self.quit_game_btn.setEnabled(False)
        if self.enable_hints:
            self.enable_hints.setEnabled(False)
        self.call_set_btn.setEnabled(False)
        self.update_buttons()

        # Show final time if in time trial mode
        if self.mode in ["recycle", "time_trial", "xl"]:
            self.timer.stop()
            
            if self.mode != "recycle":
                self.final_time.setText(f"Final Time: {self.main.translate_time(self.elapsed_time)}")
                self.final_time.show()

        # Check list of scores for current settings and challenge type
        if self.mode in ["recycle", "xl", "xs", "time_trial"]:
            times = self.main.times[f"{self.mode}_{self.num_traits}{self.num_variations}"]
        
        # Configure text for game over screen
        if self.mode == "ai":

            # AI mode: evaluate player score against AI score
            if int(self.player_score_card.text()) > int(self.ai_score_card.text()):
                self.game_over_text.setText("You Win!")
            elif int(self.player_score_card.text()) < int(self.ai_score_card.text()):
                self.game_over_text.setText("You Lose")
            else:
                self.game_over_text.setText("It's a Tie")

        elif self.mode in ["recycle", "xs"] and (not times or int(self.player_score_card.text()) > max(times)):

            # Recycle, XS challenge: Check if score is new max for scores
            self.game_over_text.setText("New High Score!")

        elif self.mode in ["xl", "time_trial"] and (not times or self.elapsed_time < min(times)):

            # Time trial or XL challenge: Check if elapsed time is new min for times
            if self.mode == "xl":
                self.game_over_text.setText("New High Score!")
            else:
                self.game_over_text.setText("New Best Time!")

        else:
            self.game_over_text.setText("Game Over")

        self.game_over_text.show()

        # Set focus after texts to guarantee next event registers with game over screen
        self.game_over.show()
        self.game_over.setFocus()

    def get_hint(self):

        # Delete colored square if it exists
        if self.color_hint:
            self.color_hint.deleteLater()
            self.color_hint = None

        # Translates internal names for variations to phrases suited for the Hint button
        variations_translator = {
            "circle": "Circles",
            "square": "Squares",
            "triangle": "Triangles",
            "diamond": "Diamonds",
            "hourglass": "Hourglasses",
            "plus": "Pluses",
            "bowtie": "Bowties",
            "cross": "Crosses",
            1: "Ones",
            2: "Twos",
            3: "Threes",
            4: "Fours",
            5: "Fives",
            "solid": "Solid Cards",
            "empty": "Empty Cards",
            "striped": "Horizontal Striped Cards",
            "crossed": "Diagonal Crossed Cards",
            "dense": "Densely Shaded Cards",
            "none": "No-Cornered Cards",
            "top_left": "Top Left Corners",
            "top_right": "Top Right Corners",
            "bottom_left" : "Bottom Left Corners",
            "bottom_right": "Bottom Right Corners"
        }

        # Choose random SET on the board
        cards = choice(self.sets)
        traits = ["color", "shape", "number", "fill", "corner"][:self.num_traits]

        # Choose a random trait, continue until one with same variations is found
        while traits:
            trait = choice(traits)
            traits.remove(trait)
            if getattr(cards[0], trait) == getattr(cards[1], trait):

                # Display common variation among chosen SET
                if trait == "color": # For colors, display colored square
                    self.enable_hints.setText(f"Search in the      !")
                    self.color_hint = QLabel(
                        parent = self.main.central_widget,
                        geometry = QRect(247 * self.main.screen_width // 320,  self.main.screen_height // 120, 3 * self.main.screen_width // 160, self.main.screen_height // 30),
                        styleSheet = f"background-color: {cards[0].color}"
                    )
                    self.color_hint.show()

                # Otherwise use text
                else:
                    self.enable_hints.setText(f"Search in the {variations_translator[getattr(cards[0], trait)]}!")
                
                return

        # If SET has no variations in common, say so
        self.enable_hints.setText("No variations in common!")
    
    def is_set(self, cards):
        traits = ["color", "shape", "number", "fill", "corner"][:self.num_traits]
        for trait in traits:
            num_values = len(set([getattr(card, trait) for card in cards]))
            if num_values != 1 and num_values != self.num_variations:
                return False
        return True
    
    def process_cards(self, is_set, source):
                
        # If SET
        if is_set:

            # Update score if in AI mode or challenge
            if self.mode in ["recycle", "xs", "xl", "practice", "time_trial"]:
                self.player_score_card.setText(str(int(self.player_score_card.text()) + 1))
            elif self.mode == "ai":
                if source == "player":
                    self.player_score_card.setText(str(int(self.player_score_card.text()) + 1))
                elif source == "ai":
                    self.ai_score_card.setText(str(int(self.ai_score_card.text()) + 1))

            # Determine whether cards can and need to be drawn
            if self.deck and len(self.current_board) <= self.num_cards:

                # Remove selected cards and draw new ones
                for _ in range(self.num_variations):
                    c = self.selected_cards.pop()
 
                    # Add card id back into deck if in recycle challenge
                    if self.mode == "recycle":
                        self.deck.append({
                            "color": c.color,
                            "shape": c.shape,
                            "number": c.number,
                            "fill": c.fill,
                            "corner": c.corner
                        })

                    card_pos = c.card_pos
                    self.current_board.remove(c)
                    c.destroy()

                    # Handle XL mode where board_height is not a multiple of num_variations
                    if self.deck:

                        # Draw card normally if deck is not empty
                        self.draw_card(card_pos)

                    else:

                        # Move card with highest card_pos into empty space
                        self.current_board.sort(key = lambda x: x.card_pos)
                        self.current_board[-1].card_pos = card_pos
                        self.current_board[-1].calc_position()
                        self.num_cards -= 1

            # Remove selected cards and move unselected cards into vacant spaces
            else:

                # If deck is empty, lower the size of the board
                if not self.deck:
                    self.num_cards -= self.num_variations

                # Find extra cards that are not selected
                cards_to_move = [card for card in self.current_board if (card.card_pos >= len(self.current_board) - self.num_variations and card not in self.selected_cards)]
                while self.selected_cards:
                    c = self.selected_cards.pop()

                    # Add card id back into deck if in recycle challenge
                    if self.mode == "recycle":
                        self.deck.append({
                            "color": c.color,
                            "shape": c.shape,
                            "number": c.number,
                            "fill": c.fill,
                            "corner": c.corner
                        })
                    
                    # Remove selected card if outside board size
                    if c.card_pos >= self.num_cards:
                        self.current_board.remove(c)
                        c.destroy()

                    # Copy extra card properties and remove the old extra card
                    else:
                        x = cards_to_move.pop()
                        c.color = x.color
                        c.shape = x.shape
                        c.number = x.number
                        c.fill = x.fill
                        c.corner = x.corner
                        c.has_border = False
                        c.has_marker = x.has_marker
                        c.update()
                        self.current_board.remove(x)
                        x.destroy()

            self.update_board()

        # If not SET
        else:
            self.apply_penalty()

            # Unselect all cards
            for c in self.selected_cards:
                c.has_border = False
                c.update()
            self.selected_cards = []

            # Start AI
            if self.mode == "ai":
                self.ai.start()
    
    def quit_game(self):

        # Check if game is paused
        if self.pause_game_btn.paused:
        
            # Hide pause controls
            self.pause_game_text.hide()
            self.show_settings_btn.hide()
            for tile in self.settings_name_tiles:
                tile.hide()
            for tile in self.settings_values_tiles:
                tile.hide()

        else:

            # Hide game controls while dialogue is up
            for card in self.current_board:
                card.hide()
            self.add_cards_btn.setEnabled(False)
            if self.enable_hints:
                self.enable_hints.setEnabled(False)
                
            # Pause Call Set button
            if self.call_set_btn.called:
                if self.mode == "ai":
                    if not self.ai.in_selection:
                        self.call_set_btn.timer.stop()
                else:
                    self.call_set_btn.timer.stop() 

            # Stop selection delay if active
            if self.selection_delay_timer_active:
                self.selection_delay_timer.stop()

            # Pause timer if in time trial mode
            if self.mode in ["recycle", "xl", "time_trial"]:
                self.timer.stop()

            # Pause AI
            if self.mode == "ai":
                self.ai.pause()
            
        # Pause, Quit, and Call Set buttons are disabled in either case
        self.quit_game_btn.setEnabled(False)
        self.pause_game_btn.setEnabled(False)
        self.call_set_btn.setEnabled(False)

        # Show "quit game" controls
        self.quit_game_text.show()
        self.quit_game_yes.show()
        self.quit_game_no.show()

        # Update buttons
        self.pause_game_btn.update()
        self.update_buttons()

        # Manage focus
        self.quit_game_no.setFocus()

    def return_to_menu(self, time = None):

        # If time supplied in time trial or challenge
        if time:

            # Select list of times based on mode and settings
            time_key = f"{self.mode}_{self.num_traits}{self.num_variations}"
            times = self.main.times[time_key]

            if time not in times:
                times.append(time)
                times.sort()

                # Max times stored is 10
                if len(times) == 11:
                    if self.mode in ["recycle", "xs"]:
                        times.pop(0)
                    else:
                        times.pop()

                # Save new list of times
                self.main.times[time_key] = times
                with open("times.json", "w") as f:
                    dump(self.main.times, f, indent = 4)

        # Return to menu called from
        if self.mode == "time_trial":
            self.main.go_to_time_trial_page()
        elif self.mode in ["ai", "practice"]:
            self.main.go_to_main_menu()
        else:
            self.main.go_to_challenges_page()            
        self.destroy()

    def show_settings(self):
        if self.show_settings_btn.text() == "Show Current Settings":
            for tile in self.settings_name_tiles:
                tile.show()
            for tile in self.settings_values_tiles:
                tile.show()
            self.show_settings_btn.setText("Hide Current Settings")
        else:
            for tile in self.settings_name_tiles:
                tile.hide()
            for tile in self.settings_values_tiles:
                tile.hide()
            self.show_settings_btn.setText("Show Current Settings")

    def unquit_game(self):

        # Hide "quit game" controls
        self.quit_game_text.hide()
        self.quit_game_yes.hide()
        self.quit_game_no.hide()

        if self.pause_game_btn.paused:
            
            # Show pause controls
            self.pause_game_text.show()
            self.show_settings_btn.show()
            if self.show_settings_btn.text() == "Hide Current Settings":
                for tile in self.settings_name_tiles:
                    tile.show()
                for tile in self.settings_values_tiles:
                    tile.show()
        
        else:

            # Show all game controls
            self.call_set_btn.setEnabled(True)
            if len(self.sets) == 0 and self.deck:
                self.add_cards_btn.setEnabled(True)
            for card in self.current_board:
                card.show()
            if self.enable_hints:
                self.enable_hints.setEnabled(True)

            # Resume timer if in time trial mode
            if self.mode in ["recycle", "xl", "time_trial"]:
                self.timer.start(100)

            # Resume selection delay if active
            if self.selection_delay_timer_active:
                self.selection_delay_timer.start(self.main.settings["selection_delay"])

            # AI and Call Set button are not resumed until selection delay is over. Otherwise, start immediately
            else:

                # Resume Call Set countdown if active
                if self.call_set_btn.called:
                    if self.mode == "ai":
                        if not self.ai.in_selection:
                            self.call_set_btn.timer.start(100)
                    else:
                        self.call_set_btn.timer.start(100)    

                # Resume AI
                if self.mode == "ai":
                    self.ai.resume()

        # Renable Pause and Quit buttons
        self.quit_game_btn.setEnabled(True)
        self.pause_game_btn.setEnabled(True)

        # Update buttons
        self.pause_game_btn.update()
        self.update_buttons()

        # Manage focus
        self.quit_game_no.clearFocus()
    
    def update_board(self):

        # Count SETs and update
        self.sets = []
        self.count_sets(self.current_board, self.all_traits, self.all_traits)
        if self.show_num_sets:
            self.show_num_sets.setText(f"Number of SETs on board: {len(self.sets)}")

        if self.show_cards_left_in_deck:
            self.show_cards_left_in_deck.setText(f"Cards remaining in deck: {len(self.deck)}")

        # Update card positions
        for card in self.current_board:
            card.calc_position()

        # Reset Hints button
        if self.enable_hints:
            self.enable_hints.setEnabled(True)
            self.enable_hints.setText("Hint!")

            # Delete colored square if it exists
            if self.color_hint:
                self.color_hint.deleteLater()
                self.color_hint = None

        # Check if any SETs exist
        if len(self.sets) == 0:

            # Check if deck contains cards to draw
            if self.deck and self.mode != "xs": # Game is over if no SETS in XS challenge
                self.add_cards_btn.setEnabled(True)
                if self.enable_hints:
                    self.enable_hints.setEnabled(False)
            else:
                self.end_game()

        # Update buttons
        self.update_buttons()

        # Sort board based on card positions
        self.current_board.sort(key = lambda x: x.card_pos)

        # Start AI
        if self.mode == "ai" and not self.call_set_btn.called:
            self.ai.start()

        # Change cursor icon to arrow when cards become unclickable
        for card in self.current_board:
            card.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def update_buttons(self):

        self.call_set_btn.update_style()
        self.add_cards_btn.update_style()
        self.pause_game_btn.update_style()
        self.quit_game_btn.update_style()
        if self.enable_hints:
            self.enable_hints.update_style()
    
    def update_time(self):
        
        # Time is counted down for recycle challenge, up otherwise
        if self.mode == "recycle":
            self.elapsed_time -= 1
            if self.elapsed_time == 0:
                self.end_game()
        else:
            self.elapsed_time += 1

        # Format time as string
        time_str = self.main.translate_time(self.elapsed_time)
        
        # Update the label text
        self.display_time.setText(time_str)

    def __init__(self, main, mode):

        self.main = main
        self.mode = mode
        
        # Set flags for settings
        self.show_num_sets = (mode == "practice" and main.settings["show_num_sets"])
        self.show_cards_left_in_deck = main.settings["show_num_sets"]
        self.enable_hints = (mode == "practice" and main.settings["enable_hints"])

        # Initialize board values
        self.num_traits = main.settings["num_traits"]
        self.num_variations = main.settings["num_variations"] # Equal to number of cards per SET
        self.deck = []
        self.sets = []
        self.selected_cards = []
        self.current_board = []
        self.all_traits = ["color", "shape", "number", "fill", "corner"][:self.num_traits]
        self.all_properties = {
            "color": main.settings["colors"][:self.num_variations],
            "shape": main.settings["selected_shapes"][:self.num_variations],
            "number": [1, 2, 3, 4, 5][:self.num_variations],
            "fill": ["solid", "empty", "striped", "crossed", "dense"][:self.num_variations],
            "corner": ["none", "top_left", "top_right", "bottom_left", "bottom_right"][:self.num_variations]
        }

        # Set board and card dimensions
        match (self.num_traits, self.num_variations):
            case (3, 3):
                if self.mode == "xl":
                    self.board_width = 5
                    self.board_height = 3
                elif self.mode == "xs":
                    self.board_width = 3
                    self.board_height = 2
                else:
                    self.board_width = 3
                    self.board_height = 3
                self.card_length = main.screen_height // 4
            case (3, 4):
                if self.mode == "xl":
                    self.board_width = 7
                    self.board_height = 4
                elif self.mode == "xs":
                    self.board_width = 4
                    self.board_height = 3
                else:
                    self.board_width = 4
                    self.board_height = 4
                self.card_length = main.screen_height // 5
            case (3, 5):
                if self.mode == "xl":
                    self.board_width = 8
                    self.board_height = 5
                elif self.mode == "xs":
                    self.board_width = 5
                    self.board_height = 4
                else:
                    self.board_width = 5
                    self.board_height = 5
                self.card_length = main.screen_height // 6
            case (4, 3):
                if self.mode == "xl":
                    self.board_width = 7
                    self.board_height = 4
                elif self.mode == "xs":
                    self.board_width = 3
                    self.board_height = 3
                else:
                    self.board_width = 4
                    self.board_height = 3
                self.card_length = main.screen_height // 5
            case (4, 4):
                if self.mode == "xl":
                    self.board_width = 10
                    self.board_height = 6
                elif self.mode == "xs":
                    self.board_width = 6
                    self.board_height = 4
                else:
                    self.board_width = 7
                    self.board_height = 4
                self.card_length = main.screen_height // 7
            case (4, 5):
                if self.mode == "xl":
                    self.board_width = 12
                    self.board_height = 8
                elif self.mode == "xs":
                    self.board_width = 8
                    self.board_height = 5
                else:
                    self.board_width = 9
                    self.board_height = 5
                self.card_length = main.screen_height // 9
            case (5, 3):
                if self.mode == "xl":
                    self.board_width = 10
                    self.board_height = 6
                elif self.mode == "xs":
                    self.board_width = 5
                    self.board_height = 3
                else:
                    self.board_width = 6
                    self.board_height = 3
                self.card_length = main.screen_height // 7
            case (5, 4):
                if self.mode == "xl":
                    self.board_width = 12
                    self.board_height = 8
                elif self.mode == "xs":
                    self.board_width = 7
                    self.board_height = 6
                else:
                    self.board_width = 6
                    self.board_height = 8
                self.card_length = main.screen_height // 9
            case (5, 5):
                if self.mode == "xl":
                    self.board_width = 17
                    self.board_height = 10
                elif self.mode == "xs":
                    self.board_width = 9
                    self.board_height = 9
                else:
                    self.board_width = 9
                    self.board_height = 10
                self.card_length = main.screen_height // 12

        # Set indices for initializing deck
        if self.num_traits == 3:
            ll = 1
            mm = 1
        elif self.num_traits == 4:
            ll = self.num_variations
            mm = 1
        elif self.num_traits == 5:
            ll = self.num_variations
            mm = self.num_variations

        # Number of cards allowed on the board
        self.num_cards = self.board_height * self.board_width

        # Generate deck
        colors = main.settings["colors"]
        shapes = main.settings["selected_shapes"]
        numbers = (1, 2, 3, 4, 5)
        fills = ("solid", "empty", "striped", "crossed", "dense")
        corners = ("none", "top_left", "top_right", "bottom_left", "bottom_right")
        self.deck = [{"color": colors[i], "shape": shapes[j], "number": numbers[k], "fill": fills[l], "corner": corners[m]} for i in range(self.num_variations) for j in range(self.num_variations) for k in range(self.num_variations) for l in range(ll) for m in range(mm)]

        # Draw cards
        for i in range(self.num_cards):
            self.draw_card(i)
            
        # Create "Call Set" Button
        self.call_set_btn = CallSetButton(main, self)
        self.call_set_btn.setFocus()

        # Create "Add Cards" Button
        self.add_cards_btn = Button(
            main = main,
            text = f"Add {self.num_variations} Cards",
            font = QFont("Trebuchet MS", main.screen_height // 72),
            geometry = QRect(5 * main.screen_width // 120, 5 * main.screen_height // 9, main.screen_width // 15, main.screen_height // 30),
            connect = self.add_cards,
            enabled = False
        )
        self.add_cards_btn.show()

        # Create "Pause Game" controls
        # Button
        self.pause_game_btn = PauseButton(main, self)

        # Text
        self.pause_game_text = QLabel(
            parent = main.central_widget,
            text = "Game Paused",
            font = QFont("Trebuchet MS", main.screen_height // 30),
            geometry = QRect(49 * main.screen_width // 320, main.screen_height // 5, 271 * main.screen_width // 320, main.screen_height // 12),
            alignment = Qt.AlignmentFlag.AlignCenter
        )

        # Show settings button
        self.show_settings_btn = Button(
            main = main,
            text = "Show Current Settings",
            geometry = QRect(63 * main.screen_width // 128, 3 * main.screen_height // 10, main.screen_width // 6, main.screen_height // 12),
            font = QFont("Trebuchet MS", main.screen_height // 60),
            connect = self.show_settings
        )
        self.show_settings_btn.hide()

        # Tiles for viewing current settings
        boolean_translator = {
            True: "Yes",
            False: "No"
        }

        difficulty_translator = {
            2: "Easy",
            1.5: "Medium",
            1: "Hard",
            0.5: "Extreme"
        }

        settings_names = [
            "Number of Traits",
            "Number of Variations per Trait",
            "AI Difficulty",
            "Show the Number of SETs on the Board?",
            "Show the Number of Cards Remaining in the Deck?",
            "Format for Displaying Times",
            "Hints Enabled?",
            "Delay Before Removing Selected Cards"
        ]

        settings_vals = [
            str(main.settings["num_traits"]),
            str(main.settings["num_variations"]),
            difficulty_translator[main.settings["ai_difficulty"]],
            boolean_translator[main.settings["show_num_sets"]],
            boolean_translator[main.settings["show_cards_left_in_deck"]],
            main.settings["time_format"].title(),
            boolean_translator[main.settings["enable_hints"]],
            str(main.settings["selection_delay"]) + " seconds",
        ]
        
        self.settings_name_tiles = []
        self.settings_values_tiles = []
        for i in range(8):

            # Alternate light and dark tiles
            color = "e5daeb" if i % 2 else "ffffff"

            self.settings_name_tiles.append(QLabel(
                parent = main.central_widget,
                text = settings_names[i],
                geometry = QRect(237 * main.screen_width // 640, (3 * i + 27) * main.screen_height // 60, 99 * main.screen_width // 320, main.screen_height // 20),
                font = QFont("Trebuchet MS", main.screen_height // 60),
                alignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                styleSheet = f"background-color: #{color}; padding :{main.screen_height // 90}px"
            ))
            self.settings_name_tiles[i].hide()

            self.settings_values_tiles.append(QLabel(
                parent = main.central_widget,
                text = settings_vals[i],
                geometry = QRect(87 * main.screen_width // 128, (3 * i + 27) * main.screen_height // 60, 33 * main.screen_width // 320, main.screen_height // 20),
                font = QFont("Trebuchet MS", main.screen_height // 60),
                alignment = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                styleSheet = f"background-color: #{color}; padding :{main.screen_height // 90}px"
            ))
            self.settings_values_tiles[i].hide()

        # Create "Quit Game" Controls
        # Button
        self.quit_game_btn = Button(
            main = main,
            text = "Quit Game",
            geometry = QRect(9 * main.screen_width // 10, main.screen_height // 360, 63 * main.screen_width // 640, 2 * main.screen_height // 45),
            font = QFont("Trebuchet MS", main.screen_height // 60),
            connect = self.quit_game
        )
        self.quit_game_btn.show()

        # Text
        self.quit_game_text = QLabel(
            parent = main.central_widget,
            text = "Quit game and return to the main menu?",
            geometry = QRect(49 * main.screen_width // 320, main.screen_height // 4, 271 * main.screen_width // 320, main.screen_height // 12),
            font = QFont("Trebuchet MS", main.screen_height // 30),
            alignment = Qt.AlignmentFlag.AlignCenter
        )

        # Yes
        self.quit_game_yes = Button(
            main = main,
            text = "Yes",
            geometry = QRect(298 * main.screen_width // 640, 35 * main.screen_height // 72, main.screen_width // 16, main.screen_height // 12),
            font = QFont("Trebuchet MS", main.screen_height // 40),
            connect = self.return_to_menu
        )

        # No
        self.quit_game_no = Button(
            main = main,
            text = "No",
            geometry = QRect(400 * main.screen_width // 640, 35 * main.screen_height // 72, main.screen_width // 16, main.screen_height // 12),
            font = QFont("Trebuchet MS", main.screen_height // 40),
            connect = self.unquit_game
        )

        # Selection delay timer
        self.selection_delay_timer = QTimer(parent = main.central_widget)
        self.selection_delay_timer.timeout.connect(self.call_set_reset)
        self.selection_delay_timer_active = False

        # Show number of SETs on the board if enabled. Will only read from settings if in practice mode
        if self.show_num_sets:
            self.show_num_sets = QLabel(
                parent = main.central_widget,
                geometry = QRect(0, 0, main.screen_width // 5, main.screen_height // 20),
                font = QFont("Trebuchet MS", main.screen_height // 60),
                alignment = Qt.AlignmentFlag.AlignCenter
            )
            self.show_num_sets.show()

        # Show cards remaining in deck if enabled
        if self.show_cards_left_in_deck:

            # Left align control based on whether other controls exist
            show_cards_left_in_deck_pos = main.screen_width // 5 if self.show_num_sets else 0

            self.show_cards_left_in_deck = QLabel(
                parent = main.central_widget,
                geometry = QRect(show_cards_left_in_deck_pos, 0, main.screen_width // 5, main.screen_height // 20),
                font = QFont("Trebuchet MS", main.screen_height // 60),
                alignment = Qt.AlignmentFlag.AlignCenter
            )
            self.show_cards_left_in_deck.show()

        # Show button to display hints if enabled. Will only show in practice mode.
        if self.enable_hints:
            self.color_hint = None # For displaying colored squares in the hints bar
            self.enable_hints = Button(
                main = main,
                text = "Hint!",
                geometry = QRect(199 * main.screen_width // 320, main.screen_height // 360, main.screen_width // 4, 2 * main.screen_height // 45),
                font = QFont("Trebuchet MS", main.screen_height // 60),
                connect = self.get_hint
            )
            self.enable_hints.show()
            
        # Player score card
        self.player_score_card = QLabel(
            parent = main.central_widget,
            text = "0",
            geometry = QRect(0, 20 * main.screen_height // 90, 3 * main.screen_width // 20, 15 * main.screen_height // 90),
            font = QFont("Trebuchet MS", main.screen_height // 15),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.player_score_card.show()

        # Player score text
        match mode:
            case "recycle":
                score_text = "Score"
            case "xs":
                score_text = "Score"
            case "xl":
                score_text = "SETs Found"
            case "time_trial":
                score_text = "SETs Found"
            case "ai":
                score_text = "You"
            case "practice":
                score_text = "SETs Found"
        
        self.player_score_text = QLabel(
            parent = main.central_widget,
            text = score_text,
            geometry = QRect(0, 16 * main.screen_height // 90, 3 * main.screen_width // 20, 3 * main.screen_height // 90),
            font = QFont("Trebuchet MS", main.screen_height // 50),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.player_score_text.show()

        # Create timer for time trials/challenges
        if mode in ["time_trial", "recycle", "xl"]:
            
            # Initialize the timer
            self.timer = QTimer(parent = main.central_widget)
            self.timer.timeout.connect(self.update_time)

            # Set initial elapsed time
            if mode == "recycle":
                recycle_times = {
                    (3, 3): 600,
                    (3, 4): 1800,
                    (3, 5): 3000,
                    (4, 3): 3000,
                    (4, 4): 9000,
                    (4, 5): 18000,
                    (5, 3): 9000,
                    (5, 4): 27000,
                    (5, 5): 36000
                }
                self.elapsed_time = recycle_times[(self.num_traits, self.num_variations)]
            else:
                self.elapsed_time = 0

            # Start the timer with an interval of 100 ms
            self.timer.start(100)

            self.display_time = QLabel(
                parent = main.central_widget,
                text = main.translate_time(self.elapsed_time),
                geometry = QRect(2 * main.screen_width // 5, 0, main.screen_width // 5, main.screen_height // 20),
                font = QFont("Trebuchet MS", main.screen_height // 60),
                alignment = Qt.AlignmentFlag.AlignCenter
            )
            self.display_time.show()

            # Display final time
            self.final_time = QLabel(
                parent = main.central_widget,
                geometry = QRect(49 * main.screen_width // 320, 17 * main.screen_height // 60, 271 * main.screen_width // 320, main.screen_height // 12),
                font = QFont("Trebuchet MS", main.screen_height // 60),
                alignment = Qt.AlignmentFlag.AlignCenter
            )
            self.final_time.hide()

        # Init AI
        if mode == "ai":
            self.ai = AI(self, main.settings["ai_difficulty"])

            # AI score card
            self.ai_score_card = QLabel(
                parent = main.central_widget,
                text = "0",
                geometry = QRect(0, 68 * main.screen_height // 90, 3 * main.screen_width // 20, 15 * main.screen_height // 90),
                font = QFont("Trebuchet MS", main.screen_height // 15),
                alignment = Qt.AlignmentFlag.AlignCenter
            )
            self.ai_score_card.show()

            # AI score text
            self.ai_score_text = QLabel(
                parent = main.central_widget,
                text = "AI",
                geometry = QRect(0, 64 * main.screen_height // 90, 3 * main.screen_width // 20, 3 * main.screen_height // 90),
                font = QFont("Trebuchet MS", main.screen_height // 50),
                alignment = Qt.AlignmentFlag.AlignCenter
            )
            self.ai_score_text.show()

        # Game over text
        self.game_over_text = QLabel(
            parent = main.central_widget,
            geometry= QRect(49 * main.screen_width // 320, main.screen_height // 5, 271 * main.screen_width // 320, main.screen_height // 12),
            font = QFont("Trebuchet MS", main.screen_height // 30),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.game_over_text.hide()

        # Game over click event
        self.game_over = GameOver(main, self)

        # Create decorations
        self.info_panel_border = InfoPanelBorder(main)
        self.score_panel_border = ScorePanelBorder(main)

        # Set arrow navigation widgets
        self.call_set_btn.arrow_navigation(
            self.quit_game_btn, self.show_settings_btn, self.enable_hints, self.add_cards_btn,
            alt_right = self.pause_game_btn, alt_up = self.pause_game_btn, alt_down = self.quit_game_btn
        )
        self.add_cards_btn.arrow_navigation(
            self.quit_game_btn, self.show_settings_btn, self.call_set_btn, self.enable_hints,
            alt_right = self.pause_game_btn, alt_down = self.quit_game_btn
        )
        self.show_settings_btn.arrow_navigation(
            self.call_set_btn, self.enable_hints, self.pause_game_btn, self.pause_game_btn,
            alt_right = self.pause_game_btn
        )
        if self.enable_hints:
            self.enable_hints.arrow_navigation(
                self.show_settings_btn, self.pause_game_btn, self.add_cards_btn, self.call_set_btn,
                alt_left = self.call_set_btn, alt_up = self.call_set_btn
            )
        self.pause_game_btn.arrow_navigation(
            self.enable_hints, self.quit_game_btn, self.show_settings_btn, self.show_settings_btn,
            alt_left = self.call_set_btn, alt_up = self.call_set_btn, alt_down = self.call_set_btn
        )
        self.quit_game_btn.arrow_navigation(
            self.pause_game_btn, self.call_set_btn, self.add_cards_btn, self.show_settings_btn,
            alt_up = self.call_set_btn, alt_down = self.call_set_btn
        )
        self.quit_game_no.arrow_navigation(self.quit_game_yes, self.quit_game_yes, None, None)
        self.quit_game_yes.arrow_navigation(self.quit_game_no, self.quit_game_no, None, None)
        
        # Set Tab Order
        main.central_widget.setTabOrder(self.call_set_btn, self.add_cards_btn)
        
        if self.enable_hints:
            main.central_widget.setTabOrder(self.add_cards_btn, self.enable_hints)
            main.central_widget.setTabOrder(self.enable_hints, self.pause_game_btn)
        else:
            main.central_widget.setTabOrder(self.add_cards_btn, self.pause_game_btn)
            
        main.central_widget.setTabOrder(self.pause_game_btn, self.quit_game_btn)
        
        main.central_widget.setTabOrder(self.show_settings_btn, self.pause_game_btn)
        main.central_widget.setTabOrder(self.pause_game_btn, self.quit_game_btn)
        
        main.central_widget.setTabOrder(self.quit_game_yes, self.quit_game_no)

        self.update_board()
