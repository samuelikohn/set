from card import Card
from dummy import DummyBoard
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel
from ui import Button


class Tutorial:

    def destroy(self):
        self.next_btn.deleteLater()
        self.prev_btn.deleteLater()
        self.exit_btn.deleteLater()
        for page in self.pages:
            page.destroy()
        self.main.tutorial_page = None

    def next_page(self):
        self.pages[self.page_number].hide()
        self.page_number += 1
        self.pages[self.page_number].show()

        if self.page_number == 5:
            self.next_btn.setEnabled(False)
        
        self.prev_btn.setEnabled(True)

        self.update_buttons()

    def previous_page(self):
        self.pages[self.page_number].hide()
        self.page_number -= 1
        self.pages[self.page_number].show()

        if self.page_number == 0:
            self.prev_btn.setEnabled(False)
        
        self.next_btn.setEnabled(True)

        self.update_buttons()

    def return_to_menu(self):
        self.main.go_to_main_menu()
        self.destroy()

    def update_buttons(self):

        self.next_btn.update_style()
        self.prev_btn.update_style()

    def __init__(self, main):
        
        self.main = main

        # Create pages
        self.page_number = 0
        self.pages = [
            Page0(main),
            Page1(main),
            Page2(main),
            Page3(main),
            Page4(main),
            Page5(main)
        ]
        self.pages[self.page_number].show()

        # Next Page Button
        self.next_btn = Button(
            main = main,
            text = "Next Page",
            geometry = QRect(9 * main.screen_width // 10, 343 * main.screen_height // 360, 63 * main.screen_width // 640, 2 * main.screen_height // 45),
            font = QFont("Trebuchet MS", main.screen_height // 60),
            connect = self.next_page
        )
        self.next_btn.show()
        self.next_btn.setFocus()

        # Previous Page Button
        self.prev_btn = Button(
            main = main,
            text = "Previous Page",
            geometry = QRect(main.screen_width // 640, 343 * main.screen_height // 360, 63 * main.screen_width // 640, 2 * main.screen_height // 45),
            font = QFont("Trebuchet MS", main.screen_height // 60),
            connect = self.previous_page
        )
        self.prev_btn.show()
        self.prev_btn.setEnabled(False)
        
        # Exit Tutorial Button
        self.exit_btn = Button(
            main = main,
            text = "Exit Tutorial",
            geometry = QRect(9 * main.screen_width // 10, main.screen_height // 360, 63 * main.screen_width // 640, 2 * main.screen_height // 45),
            font = QFont("Trebuchet MS", main.screen_height // 60),
            connect = self.return_to_menu
        )
        self.exit_btn.show()

        # Update buttons
        self.update_buttons()

        # Set arrow navigation widgets
        self.next_btn.arrow_navigation(self.prev_btn, self.prev_btn, self.exit_btn, self.exit_btn)
        self.prev_btn.arrow_navigation(self.next_btn, self.next_btn, self.exit_btn, self.exit_btn)
        self.exit_btn.arrow_navigation(self.next_btn, self.prev_btn, self.next_btn, self.next_btn)
        
        # Set Tab Order
        main.central_widget.setTabOrder(self.next_btn, self.prev_btn)
        main.central_widget.setTabOrder(self.prev_btn, self.exit_btn)


class Page0:

    def destroy(self):
        self.title.deleteLater()
        self.card_1.deleteLater()
        self.card_2.deleteLater()
        self.card_3.deleteLater()
        self.text_1.deleteLater()

    def hide(self):
        self.title.hide()
        self.card_1.hide()
        self.card_2.hide()
        self.card_3.hide()
        self.text_1.hide()

    def show(self):
        self.title.show()
        self.card_1.show()
        self.card_2.show()
        self.card_3.show()
        self.text_1.show()

    def __init__(self, main):
        
        # Title
        self.title = QLabel(
            parent = main.central_widget,
            text = "Welcome to SET!",
            font = QFont("Trebuchet MS", main.screen_height // 30),
            geometry = QRect(3 * main.screen_width // 8, main.screen_height // 24, main.screen_width // 4, main.screen_height // 20),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.title.hide()

        # Text 1
        self.text_1 = QLabel(
            parent = main.central_widget,
            text = "SET is a pattern matching game. The game consists of cards with different symbols,\nand the goal is to find groups of cards that meet certain criteria.",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(main.screen_width // 4, 3 * main.screen_height // 4, main.screen_width // 2, main.screen_height // 18),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.text_1.hide()

        # Cards
        # Card 1
        self.card_1 = Card(
            main.settings["colors"][0],
            main.settings["selected_shapes"][0],
            1,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 3),
            geometry = QRect(3 * main.screen_width // 16, main.screen_height // 4, main.screen_height // 3, main.screen_height // 3)
        )
        self.card_1.hide()

        # Card 2
        self.card_2 = Card(
            main.settings["colors"][1],
            main.settings["selected_shapes"][1],
            2,
            "empty",
            "none",
            0,
            DummyBoard(main, main.screen_height // 3),
            geometry = QRect(13 * main.screen_width // 32, main.screen_height // 4, main.screen_height // 3, main.screen_height // 3)
        )
        self.card_2.hide()

        # Card 3
        self.card_3 = Card(
            main.settings["colors"][2],
            main.settings["selected_shapes"][2],
            3,
            "striped",
            "none",
            0,
            DummyBoard(main, main.screen_height // 3),
            geometry = QRect(5 * main.screen_width // 8, main.screen_height // 4, main.screen_height // 3, main.screen_height // 3)
        )
        self.card_3.hide()


class Page1:

    def destroy(self):
        self.title.deleteLater()
        self.color_panel.deleteLater()
        self.shape_panel.deleteLater()
        self.number_panel.deleteLater()
        self.fill_panel.deleteLater()
        self.color_text.deleteLater()
        self.shape_text.deleteLater()
        self.number_text.deleteLater()
        self.fill_text.deleteLater()
        self.color_card_1.deleteLater()
        self.color_card_2.deleteLater()
        self.color_card_3.deleteLater()
        self.shape_card_1.deleteLater()
        self.shape_card_2.deleteLater()
        self.shape_card_3.deleteLater()
        self.number_card_1.deleteLater()
        self.number_card_2.deleteLater()
        self.number_card_3.deleteLater()
        self.fill_card_1.deleteLater()
        self.fill_card_2.deleteLater()
        self.fill_card_3.deleteLater()
        self.text_1.deleteLater()

    def hide(self):
        self.title.hide()
        self.color_panel.hide()
        self.shape_panel.hide()
        self.number_panel.hide()
        self.fill_panel.hide()
        self.color_text.hide()
        self.shape_text.hide()
        self.number_text.hide()
        self.fill_text.hide()
        self.color_card_1.hide()
        self.color_card_2.hide()
        self.color_card_3.hide()
        self.shape_card_1.hide()
        self.shape_card_2.hide()
        self.shape_card_3.hide()
        self.number_card_1.hide()
        self.number_card_2.hide()
        self.number_card_3.hide()
        self.fill_card_1.hide()
        self.fill_card_2.hide()
        self.fill_card_3.hide()
        self.text_1.hide()

    def show(self):
        self.title.show()
        self.color_panel.show()
        self.shape_panel.show()
        self.number_panel.show()
        self.fill_panel.show()
        self.color_text.show()
        self.shape_text.show()
        self.number_text.show()
        self.fill_text.show()
        self.color_card_1.show()
        self.color_card_2.show()
        self.color_card_3.show()
        self.shape_card_1.show()
        self.shape_card_2.show()
        self.shape_card_3.show()
        self.number_card_1.show()
        self.number_card_2.show()
        self.number_card_3.show()
        self.fill_card_1.show()
        self.fill_card_2.show()
        self.fill_card_3.show()
        self.text_1.show()

    def __init__(self, main):

        # Title
        self.title = QLabel(
            parent = main.central_widget,
            text = "Traits and Variations",
            font = QFont("Trebuchet MS", main.screen_height // 30),
            geometry = QRect(3 * main.screen_width // 8, main.screen_height // 24, main.screen_width // 4, main.screen_height // 20),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.title.hide()

        # Text 1
        self.text_1 = QLabel(
            parent = main.central_widget,
            text = "There are four traits that define the symbol on each card: Color, Shape, Number, and Fill.\nEach of these traits has three different variations as shown above.\n(These numbers can be changed in the settings, but if you are new to SET, don't worry about that for now.)",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(main.screen_width // 6, 3 * main.screen_height // 4, 2 * main.screen_width // 3, main.screen_height // 12),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.text_1.hide()

        # Color Cards
        # Bkgd Panel
        self.color_panel = QLabel(
            parent = main.central_widget,
            geometry = QRect(9 * main.screen_width // 64, 5 * main.screen_height // 36, 11 * main.screen_width // 32, main.screen_height // 4),
            styleSheet = "background-color: #e5daeb"
        )
        self.color_panel.hide()

        # Color Text
        self.color_text = QLabel(
            parent = main.central_widget,
            text = "Color",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(17 * main.screen_width // 64, 5 * main.screen_height // 36, main.screen_height // 6, main.screen_height // 18),
            alignment = Qt.AlignmentFlag.AlignCenter,
            styleSheet = "background-color: #e5daeb"
        )
        self.color_text.hide()

        # Color Card 1
        self.color_card_1 = Card(
            main.settings["colors"][0],
            main.settings["selected_shapes"][0],
            1,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(5 * main.screen_width // 32, 7 * main.screen_height // 36, main.screen_height // 6, main.screen_height // 6)
        )
        self.color_card_1.hide()

        # Color Card 2
        self.color_card_2 = Card(
            main.settings["colors"][1],
            main.settings["selected_shapes"][0],
            1,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(17 * main.screen_width // 64, 7 * main.screen_height // 36, main.screen_height // 6, main.screen_height // 6)
        )
        self.color_card_2.hide()

        # Color Card 3
        self.color_card_3 = Card(
            main.settings["colors"][2],
            main.settings["selected_shapes"][0],
            1,
            "solid",
            "none", 0, DummyBoard(main, main.screen_height // 6),
            geometry = QRect(3 * main.screen_width // 8, 7 * main.screen_height // 36, main.screen_height // 6, main.screen_height // 6)
        )
        self.color_card_3.hide()

        # Shape Cards
        # Bkgd Panel
        self.shape_panel = QLabel(
            parent = main.central_widget,
            geometry = QRect(33 * main.screen_width // 64, 5 * main.screen_height // 36, 11 * main.screen_width // 32, main.screen_height // 4),
            styleSheet = "background-color: #e5daeb"
        )
        self.shape_panel.hide()

        # Shape Text
        self.shape_text = QLabel(
            parent = main.central_widget,
            text = "Shape",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(41 * main.screen_width // 64, 5 * main.screen_height // 36, main.screen_height // 6, main.screen_height // 18),
            alignment = Qt.AlignmentFlag.AlignCenter,
            styleSheet = "background-color: #e5daeb"
        )
        self.shape_text.hide()

        # Shape Card 1
        self.shape_card_1 = Card(
            main.settings["colors"][0],
            main.settings["selected_shapes"][0],
            1,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(17 * main.screen_width // 32, 7 * main.screen_height // 36, main.screen_height // 6, main.screen_height // 6)
        )
        self.shape_card_1.hide()

        # Shape Card 2
        self.shape_card_2 = Card(
            main.settings["colors"][0],
            main.settings["selected_shapes"][1],
            1,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(41 * main.screen_width // 64, 7 * main.screen_height // 36, main.screen_height // 6, main.screen_height // 6)
        )
        self.shape_card_2.hide()

        # Shape Card 3
        self.shape_card_3 = Card(
            main.settings["colors"][0],
            main.settings["selected_shapes"][2],
            1,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(3 * main.screen_width // 4, 7 * main.screen_height // 36, main.screen_height // 6, main.screen_height // 6)
        )
        self.shape_card_3.hide()

        # Number Cards
        # Bkgd Panel
        self.number_panel = QLabel(
            parent = main.central_widget,
            geometry = QRect(9 * main.screen_width // 64, 4 * main.screen_height // 9, 11 * main.screen_width // 32, main.screen_height // 4),
            styleSheet = "background-color: #e5daeb"
        )
        self.number_panel.hide()

        # Number Text
        self.number_text = QLabel(
            parent = main.central_widget,
            text = "Number",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(17 * main.screen_width // 64, 4 * main.screen_height // 9, main.screen_height // 6, main.screen_height // 18),
            alignment = Qt.AlignmentFlag.AlignCenter,
            styleSheet = "background-color: #e5daeb"
        )
        self.number_text.hide()

        # Number Card 1
        self.number_card_1 = Card(
            main.settings["colors"][0],
            main.settings["selected_shapes"][0],
            1,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(5 * main.screen_width // 32, main.screen_height // 2, main.screen_height // 6, main.screen_height // 6)
        )
        self.number_card_1.hide()

        # Number Card 2
        self.number_card_2 = Card(
            main.settings["colors"][0],
            main.settings["selected_shapes"][0],
            2,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(17 * main.screen_width // 64, main.screen_height // 2, main.screen_height // 6, main.screen_height // 6)
        )
        self.number_card_2.hide()

        # Number Card 3
        self.number_card_3 = Card(
            main.settings["colors"][0],
            main.settings["selected_shapes"][0],
            3,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(3 * main.screen_width // 8, main.screen_height // 2, main.screen_height // 6, main.screen_height // 6)
        )
        self.number_card_3.hide()

        # Fill Cards
        # Bkgd Panel
        self.fill_panel = QLabel(
            parent = main.central_widget,
            geometry = QRect(33 * main.screen_width // 64, 4 * main.screen_height // 9, 11 * main.screen_width // 32, main.screen_height // 4),
            styleSheet = "background-color: #e5daeb"
        )
        self.fill_panel.hide()

        # Fill Text
        self.fill_text = QLabel(
            parent = main.central_widget,
            text = "Fill",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(41 * main.screen_width // 64, 4 * main.screen_height // 9, main.screen_height // 6, main.screen_height // 18),
            alignment = Qt.AlignmentFlag.AlignCenter,
            styleSheet = "background-color: #e5daeb"
        )
        self.fill_text.hide()

        # Fill Card 1
        self.fill_card_1 = Card(
            main.settings["colors"][0],
            main.settings["selected_shapes"][0],
            1,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(17 * main.screen_width // 32, main.screen_height // 2, main.screen_height // 6, main.screen_height // 6)
        )
        self.fill_card_1.hide()

        # Fill Card 2
        self.fill_card_2 = Card(
            main.settings["colors"][0],
            main.settings["selected_shapes"][0],
            1,
            "empty",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(41 * main.screen_width // 64, main.screen_height // 2, main.screen_height // 6, main.screen_height // 6)
        )
        self.fill_card_2.hide()

        # Fill Card 3
        self.fill_card_3 = Card(
            main.settings["colors"][0],
            main.settings["selected_shapes"][0],
            1,
            "striped",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(3 * main.screen_width // 4, main.screen_height // 2, main.screen_height // 6, main.screen_height // 6)
        )
        self.fill_card_3.hide()


class Page2:

    def destroy(self):
        self.title.deleteLater()
        self.example_1_panel.deleteLater()
        self.example_2_panel.deleteLater()
        self.example_3_panel.deleteLater()
        self.example_4_panel.deleteLater()
        self.example_1_text.deleteLater()
        self.example_2_text.deleteLater()
        self.example_3_text.deleteLater()
        self.example_4_text.deleteLater()
        self.example_1_card_1.deleteLater()
        self.example_1_card_2.deleteLater()
        self.example_1_card_3.deleteLater()
        self.example_2_card_1.deleteLater()
        self.example_2_card_2.deleteLater()
        self.example_2_card_3.deleteLater()
        self.example_3_card_1.deleteLater()
        self.example_3_card_2.deleteLater()
        self.example_3_card_3.deleteLater()
        self.example_4_card_1.deleteLater()
        self.example_4_card_2.deleteLater()
        self.example_4_card_3.deleteLater()
        self.text_1.deleteLater()

    def hide(self):
        self.title.hide()
        self.example_1_panel.hide()
        self.example_2_panel.hide()
        self.example_3_panel.hide()
        self.example_4_panel.hide()
        self.example_1_text.hide()
        self.example_2_text.hide()
        self.example_3_text.hide()
        self.example_4_text.hide()
        self.example_1_card_1.hide()
        self.example_1_card_2.hide()
        self.example_1_card_3.hide()
        self.example_2_card_1.hide()
        self.example_2_card_2.hide()
        self.example_2_card_3.hide()
        self.example_3_card_1.hide()
        self.example_3_card_2.hide()
        self.example_3_card_3.hide()
        self.example_4_card_1.hide()
        self.example_4_card_2.hide()
        self.example_4_card_3.hide()
        self.text_1.hide()

    def show(self):
        self.title.show()
        self.example_1_panel.show()
        self.example_2_panel.show()
        self.example_3_panel.show()
        self.example_4_panel.show()
        self.example_1_text.show()
        self.example_2_text.show()
        self.example_3_text.show()
        self.example_4_text.show()
        self.example_1_card_1.show()
        self.example_1_card_2.show()
        self.example_1_card_3.show()
        self.example_2_card_1.show()
        self.example_2_card_2.show()
        self.example_2_card_3.show()
        self.example_3_card_1.show()
        self.example_3_card_2.show()
        self.example_3_card_3.show()
        self.example_4_card_1.show()
        self.example_4_card_2.show()
        self.example_4_card_3.show()
        self.text_1.show()

    def __init__(self, main):

        # Title
        self.title = QLabel(
            parent = main.central_widget,
            text = "Examples of SETs",
            font = QFont("Trebuchet MS", main.screen_height // 30),
            geometry = QRect(3 * main.screen_width // 8, main.screen_height // 24, main.screen_width // 4, main.screen_height // 20),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.title.hide()

        # Text 1
        self.text_1 = QLabel(
            parent = main.central_widget,
            text = "A group of three cards form a SET if each trait has either all the same or all different variations.",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(main.screen_width // 6, 3 * main.screen_height // 4, 2 * main.screen_width // 3, main.screen_height // 18),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.text_1.hide()

        # Example 1
        # Bkgd Panel
        self.example_1_panel = QLabel(
            parent = main.central_widget,
            geometry = QRect(9 * main.screen_width // 64, 5 * main.screen_height // 36, 11 * main.screen_width // 32, main.screen_height // 4),
            styleSheet = "background-color: #e5daeb"
        )
        self.example_1_panel.hide()

        # Text
        self.example_1_text = QLabel(
            parent = main.central_widget,
            text = "Different colors, same shapes, same numbers, same fills.",
            font = QFont("Trebuchet MS", main.screen_height // 72),
            geometry = QRect(9 * main.screen_width // 64, 5 * main.screen_height // 36, 11 * main.screen_width // 32, main.screen_height // 18),
            alignment = Qt.AlignmentFlag.AlignCenter,
            styleSheet = "background-color: #e5daeb"
        )
        self.example_1_text.hide()

        # Card 1
        self.example_1_card_1 = Card(
            main.settings["colors"][0],
            main.settings["selected_shapes"][0],
            1,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(5 * main.screen_width // 32, 7 * main.screen_height // 36, main.screen_height // 6, main.screen_height // 6)
        )
        self.example_1_card_1.hide()

        # Card 2
        self.example_1_card_2 = Card(
            main.settings["colors"][1],
            main.settings["selected_shapes"][0],
            1,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(17 * main.screen_width // 64, 7 * main.screen_height // 36, main.screen_height // 6, main.screen_height // 6)
        )
        self.example_1_card_2.hide()

        # Card 3
        self.example_1_card_3 = Card(
            main.settings["colors"][2],
            main.settings["selected_shapes"][0],
            1,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(3 * main.screen_width // 8, 7 * main.screen_height // 36, main.screen_height // 6, main.screen_height // 6)
        )
        self.example_1_card_3.hide()

        # Example 2
        # Bkgd Panel
        self.example_2_panel = QLabel(
            parent = main.central_widget,
            geometry = QRect(33 * main.screen_width // 64, 5 * main.screen_height // 36, 11 * main.screen_width // 32, main.screen_height // 4),
            styleSheet = "background-color: #e5daeb"
        )
        self.example_2_panel.hide()

        # Text
        self.example_2_text = QLabel(
            parent = main.central_widget,
            text = "Same colors, different shapes, different numbers, same fills.",
            font = QFont("Trebuchet MS", main.screen_height // 72),
            geometry = QRect(33 * main.screen_width // 64, 5 * main.screen_height // 36, 11 * main.screen_width // 32, main.screen_height // 18),
            alignment = Qt.AlignmentFlag.AlignCenter,
            styleSheet = "background-color: #e5daeb"
        )
        self.example_2_text.hide()

        # Card 1
        self.example_2_card_1 = Card(
            main.settings["colors"][1],
            main.settings["selected_shapes"][0],
            1,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(17 * main.screen_width // 32, 7 * main.screen_height // 36, main.screen_height // 6, main.screen_height // 6)
        )
        self.example_2_card_1.hide()

        # Card 2
        self.example_2_card_2 = Card(
            main.settings["colors"][1],
            main.settings["selected_shapes"][1],
            2,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(41 * main.screen_width // 64, 7 * main.screen_height // 36, main.screen_height // 6, main.screen_height // 6)
        )
        self.example_2_card_2.hide()

        # Card 3
        self.example_2_card_3 = Card(
            main.settings["colors"][1],
            main.settings["selected_shapes"][2],
            3,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(3 * main.screen_width // 4, 7 * main.screen_height // 36, main.screen_height // 6, main.screen_height // 6)
        )
        self.example_2_card_3.hide()

        # Example 3
        # Bkgd Panel
        self.example_3_panel = QLabel(
            parent = main.central_widget,
            geometry = QRect(9 * main.screen_width // 64, 4 * main.screen_height // 9, 11 * main.screen_width // 32, main.screen_height // 4),
            styleSheet = "background-color: #e5daeb"
        )
        self.example_3_panel.hide()

        # Text
        self.example_3_text = QLabel(
            parent = main.central_widget,
            text = "Different colors, different shapes, same numbers, different fills.",
            font = QFont("Trebuchet MS", main.screen_height // 72),
            geometry = QRect(9 * main.screen_width // 64, 4 * main.screen_height // 9, 11 * main.screen_width // 32, main.screen_height // 18),
            alignment = Qt.AlignmentFlag.AlignCenter,
            styleSheet = "background-color: #e5daeb"
        )
        self.example_3_text.hide()

        # Card 1
        self.example_3_card_1 = Card(
            main.settings["colors"][0],
            main.settings["selected_shapes"][0],
            2,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(5 * main.screen_width // 32, main.screen_height // 2, main.screen_height // 6, main.screen_height // 6)
        )
        self.example_3_card_1.hide()

        # Card 2
        self.example_3_card_2 = Card(
            main.settings["colors"][1],
            main.settings["selected_shapes"][1],
            2,
            "empty",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(17 * main.screen_width // 64, main.screen_height // 2, main.screen_height // 6, main.screen_height // 6),
        )
        self.example_3_card_2.hide()

        # Card 3
        self.example_3_card_3 = Card(
            main.settings["colors"][2],
            main.settings["selected_shapes"][2],
            2,
            "striped",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(3 * main.screen_width // 8, main.screen_height // 2, main.screen_height // 6, main.screen_height // 6)
        )
        self.example_3_card_3.hide()

        # Example 4
        # Bkgd Panel
        self.example_4_panel = QLabel(
            parent = main.central_widget,
            geometry = QRect(33 * main.screen_width // 64, 4 * main.screen_height // 9, 11 * main.screen_width // 32, main.screen_height // 4),
            styleSheet = "background-color: #e5daeb"
        )
        self.example_4_panel.hide()

        # Text
        self.example_4_text = QLabel(
            parent = main.central_widget,
            text = "All traits have different variations.",
            font = QFont("Trebuchet MS", main.screen_height // 72),
            geometry = QRect(33 * main.screen_width // 64, 4 * main.screen_height // 9, 11 * main.screen_width // 32, main.screen_height // 18),
            alignment = Qt.AlignmentFlag.AlignCenter,
            styleSheet = "background-color: #e5daeb"
        )
        self.example_4_text.hide()

        # Card 1
        self.example_4_card_1 = Card(
            main.settings["colors"][0],
            main.settings["selected_shapes"][0],
            1,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(17 * main.screen_width // 32, main.screen_height // 2, main.screen_height // 6, main.screen_height // 6)
        )
        self.example_4_card_1.hide()

        # Card 2
        self.example_4_card_2 = Card(
            main.settings["colors"][1],
            main.settings["selected_shapes"][1],
            2,
            "empty",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(41 * main.screen_width // 64, main.screen_height // 2, main.screen_height // 6, main.screen_height // 6)
        )
        self.example_4_card_2.hide()

        # Card 3
        self.example_4_card_3 = Card(
            main.settings["colors"][2],
            main.settings["selected_shapes"][2],
            3,
            "striped",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(3 * main.screen_width // 4, main.screen_height // 2, main.screen_height // 6, main.screen_height // 6)
        )
        self.example_4_card_3.hide()


class Page3:

    def destroy(self):
        self.title.deleteLater()
        self.example_1_panel.deleteLater()
        self.example_1_text.deleteLater()
        self.example_2_panel.deleteLater()
        self.example_2_text.deleteLater()
        self.example_1_card_1.deleteLater()
        self.example_1_card_2.deleteLater()
        self.example_1_card_3.deleteLater()
        self.example_2_card_1.deleteLater()
        self.example_2_card_2.deleteLater()
        self.example_2_card_3.deleteLater()
        self.text_1.deleteLater()

    def hide(self):
        self.title.hide()
        self.example_1_panel.hide()
        self.example_1_text.hide()
        self.example_2_panel.hide()
        self.example_2_text.hide()
        self.example_1_card_1.hide()
        self.example_1_card_2.hide()
        self.example_1_card_3.hide()
        self.example_2_card_1.hide()
        self.example_2_card_2.hide()
        self.example_2_card_3.hide()
        self.text_1.hide()

    def show(self):
        self.title.show()
        self.example_1_panel.show()
        self.example_1_text.show()
        self.example_2_panel.show()
        self.example_2_text.show()
        self.example_1_card_1.show()
        self.example_1_card_2.show()
        self.example_1_card_3.show()
        self.example_2_card_1.show()
        self.example_2_card_2.show()
        self.example_2_card_3.show()
        self.text_1.show()

    def __init__(self, main):

        # Title
        self.title = QLabel(
            parent = main.central_widget,
            text = "Examples of non-SETs",
            font = QFont("Trebuchet MS", main.screen_height // 30),
            geometry = QRect(3 * main.screen_width // 8, main.screen_height // 24, main.screen_width // 4, main.screen_height // 20),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.title.hide()

        # Text 1
        self.text_1 = QLabel(
            parent = main.central_widget,
            text = "Likewise, if any trait has variations that are not all different or all the same, the cards fail to be a SET.",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(main.screen_width // 6, 3 * main.screen_height // 4, 2 * main.screen_width // 3, main.screen_height // 20),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.text_1.hide()

        # Example 1
        # Bkgd Panel
        self.example_1_panel = QLabel(
            parent = main.central_widget,
            geometry = QRect(21 * main.screen_width // 64, 5 * main.screen_height // 36, 11 * main.screen_width // 32, main.screen_height // 4),
            styleSheet = "background-color: #e5daeb"
        )
        self.example_1_panel.hide()

        # Text
        self.example_1_text = QLabel(parent = main.central_widget, text = "The first two cards have the same color and number\nbut the color and number of the third card are different.")
        self.example_1_text.setFont(QFont("Trebuchet MS", main.screen_height // 72))
        self.example_1_text.setGeometry(21 * main.screen_width // 64, 5 * main.screen_height // 36, 11 * main.screen_width // 32, main.screen_height // 18)
        self.example_1_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.example_1_text.setStyleSheet("background-color: #e5daeb")
        self.example_1_text.hide()

        # Card 1
        self.example_1_card_1 = Card(
            main.settings["colors"][0],
            main.settings["selected_shapes"][0],
            2,
            "striped",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(11 * main.screen_width // 32, 7 * main.screen_height // 36, main.screen_height // 6, main.screen_height // 6)
        )
        self.example_1_card_1.hide()

        # Card 2
        self.example_1_card_2 = Card(
            main.settings["colors"][0],
            main.settings["selected_shapes"][1],
            2,
            "striped",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(29 * main.screen_width // 64, 7 * main.screen_height // 36, main.screen_height // 6, main.screen_height // 6)
        )
        self.example_1_card_2.hide()

        # Card 3
        self.example_1_card_3 = Card(
            main.settings["colors"][2],
            main.settings["selected_shapes"][2],
            3,
            "striped",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(9 * main.screen_width // 16, 7 * main.screen_height // 36, main.screen_height // 6, main.screen_height // 6)
        )
        self.example_1_card_3.hide()

        # Example 2
        # Bkgd Panel
        self.example_2_panel = QLabel(
            parent = main.central_widget,
            geometry = QRect(21 * main.screen_width // 64, 4 * main.screen_height // 9, 11 * main.screen_width // 32, main.screen_height // 4),
            styleSheet = "background-color: #e5daeb"
        )
        self.example_2_panel.hide()

        # Text
        self.example_2_text = QLabel(
            parent = main.central_widget,
            text = "While the shapes are all the same and the colors and numbers are\nall different, the fills are neither all the same nor all different.",
            font = QFont("Trebuchet MS", main.screen_height // 72),
            geometry = QRect(21 * main.screen_width // 64, 4 * main.screen_height // 9, 11 * main.screen_width // 32, main.screen_height // 18),
            alignment = Qt.AlignmentFlag.AlignCenter,
            styleSheet = "background-color: #e5daeb"
        )
        self.example_2_text.hide()

        # Card 1
        self.example_2_card_1 = Card(
            main.settings["colors"][0],
            main.settings["selected_shapes"][2],
            1,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(11 * main.screen_width // 32, main.screen_height // 2, main.screen_height // 6, main.screen_height // 6)
        )
        self.example_2_card_1.hide()

        # Card 2
        self.example_2_card_2 = Card(
            main.settings["colors"][1],
            main.settings["selected_shapes"][2],
            2,
            "striped",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(29 * main.screen_width // 64, main.screen_height // 2, main.screen_height // 6, main.screen_height // 6)
        )
        self.example_2_card_2.hide()

        # Card 3
        self.example_2_card_3 = Card(
            main.settings["colors"][2],
            main.settings["selected_shapes"][2],
            3,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 6),
            geometry = QRect(9 * main.screen_width // 16, main.screen_height // 2, main.screen_height // 6, main.screen_height // 6)
        )
        self.example_2_card_3.hide()


class Page4:

    def destroy(self):
        self.title.deleteLater()
        self.step_1_panel.deleteLater()
        self.step_1_title.deleteLater()
        self.step_2_panel.deleteLater()
        self.step_2_title.deleteLater()
        self.step_3_panel.deleteLater()
        self.step_3_title.deleteLater()
        self.card_1.deleteLater()
        self.card_2.deleteLater()
        self.card_3.deleteLater()
        self.card_4.deleteLater()
        self.card_5.deleteLater()
        self.card_6.deleteLater()
        self.card_7.deleteLater()
        self.card_8.deleteLater()
        self.card_9.deleteLater()
        self.card_10.deleteLater()
        self.card_11.deleteLater()
        self.card_12.deleteLater()
        self.step_1_text.deleteLater()
        self.step_2_text_1.deleteLater()
        self.step_2_text_2.deleteLater()
        self.step_2_call_set.deleteLater()
        self.step_2_text_3.deleteLater()
        self.step_2_add_cards.deleteLater()
        self.step_3_text_1.deleteLater()

    def hide(self):
        self.title.hide()
        self.step_1_panel.hide()
        self.step_1_title.hide()
        self.step_2_panel.hide()
        self.step_2_title.hide()
        self.step_3_panel.hide()
        self.step_3_title.hide()
        self.card_1.hide()
        self.card_2.hide()
        self.card_3.hide()
        self.card_4.hide()
        self.card_5.hide()
        self.card_6.hide()
        self.card_7.hide()
        self.card_8.hide()
        self.card_9.hide()
        self.card_10.hide()
        self.card_11.hide()
        self.card_12.hide()
        self.step_1_text.hide()
        self.step_2_text_1.hide()
        self.step_2_text_2.hide()
        self.step_2_call_set.hide()
        self.step_2_text_3.hide()
        self.step_2_add_cards.hide()
        self.step_3_text_1.hide()

    def rgb_to_hex(self, color):
        return "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])

    def shift_color_lightness(self, color, amount):

        # Lighten for positive "amount" values, darken for negative
        if not amount:
            return color
        target = (255, 255, 255) if amount > 0 else (0, 0, 0)
        amount = abs(amount)

        color = (int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16))
        
        # Color is linearly interpolated between input and white/black
        return self.rgb_to_hex(tuple(int(a + (b - a) * amount / 100) for a, b in zip(color, target)))

    def show(self):
        self.title.show()
        self.step_1_panel.show()
        self.step_1_title.show()
        self.step_2_panel.show()
        self.step_2_title.show()
        self.step_3_panel.show()
        self.step_3_title.show()
        self.card_1.show()
        self.card_2.show()
        self.card_3.show()
        self.card_4.show()
        self.card_5.show()
        self.card_6.show()
        self.card_7.show()
        self.card_8.show()
        self.card_9.show()
        self.card_10.show()
        self.card_11.show()
        self.card_12.show()
        self.step_1_text.show()
        self.step_2_text_1.show()
        self.step_2_text_2.show()
        self.step_2_call_set.show()
        self.step_2_text_3.show()
        self.step_2_add_cards.show()
        self.step_3_text_1.show()

    def __init__(self, main):
        
        # Title
        self.title = QLabel(
            parent = main.central_widget,
            text = "How to Play",
            font = QFont("Trebuchet MS", main.screen_height // 30),
            geometry = QRect(5 * main.screen_width // 12, main.screen_height // 24, main.screen_width // 6, main.screen_height // 20),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.title.hide()

        # Step 1
        # Bkgd panel
        self.step_1_panel = QLabel(
            parent = main.central_widget,
            geometry = QRect(main.screen_width // 12, main.screen_height // 8, 59 * main.screen_width // 120, 3 * main.screen_height // 8),
            styleSheet = "background-color: #e5daeb"
        )
        self.step_1_panel.hide()

        # Title text
        self.step_1_title = QLabel(
            parent = main.central_widget,
            text = "Step 1:",
            font = QFont("Trebuchet MS", main.screen_height // 40),
            geometry = QRect(11 * main.screen_width // 120, main.screen_height // 8, 20 * main.screen_width // 120, main.screen_height // 20),
            styleSheet = "background-color: #e5daeb"
        )
        self.step_1_title.hide()

        # Card 1
        self.card_1 = Card(
            main.settings["colors"][1],
            main.settings["selected_shapes"][2],
            1,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 9),
            geometry = QRect(41 * main.screen_width // 136, 13 * main.screen_height // 96, main.screen_height // 9, main.screen_height // 9)
        )
        self.card_1.hide()

        # Card 2
        self.card_2 = Card(
            main.settings["colors"][1],
            main.settings["selected_shapes"][1],
            2,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 9),
            geometry = QRect(41 * main.screen_width // 136, 37 * main.screen_height // 144, main.screen_height // 9, main.screen_height // 9)
        )
        self.card_2.hide()

        # Card 3
        self.card_3 = Card(
            main.settings["colors"][0],
            main.settings["selected_shapes"][1],
            3,
            "empty",
            "none",
            0,
            DummyBoard(main, main.screen_height // 9),
            geometry = QRect(41 * main.screen_width // 136, 109 * main.screen_height // 288, main.screen_height // 9, main.screen_height // 9)
        )
        self.card_3.hide()

        # Card 4
        self.card_4 = Card(
            main.settings["colors"][1],
            main.settings["selected_shapes"][0],
            2,
            "striped",
            "none",
            0,
            DummyBoard(main, main.screen_height // 9),
            geometry = QRect(63 * main.screen_width // 170, 13 * main.screen_height // 96, main.screen_height // 9, main.screen_height // 9)
        )
        self.card_4.hide()

        # Card 5
        self.card_5 = Card(
            main.settings["colors"][0],
            main.settings["selected_shapes"][0],
            2,
            "empty",
            "none",
            0,
            DummyBoard(main, main.screen_height // 9),
            geometry = QRect(63 * main.screen_width // 170, 37 * main.screen_height // 144, main.screen_height // 9, main.screen_height // 9)
        )
        self.card_5.hide()

        # Card 6
        self.card_6 = Card(
            main.settings["colors"][2],
            main.settings["selected_shapes"][2],
            3,
            "empty",
            "none",
            0,
            DummyBoard(main, main.screen_height // 9),
            geometry = QRect(63 * main.screen_width // 170, 109 * main.screen_height // 288, main.screen_height // 9, main.screen_height // 9)
        )
        self.card_6.hide()

        # Card 7
        self.card_7 = Card(
            main.settings["colors"][2],
            main.settings["selected_shapes"][2],
            3,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 9),
            geometry = QRect(149 * main.screen_width // 340, 13 * main.screen_height // 96, main.screen_height // 9, main.screen_height // 9)
        )
        self.card_7.hide()

        # Card 8
        self.card_8 = Card(
            main.settings["colors"][1],
            main.settings["selected_shapes"][0],
            1,
            "empty",
            "none",
            0,
            DummyBoard(main, main.screen_height // 9),
            geometry = QRect(149 * main.screen_width // 340, 37 * main.screen_height // 144, main.screen_height // 9, main.screen_height // 9)
        )
        self.card_8.hide()

        # Card 9
        self.card_9 = Card(
            main.settings["colors"][1],
            main.settings["selected_shapes"][2],
            1,
            "empty",
            "none",
            0,
            DummyBoard(main, main.screen_height // 9),
            geometry = QRect(149 * main.screen_width // 340, 109 * main.screen_height // 288, main.screen_height // 9, main.screen_height // 9)
        )
        self.card_9.hide()

        # Card 10
        self.card_10 = Card(
            main.settings["colors"][0],
            main.settings["selected_shapes"][0],
            1,
            "striped",
            "none",
            0,
            DummyBoard(main, main.screen_height // 9),
            geometry = QRect(43 * main.screen_width // 85, 13 * main.screen_height // 96, main.screen_height // 9, main.screen_height // 9)
        )
        self.card_10.hide()

        # Card 11
        self.card_11 = Card(
            main.settings["colors"][2],
            main.settings["selected_shapes"][1],
            2,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 9),
            geometry = QRect(43 * main.screen_width // 85, 37 * main.screen_height // 144, main.screen_height // 9, main.screen_height // 9)
        )
        self.card_11.hide()

        # Card 12
        self.card_12 = Card(
            main.settings["colors"][0],
            main.settings["selected_shapes"][0],
            1,
            "solid",
            "none",
            0,
            DummyBoard(main, main.screen_height // 9),
            geometry = QRect(43 * main.screen_width // 85, 109 * main.screen_height // 288, main.screen_height // 9, main.screen_height // 9)
        )
        self.card_12.hide()

        # Body text
        self.step_1_text = QLabel(
            parent = main.central_widget,
            text = "Search the board for SETs",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(main.screen_width // 12, 7 * main.screen_height // 40, 89 * main.screen_width // 408, 11 * main.screen_height // 40),
            styleSheet = "background-color: #e5daeb",
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.step_1_text.hide()

        # Step 2
        # Bkgd panel
        self.step_2_panel = QLabel(
            parent = main.central_widget,
            geometry = QRect(71 * main.screen_width // 120, main.screen_height // 8, 39 * main.screen_width // 120, 3 * main.screen_height // 8),
            styleSheet = "background-color: #e5daeb"
        )
        self.step_2_panel.hide()

        # Title text
        self.step_2_title = QLabel(
            parent = main.central_widget,
            text = "Step 2:",
            font = QFont("Trebuchet MS", main.screen_height // 40),
            geometry = QRect(3 * main.screen_width // 5, main.screen_height // 8, 20 * main.screen_width // 120, main.screen_height // 20),
            styleSheet = "background-color: #e5daeb"
        )
        self.step_2_title.hide()

        # Body text 1
        self.step_2_text_1 = QLabel(
            parent = main.central_widget,
            text = "Once you find a SET, click                                   ",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(71 * main.screen_width // 120, 11 * main.screen_height // 64, 39 * main.screen_width // 120, 3 * main.screen_height // 32),
            styleSheet = "background-color: #e5daeb",
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.step_2_text_1.hide()

        # Call Set dummy button
        self.step_2_call_set = QLabel(
            parent = main.central_widget,
            text = "Call SET",
            font = QFont("Trebuchet MS", main.screen_height // 40),
            geometry = QRect(23 * main.screen_width // 30, 17 * main.screen_height // 96, 7 * main.screen_width // 60, main.screen_height // 12),
            alignment = Qt.AlignmentFlag.AlignCenter,
            styleSheet = f"""
                background-color: {main.settings["accent_color"]};
                border: {main.screen_height // 180}px solid {self.shift_color_lightness(main.settings["accent_color"], -50)};
            """
        )
        self.step_2_call_set.hide()

        # Body text 2
        self.step_2_text_2 = QLabel(
            parent = main.central_widget,
            text = "Or, press the Space Bar.",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(71 * main.screen_width // 120, 17 * main.screen_height // 64, 39 * main.screen_width // 120, 3 * main.screen_height // 32),
            styleSheet = "background-color: #e5daeb",
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.step_2_text_2.hide()

        # Body text 3
        self.step_2_text_3 = QLabel(
            parent = main.central_widget,
            text = "If no SETs exist,                   will light up.",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(71 * main.screen_width // 120, 23 * main.screen_height // 64, 39 * main.screen_width // 120, 3 * main.screen_height // 32),
            styleSheet = "background-color: #e5daeb",
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.step_2_text_3.hide()

        # Add Cards dummy button
        self.step_2_add_cards = QLabel(
            parent = main.central_widget,
            text = f"Add {main.settings["num_variations"]} Cards",
            font = QFont("Trebuchet MS", main.screen_height // 72),
            geometry = QRect(35 * main.screen_width // 48, 187 * main.screen_height // 480, main.screen_width // 15, main.screen_height // 30),
            alignment = Qt.AlignmentFlag.AlignCenter,
            styleSheet = f"""
                background-color: {main.settings["accent_color"]};
                border: {main.screen_height // 450}px solid {self.shift_color_lightness(main.settings["accent_color"], -50)};
            """
        )
        self.step_2_add_cards.hide()

        # Step 3
        # Bkgd panel
        self.step_3_panel = QLabel(
            parent = main.central_widget,
            geometry = QRect(main.screen_width // 12, 21 * main.screen_height // 40, 5 * main.screen_width // 6, 31 * main.screen_height // 80),
            styleSheet = "background-color: #e5daeb"
        )
        self.step_3_panel.hide()

        # Title text
        self.step_3_title = QLabel(
            parent = main.central_widget,
            text = "Step 3:",
            font = QFont("Trebuchet MS", main.screen_height // 40),
            geometry = QRect(11 * main.screen_width // 120, 21 * main.screen_height // 40, 20 * main.screen_width // 120, main.screen_height // 20),
            styleSheet = "background-color: #e5daeb"
        )
        self.step_3_title.hide()

        # Body text 1
        self.step_3_text_1 = QLabel(
            parent = main.central_widget,
            text = "• Select the cards in your SET by clicking on them. Once you call SET, you will have 10 seconds to select your cards.\n\n• If you do not select enough cards to form a SET, or the cards you chose do not correctly form a SET, a penalty is applied.\n\t• In AI mode and challenges that count a score, the penalty is -1 point.\n\t• In time trials and challenges with a timer, the penalty is time added to the clock.\n\t• There are no penalties in practice mode.",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(main.screen_width // 6, 23 * main.screen_height // 40, 3 * main.screen_width // 4, 23 * main.screen_height // 80),
            styleSheet = "background-color: #e5daeb",
            alignment = Qt.AlignmentFlag.AlignVCenter
        )
        self.step_3_text_1.hide()


class Page5:

    def destroy(self):
        self.title.deleteLater()
        self.ai_panel.deleteLater()
        self.ai_text.deleteLater()
        self.ai_body_text.deleteLater()
        self.practice_panel.deleteLater()
        self.practice_text.deleteLater()
        self.practice_body_text.deleteLater()
        self.time_trial_panel.deleteLater()
        self.time_trial_text.deleteLater()
        self.time_trial_body_text.deleteLater()
        self.challenge_panel.deleteLater()
        self.challenge_text.deleteLater()
        self.challenge_body_text.deleteLater()

    def hide(self):
        self.title.hide()
        self.ai_panel.hide()
        self.ai_text.hide()
        self.ai_body_text.hide()
        self.practice_panel.hide()
        self.practice_text.hide()
        self.practice_body_text.hide()
        self.time_trial_panel.hide()
        self.time_trial_text.hide()
        self.time_trial_body_text.hide()
        self.challenge_panel.hide()
        self.challenge_text.hide()
        self.challenge_body_text.hide()

    def show(self):
        self.title.show()
        self.ai_panel.show()
        self.ai_text.show()
        self.ai_body_text.show()
        self.practice_panel.show()
        self.practice_text.show()
        self.practice_body_text.show()
        self.time_trial_panel.show()
        self.time_trial_text.show()
        self.time_trial_body_text.show()
        self.challenge_panel.show()
        self.challenge_text.show()
        self.challenge_body_text.show()

    def __init__(self, main):
        
        # Title
        self.title = QLabel(
            parent = main.central_widget,
            text = "Game Modes",
            font = QFont("Trebuchet MS", main.screen_height // 30),
            geometry = QRect(5 * main.screen_width // 12, main.screen_height // 24, main.screen_width // 6, main.screen_height // 20),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.title.hide()

        # AI Mode
        # Bkgd Panel
        self.ai_panel = QLabel(
            parent = main.central_widget,
            geometry = QRect(9 * main.screen_width // 64, 5 * main.screen_height // 36, 11 * main.screen_width // 32, main.screen_height // 4),
            styleSheet = "background-color: #e5daeb"
        )
        self.ai_panel.hide()

        # Text
        self.ai_text = QLabel(
            parent = main.central_widget,
            text = "Versus AI",
            font = QFont("Trebuchet MS", main.screen_height // 48),
            geometry = QRect(9 * main.screen_width // 64, 5 * main.screen_height // 36, 11 * main.screen_width // 32, main.screen_height // 18),
            alignment = Qt.AlignmentFlag.AlignCenter,
            styleSheet = "background-color: #e5daeb"
        )
        self.ai_text.hide()

        # Body Text
        self.ai_body_text = QLabel(
            parent = main.central_widget,
            text = "Test your skills against the computer!\nWhoever finds the most SETs wins.",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(9 * main.screen_width // 64, 7 * main.screen_height // 36, 11 * main.screen_width // 32, 7 * main.screen_height // 36),
            alignment = Qt.AlignmentFlag.AlignCenter,
            styleSheet = "background-color: #e5daeb"
        )
        self.ai_body_text.hide()

        # Practice Mode
        # Bkgd Panel
        self.practice_panel = QLabel(
            parent = main.central_widget,
            geometry = QRect(33 * main.screen_width // 64, 5 * main.screen_height // 36, 11 * main.screen_width // 32, main.screen_height // 4),
            styleSheet = "background-color: #e5daeb"
        )
        self.practice_panel.hide()

        # Text
        self.practice_text = QLabel(
            parent = main.central_widget,
            text = "Practice",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(33 * main.screen_width // 64, 5 * main.screen_height // 36, 11 * main.screen_width // 32, main.screen_height // 18),
            alignment = Qt.AlignmentFlag.AlignCenter,
            styleSheet = "background-color: #e5daeb"
        )
        self.practice_text.hide()

        # Body Text
        self.practice_body_text = QLabel(
            parent = main.central_widget,
            text = "Practice finding SETs with no opponent,\nno score, and no pressure.\nPenalties are not applied in this game mode.",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(33 * main.screen_width // 64, 7 * main.screen_height // 36, 11 * main.screen_width // 32, 7 * main.screen_height // 36),
            alignment = Qt.AlignmentFlag.AlignCenter,
            styleSheet = "background-color: #e5daeb"
        )
        self.practice_body_text.hide()

        # Time Trial
        # Bkgd Panel
        self.time_trial_panel = QLabel(
            parent = main.central_widget,
            geometry = QRect(9 * main.screen_width // 64, 4 * main.screen_height // 9, 11 * main.screen_width // 32, main.screen_height // 4),
            styleSheet = "background-color: #e5daeb"
        )
        self.time_trial_panel.hide()

        # Text
        self.time_trial_text = QLabel(
            parent = main.central_widget,
            text = "Time Trial",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(9 * main.screen_width // 64, 4 * main.screen_height // 9, 11 * main.screen_width // 32, main.screen_height // 18),
            alignment = Qt.AlignmentFlag.AlignCenter,
            styleSheet = "background-color: #e5daeb"
        )
        self.time_trial_text.hide()

        # Body Text
        self.time_trial_body_text = QLabel(
            parent = main.central_widget,
            text = "Race against the clock to clear a deck of cards.\nShow off your fastest times!",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(9 * main.screen_width // 64, main.screen_height // 2, 11 * main.screen_width // 32, 7 * main.screen_height // 36),
            alignment = Qt.AlignmentFlag.AlignCenter,
            styleSheet = "background-color: #e5daeb"
        )
        self.time_trial_body_text.hide()

        # Challenges
        # Bkgd Panel
        self.challenge_panel = QLabel(
            parent = main.central_widget,
            geometry = QRect(33 * main.screen_width // 64, 4 * main.screen_height // 9, 11 * main.screen_width // 32, main.screen_height // 4),
            styleSheet = "background-color: #e5daeb"
        )
        self.challenge_panel.hide()

        # Text
        self.challenge_text = QLabel(
            parent = main.central_widget,
            text = "Challenges",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(33 * main.screen_width // 64, 4 * main.screen_height // 9, 11 * main.screen_width // 32, main.screen_height // 18),
            alignment = Qt.AlignmentFlag.AlignCenter,
            styleSheet = "background-color: #e5daeb"
        )
        self.challenge_text.hide()

        # Body Text
        self.challenge_body_text = QLabel(
            parent = main.central_widget,
            text = "Break your brain with fun, alternate way to play SET!",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(33 * main.screen_width // 64, main.screen_height // 2, 11 * main.screen_width // 32, 7 * main.screen_height // 36),
            alignment = Qt.AlignmentFlag.AlignCenter,
            styleSheet = "background-color: #e5daeb"
        )
        self.challenge_body_text.hide()