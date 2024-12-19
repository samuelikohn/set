from color_select import ColorSelect
from copy import deepcopy
from json import dump
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtWidgets import QColorDialog, QLabel, QMessageBox, QToolTip
from shape_select import ShapeSelect
from ui import Button, Slider, SpinBox


class SettingsPage:

    def ai_difficulty_easy(self):
        self.ai_difficulty_easy_btn.setEnabled(False)
        self.ai_difficulty_medium_btn.setEnabled(True)
        self.ai_difficulty_hard_btn.setEnabled(True)
        self.ai_difficulty_extreme_btn.setEnabled(True)
        self.settings["ai_difficulty"] = 2
        self.save_btn.setText("Save Current Settings")
        self.update_buttons(self.settings["accent_color"])

    def ai_difficulty_medium(self):
        self.ai_difficulty_easy_btn.setEnabled(True)
        self.ai_difficulty_medium_btn.setEnabled(False)
        self.ai_difficulty_hard_btn.setEnabled(True)
        self.ai_difficulty_extreme_btn.setEnabled(True)
        self.settings["ai_difficulty"] = 1.5
        self.save_btn.setText("Save Current Settings")
        self.update_buttons(self.settings["accent_color"])

    def ai_difficulty_hard(self):
        self.ai_difficulty_easy_btn.setEnabled(True)
        self.ai_difficulty_medium_btn.setEnabled(True)
        self.ai_difficulty_hard_btn.setEnabled(False)
        self.ai_difficulty_extreme_btn.setEnabled(True)
        self.settings["ai_difficulty"] = 1
        self.save_btn.setText("Save Current Settings")
        self.update_buttons(self.settings["accent_color"])

    def ai_difficulty_extreme(self):
        self.ai_difficulty_easy_btn.setEnabled(True)
        self.ai_difficulty_medium_btn.setEnabled(True)
        self.ai_difficulty_hard_btn.setEnabled(True)
        self.ai_difficulty_extreme_btn.setEnabled(False)
        self.settings["ai_difficulty"] = 0.5
        self.save_btn.setText("Save Current Settings")
        self.update_buttons(self.settings["accent_color"])

    def attempt_return_to_menu(self):
        if self.settings != self.main.settings:
            
            # Hide settings controls
            self.title.hide()
            self.num_traits.hide()
            self.num_traits_text.hide()
            self.num_traits_3.hide()
            self.num_traits_4.hide()
            self.num_traits_5.hide()
            self.num_variations.hide()
            self.num_variations_text.hide()
            self.num_variations_3.hide()
            self.num_variations_4.hide()
            self.num_variations_5.hide()
            self.show_num_sets_text_1.hide()
            self.show_num_sets_text_2.hide()
            self.show_num_sets_yes_btn.hide()
            self.show_num_sets_no_btn.hide()
            self.show_cards_left_in_deck_text.hide()
            self.show_cards_left_in_deck_yes_btn.hide()
            self.show_cards_left_in_deck_no_btn.hide()
            self.save_btn.hide()
            self.return_to_menu_btn.hide()
            self.time_format_numeric_btn.hide()
            self.time_format_text_btn.hide()
            self.time_format_raw_btn.hide()
            self.time_format_text_text.hide()
            self.enable_hints_text_1.hide()
            self.enable_hints_text_2.hide()
            self.enable_hints_yes_btn.hide()
            self.enable_hints_no_btn.hide()
            self.accent_color_btn.hide()
            self.accent_color_text.hide()
            self.accent_color_current.hide()
            self.color_dialogue = None
            self.color_select.hide()
            self.shape_select.hide()
            self.ai_difficulty_text.hide()
            self.ai_difficulty_easy_btn.hide()
            self.ai_difficulty_medium_btn.hide()
            self.ai_difficulty_hard_btn.hide()
            self.ai_difficulty_extreme_btn.hide()
            self.selection_delay_box.hide()
            self.selection_delay_text.hide()

            # Show confirmation controls
            self.return_to_menu_text.show()
            self.return_to_menu_yes.show()
            self.return_to_menu_no.show()

            # Manage focus
            self.focus_widget = self.main.app.focusWidget()
            self.focus_widget.clearFocus()
            self.return_to_menu_no.setFocus()

        else:
            self.return_to_menu()

    def back_to_settings(self):
        
        # Hide confirmation controls
        self.return_to_menu_text.hide()
        self.return_to_menu_yes.hide()
        self.return_to_menu_no.hide()

        # Hide settings controls
        self.title.show()
        self.num_traits.show()
        self.num_traits_text.show()
        self.num_traits_3.show()
        self.num_traits_4.show()
        self.num_traits_5.show()
        self.num_variations.show()
        self.num_variations_text.show()
        self.num_variations_3.show()
        self.num_variations_4.show()
        self.num_variations_5.show()
        self.show_num_sets_text_1.show()
        self.show_num_sets_text_2.show()
        self.show_num_sets_yes_btn.show()
        self.show_num_sets_no_btn.show()
        self.show_cards_left_in_deck_text.show()
        self.show_cards_left_in_deck_yes_btn.show()
        self.show_cards_left_in_deck_no_btn.show()
        self.save_btn.show()
        self.return_to_menu_btn.show()
        self.time_format_numeric_btn.show()
        self.time_format_text_btn.show()
        self.time_format_raw_btn.show()
        self.time_format_text_text.show()
        self.enable_hints_text_1.show()
        self.enable_hints_text_2.show()
        self.enable_hints_yes_btn.show()
        self.enable_hints_no_btn.show()
        self.accent_color_btn.show()
        self.accent_color_text.show()
        self.accent_color_current.show()
        self.color_select.show()
        self.shape_select.show()
        self.ai_difficulty_text.show()
        self.ai_difficulty_easy_btn.show()
        self.ai_difficulty_medium_btn.show()
        self.ai_difficulty_hard_btn.show()
        self.ai_difficulty_extreme_btn.show()
        self.selection_delay_box.show()
        self.selection_delay_text.show()

        # Manage focus
        self.return_to_menu_no.clearFocus()
        self.focus_widget.setFocus()

    def change_num_traits(self, value):
        self.settings["num_traits"] = value
        self.save_btn.setText("Save Current Settings")

    def change_num_variations(self, value):
        self.settings["num_variations"] = value
        self.save_btn.setText("Save Current Settings")

    def change_select_color(self, color):
        hex_code = self.rgb_to_hex(color.getRgb())
        self.settings["accent_color"] = hex_code
        self.accent_color_current.setStyleSheet(f"background-color: {hex_code}; border: 2px outset grey;")
        self.save_btn.setText("Save Current Settings")
        
        # Update style on settings page buttons
        self.update_buttons(hex_code)

    def choose_accent_color(self):
        self.color_dialogue = QColorDialog()
        self.color_dialogue.colorSelected.connect(self.change_select_color)
        self.color_dialogue.show()

    def destroy(self):
        self.title.deleteLater()
        self.num_traits.deleteLater()
        self.num_traits_text.deleteLater()
        self.num_traits_3.deleteLater()
        self.num_traits_4.deleteLater()
        self.num_traits_5.deleteLater()
        self.num_variations.deleteLater()
        self.num_variations_text.deleteLater()
        self.num_variations_3.deleteLater()
        self.num_variations_4.deleteLater()
        self.num_variations_5.deleteLater()
        self.show_num_sets_text_1.deleteLater()
        self.show_num_sets_text_2.deleteLater()
        self.show_num_sets_yes_btn.deleteLater()
        self.show_num_sets_no_btn.deleteLater()
        self.show_cards_left_in_deck_text.deleteLater()
        self.show_cards_left_in_deck_yes_btn.deleteLater()
        self.show_cards_left_in_deck_no_btn.deleteLater()
        self.save_btn.deleteLater()
        self.return_to_menu_btn.deleteLater()
        self.return_to_menu_text.deleteLater()
        self.return_to_menu_yes.deleteLater()
        self.return_to_menu_no.deleteLater()
        self.time_format_numeric_btn.deleteLater()
        self.time_format_text_btn.deleteLater()
        self.time_format_raw_btn.deleteLater()
        self.time_format_text_text.deleteLater()
        self.enable_hints_text_1.deleteLater()
        self.enable_hints_text_2.deleteLater()
        self.enable_hints_yes_btn.deleteLater()
        self.enable_hints_no_btn.deleteLater()
        self.accent_color_btn.deleteLater()
        self.accent_color_text.deleteLater()
        self.accent_color_current.deleteLater()
        self.color_dialogue = None
        self.color_select.destroy()
        self.shape_select.destroy()
        self.ai_difficulty_text.deleteLater()
        self.ai_difficulty_easy_btn.deleteLater()
        self.ai_difficulty_medium_btn.deleteLater()
        self.ai_difficulty_hard_btn.deleteLater()
        self.ai_difficulty_extreme_btn.deleteLater()
        self.selection_delay_box.deleteLater()
        self.selection_delay_text.deleteLater()
        self.main.settings_page = None

    def enable_hints_yes(self):
        self.enable_hints_no_btn.setEnabled(True)
        self.enable_hints_yes_btn.setEnabled(False)
        self.settings["enable_hints"] = True
        self.save_btn.setText("Save Current Settings")
        self.update_buttons(self.settings["accent_color"])

    def enable_hints_no(self):
        self.enable_hints_no_btn.setEnabled(False)
        self.enable_hints_yes_btn.setEnabled(True)
        self.settings["enable_hints"] = False
        self.save_btn.setText("Save Current Settings")
        self.update_buttons(self.settings["accent_color"])

    def return_to_menu(self):
        self.main.go_to_main_menu()
        self.destroy()

    def rgb_to_hex(self, color):
        return "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])

    def save_settings(self):

        # Check if all color slots are filled
        if len(self.settings["colors"]) < 5:
            missing_colors = QMessageBox(
                parent = self.main.central_widget,
                text = "Five colors must be selected!",
                windowTitle = "Not Enough Colors"
            )
            missing_colors.show()

            # Prevent saving if less than 5 colors
            return
        
        # Check if all shape slots are filled
        if len(self.settings["selected_shapes"]) < 5:
            missing_shapes = QMessageBox(
                parent = self.main.central_widget,
                text = "Five shapes must be selected!",
                windowTitle = "Not Enough Shapes"
            )
            missing_shapes.show()

            # Prevent saving if less than 5 shapes
            return

        self.save_btn.setText("Saved!")
        self.main.settings = deepcopy(self.settings)
        with open("settings.json", "w") as f:
            dump(self.settings, f, indent = 4)

    def selection_delay(self, value):
        self.settings["selection_delay"] = value
        self.save_btn.setText("Save Current Settings")

    def show_num_sets_yes(self):
        self.show_num_sets_no_btn.setEnabled(True)
        self.show_num_sets_yes_btn.setEnabled(False)
        self.settings["show_num_sets"] = True
        self.save_btn.setText("Save Current Settings")
        self.update_buttons(self.settings["accent_color"])

    def show_num_sets_no(self):
        self.show_num_sets_no_btn.setEnabled(False)
        self.show_num_sets_yes_btn.setEnabled(True)
        self.settings["show_num_sets"] = False
        self.save_btn.setText("Save Current Settings")
        self.update_buttons(self.settings["accent_color"])

    def show_cards_left_in_deck_yes(self):
        self.show_cards_left_in_deck_no_btn.setEnabled(True)
        self.show_cards_left_in_deck_yes_btn.setEnabled(False)
        self.settings["show_cards_left_in_deck"] = True
        self.save_btn.setText("Save Current Settings")
        self.update_buttons(self.settings["accent_color"])

    def show_cards_left_in_deck_no(self):
        self.show_cards_left_in_deck_no_btn.setEnabled(False)
        self.show_cards_left_in_deck_yes_btn.setEnabled(True)
        self.settings["show_cards_left_in_deck"] = False
        self.save_btn.setText("Save Current Settings")
        self.update_buttons(self.settings["accent_color"])

    def time_format_numeric(self):
        self.time_format_numeric_btn.setEnabled(False)
        self.time_format_text_btn.setEnabled(True)
        self.time_format_raw_btn.setEnabled(True)
        self.settings["time_format"] = "numeric"
        self.save_btn.setText("Save Current Settings")
        self.update_buttons(self.settings["accent_color"])

    def time_format_raw(self):
        self.time_format_numeric_btn.setEnabled(True)
        self.time_format_text_btn.setEnabled(True)
        self.time_format_raw_btn.setEnabled(False)
        self.settings["time_format"] = "raw"
        self.save_btn.setText("Save Current Settings")
        self.update_buttons(self.settings["accent_color"])

    def time_format_text(self):
        self.time_format_numeric_btn.setEnabled(True)
        self.time_format_text_btn.setEnabled(False)
        self.time_format_raw_btn.setEnabled(True)
        self.settings["time_format"] = "text"
        self.save_btn.setText("Save Current Settings")
        self.update_buttons(self.settings["accent_color"])

    def update_buttons(self, hex_code):

        self.num_traits.update_style(hex_code)
        self.num_variations.update_style(hex_code)

        self.ai_difficulty_easy_btn.update_style(hex_code)
        self.ai_difficulty_medium_btn.update_style(hex_code)
        self.ai_difficulty_hard_btn.update_style(hex_code)
        self.ai_difficulty_extreme_btn.update_style(hex_code)

        self.show_num_sets_no_btn.update_style(hex_code)
        self.show_num_sets_yes_btn.update_style(hex_code)

        self.show_cards_left_in_deck_yes_btn.update_style(hex_code)
        self.show_cards_left_in_deck_no_btn.update_style(hex_code)

        self.time_format_numeric_btn.update_style(hex_code)
        self.time_format_text_btn.update_style(hex_code)
        self.time_format_raw_btn.update_style(hex_code)

        self.enable_hints_no_btn.update_style(hex_code)
        self.enable_hints_yes_btn.update_style(hex_code)

        self.accent_color_btn.update_style(hex_code)

        self.color_select.custom_color_btn.update_style(hex_code)
        self.color_select.reset.update_style(hex_code)

        self.shape_select.reset.update_style(hex_code)

        self.save_btn.update_style(hex_code)

        self.return_to_menu_btn.update_style(hex_code)
        self.return_to_menu_no.update_style(hex_code)
        self.return_to_menu_yes.update_style(hex_code)

    def __init__(self, main):

        self.main = main

        QToolTip.setFont(QFont("Trebuchet MS", main.screen_height // 90))
        tooltips = {
            "num_traits": "Changes the number of traits (e.g. Color, Shape)\nused to generate the deck of cards. The traits\nused will be first from: Color, Shape, Number,\nFill, Corners, in that order.",
            "num_variations": "Changes the number of variations used for each\ntrait (e.g. Red, Green for color, or Circles,\nSquares for shape) when generating the deck. If a\ntrait is not used to generate the deck, all cards\nwill have the same variation of that trait.",
            "ai_difficulty": "Adjusts the average time taken for the AI to find\na SET. The AI will find SETs faster on harder\ndifficulties.",
            "show_num_sets": "Adds a display for the number of SETs currently\non the board. The display will only show in\nPractice Mode.",
            "show_cards_left_in_deck": "Adds a display for the number of cards that have\nnot been drawn from the deck.",
            "time_format": "Changes how game completion times are displayed\nfor Time Trials. The formats are as follows:\n\tNumeric: hh:mm:ss.t\n\tText: H hours, M minutes, S.t seconds\n\tRaw: the number of 1/10 second intervals in the given time",
            "enable_hints": "Adds a button that displays a hint for finding\nSETs. When clicked, a random SET is chosen, and a\nrandom variation that all cards of the SET have in\ncommon is displayed. If the cards have no\nvariations in common, the Hint button will say so.\nThis button is only available in Practice Mode.",
            "accent_color": "Changes the color of the highlight when selecting\ncards, as well as the color of buttons and certain\nother widgets.",
            "choose_color": "Choose the colors used as variations of the Color\ntrait. Colors will be used in reading order from\nthe \"Current Colors\" panel. You can add your own\ncolors with the \"Add Custom Color\" button.\nMultiple copies of the same color may not be\nadded. You can delete colors that are not selected\nby right-clicking on them. Five colors must be\nselected in order to save your current settings.",
            "choose_shape": "Choose the shapes used as variations on the Shape\ntrait. Shapes will be used in reading order from\nthe \"Current Shapes\" panel. Five shapes must be\nselected in order to save your current settings.",
            "selection_delay": "Adjust the amount of time between when cards are\nselected for being a SET and when they are removed\nfrom the board. Ranges from 0 to 10 seconds."
        }

        # Copy settings for overwriting
        self.settings = deepcopy(main.settings)

        # Title
        self.title = QLabel(
            parent = main.central_widget,
            text = "Settings",
            font = QFont("Trebuchet MS", main.screen_height // 30),
            geometry = QRect(5 * main.screen_width // 12, main.screen_height // 24, main.screen_width // 6, main.screen_height // 20),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.title.show()

        # Slider for number of traits
        self.num_traits = Slider(
            main = main,
            geometry = QRect(main.screen_width // 12, 7 * main.screen_height // 36, 3 * main.screen_width // 24, main.screen_height // 48),
            orientation = Qt.Orientation.Horizontal,
            minimum = 3,
            maximum = 5,
            value = self.settings["num_traits"],
            cursor = QCursor(Qt.CursorShape.PointingHandCursor)
        )
        self.num_traits.valueChanged.connect(self.change_num_traits)
        self.num_traits.show()
        self.num_traits.setFocus()

        # Text for number of traits
        self.num_traits_text = QLabel(
            parent = main.central_widget,
            text = "Number of Traits",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(main.screen_width // 12, 5 * main.screen_height // 36, 3 * main.screen_width // 24, main.screen_height // 18),
            alignment = Qt.AlignmentFlag.AlignCenter,
            toolTip = tooltips["num_traits"]
        )
        self.num_traits_text.show()

        # Number labels for traits slider
        # 3
        self.num_traits_3 = QLabel(
            parent = main.central_widget,
            text = "3",
            font = QFont("Trebuchet MS", main.screen_height // 72),
            geometry = QRect(main.screen_width // 12, 2 * main.screen_height // 9, main.screen_width // 180, main.screen_height // 60),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.num_traits_3.show()

        # 4
        self.num_traits_4 = QLabel(
            parent = main.central_widget,
            text = "4",
            font = QFont("Trebuchet MS", main.screen_height // 72),
            geometry = QRect(103 * main.screen_width // 720, 2 * main.screen_height // 9, main.screen_width // 180, main.screen_height // 60),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.num_traits_4.show()

        # 5
        self.num_traits_5 = QLabel(
            parent = main.central_widget,
            text = "5",
            font = QFont("Trebuchet MS", main.screen_height // 72),
            geometry = QRect(73 * main.screen_width // 360, 2 * main.screen_height // 9, main.screen_width // 180, main.screen_height // 60),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.num_traits_5.show()

        # Slider for number of variations
        self.num_variations = Slider(
            main = main,
            geometry = QRect(7 * main.screen_width // 24, 7 * main.screen_height // 36, 3 * main.screen_width // 24, main.screen_height // 48),
            orientation = Qt.Orientation.Horizontal,
            minimum = 3,
            maximum = 5,
            value = self.settings["num_variations"],
            cursor = QCursor(Qt.CursorShape.PointingHandCursor)
        )
        self.num_variations.valueChanged.connect(self.change_num_variations)
        self.num_variations.show()

        # Text for number of variations
        self.num_variations_text = QLabel(
            parent = main.central_widget,
            text = "Number of Variations\nper Trait",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(7 * main.screen_width // 24, 5 * main.screen_height // 36, 3 * main.screen_width // 24, main.screen_height // 18),
            alignment = Qt.AlignmentFlag.AlignCenter,
            toolTip = tooltips["num_variations"]
        )
        self.num_variations_text.show()

        # Number labels for variations slider
        # 3
        self.num_variations_3 = QLabel(
            parent = main.central_widget,
            text = "3",
            font = QFont("Trebuchet MS", main.screen_height // 72),
            geometry = QRect(7 * main.screen_width // 24, 2 * main.screen_height // 9, main.screen_width // 180, main.screen_height // 60),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.num_variations_3.show()

        # 4
        self.num_variations_4 = QLabel(
            parent = main.central_widget,
            text = "4",
            font = QFont("Trebuchet MS", main.screen_height // 72),
            geometry = QRect(253 * main.screen_width // 720, 2 * main.screen_height // 9, main.screen_width // 180, main.screen_height // 60),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.num_variations_4.show()

        # 5
        self.num_variations_5 = QLabel(
            parent = main.central_widget,
            text = "5",
            font = QFont("Trebuchet MS", main.screen_height // 72),
            geometry = QRect(74 * main.screen_width // 180, 2 * main.screen_height // 9, main.screen_width // 180, main.screen_height // 60),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.num_variations_5.show()

        # Controls for AI difficulty
        # Text
        self.ai_difficulty_text = QLabel(
            parent = main.central_widget,
            text = "AI Difficulty",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(main.screen_width // 12, 13 * main.screen_height // 48, 3 * main.screen_width // 24, main.screen_height // 18),
            toolTip = tooltips["ai_difficulty"]
        )
        self.ai_difficulty_text.show()

        # Easy button
        self.ai_difficulty_easy_btn = Button(
            main = main,
            text = "Easy",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(11 * main.screen_width // 48, 13 * main.screen_height // 48, 3 * main.screen_width // 48, main.screen_height // 18),
            connect = self.ai_difficulty_easy,
            enabled = self.settings["ai_difficulty"] != 2
        )
        self.ai_difficulty_easy_btn.show()

        # Medium button
        self.ai_difficulty_medium_btn = Button(
            main = main,
            text = "Medium",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(7 * main.screen_width // 24, 13 * main.screen_height // 48, 3 * main.screen_width // 48, main.screen_height // 18),
            connect = self.ai_difficulty_medium,
            enabled = self.settings["ai_difficulty"] != 1.5
        )
        self.ai_difficulty_medium_btn.show()

        # Hard button
        self.ai_difficulty_hard_btn = Button(
            main = main,
            text = "Hard",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(17 * main.screen_width // 48, 13 * main.screen_height // 48, 3 * main.screen_width // 48, main.screen_height // 18),
            connect = self.ai_difficulty_hard,
            enabled = self.settings["ai_difficulty"] != 1
        )
        self.ai_difficulty_hard_btn.show()

        # Extreme button
        self.ai_difficulty_extreme_btn = Button(
            main = main,
            text = "Extreme",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(5 * main.screen_width // 12, 13 * main.screen_height // 48, 3 * main.screen_width // 48, main.screen_height // 18),
            connect = self.ai_difficulty_extreme,
            enabled = self.settings["ai_difficulty"] != 0.5
        )
        self.ai_difficulty_extreme_btn.show()

        # Controls for showing number of SETs toggle
        # Text 1
        self.show_num_sets_text_1 = QLabel(
            parent = main.central_widget,
            text = "Show the Number of\nSETs on the Board?",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(main.screen_width // 12, 17 * main.screen_height // 48, 3 * main.screen_width // 24, main.screen_height // 18),
            toolTip = tooltips["show_num_sets"]
        )
        self.show_num_sets_text_1.show()

        # Text 2
        self.show_num_sets_text_2 = QLabel(
            parent = main.central_widget,
            text = "(Only available in Practice Mode)",
            font = QFont("Trebuchet MS", main.screen_height // 90),
            geometry = QRect(main.screen_width // 12, 49 * main.screen_height // 120, 3 * main.screen_width // 24, main.screen_height // 60)
        )
        self.show_num_sets_text_2.show()

        # Yes button
        self.show_num_sets_yes_btn = Button(
            main = main,
            text = "Yes",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(7 * main.screen_width // 24, 17 * main.screen_height // 48, 3 * main.screen_width // 48, main.screen_height // 18),
            connect = self.show_num_sets_yes,
            enabled = not self.settings["show_num_sets"]
        )
        self.show_num_sets_yes_btn.show()

        # No button
        self.show_num_sets_no_btn = Button(
            main = main,
            text = "No",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(17 * main.screen_width // 48, 17 * main.screen_height // 48, 3 * main.screen_width // 48, main.screen_height // 18),
            connect = self.show_num_sets_no,
            enabled = self.settings["show_num_sets"]
        )
        self.show_num_sets_no_btn.show()

        # Controls for showing number of card remaining toggle
        # Text
        self.show_cards_left_in_deck_text = QLabel(
            parent = main.central_widget,
            text = "Show the Number of Cards\nRemaining in the Deck?",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(main.screen_width // 12, 7 * main.screen_height // 16, 4 * main.screen_width // 24, main.screen_height // 18),
            toolTip = tooltips["show_cards_left_in_deck"]
        )
        self.show_cards_left_in_deck_text.show()

        # Yes button
        self.show_cards_left_in_deck_yes_btn = Button(
            main = main,
            text = "Yes",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(7 * main.screen_width // 24, 7 * main.screen_height // 16, 3 * main.screen_width // 48, main.screen_height // 18),
            connect = self.show_cards_left_in_deck_yes,
            enabled = not self.settings["show_cards_left_in_deck"]
        )
        self.show_cards_left_in_deck_yes_btn.show()

        # No button
        self.show_cards_left_in_deck_no_btn = Button(
            main = main,
            text = "No",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(17 * main.screen_width // 48, 7 * main.screen_height // 16, 3 * main.screen_width // 48, main.screen_height // 18),
            connect = self.show_cards_left_in_deck_no,
            enabled = self.settings["show_cards_left_in_deck"]
        )
        self.show_cards_left_in_deck_no_btn.show()

        # Controls for selecting time format
        # Text
        self.time_format_text_text = QLabel(
            parent = main.central_widget,
            text = "Choose Format for\nDisplaying Times",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(main.screen_width // 12, 25 * main.screen_height // 48, 4 * main.screen_width // 24, main.screen_height // 18),
            toolTip = tooltips["time_format"]
        )
        self.time_format_text_text.show()

        # Numeric button
        self.time_format_numeric_btn = Button(
            main = main,
            text = "Numeric",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(25 * main.screen_width // 96, 25 * main.screen_height // 48, 3 * main.screen_width // 48, main.screen_height // 18),
            connect = self.time_format_numeric,
            enabled = self.settings["time_format"] != "numeric"
        )
        self.time_format_numeric_btn.show()

        # Text button
        self.time_format_text_btn = Button(
            main = main,
            text = "Text",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(31 * main.screen_width // 96, 25 * main.screen_height // 48, 3 * main.screen_width // 48, main.screen_height // 18),
            connect = self.time_format_text,
            enabled = self.settings["time_format"] != "text"
        )
        self.time_format_text_btn.show()

        # Raw button
        self.time_format_raw_btn = Button(
            main = main,
            text = "Raw",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(37 * main.screen_width // 96, 25 * main.screen_height // 48, 3 * main.screen_width // 48, main.screen_height // 18),
            connect = self.time_format_raw,
            enabled = self.settings["time_format"] != "raw"
        )
        self.time_format_raw_btn.show()

        # Controls for enabling hints
        # Text 1
        self.enable_hints_text_1 = QLabel(
            parent = main.central_widget,
            text = "Enable Hints?",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(main.screen_width // 12, 29 * main.screen_height // 48, 4 * main.screen_width // 24, main.screen_height // 18),
            toolTip = tooltips["enable_hints"]
        )
        self.enable_hints_text_1.show()

        # Text 2
        self.enable_hints_text_2 = QLabel(
            parent = main.central_widget,
            text = "(Only available in Practice Mode)",
            font = QFont("Trebuchet MS", main.screen_height // 90),
            geometry = QRect(main.screen_width // 12, 31 * main.screen_height // 48, 3 * main.screen_width // 24, main.screen_height // 60)
        )
        self.enable_hints_text_2.show()

        # Yes button
        self.enable_hints_yes_btn = Button(
            main = main,
            text = "Yes",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(7 * main.screen_width // 24, 29 * main.screen_height // 48, 3 * main.screen_width // 48, main.screen_height // 18),
            connect = self.enable_hints_yes,
            enabled = not self.settings["enable_hints"]
        )
        self.enable_hints_yes_btn.show()

        # No button
        self.enable_hints_no_btn = Button(
            main = main,
            text = "No",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(17 * main.screen_width // 48, 29 * main.screen_height // 48, 3 * main.screen_width // 48, main.screen_height // 18),
            connect = self.enable_hints_no,
            enabled = self.settings["enable_hints"]
        )
        self.enable_hints_no_btn.show()

        # Controls for selection delay
        # Text
        self.selection_delay_text = QLabel(
            parent = main.central_widget,
            text = "Delay Before Removing\nSelected Cards",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(main.screen_width // 12, 11 * main.screen_height // 16, 4 * main.screen_width // 24, main.screen_height // 18),
            toolTip = tooltips["selection_delay"]
        )
        self.selection_delay_text.show()

        # Spin box
        self.selection_delay_box = SpinBox(
            main = main,
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(7 * main.screen_width // 24, 11 * main.screen_height // 16, 3 * main.screen_width // 24, main.screen_height // 18),
            minimum = 0,
            maximum = 10,
            value = self.settings["selection_delay"],
            suffix = " seconds",
            cursor = QCursor(Qt.CursorShape.PointingHandCursor),
            connect = self.selection_delay
        )
        self.selection_delay_box.show()

        # Accent color text
        self.accent_color_text = QLabel(
            parent = main.central_widget,
            text = "Accent Color:",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(11 * main.screen_width // 18, 5 * main.screen_height // 36, 5 * main.screen_width // 64, main.screen_height // 18),
            toolTip = tooltips["accent_color"]
        )
        self.accent_color_text.show()

        # Accent color current
        self.accent_color_current = QLabel(
            parent = main.central_widget,
            geometry = QRect(17 * main.screen_width // 24, 5 * main.screen_height // 36, main.screen_width // 32, main.screen_height // 18),
            styleSheet = f"background-color: {self.settings["accent_color"]}; border: 2px outset grey;"
        )
        self.accent_color_current.show()

        # Accent color choose
        self.accent_color_btn = Button(
            main = main,
            text = "Choose Color",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(55 * main.screen_width // 72, 5 * main.screen_height // 36, 3 * main.screen_width // 24, main.screen_height // 18),
            connect = self.choose_accent_color
        )
        self.accent_color_btn.show()
        
        # Save button
        self.save_btn = Button(
            main = main,
            text = "Save Current Settings",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(5 * main.screen_width // 12, 5 * main.screen_height // 6, main.screen_width // 6, main.screen_height // 18),
            connect = self.save_settings
        )
        self.save_btn.show()

        # Color Select
        self.color_select = ColorSelect(main, self.settings, self.save_btn, tooltips)

        # Shape Select
        self.shape_select = ShapeSelect(main, self.settings, self.save_btn, tooltips)

        # Controls for returning to the main menu
        # Button
        self.return_to_menu_btn = Button(
            main = main,
            text = "Return to Main Menu",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(7 * main.screen_width // 8, main.screen_height // 360, 79 * main.screen_width // 640, main.screen_height // 24),
            connect = self.attempt_return_to_menu
        )
        self.return_to_menu_btn.show()

        # Text
        self.return_to_menu_text = QLabel(
            parent = main.central_widget,
            text = "You have unsaved changes.\nAre you sure you want to return to the main menu?",
            geometry = QRect(0, main.screen_height // 5, main.screen_width, main.screen_height // 10),
            font = QFont("Trebuchet MS", main.screen_height // 30),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.return_to_menu_text.hide()

        # Yes
        self.return_to_menu_yes = Button(
            main = main,
            text = "Yes",
            geometry = QRect(3 * main.screen_width // 8, 35 * main.screen_height // 72, main.screen_width // 16, main.screen_height // 12),
            font = QFont("Trebuchet MS", main.screen_height // 40),
            connect = self.return_to_menu
        )
        self.return_to_menu_yes.hide()

        # No
        self.return_to_menu_no = Button(
            main = main,
            text = "No",
            geometry = QRect(9 * main.screen_width // 16, 35 * main.screen_height // 72, main.screen_width // 16, main.screen_height // 12),
            font = QFont("Trebuchet MS", main.screen_height // 40),
            connect = self.back_to_settings
        )
        self.return_to_menu_no.hide()

        # Set arrow navigation widgets
        self.num_traits.arrow_navigation(self.save_btn, self.num_variations)
        self.num_variations.arrow_navigation(self.num_traits, self.ai_difficulty_easy_btn, alt_down = self.ai_difficulty_medium_btn)
        self.ai_difficulty_easy_btn.arrow_navigation(
            self.ai_difficulty_extreme_btn, self.ai_difficulty_medium_btn, self.num_variations, self.show_num_sets_yes_btn,
            alt_left = self.ai_difficulty_hard_btn, alt_right = self.ai_difficulty_hard_btn, alt_down = self.show_num_sets_no_btn
        )
        self.ai_difficulty_medium_btn.arrow_navigation(
            self.ai_difficulty_easy_btn, self.ai_difficulty_hard_btn, self.num_variations, self.show_num_sets_yes_btn,
            alt_left = self.ai_difficulty_extreme_btn, alt_right = self.ai_difficulty_extreme_btn, alt_down = self.show_num_sets_no_btn
        )
        self.ai_difficulty_hard_btn.arrow_navigation(
            self.ai_difficulty_medium_btn, self.ai_difficulty_extreme_btn, self.num_variations, self.show_num_sets_yes_btn,
            alt_left = self.ai_difficulty_easy_btn, alt_right = self.ai_difficulty_easy_btn, alt_down = self.show_num_sets_no_btn
        )
        self.ai_difficulty_extreme_btn.arrow_navigation(
            self.ai_difficulty_hard_btn, self.ai_difficulty_easy_btn, self.num_variations, self.show_num_sets_yes_btn,
            alt_left = self.ai_difficulty_medium_btn, alt_right = self.ai_difficulty_medium_btn, alt_down = self.show_num_sets_no_btn
        )
        self.show_num_sets_yes_btn.arrow_navigation(
            self.show_num_sets_no_btn, self.show_num_sets_no_btn, self.ai_difficulty_easy_btn, self.show_cards_left_in_deck_yes_btn,
            alt_up = self.ai_difficulty_medium_btn, alt_down = self.show_cards_left_in_deck_no_btn
        )
        self.show_num_sets_no_btn.arrow_navigation(
            self.show_num_sets_yes_btn, self.show_num_sets_yes_btn, self.ai_difficulty_easy_btn, self.show_cards_left_in_deck_yes_btn,
            alt_up = self.ai_difficulty_medium_btn, alt_down = self.show_cards_left_in_deck_no_btn
        )
        self.show_cards_left_in_deck_yes_btn.arrow_navigation(
            self.show_cards_left_in_deck_no_btn, self.show_cards_left_in_deck_no_btn, self.show_num_sets_yes_btn, self.time_format_numeric_btn,
            alt_up = self.show_num_sets_no_btn, alt_down = self.time_format_text_btn
        )
        self.show_cards_left_in_deck_no_btn.arrow_navigation(
            self.show_cards_left_in_deck_yes_btn, self.show_cards_left_in_deck_yes_btn, self.show_num_sets_yes_btn, self.time_format_numeric_btn,
            alt_up = self.show_num_sets_no_btn, alt_down = self.time_format_text_btn
        )
        self.time_format_numeric_btn.arrow_navigation(
            self.time_format_raw_btn, self.time_format_text_btn, self.show_cards_left_in_deck_yes_btn, self.enable_hints_yes_btn,
            alt_left = self.time_format_text_btn, alt_right = self.time_format_raw_btn, alt_up = self.show_cards_left_in_deck_no_btn, alt_down = self.enable_hints_no_btn
        )
        self.time_format_text_btn.arrow_navigation(
            self.time_format_numeric_btn, self.time_format_raw_btn, self.show_cards_left_in_deck_yes_btn, self.enable_hints_yes_btn,
            alt_left = self.time_format_raw_btn, alt_right = self.time_format_numeric_btn, alt_up = self.show_cards_left_in_deck_no_btn, alt_down = self.enable_hints_no_btn
        )
        self.time_format_raw_btn.arrow_navigation(
            self.time_format_text_btn, self.time_format_numeric_btn, self.show_cards_left_in_deck_yes_btn, self.enable_hints_yes_btn,
            alt_left = self.time_format_numeric_btn, alt_right = self.time_format_text_btn, alt_up = self.show_cards_left_in_deck_no_btn, alt_down = self.enable_hints_no_btn
        )
        self.enable_hints_yes_btn.arrow_navigation(
            self.enable_hints_no_btn, self.enable_hints_no_btn, self.time_format_numeric_btn, self.selection_delay_box,
            alt_up = self.time_format_text_btn
        )
        self.enable_hints_no_btn.arrow_navigation(
            self.enable_hints_yes_btn, self.enable_hints_yes_btn, self.time_format_numeric_btn, self.selection_delay_box,
            alt_up = self.time_format_text_btn
        )
        self.selection_delay_box.arrow_navigation(self.enable_hints_yes_btn, self.accent_color_btn, alt_up = self.enable_hints_no_btn)
        self.accent_color_btn.arrow_navigation(self.selection_delay_box, self.return_to_menu_btn, self.selection_delay_box, self.color_select.custom_color_btn)
        self.color_select.custom_color_btn.arrow_navigation(self.selection_delay_box, self.color_select.reset, self.accent_color_btn, self.shape_select.reset)
        self.color_select.reset.arrow_navigation(self.color_select.custom_color_btn, None, self.accent_color_btn, self.shape_select.reset)
        self.shape_select.reset.arrow_navigation(self.selection_delay_box, None, self.color_select.custom_color_btn, self.save_btn)
        self.return_to_menu_btn.arrow_navigation(self.accent_color_btn, self.num_traits, self.save_btn, self.accent_color_btn)
        self.save_btn.arrow_navigation(None, None, self.shape_select.reset, self.num_traits)

        # Set Tab Order
        main.central_widget.setTabOrder(self.num_traits, self.num_variations)
        main.central_widget.setTabOrder(self.num_variations, self.ai_difficulty_easy_btn)
        main.central_widget.setTabOrder(self.ai_difficulty_easy_btn, self.ai_difficulty_medium_btn)
        main.central_widget.setTabOrder(self.ai_difficulty_medium_btn, self.ai_difficulty_hard_btn)
        main.central_widget.setTabOrder(self.ai_difficulty_hard_btn, self.ai_difficulty_extreme_btn)
        main.central_widget.setTabOrder(self.ai_difficulty_extreme_btn, self.show_num_sets_yes_btn)
        main.central_widget.setTabOrder(self.show_num_sets_yes_btn, self.show_num_sets_no_btn)
        main.central_widget.setTabOrder(self.show_num_sets_no_btn, self.show_cards_left_in_deck_yes_btn)
        main.central_widget.setTabOrder(self.show_cards_left_in_deck_yes_btn, self.show_cards_left_in_deck_no_btn)
        main.central_widget.setTabOrder(self.show_cards_left_in_deck_no_btn, self.time_format_numeric_btn)
        main.central_widget.setTabOrder(self.time_format_numeric_btn, self.time_format_text_btn)
        main.central_widget.setTabOrder(self.time_format_text_btn, self.time_format_raw_btn)
        main.central_widget.setTabOrder(self.time_format_raw_btn, self.enable_hints_yes_btn)
        main.central_widget.setTabOrder(self.enable_hints_yes_btn, self.enable_hints_no_btn)
        main.central_widget.setTabOrder(self.enable_hints_no_btn, self.selection_delay_box)
        main.central_widget.setTabOrder(self.selection_delay_box, self.accent_color_btn)
        main.central_widget.setTabOrder(self.accent_color_btn, self.color_select.custom_color_btn)
        main.central_widget.setTabOrder(self.color_select.custom_color_btn, self.color_select.reset)
        main.central_widget.setTabOrder(self.color_select.reset, self.shape_select.reset)
        main.central_widget.setTabOrder(self.shape_select.reset, self.save_btn)
        main.central_widget.setTabOrder(self.save_btn, self.return_to_menu_btn)
        
        main.central_widget.setTabOrder(self.return_to_menu_yes, self.return_to_menu_no)