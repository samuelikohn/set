from board import Board
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtWidgets import QLabel
from ui import Button, Dropdown


class TimeTrialPage():

    def destroy(self):
        self.title.deleteLater()
        self.view_times_btn.deleteLater()
        self.start_time_trial_btn.deleteLater()
        self.return_to_menu_btn.deleteLater()
        self.go_back_btn.deleteLater()
        self.traits_list.deleteLater()
        self.variations_list.deleteLater()
        self.view_times_title.deleteLater()
        self.num_traits_text.deleteLater()
        self.num_variations_text.deleteLater()
        for tile in self.background_tiles:
            tile.deleteLater()
        self.main.time_trial_page = None

    def go_back(self):

        # Hide controls for viewing times
        self.go_back_btn.hide()
        self.traits_list.hide()
        self.variations_list.hide()
        self.view_times_title.hide()
        self.num_variations_text.hide()
        self.num_traits_text.hide()
        for tile in self.background_tiles:
            tile.hide()

        # Show menu controls
        self.title.show()
        self.start_time_trial_btn.show()
        self.view_times_btn.show()
        self.return_to_menu_btn.show()

        # Reset controls for viewing times
        for i in range(10):
            self.background_tiles[i].setText("")
        self.traits_list.setCurrentText("Select...")
        self.variations_list.setCurrentText("Select...")

        # Manage focus
        self.go_back_btn.clearFocus()
        self.focus_widget.setFocus()

    def hide(self):
        self.start_time_trial_btn.hide()
        self.view_times_btn.hide()
        self.return_to_menu_btn.hide()
        self.title.hide()

    def return_to_menu(self):
        self.main.go_to_main_menu()
        self.destroy()

    def show(self):
        self.start_time_trial_btn.show()
        self.view_times_btn.show()
        self.return_to_menu_btn.show()
        self.title.show()

    def show_times(self):

        # Get list of times based on selection
        time_key = ""
        match (self.traits_list.currentText(), self.variations_list.currentText()):
            case ("3", "3"):
                time_key = "3_trait_3_var"
            case ("3", "4"):
                time_key = "3_trait_4_var"
            case ("3", "5"):
                time_key = "3_trait_5_var"
            case ("4", "3"):
                time_key = "4_trait_3_var"
            case ("4", "4"):
                time_key = "4_trait_4_var"
            case ("4", "5"):
                time_key = "4_trait_5_var"
            case ("5", "3"):
                time_key = "5_trait_3_var"
            case ("5", "4"):
                time_key = "5_trait_4_var"
            case ("5", "5"):
                time_key = "5_trait_5_var"

        # If no value selected, do nothing
        if time_key:

            # Erase currently displayed times
            for i in range(10):
                self.background_tiles[i].setText("")

            # Set text to background tiles
            if self.main.times[time_key]:
                i = 0
                for time in self.main.times[time_key]:
                    self.background_tiles[i].setText(self.main.translate_time(time))
                    i += 1

            # If no times recorded
            else:
                self.background_tiles[0].setText("No time trials completed for these settings!")

    def start_time_trial(self):
        self.main.board = Board(
            self.main,
            self.main.settings["num_traits"],
            self.main.settings["num_variations"],
            show_cards_left_in_deck = self.main.settings["show_cards_left_in_deck"],
            called_from_time_trial = True
        )
        self.destroy()

    def view_times(self):

        # Hide menu controls
        self.title.hide()
        self.start_time_trial_btn.hide()
        self.view_times_btn.hide()
        self.return_to_menu_btn.hide()

        # Show controls for viewing times
        self.go_back_btn.show()
        self.traits_list.show()
        self.variations_list.show()
        self.view_times_title.show()
        self.num_variations_text.show()
        self.num_traits_text.show()
        for tile in self.background_tiles:
            tile.show()

        # Manage focus
        self.focus_widget = self.main.app.focusWidget()
        self.focus_widget.clearFocus()
        self.traits_list.setFocus()

    def __init__(self, main):

        self.main = main

        # Title
        self.title = QLabel(
            parent = main.central_widget,
            text = "Time Trial",
            font = QFont("Trebuchet MS", main.screen_height // 30),
            geometry = QRect(5 * main.screen_width // 12, main.screen_height // 24, main.screen_width // 6, main.screen_height // 20),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.title.show()

        # Start button
        self.start_time_trial_btn = Button(
            main = main,
            text = "Start",
            geometry = QRect(5 * main.screen_width // 12, 7 * main.screen_height // 24, main.screen_width // 6, main.screen_height // 12),
            font = QFont("Trebuchet MS", main.screen_height // 30),
            connect = self.start_time_trial
        )
        self.start_time_trial_btn.show()
        self.start_time_trial_btn.setFocus()

        # View Times button
        self.view_times_btn = Button(
            main = main,
            text = "View Times",
            geometry = QRect(5 * main.screen_width // 12, 11 * main.screen_height // 24, main.screen_width // 6, main.screen_height // 12),
            font = QFont("Trebuchet MS", main.screen_height // 30),
            connect = self.view_times
        )
        self.view_times_btn.show()

        # Button for returning to the main menu
        self.return_to_menu_btn = Button(
            main = main,
            text = "Return to Main Menu",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(7 * main.screen_width // 8, main.screen_height // 360, 79 * main.screen_width // 640, main.screen_height // 24),
            connect = self.return_to_menu
        )
        self.return_to_menu_btn.show()

        # Button for going back from viewing times to time trial menu
        self.go_back_btn = Button(
            main = main,
            text = "Go Back",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(15 * main.screen_width // 16, main.screen_height // 360, 39 * main.screen_width // 640, main.screen_height // 24),
            connect = self.go_back
        )
        self.go_back_btn.hide()

        # View Times Title
        self.view_times_title = QLabel(
            parent = main.central_widget,
            text = "Select Number of Traits and Variations",
            font = QFont("Trebuchet MS", main.screen_height // 30),
            geometry = QRect(main.screen_width // 4, main.screen_height // 24, main.screen_width // 2, main.screen_height // 20),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.view_times_title.hide()

        # Controls for dropdown menus for viewing time lists
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
        self.traits_list.currentTextChanged.connect(self.show_times)
        self.variations_list.currentTextChanged.connect(self.show_times)
        self.variations_list.addItems(["Select...", "3", "4", "5"])
        self.variations_list.hide()

        # Background tiles for viewing times
        self.background_tiles = []
        for i in range(10):

            # Alternate light and dark tiles
            color = "e5daeb" if i % 2 else "ffffff"

            self.background_tiles.append(QLabel(
                parent = main.central_widget,
                geometry = QRect(7 * main.screen_width // 24, (3 * i + 19) * main.screen_height // 60, 5 * main.screen_width // 12, main.screen_height // 20),
                font = QFont("Trebuchet MS", main.screen_height // 60),
                alignment = Qt.AlignmentFlag.AlignCenter,
                styleSheet = f"background-color: #{color}"
            ))
            self.background_tiles[i].hide()

        # Set arrow navigation widgets
        self.start_time_trial_btn.arrow_navigation(None, None, self.return_to_menu_btn, self.view_times_btn)
        self.view_times_btn.arrow_navigation(None, None, self.start_time_trial_btn, self.return_to_menu_btn)
        self.return_to_menu_btn.arrow_navigation(None, None, self.view_times_btn, self.start_time_trial_btn)

        self.traits_list.arrow_navigation(self.go_back_btn, self.variations_list, None, None)
        self.variations_list.arrow_navigation(self.traits_list, self.go_back_btn, None, None)
        self.go_back_btn.arrow_navigation(self.variations_list, self.traits_list, self.traits_list, self.traits_list)

        # Set Tab Order
        main.central_widget.setTabOrder(self.start_time_trial_btn, self.view_times_btn)
        main.central_widget.setTabOrder(self.view_times_btn, self.return_to_menu_btn)
        
        main.central_widget.setTabOrder(self.traits_list, self.variations_list)
        main.central_widget.setTabOrder(self.variations_list, self.go_back_btn)
