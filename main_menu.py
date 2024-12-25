from board import Board
from challenges import Challenges
from PyQt6.QtCore import QRect, QSize, Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QLabel
from settings_page import SettingsPage
from time_trial_page import TimeTrialPage
from tutorial import Tutorial
from ui import Button


class MainMenu:

    def back_to_main_menu(self):

        # Hide conformation controls
        self.confirm_exit_text.hide()
        self.confirm_exit_yes.hide()
        self.confirm_exit_no.hide()

        # Show main menu controls
        self.ai_game.show()
        self.practice_game.show()
        self.tutorial.show()
        self.time_trial.show()
        self.settings_btn.show()
        self.challenges.show()
        self.logo.show()
        self.exit_btn.show()

        # Manage focus
        self.confirm_exit_no.clearFocus()
        self.focus_widget.setFocus()

    def confirm_exit(self):

        # Hide main menu controls
        self.ai_game.hide()
        self.practice_game.hide()
        self.tutorial.hide()
        self.time_trial.hide()
        self.settings_btn.hide()
        self.challenges.hide()
        self.logo.hide()
        self.exit_btn.hide()

        # Show conformation controls
        self.confirm_exit_text.show()
        self.confirm_exit_yes.show()
        self.confirm_exit_no.show()

        # Manage focus
        self.focus_widget = self.main.app.focusWidget()
        self.focus_widget.clearFocus()
        self.confirm_exit_no.setFocus()

    def destroy(self):
        self.ai_game.deleteLater()
        self.practice_game.deleteLater()
        self.time_trial.deleteLater()
        self.challenges.deleteLater()
        self.settings_btn.deleteLater()
        self.exit_btn.deleteLater()
        self.tutorial.deleteLater()
        self.logo.deleteLater()
        self.confirm_exit_text.deleteLater()
        self.confirm_exit_yes.deleteLater()
        self.confirm_exit_no.deleteLater()
        self.main.main_menu = None

    def exit_game(self):
        self.main.app.quit()

    def go_to_challenges(self):
        if self.focus_widget:
            self.focus_widget.clearFocus()
        self.main.challenges_page = Challenges(self.main)
        self.destroy()

    def go_to_settings(self):
        if self.focus_widget:
            self.focus_widget.clearFocus()
        self.main.settings_page = SettingsPage(self.main)
        self.destroy()

    def go_to_time_trial(self):
        if self.focus_widget:
            self.focus_widget.clearFocus()
        self.main.time_trial_page = TimeTrialPage(self.main)
        self.destroy()

    def go_to_tutorial(self):
        if self.focus_widget:
            self.focus_widget.clearFocus()
        self.main.tutorial_page = Tutorial(self.main)
        self.destroy()

    def start_ai_game(self):
        if self.focus_widget:
            self.focus_widget.clearFocus()
        self.main.board = Board(self.main, "ai")
        self.destroy()

    def start_practice_game(self):
        if self.focus_widget:
            self.focus_widget.clearFocus()
        self.main.board = Board(self.main, "practice")
        self.destroy()

    def __init__(self, main):

        self.main = main

        # Logo image
        self.logo = QLabel(
            parent = main.central_widget,
            geometry = QRect(main.screen_width // 6, main.screen_height // 30, 2 * main.screen_width // 3, main.screen_height // 2),
            pixmap = QPixmap("logo.png").scaled(
                QSize(2 * main.screen_width // 3, main.screen_height // 2),
                aspectRatioMode = Qt.AspectRatioMode.IgnoreAspectRatio,
                transformMode = Qt.TransformationMode.FastTransformation
            )
        )
        self.logo.show()

        # "Versus AI" button
        self.ai_game = Button(
            main = main,
            text = "Versus AI",
            geometry = QRect(2 * main.screen_width // 5, 73 * main.screen_height // 120, main.screen_width // 5, 7 * main.screen_height // 60),
            font = QFont("Trebuchet MS", main.screen_height // 20),
            connect = self.start_ai_game
        )
        self.ai_game.show()
        self.ai_game.setFocus()

        # Practice button
        self.practice_game = Button(
            main = main,
            text = "Practice",
            geometry = QRect(2 * main.screen_width // 5, 93 * main.screen_height // 120, main.screen_width // 5, 7 * main.screen_height // 60),
            font = QFont("Trebuchet MS", main.screen_height // 20),
            connect = self.start_practice_game
        )
        self.practice_game.show()

        # Time Trial button
        self.time_trial = Button(
            main = main,
            text = "Time Trial",
            geometry = QRect(main.screen_width // 6, 5 * main.screen_height // 8, main.screen_width // 6, main.screen_height // 12),
            font = QFont("Trebuchet MS", main.screen_height // 30),
            connect = self.go_to_time_trial
        )
        self.time_trial.show()

        # Challenges button
        self.challenges = Button(
            main = main,
            text = "Challenges",
            geometry = QRect(2 * main.screen_width // 3, 5 * main.screen_height // 8, main.screen_width // 6, main.screen_height // 12),
            font = QFont("Trebuchet MS", main.screen_height // 30),
            connect = self.go_to_challenges
        )
        self.challenges.show()

        # Tutorial button
        self.tutorial = Button(
            main = main,
            text = "Tutorial",
            geometry = QRect(main.screen_width // 6, 19 * main.screen_height // 24, main.screen_width // 6, main.screen_height // 12),
            font = QFont("Trebuchet MS", main.screen_height // 30),
            connect = self.go_to_tutorial
        )
        self.tutorial.show()

        # Settings button
        self.settings_btn = Button(
            main = main,
            text = "Settings",
            geometry = QRect(2 * main.screen_width // 3, 19 * main.screen_height // 24, main.screen_width // 6, main.screen_height // 12),
            font = QFont("Trebuchet MS", main.screen_height // 30),
            connect = self.go_to_settings
        )
        self.settings_btn.show()

        # Exit button
        self.exit_btn = Button(
            main = main,
            text = "Exit Game",
            geometry = QRect(9 * main.screen_width // 10, main.screen_height // 360, 63 * main.screen_width // 640, 2 * main.screen_height // 45),
            font = QFont("Trebuchet MS", main.screen_height // 60),
            connect = self.confirm_exit
        )
        self.exit_btn.show()

        # Confirm Exit Text
        self.confirm_exit_text = QLabel(
            parent = main.central_widget,
            text = "Are you sure you want to exit the game?",
            geometry = QRect(0, main.screen_height // 5, main.screen_width, main.screen_height // 10),
            font = QFont("Trebuchet MS", main.screen_height // 30),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.confirm_exit_text.hide()

        # Confirm Exit Yes
        self.confirm_exit_yes = Button(
            main = main,
            text = "Yes",
            geometry = QRect(3 * main.screen_width // 8, 35 * main.screen_height // 72, main.screen_width // 16, main.screen_height // 12),
            font = QFont("Trebuchet MS", main.screen_height // 40),
            connect = self.exit_game
        )
        self.confirm_exit_yes.hide()

        # Confirm Exit No
        self.confirm_exit_no = Button(
            main = main,
            text = "No",
            geometry = QRect(9 * main.screen_width // 16, 35 * main.screen_height // 72, main.screen_width // 16, main.screen_height // 12),
            font = QFont("Trebuchet MS", main.screen_height // 40),
            connect = self.back_to_main_menu
        )
        self.confirm_exit_no.hide()

        # Set arrow navigation widgets
        self.time_trial.arrow_navigation(self.challenges, self.ai_game, self.exit_btn, self.tutorial)
        self.ai_game.arrow_navigation(self.time_trial, self.challenges, self.exit_btn, self.practice_game)
        self.challenges.arrow_navigation(self.ai_game, self.time_trial, self.exit_btn, self.settings_btn)
        self.tutorial.arrow_navigation(self.settings_btn, self.practice_game, self.time_trial, self.exit_btn)
        self.practice_game.arrow_navigation(self.tutorial, self.settings_btn, self.ai_game, self.exit_btn)
        self.settings_btn.arrow_navigation(self.practice_game, self.tutorial, self.challenges, self.exit_btn)
        self.exit_btn.arrow_navigation(self.challenges, self.time_trial, self.practice_game, self.ai_game)
        self.confirm_exit_yes.arrow_navigation(self.confirm_exit_no, self.confirm_exit_no, None, None)
        self.confirm_exit_no.arrow_navigation(self.confirm_exit_yes, self.confirm_exit_yes, None, None)
        self.focus_widget = None
        
        # Set Tab Order
        main.central_widget.setTabOrder(self.time_trial, self.ai_game)
        main.central_widget.setTabOrder(self.ai_game, self.challenges)
        main.central_widget.setTabOrder(self.challenges, self.tutorial)
        main.central_widget.setTabOrder(self.tutorial, self.practice_game)
        main.central_widget.setTabOrder(self.practice_game, self.settings_btn)
        main.central_widget.setTabOrder(self.settings_btn, self.exit_btn)
        
        main.central_widget.setTabOrder(self.confirm_exit_yes, self.confirm_exit_no)