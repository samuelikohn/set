from board import Board
from dummy import StaticBoard
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel
from ui import Button, Dropdown


class Challenges:

    def destroy(self):
        self.title.deleteLater()
        self.play_btn.deleteLater()
        self.scores_btn.deleteLater()
        self.return_to_menu_btn.deleteLater()
        self.recycle_cards_btn.deleteLater()
        self.recycle_cards_text.deleteLater()
        self.static_board_btn.deleteLater()
        self.static_board_text.deleteLater()
        self.xl_board_btn.deleteLater()
        self.xl_board_text.deleteLater()
        self.xs_board_btn.deleteLater()
        self.xs_board_text.deleteLater()
        self.go_back_from_challenges_btn.deleteLater()
        self.scores_title.deleteLater()
        self.static_scores_btn.deleteLater()
        self.recycle_scores_btn.deleteLater()
        self.xl_scores_btn.deleteLater()
        self.xs_scores_btn.deleteLater()
        self.num_traits_text.deleteLater()
        self.traits_list.deleteLater()
        self.num_variations_text.deleteLater()
        self.variations_list.deleteLater()
        for tile in self.background_tiles:
            tile.deleteLater()
        self.go_back_from_scores_btn.deleteLater
        self.main.challenges_page = None

    def display_scores(self, btn = None):

        # Update buttons
        challenge_type = None
        if btn == "static":
            self.static_scores_btn.setEnabled(False)
            self.recycle_scores_btn.setEnabled(True)
            self.xl_scores_btn.setEnabled(True)
            self.xs_scores_btn.setEnabled(True)
            challenge_type = btn

        elif btn == "recycle":
            self.static_scores_btn.setEnabled(True)
            self.recycle_scores_btn.setEnabled(False)
            self.xl_scores_btn.setEnabled(True)
            self.xs_scores_btn.setEnabled(True)
            challenge_type = btn

        elif btn == "xl":
            self.static_scores_btn.setEnabled(True)
            self.recycle_scores_btn.setEnabled(True)
            self.xl_scores_btn.setEnabled(False)
            self.xs_scores_btn.setEnabled(True)
            challenge_type = btn

        elif btn == "xs":
            self.static_scores_btn.setEnabled(True)
            self.recycle_scores_btn.setEnabled(True)
            self.xl_scores_btn.setEnabled(True)
            self.xs_scores_btn.setEnabled(False)
            challenge_type = btn

        else:
            button_codes = {
                self.static_scores_btn.isEnabled(): "static",
                self.recycle_scores_btn.isEnabled(): "recycle",
                self.xl_scores_btn.isEnabled(): "xl",
                self.xs_scores_btn.isEnabled(): "xs"
            }
            for b in button_codes:
                if not b:
                    challenge_type = button_codes[b]
                    break

        self.update_buttons()

        if challenge_type and self.traits_list.currentText() != "Select..." and self.variations_list.currentText() != "Select...":

            # Show scores
            for i in range(10):
                self.background_tiles[i].setText("") # Erase currently displayed scores

            # Set text to background tiles
            score_key = f"{challenge_type}_{self.traits_list.currentText()}{self.variations_list.currentText()}"
            if self.main.scores[score_key]:
                i = 0
                for score in self.main.scores[score_key]:
                    if challenge_type == "recycle" or challenge_type == "xs":

                        # Reverse ordering for score based challenges
                        self.background_tiles[len(self.main.scores[score_key]) - i - 1].setText(f"{score} SET{"" if score == 1 else "s"}")
                    else:
                        self.background_tiles[i].setText(self.main.translate_time(score))
                    i += 1

            # If no scores recorded
            else:
                translator = {
                    "static": "Static Board",
                    "recycle": "Recycle Cards",
                    "xl": "XL Board",
                    "xs": "XS Board"
                }
                self.background_tiles[0].setText(f"No {translator[challenge_type]} challenges completed for these Settings!")

    def go_back_from_challenges(self):
        
        # Hide challenges controls
        self.static_board_btn.hide()
        self.static_board_text.hide()
        self.recycle_cards_btn.hide()
        self.recycle_cards_text.hide()
        self.xl_board_btn.hide()
        self.xl_board_text.hide()
        self.xs_board_btn.hide()
        self.xs_board_text.hide()
        self.go_back_from_challenges_btn.hide()

        # Show main page controls
        self.play_btn.show()
        self.scores_btn.show()
        self.return_to_menu_btn.show()

        # Manage focus
        self.play_btn.setFocus()

    def go_back_from_scores(self):

        # Reset controls for viewing scores
        for i in range(10):
            self.background_tiles[i].setText("")
        self.traits_list.setCurrentText("Select...")
        self.variations_list.setCurrentText("Select...")
        self.static_scores_btn.setEnabled(True)
        self.recycle_scores_btn.setEnabled(True)
        self.xl_scores_btn.setEnabled(True)
        self.xs_scores_btn.setEnabled(True)
        self.update_buttons()
        
        # Hide scores page controls
        self.scores_title.hide()
        self.static_scores_btn.hide()
        self.recycle_scores_btn.hide()
        self.xl_scores_btn.hide()
        self.xs_scores_btn.hide()
        self.num_traits_text.hide()
        self.traits_list.hide()
        self.num_variations_text.hide()
        self.variations_list.hide()
        for tile in self.background_tiles:
            tile.hide()
        self.go_back_from_scores_btn.hide()

        # Show main page controls
        self.title.show()
        self.play_btn.show()
        self.scores_btn.show()
        self.return_to_menu_btn.show()

        # Manage focus
        self.play_btn.setFocus()

    def play(self):

        # Hide main page controls
        self.play_btn.hide()
        self.scores_btn.hide()
        self.return_to_menu_btn.hide()

        # Show challenges controls
        self.static_board_btn.show()
        self.static_board_text.show()
        self.recycle_cards_btn.show()
        self.recycle_cards_text.show()
        self.xl_board_btn.show()
        self.xl_board_text.show()
        self.xs_board_btn.show()
        self.xs_board_text.show()
        self.go_back_from_challenges_btn.show()

        # Manage focus
        self.static_board_btn.setFocus()

    def recycle_cards(self):     
        self.main.board = Board(
            self.main,
            self.main.settings["num_traits"],
            self.main.settings["num_variations"],
            show_cards_left_in_deck = self.main.settings["show_cards_left_in_deck"],
            called_from_recycle_challenge = True
        )
        self.destroy()

    def return_to_menu(self):
        self.main.go_to_main_menu()
        self.destroy()

    def scores(self):

        # Hide menu controls
        self.title.hide()
        self.play_btn.hide()
        self.scores_btn.hide()
        self.return_to_menu_btn.hide()

        # Show controls for viewing scores
        self.scores_title.show()
        self.static_scores_btn.show()
        self.recycle_scores_btn.show()
        self.xl_scores_btn.show()
        self.xs_scores_btn.show()
        self.num_traits_text.show()
        self.traits_list.show()
        self.num_variations_text.show()
        self.variations_list.show()
        self.go_back_from_scores_btn.show()
        for tile in self.background_tiles:
            tile.show()

        # Manage focus
        self.traits_list.setFocus()

    def static_board(self):
        self.main.board = StaticBoard(
            self.main,
            self.main.settings["num_traits"],
            self.main.settings["num_variations"]
        )
        self.destroy()

    def update_buttons(self):
        self.static_scores_btn.update_style()
        self.recycle_scores_btn.update_style()
        self.xl_scores_btn.update_style()
        self.xs_scores_btn.update_style()

    def xl_board(self):
        self.main.board = Board(
            self.main,
            self.main.settings["num_traits"],
            self.main.settings["num_variations"],
            show_cards_left_in_deck = self.main.settings["show_cards_left_in_deck"],
            called_from_xl_challenge = True
        )
        self.destroy()

    def xs_board(self):
        self.main.board = Board(
            self.main,
            self.main.settings["num_traits"],
            self.main.settings["num_variations"],
            show_cards_left_in_deck = self.main.settings["show_cards_left_in_deck"],
            called_from_xs_challenge = True
        )
        self.destroy()

    def __init__(self, main):
        
        self.main = main

        # Main Page
        # Title
        self.title = QLabel(
            parent = main.central_widget,
            text = "Challenges",
            font = QFont("Trebuchet MS", main.screen_height // 30),
            geometry = QRect(5 * main.screen_width // 12, main.screen_height // 24, main.screen_width // 6, main.screen_height // 20),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.title.show()

        # Play button shows challenge formats
        self.play_btn = Button(
            main = main,
            text = "Play",
            geometry = QRect(5 * main.screen_width // 12, 7 * main.screen_height // 24, main.screen_width // 6, main.screen_height // 12),
            font = QFont("Trebuchet MS", main.screen_height // 30),
            connect = self.play
        )
        self.play_btn.show()
        self.play_btn.setFocus()

        # Scores button shows list of scores with challenge format selector
        self.scores_btn = Button(
            main = main,
            text = "View Scores",
            geometry = QRect(5 * main.screen_width // 12, 11 * main.screen_height // 24, main.screen_width // 6, main.screen_height // 12),
            font = QFont("Trebuchet MS", main.screen_height // 30),
            connect = self.scores
        )
        self.scores_btn.show()

        # Return to main menu
        self.return_to_menu_btn = Button(
            main = main,
            text = "Return to Main Menu",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(7 * main.screen_width // 8, main.screen_height // 360, 79 * main.screen_width // 640, main.screen_height // 24),
            connect = self.return_to_menu
        )
        self.return_to_menu_btn.show()

        # Challenges Page
        # Find fixed number of SETs on static board
        self.static_board_btn = Button(
            main = main,
            text = "Static Board",
            geometry = QRect(main.screen_width // 6, 5 * main.screen_height // 24, main.screen_width // 4, main.screen_height // 12),
            font = QFont("Trebuchet MS", main.screen_height // 30),
            connect = self.static_board
        )
        self.static_board_btn.hide()

        # Static board explanation
        static_num_sets = {
            (3, 3): 3,
            (3, 4): 4,
            (3, 5): 5,
            (4, 3): 4,
            (4, 4): 7,
            (4, 5): 9,
            (5, 3): 6,
            (5, 4): 12,
            (5, 5): 18
        }
        self.static_board_text = QLabel(
            parent = main.central_widget,
            text = f"How fast can you find {static_num_sets[(main.settings["num_traits"], main.settings["num_variations"])]} SETs on\na static board? Cards are not\nremoved when a SET is found.",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(main.screen_width // 6, 7 * main.screen_height // 24, main.screen_width // 4, main.screen_height // 8),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.static_board_text.hide()

        # Fixed timer, cards recycled after SET
        self.recycle_cards_btn = Button(
            main = main,
            text = "Recycle Cards",
            geometry = QRect(7 * main.screen_width // 12, 5 * main.screen_height // 24, main.screen_width // 4, main.screen_height // 12),
            font = QFont("Trebuchet MS", main.screen_height // 30),
            connect = self.recycle_cards
        )
        self.recycle_cards_btn.hide()

        # Recycle cards explanation
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
        recycle_time = recycle_times[(main.settings["num_traits"], main.settings["num_variations"])] // 600
        self.recycle_cards_text = QLabel(
            parent = main.central_widget,
            text = f"How many SETs can you find in {recycle_time}\nminute{"" if recycle_time == 1 else "s"}? Cards are recycled back\ninto the deck when a SET is found.",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(7 * main.screen_width // 12, 7 * main.screen_height // 24, main.screen_width // 4, main.screen_height // 8),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.recycle_cards_text.hide()

        # XL board
        self.xl_board_btn = Button(
            main = main,
            text = "XL Board",
            geometry = QRect(main.screen_width // 6, 13 * main.screen_height // 24, main.screen_width // 4, main.screen_height // 12),
            font = QFont("Trebuchet MS", main.screen_height // 30),
            connect = self.xl_board
        )
        self.xl_board_btn.hide()

        # XL Board explanation
        self.xl_board_text = QLabel(
            parent = main.central_widget,
            text = "How fast can you complete a game\nusing an extra large board?",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(main.screen_width // 6, 5 * main.screen_height // 8, main.screen_width // 4, main.screen_height // 8),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.xl_board_text.hide()

        # XS board, game over on no SETs
        self.xs_board_btn = Button(
            main = main,
            text = "XS Board",
            geometry = QRect(7 * main.screen_width // 12, 13 * main.screen_height // 24, main.screen_width // 4, main.screen_height // 12),
            font = QFont("Trebuchet MS", main.screen_height // 30),
            connect = self.xs_board
        )
        self.xs_board_btn.hide()

        # XS Board explanation
        self.xs_board_text = QLabel(
            parent = main.central_widget,
            text = "How many SETs can you find on\nan extra small board? If no\nSETs exist, the game is over.",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(7 * main.screen_width // 12, 5 * main.screen_height // 8, main.screen_width // 4, main.screen_height // 8),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.xs_board_text.hide()

        # Return to main page from challenges page
        self.go_back_from_challenges_btn = Button(
            main = main,
            text = "Go Back",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(7 * main.screen_width // 8, main.screen_height // 360, 79 * main.screen_width // 640, main.screen_height // 24),
            connect = self.go_back_from_challenges
        )
        self.go_back_from_challenges_btn.hide()

        # Scores Page
        # Title
        self.scores_title = QLabel(
            parent = main.central_widget,
            text = "Select Number of Traits, Variations, and Challenge Type",
            font = QFont("Trebuchet MS", main.screen_height // 30),
            geometry = QRect(main.screen_width // 8, main.screen_height // 24, 3 * main.screen_width // 4, main.screen_height // 20),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.scores_title.hide()

        # Number of traits text
        self.num_traits_text = QLabel(
            parent = main.central_widget,
            text = "Number of Traits",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(7 * main.screen_width // 24, main.screen_height // 6, main.screen_width // 6, main.screen_height // 20),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.num_traits_text.hide()

        # Number of variations text
        self.num_variations_text = QLabel(
            parent = main.central_widget,
            text = "Number of Variations",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(13 * main.screen_width // 24, main.screen_height // 6, main.screen_width // 6, main.screen_height // 20),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.num_variations_text.hide()

        # Traits dropdown
        self.traits_list = Dropdown(
            main = main,
            currentText = "Select...",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(main.screen_width // 3, 13 * main.screen_height // 60, main.screen_width // 12, main.screen_height // 20)
        )
        self.traits_list.addItems(["Select...", "3", "4", "5"])
        self.traits_list.hide()

        # Variations dropdown
        self.variations_list = Dropdown(
            main = main,
            currentText = "Select...",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(7 * main.screen_width // 12, 13 * main.screen_height // 60, main.screen_width // 12, main.screen_height // 20)
        )
        self.variations_list.addItems(["Select...", "3", "4", "5"])
        self.variations_list.hide()

        # Static board score button
        self.static_scores_btn = Button(
            main = main,
            text = "Static Board",
            geometry = QRect(3 * main.screen_width // 10, 19 * main.screen_height // 60, main.screen_width // 10, main.screen_height // 20),
            font = QFont("Trebuchet MS", main.screen_height // 60)
        )
        self.static_scores_btn.hide()

        # Recycle cards score button
        self.recycle_scores_btn = Button(
            main = main,
            text = "Recycle Cards",
            geometry = QRect(2 * main.screen_width // 5, 19 * main.screen_height // 60, main.screen_width // 10, main.screen_height // 20),
            font = QFont("Trebuchet MS", main.screen_height // 60)
        )
        self.recycle_scores_btn.hide()

        # XL board score button
        self.xl_scores_btn = Button(
            main = main,
            text = "XL Board",
            geometry = QRect(main.screen_width // 2, 19 * main.screen_height // 60, main.screen_width // 10, main.screen_height // 20),
            font = QFont("Trebuchet MS", main.screen_height // 60)
        )
        self.xl_scores_btn.hide()

        # XS board score button
        self.xs_scores_btn = Button(
            main = main,
            text = "XS Board",
            geometry = QRect(3 * main.screen_width // 5, 19 * main.screen_height // 60, main.screen_width // 10, main.screen_height // 20),
            font = QFont("Trebuchet MS", main.screen_height // 60)
        )
        self.xl_scores_btn.hide()

        # Connections for controls for displaying score
        self.traits_list.currentTextChanged.connect(self.display_scores)
        self.variations_list.currentTextChanged.connect(self.display_scores)
        self.static_scores_btn.clicked.connect(lambda: self.display_scores("static"))
        self.recycle_scores_btn.clicked.connect(lambda: self.display_scores("recycle"))
        self.xl_scores_btn.clicked.connect(lambda: self.display_scores("xl"))
        self.xs_scores_btn.clicked.connect(lambda: self.display_scores("xs"))

        # Background tiles for viewing times
        self.background_tiles = []
        for i in range(10):

            # Alternate light and dark tiles
            color = "e5daeb" if i % 2 else "ffffff"

            self.background_tiles.append(QLabel(
                parent = main.central_widget,
                geometry = QRect(7 * main.screen_width // 24, (3 * i + 25) * main.screen_height // 60, 5 * main.screen_width // 12, main.screen_height // 20),
                font = QFont("Trebuchet MS", main.screen_height // 60),
                alignment = Qt.AlignmentFlag.AlignCenter,
                styleSheet = f"background-color: #{color}"
            ))
            self.background_tiles[i].hide()

        # Return to main page from scores page
        self.go_back_from_scores_btn = Button(
            main = main,
            text = "Go Back",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(7 * main.screen_width // 8, main.screen_height // 360, 79 * main.screen_width // 640, main.screen_height // 24),
            connect = self.go_back_from_scores
        )
        self.go_back_from_scores_btn.hide()

        # Set arrow navigaton widgets
        # Main page
        self.play_btn.arrow_navigation(None, None, self.return_to_menu_btn, self.scores_btn)
        self.scores_btn.arrow_navigation(None, None, self.play_btn, self.return_to_menu_btn)
        self.return_to_menu_btn.arrow_navigation(None, None, self.scores_btn, self.play_btn)

        # Challenges page
        self.static_board_btn.arrow_navigation(self.go_back_from_challenges_btn, self.recycle_cards_btn, self.go_back_from_challenges_btn, self.xl_board_btn)
        self.recycle_cards_btn.arrow_navigation(self.static_board_btn, self.go_back_from_challenges_btn, self.go_back_from_challenges_btn, self.xs_board_btn)
        self.xl_board_btn.arrow_navigation(self.go_back_from_challenges_btn, self.xs_board_btn, self.static_board_btn, self.go_back_from_challenges_btn)
        self.xs_board_btn.arrow_navigation(self.xl_board_btn, self.go_back_from_challenges_btn, self.recycle_cards_btn, self.go_back_from_challenges_btn)
        self.go_back_from_challenges_btn.arrow_navigation(self.recycle_cards_btn, self.static_board_btn, self.xs_board_btn, self.recycle_cards_btn)

        # Scores page
        self.traits_list.arrow_navigation(
            self.go_back_from_scores_btn, self.variations_list, self.go_back_from_scores_btn, self.static_scores_btn,
            alt_down = self.recycle_scores_btn
        )
        self.variations_list.arrow_navigation(
            self.traits_list, self.static_scores_btn, self.go_back_from_scores_btn, self.static_scores_btn,
            alt_right = self.recycle_scores_btn, alt_down = self.recycle_scores_btn
        )
        self.static_scores_btn.arrow_navigation(
            self.variations_list, self.recycle_scores_btn, self.go_back_from_scores_btn, self.go_back_from_scores_btn,
            alt_right = self.xl_scores_btn
        )
        self.recycle_scores_btn.arrow_navigation(
            self.static_scores_btn, self.xl_scores_btn, self.go_back_from_scores_btn, self.go_back_from_scores_btn,
            alt_left = self.variations_list, alt_right = self.xs_scores_btn
        )
        self.xl_scores_btn.arrow_navigation(
            self.recycle_scores_btn, self.xs_scores_btn, self.go_back_from_scores_btn, self.go_back_from_scores_btn,
            alt_left = self.static_scores_btn, alt_right = self.go_back_from_scores_btn
        )
        self.xs_scores_btn.arrow_navigation(
            self.xl_scores_btn, self.go_back_from_scores_btn, self.go_back_from_scores_btn, self.go_back_from_scores_btn,
            alt_left = self.recycle_scores_btn
        )
        self.go_back_from_scores_btn.arrow_navigation(
            self.xs_scores_btn, self.traits_list, self.static_scores_btn, self.traits_list,
            alt_left = self.xl_scores_btn, alt_up = self.recycle_scores_btn
        )

        # Set tab order
        # Main page
        main.central_widget.setTabOrder(self.play_btn, self.scores_btn)
        main.central_widget.setTabOrder(self.scores_btn, self.return_to_menu_btn)

        # Challenges page
        main.central_widget.setTabOrder(self.static_board_btn, self.recycle_cards_btn)
        main.central_widget.setTabOrder(self.recycle_cards_btn, self.xl_board_btn)
        main.central_widget.setTabOrder(self.xl_board_btn, self.xs_board_btn)
        main.central_widget.setTabOrder(self.xs_board_btn, self.go_back_from_challenges_btn)

        # Scores page
        main.central_widget.setTabOrder(self.traits_list, self.variations_list)
        main.central_widget.setTabOrder(self.variations_list, self.static_scores_btn)
        main.central_widget.setTabOrder(self.static_scores_btn, self.recycle_scores_btn)
        main.central_widget.setTabOrder(self.recycle_scores_btn, self.xl_scores_btn)
        main.central_widget.setTabOrder(self.xl_scores_btn, self.xs_scores_btn)
        main.central_widget.setTabOrder(self.xs_scores_btn, self.go_back_from_scores_btn)