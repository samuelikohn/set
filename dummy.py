from copy import deepcopy
from card import Card
from json import dump
from PyQt6.QtCore import QRect, Qt, QTimer
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtWidgets import QLabel, QScrollArea, QWidget
from random import choice, shuffle
from ui import Button, CallSetButton, GameOver, InfoPanelBorder, PauseButton, ScorePanelBorder


class DummyAddCardsButton:

    def setEnabled(self, _):
        pass

    def __init__(self):
        pass


class DummyBoard:

    def card_clicked(self, _):
        pass

    def __init__(self, main, card_length):
        self.main = main
        self.card_length = card_length
        self.board_height = 1
        self.current_board = [None]
        self.ai = None
        self.call_set_btn = DummyButton()

    
class DummyButton:

    def __init__(self):
        self.called = False


class StaticBoard:

    def add_to_found_display(self):

        for i, card in enumerate(self.selected_cards):
            self.found_cards.append(Card(
                card.color,
                card.shape,
                card.number,
                card.fill,
                card.corner,
                0,
                DummyBoard(self.main, self.main.screen_width // 40),
                geometry = QRect(
                    (34 * i - 17 * self.num_variations + 91) * self.main.screen_width // 1280,
                    (17 * len(self.unique_sets) + 188) * self.main.screen_height // 360,
                    self.main.screen_width // 40,
                    self.main.screen_width // 40
                )
            ))
            self.found_cards[-1].show()

        self.choose_panel.setGeometry(
            self.main.screen_width // 640,
            17 * self.main.screen_height // 30,
            47 * self.main.screen_width // 320,
            len(self.unique_sets) * 17 * self.main.screen_height // 360
        )
        
    def call_set(self):

        # Change cursor icon to pointing hand over cards when clickable
        for card in self.current_board:
            card.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        # Styling is updated over 10 seconds at 10 updates/sec
        if not self.call_set_btn.called:
            self.call_set_btn.called = True
            self.call_set_btn.timer.start(100)

    def call_set_reset(self, remove_cards, is_set):

        self.selection_delay_timer.stop()
        self.selection_delay_timer_active = False

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
        
        else:
            self.process_cards(is_set)

    def call_set_stop_timer(self, remove_cards = False, is_set = None):
        
        # Stop timer
        self.call_set_btn.timer.stop()

        # Update button text based on called condition, pause, then continue
        self.call_set_btn.called = False
        if is_set == True:
            if self.selected_cards in self.unique_sets:
                self.call_set_btn.setText("SET Already\nFound!")
            else:
                self.call_set_btn.setText("SET!")
        elif is_set == False:
            self.call_set_btn.setText("Not a SET!")
        elif remove_cards:
            self.call_set_btn.setText("Time's Up!")

        # Delay before processing selected cards
        self.selection_delay_timer.timeout.disconnect()
        self.selection_delay_timer.timeout.connect(lambda: self.call_set_reset(remove_cards, is_set))
        self.selection_delay_timer.start(1000 * self.main.settings["selection_delay"])
        self.selection_delay_timer_active = True
            
    def call_set_update_button(self):
        
        # Stop updates after 100 total
        if self.call_set_btn.time_left == 0:

            # Apply time penalty, amount based on settings
            self.elapsed_time += self.main.settings["num_variations"] ** self.main.settings["num_traits"]
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
        
    def card_clicked(self, card, _):

        # Toggle card selection border
        card.has_border = not card.has_border
        card.update()

        if card in self.selected_cards:
            self.selected_cards.remove(card)
        else:
            self.selected_cards.append(card)
            if len(self.selected_cards) == self.num_variations:

                self.selected_cards.sort()
                
                # Stop "Call Set" timer
                self.call_set_stop_timer(is_set = self.is_set(self.selected_cards))
    
    def destroy(self):
        for card in self.current_board:
            card.deleteLater()
        for card in self.found_cards:
            card.deleteLater()
        self.info_panel_border.destroy()
        self.score_panel_border.destroy()
        self.call_set_btn.destroy()
        self.pause_game_btn.destroy()
        self.quit_game_btn.deleteLater()
        self.quit_game_text.deleteLater()
        self.quit_game_yes.deleteLater()
        self.quit_game_no.deleteLater()
        self.show_settings_btn.deleteLater()
        self.challenge_score_card.deleteLater()
        self.challenge_score_text.deleteLater()
        self.choose_panel.deleteLater()
        self.scroller.deleteLater()
        for tile in self.settings_name_tiles:
            tile.deleteLater()
        for tile in self.settings_values_tiles:
            tile.deleteLater()
        if self.timer:
            self.timer.deleteLater()
            self.display_time.deleteLater()
            self.final_time.deleteLater()
        self.game_over_text.deleteLater()
        self.game_over.destroy()
        self.selection_delay_timer.deleteLater()
        self.main.board = None

    def draw_sets(self):

        cards = []
        i = 0
        while i < (self.num_cards // self.num_variations):

            # Draw 2 random cards
            card_id1 = choice(self.deck)
            self.deck.remove(card_id1)
            cards.append(card_id1)

            card_id2 = choice(self.deck)
            self.deck.remove(card_id2)
            cards.append(card_id2)

            # Define list of acceptable variations for each trait
            all_vars = deepcopy(self.all_properties)
            for trait in all_vars:
                    
                # If cards 1 and 2 share a variation, only that variation is acceptable
                if card_id1[trait] == card_id2[trait]:
                    all_vars[trait] = [card_id1[trait]]

                # If different variations, all completely different variations are acceptable
                else:
                    all_vars[trait].remove(card_id1[trait])
                    all_vars[trait].remove(card_id2[trait])

            # If 4 cards per SET
            if self.num_variations > 3:

                # Card 3 must have acceptable variations for all traits
                card_id3 = choice(self.deck)
                while any(card_id3[trait] not in all_vars[trait] for trait in all_vars):
                    card_id3 = choice(self.deck)
                cards.append(card_id3)
                self.deck.remove(card_id3)

                # Update list of acceptable variations for card 3
                for trait in self.all_traits:
                    if card_id3[trait] != card_id1[trait]:
                        all_vars[trait].remove(card_id3[trait])

                # If 5 cards per SET
                if self.num_variations > 4:

                    # Card 4 must have acceptable variations for all traits
                    card_id4 = choice(self.deck)
                    while any(card_id4[trait] not in all_vars[trait] for trait in all_vars):
                        card_id4 = choice(self.deck)
                    cards.append(card_id4)
                    self.deck.remove(card_id4)

                    # Update list of acceptable variations for card 4
                    for trait in self.all_traits:
                        if card_id4[trait] != card_id1[trait]:
                            all_vars[trait].remove(card_id4[trait])

            # Calculate last card needed to complete the SET
            last_card_id = {trait: all_vars[trait][0] for trait in all_vars}

            # If last card is shared between different sets, discard last set and redraw
            if last_card_id in self.deck:
                cards.append(last_card_id)
                self.deck.remove(last_card_id)
            else:
                for _ in range(self.num_variations - 1):
                    cards.pop()
                i -= 1

            i += 1

        # Shuffle all cards then place on screen
        shuffle(cards)
        card_pos = 0
        while cards:
            card_id = cards.pop()        
            self.current_board.append(Card(
                card_id["color"],
                card_id["shape"],
                card_id["number"],
                card_id["fill"],
                card_id["corner"],
                card_pos,
                self
            ))
            card_pos += 1

    def end_game(self):
            
        # Hide cards
        for card in self.current_board:
            card.hide()

        # Disable buttons
        self.pause_game_btn.setEnabled(False)
        self.quit_game_btn.setEnabled(False)
        self.call_set_btn.setEnabled(False)
        self.update_buttons()

        # Show final time
        self.timer.stop()
        self.final_time.setText(f"Final Time: {self.main.translate_time(self.elapsed_time)}")
        self.final_time.show()

        # Check list of scores for current settings and static challenge
        times = self.main.scores[f"{"static"}_{self.main.settings["num_traits"]}{self.main.settings["num_variations"]}"]
        
        # Static challenge: Check if elapsed time is new min for times
        if not times or self.elapsed_time < min(times):
            self.game_over_text.setText("New High Score!")

        else:
            self.game_over_text.setText("Game Over")

        self.game_over_text.show()

        # Set focus after texts to guarantee next event registers with game over screen
        self.game_over.show()
        self.game_over.setFocus()
    
    def is_set(self, cards):
        traits = ["color", "shape", "number", "fill", "corner"][:self.num_traits]
        for trait in traits:
            num_values = len(set([getattr(card, trait) for card in cards]))
            if num_values != 1 and num_values != self.num_variations:
                return False
        return True
    
    def process_cards(self, is_set):
                
        # If SET
        if is_set:

            if self.selected_cards not in self.unique_sets:

                # Keep track of sets found
                self.unique_sets.append(self.selected_cards)
                self.add_to_found_display()

                # Increment score
                current_score = self.challenge_score_card.text()[0]
                self.challenge_score_card.setText(f"{int(current_score) + 1}/{self.num_cards // self.num_variations}")

            self.update_board()

        # If not SET
        else:

            # Apply time penalty if in time trial mode/challenge, amount based on settings
            self.elapsed_time += self.main.settings["num_variations"] ** self.main.settings["num_traits"]

        # Unselect all cards
        for c in self.selected_cards:
            c.has_border = False
            c.update()
        self.selected_cards = []

        if len(self.unique_sets) == self.num_cards // self.num_variations:
            self.end_game()
    
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

            for card in self.found_cards:
                card.hide()
                
            # Pause Call Set button
            if self.call_set_btn.called:
                self.call_set_btn.timer.stop() 

            # Stop selection delay if active
            if self.selection_delay_timer_active:
                self.selection_delay_timer.stop()

            # Pause timer
            self.timer.stop()
            
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

    def return_to_menu(self, static_score = None):

        if static_score:

            # Get existing scores for current settings
            score_key = f"static_{self.main.settings["num_traits"]}{self.main.settings["num_variations"]}"
            scores = self.main.scores[score_key]
            scores.append(static_score)
            scores.sort()

            # Max scores stored is 10
            if len(scores) == 11:
                scores.pop()

            # Save new list of scores
            self.main.scores[score_key] = scores
            with open("scores.json", "w") as f:
                dump(self.main.scores, f, indent = 4)

            self.main.go_to_challenges_page()

        else:
            self.main.go_to_main_menu()

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
            for card in self.current_board:
                card.show()

            for card in self.found_cards:
                card.show()

            # Resume timer
            self.timer.start(100)

            # Resume selection delay if active
            if self.selection_delay_timer_active:
                self.selection_delay_timer.start(self.main.settings["selection_delay"])

            # AI and Call Set button are not resumed until selection delay is over. Otherwise, start immediately
            else:

                # Resume Call Set countdown if active
                if self.call_set_btn.called:
                    self.call_set_btn.timer.start(100)    

        # Renable Pause and Quit buttons
        self.quit_game_btn.setEnabled(True)
        self.pause_game_btn.setEnabled(True)

        # Update buttons
        self.pause_game_btn.update()
        self.update_buttons()

        # Manage focus
        self.quit_game_no.clearFocus()
    
    def update_board(self):

        # Update card positions
        for card in self.current_board:
            card.calc_position()

        # Update buttons
        self.update_buttons()

        # Sort board based on card positions
        self.current_board.sort(key = lambda x: x.card_pos)

        # Change cursor icon to arrow when cards become unclickable
        for card in self.current_board:
            card.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def update_buttons(self):
        self.call_set_btn.update_style()
        self.pause_game_btn.update_style()
        self.quit_game_btn.update_style()
    
    def update_time(self):
        
        # Increment time
        self.elapsed_time += 1

        # Format time as string
        time_str = self.main.translate_time(self.elapsed_time)
        
        # Update the label text
        self.display_time.setText(time_str)

    def __init__(
            self,
            main,
            num_traits,
            num_variations
        ):

        self.main = main
        self.unique_sets = []
        self.found_cards = []

        # Dummy attributes
        self.ai = None
        self.challenge_type = "static"
        self.add_cards_btn = DummyAddCardsButton()
        self.enable_hints = None
        self.sets = []

        # Initialize board values
        self.num_traits = num_traits
        self.num_variations = num_variations # Equal to number of cards per SET
        self.deck = []
        self.selected_cards = []
        self.current_board = []
        self.all_traits = ["color", "shape", "number", "fill", "corner"][:num_traits]
        self.all_properties = {
            "color": main.settings["colors"][:num_variations],
            "shape": main.settings["selected_shapes"][:num_variations],
            "number": [1, 2, 3, 4, 5][:num_variations],
            "fill": ["solid", "empty", "striped", "crossed", "dense"][:num_variations],
            "corner": ["none", "top_left", "top_right", "bottom_left", "bottom_right"][:num_variations]
        }

        # Set board and card dimensions
        match (num_traits, num_variations):
            case (3, 3):
                self.board_width = 3
                self.board_height = 3
                self.card_length = main.screen_height // 4
            case (3, 4):
                self.board_width = 4
                self.board_height = 4
                self.card_length = main.screen_height // 5
            case (3, 5):
                self.board_width = 5
                self.board_height = 5
                self.card_length = main.screen_height // 6
            case (4, 3):
                self.board_width = 4
                self.board_height = 3
                self.card_length = main.screen_height // 5
            case (4, 4):
                self.board_width = 7
                self.board_height = 4
                self.card_length = main.screen_height // 7
            case (4, 5):
                self.board_width = 9
                self.board_height = 5
                self.card_length = main.screen_height // 9
            case (5, 3):
                self.board_width = 6
                self.board_height = 3
                self.card_length = main.screen_height // 7
            case (5, 4):
                self.board_width = 6
                self.board_height = 8
                self.card_length = main.screen_height // 9
            case (5, 5):
                self.board_width = 9
                self.board_height = 10
                self.card_length = main.screen_height // 12

        # Set indices for initializing deck
        if num_traits == 3:
            ll = 1
            mm = 1
        elif num_traits == 4:
            ll = num_variations
            mm = 1
        elif num_traits == 5:
            ll = num_variations
            mm = num_variations

        # Number of cards allowed on the board
        self.num_cards = self.board_height * self.board_width

        # Generate deck
        colors = main.settings["colors"]
        shapes = main.settings["selected_shapes"]
        numbers = (1, 2, 3, 4, 5)
        fills = ("solid", "empty", "striped", "crossed", "dense")
        corners = ("none", "top_left", "top_right", "bottom_left", "bottom_right")
        self.deck = [{"color": colors[i], "shape": shapes[j], "number": numbers[k], "fill": fills[l], "corner": corners[m]} for i in range(num_variations) for j in range(num_variations) for k in range(num_variations) for l in range(ll) for m in range(mm)]

        # Draw cards to guarantee a minimum number of SETs
        self.draw_sets()
            
        # Create "Call Set" Button
        self.call_set_btn = CallSetButton(main, self)
        self.call_set_btn.setFocus()

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

        # Score card
        self.challenge_score_card = QLabel(
            parent = main.central_widget,
            text = f"0/{self.num_cards // self.num_variations}",
            geometry = QRect(0, 20 * main.screen_height // 90, 3 * main.screen_width // 20, 15 * main.screen_height // 90),
            font = QFont("Trebuchet MS", main.screen_height // 15),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.challenge_score_card.show()

        # Score text
        self.challenge_score_text = QLabel(
            parent = main.central_widget,
            text = "SETs Found",
            geometry = QRect(0, 16 * main.screen_height // 90, 3 * main.screen_width // 20, 3 * main.screen_height // 90),
            font = QFont("Trebuchet MS", main.screen_height // 50),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.challenge_score_text.show()

        # Display found SETs
        # Choose Panel
        self.choose_panel = QWidget(
            parent = main.central_widget,
            geometry = QRect(main.screen_width // 640, 17 * main.screen_height // 30, 47 * main.screen_width // 320, main.screen_height // 360)
        )
        self.choose_panel.show()

        # Scroller for custom colors
        self.scroller = QScrollArea(
            parent = main.central_widget,
            verticalScrollBarPolicy = Qt.ScrollBarPolicy.ScrollBarAlwaysOn,
            horizontalScrollBarPolicy = Qt.ScrollBarPolicy.ScrollBarAlwaysOff,
            geometry = QRect(main.screen_width // 640, 17 * main.screen_height // 30, 47 * main.screen_width // 320, 5 * main.screen_height // 12),
            styleSheet = "QScrollArea {border: 2px inset gray;}"
        )
        self.scroller.setWidget(self.choose_panel)
        self.scroller.show()

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

        # Initialize timer
        self.timer = QTimer(parent = main.central_widget)
        self.timer.timeout.connect(self.update_time)

        # Set initial elapsed time
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
            self.quit_game_btn, self.show_settings_btn, self.pause_game_btn, self.quit_game_btn,
            alt_right = self.pause_game_btn
        )
        self.show_settings_btn.arrow_navigation(self.call_set_btn, self.pause_game_btn, self.pause_game_btn, self.pause_game_btn)
        self.pause_game_btn.arrow_navigation(
            self.call_set_btn, self.quit_game_btn, self.show_settings_btn, self.show_settings_btn,
            alt_up = self.call_set_btn, alt_down = self.call_set_btn
        )
        self.quit_game_btn.arrow_navigation(
            self.pause_game_btn, self.call_set_btn, self.call_set_btn, self.show_settings_btn,
            alt_down = self.call_set_btn
        )
        self.quit_game_no.arrow_navigation(self.quit_game_yes, self.quit_game_yes, None, None)
        self.quit_game_yes.arrow_navigation(self.quit_game_no, self.quit_game_no, None, None)
        
        # Set Tab Order
        main.central_widget.setTabOrder(self.call_set_btn, self.pause_game_btn)    
        main.central_widget.setTabOrder(self.pause_game_btn, self.quit_game_btn)
        
        main.central_widget.setTabOrder(self.show_settings_btn, self.pause_game_btn)
        main.central_widget.setTabOrder(self.pause_game_btn, self.quit_game_btn)
        
        main.central_widget.setTabOrder(self.quit_game_yes, self.quit_game_no)

        self.update_board()