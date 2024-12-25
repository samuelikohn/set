from PyQt6.QtCore import QPoint, QRect, Qt, QTimer
from PyQt6.QtGui import QBrush, QColor, QCursor, QFont, QPainter, QPolygon
from PyQt6.QtWidgets import QPushButton, QComboBox, QSlider, QSpinBox, QWidget


class Button(QPushButton):

    def arrow_navigation(self, left, right, up, down, alt_left = None, alt_right = None, alt_up = None, alt_down = None):

        # Defines the neighboring widgets used for arrow key navigation
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.alt_left = alt_left
        self.alt_right = alt_right
        self.alt_up = alt_up
        self.alt_down = alt_down

    def enterEvent(self, event):
        self.update_style(border_scale = self.border_scale, shift = 20)
        return super().enterEvent(event)
    
    def focusInEvent(self, event):
        self.update_style(border_scale = 2, shift = self.shift)
        return super().focusInEvent(event)
    
    def focusOutEvent(self, event):
        self.update_style(border_scale = 1, shift = self.shift)
        return super().focusOutEvent(event)
    
    def keyPressEvent(self, event):

        # Selection via Enter/Return
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.click()

        # Go back a page on Esc
        elif event.key() == Qt.Key.Key_Escape:

            # Main menu
            if self.main.main_menu:

                # "No" on confirm exit screen
                if self.main.main_menu.exit_btn.isHidden():
                    self.main.main_menu.confirm_exit_no.click()

                # Exit game from main menu
                else:
                    self.main.main_menu.exit_btn.click()

            # Time trial page
            elif self.main.time_trial_page:

                # Go back from times screen to time trial menu
                if self.main.time_trial_page.go_back_btn.isHidden():
                    self.main.time_trial_page.return_to_menu_btn.click()

                # Return to main menu from time trial page
                else:
                    self.main.time_trial_page.go_back_btn.click()

            # Exit tutorial to main menu
            elif self.main.tutorial_page:
                self.main.tutorial_page.exit_btn.click()

            # Pause game on Esc
            elif self.main.board:
                self.main.board.pause_game_btn.click()

            # Settings page
            elif self.main.settings_page:
                
                # "No" on unsaved changes screen
                if self.main.settings_page.return_to_menu_btn.isHidden():
                    self.main.settings_page.return_to_menu_no.click()

                # Return to main menu from settings
                else:
                    self.main.settings_page.return_to_menu_btn.click()

            # Challenges page
            elif self.main.challenges_page:

                # Go back to challenges menu from play menu
                if not self.main.challenges_page.go_back_from_challenges_btn.isHidden():
                    self.main.challenges_page.go_back_from_challenges_btn.click()

                # Go back from scores menu to challenges
                elif not self.main.challenges_page.go_back_from_scores_btn.isHidden():
                    self.main.challenges_page.go_back_from_scores_btn.click()

                # Go back to main menu from challenges
                else:
                    self.main.challenges_page.return_to_menu_btn.click()

        # Left arrow
        elif event.key() == Qt.Key.Key_Left:
            self.clearFocus()
            if self.left and self.left.isEnabled() and not self.left.isHidden():
                self.left.setFocus()
            elif self.alt_left:
                self.alt_left.setFocus()

        # Right arrow
        elif event.key() == Qt.Key.Key_Right:
            self.clearFocus()
            if self.right and self.right.isEnabled() and not self.right.isHidden():
                self.right.setFocus()
            elif self.alt_right:
                self.alt_right.setFocus()

        # Up arrow
        elif event.key() == Qt.Key.Key_Up:
            self.clearFocus()
            if self.up and self.up.isEnabled() and not self.up.isHidden():
                self.up.setFocus()
            elif self.alt_up:
                self.alt_up.setFocus()

        # Down arrow
        elif event.key() == Qt.Key.Key_Down:
            self.clearFocus()
            if self.down and self.down.isEnabled() and not self.down.isHidden():
                self.down.setFocus()
            elif self.alt_down:
                self.alt_down.setFocus()

    def leaveEvent(self, event):
        self.update_style(border_scale = self.border_scale, shift = 0)
        return super().leaveEvent(event)

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
    
    def update_style(self, hex_code = None, border_scale = 1, shift = 0):

        if hex_code:
            self.color = hex_code

        self.border_scale = border_scale
        self.shift = shift
        
        if isinstance(self, CallSetButton) and self.isEnabled():

            time_left = self.time_left if hasattr(self, "time_left") else 100
            if time_left != 100:
                border_scale =  1
                shift = 0

            self.setStyleSheet(f"""
                background-color: qlineargradient(
                    x1: 0,
                    x2: 1,
                    stop: {(time_left - 1) / 100} {self.shift_color_lightness(self.color, shift)},
                    stop: {time_left / 100} #f3eef6
                );
                border: {self.height() // (15 / border_scale)}px solid {self.shift_color_lightness(self.color, -60)};
                outline: 0;
            """)
        
        elif not self.isEnabled():
            self.setStyleSheet(f"""
                background-color: #f3eef6;
                border: {self.height() // 15}px solid {self.shift_color_lightness("#f3eef6", -50)};
            """)
        
        else:
            self.setStyleSheet(f"""
                background-color: {self.shift_color_lightness(self.color, shift)};
                border: {self.height() // (15 / border_scale)}px solid {self.shift_color_lightness(self.color, -50)};
                outline: 0;
            """)

    def __init__(self, main, text = "", font = QFont(), geometry = QRect(), connect = None, enabled = True):
        super().__init__(
            parent = main.central_widget,
            text = text,
            font = font,
            geometry = geometry,
            enabled = enabled,
            cursor = QCursor(Qt.CursorShape.PointingHandCursor)
        )
        if connect:
            self.clicked.connect(connect)

        self.main = main
        self.color = main.settings["accent_color"]
        self.update_style(self.color)


class CallSetButton(Button):

    def destroy(self):
        self.timer.stop()
        super().deleteLater()

    def paintEvent(self, event):

        # Call default paint event
        super().paintEvent(event)
    
        # Draw "Press Space" text
        if self.text() == "Call SET":
            qp = QPainter(self)
            qp.setFont(QFont("Trebuchet MS", self.main.screen_height // 120))
            qp.drawText(
                0,
                0,
                self.width(),
                13 * self.height() // 15,
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom,
                "(Press Space)"
            )
    
    def __init__(self, main, board):
        super().__init__(
            main,
            text = "Call SET",
            geometry = QRect(main.screen_width // 60, 7 * main.screen_height // 15, 7 * main.screen_width // 60, main.screen_height // 12),
            font = QFont("Trebuchet MS", main.screen_height // 40),
            connect = board.call_set
        )
        self.called = False
        self.time_left = 100
        self.timer = QTimer(parent = main.central_widget)
        self.timer.timeout.connect(board.call_set_update_button)
        self.show()


class Dropdown(QComboBox):

    def arrow_navigation(self, left, right, up, down, alt_left = None, alt_right = None, alt_up = None, alt_down = None):

        # Defines the neighboring widgets used for arrow key navigation
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.alt_left = alt_left
        self.alt_right = alt_right
        self.alt_up = alt_up
        self.alt_down = alt_down

    def keyPressEvent(self, event):

        # Go back a page on Esc
        if event.key() == Qt.Key.Key_Escape:
            
            # Time trial page
            if self.main.time_trial_page:

                # Go back from times screen to time trial menu
                if self.main.time_trial_page.go_back_btn.isHidden():
                    self.main.time_trial_page.return_to_menu_btn.click()

                # Return to main menu from time trial page
                else:
                    self.main.time_trial_page.go_back_btn.click()

            # Challenges page
            elif self.main.challenges_page:

                # Go back to challenges menu from play menu
                if not self.main.challenges_page.go_back_from_challenges_btn.isHidden():
                    self.main.challenges_page.go_back_from_challenges_btn.click()

                # Go back from scores menu to challenges
                elif not self.main.challenges_page.go_back_from_scores_btn.isHidden():
                    self.main.challenges_page.go_back_from_scores_btn.click()

                # Go back to main menu from challenges
                else:
                    self.main.challenges_page.return_to_menu_btn.click()

        # Left arrow
        elif self.left and event.key() == Qt.Key.Key_Left:
            self.clearFocus()
            self.left.setFocus()

        # Right arrow
        elif self.right and event.key() == Qt.Key.Key_Right:
            self.clearFocus()
            self.right.setFocus()

        return super().keyPressEvent(event)

    def __init__(self, main, currentText, font, geometry):
        super().__init__(
            parent = main.central_widget,
            currentText = currentText,
            font = font,
            geometry = geometry,
            cursor = QCursor(Qt.CursorShape.PointingHandCursor)
        )

        self.main = main

        # Place holders for arrow navigation
        self.left = None
        self.right = None
        self.up = None
        self.down = None


class GameOver(QWidget):

    def destroy(self):
        super().deleteLater()
        
    def keyPressEvent(self, event):
        
        keys = [
            Qt.Key.Key_Return,
            Qt.Key.Key_Enter,
            Qt.Key.Key_Space,
            Qt.Key.Key_Left,
            Qt.Key.Key_Right,
            Qt.Key.Key_Up,
            Qt.Key.Key_Down
        ]
        
        if event.key() in keys:

            if self.board.mode in ["static", "xl", "time_trial"]:
                self.board.return_to_menu(time = self.board.elapsed_time)

            elif self.board.mode in ["recycle", "xs"]:
                self.board.return_to_menu(time = int(self.board.player_score_card.text()))

            else:
                self.board.return_to_menu()
            
    def mousePressEvent(self, event):
            
        if self.board.mode in ["static", "xl", "time_trial"]:
            self.board.return_to_menu(time = self.board.elapsed_time)

        elif self.board.mode in ["recycle", "xs"]:
            self.board.return_to_menu(time = int(self.board.player_score_card.text()))

        else:
            self.board.return_to_menu()
                
    def __init__(self, main, board):
        super().__init__(main.central_widget)
        self.board = board
        self.time_trial_page = main.time_trial_page
        self.screen_width = main.screen_width
        self.screen_height = main.screen_height
        self.setGeometry(0, 0, self.screen_width, self.screen_height)
        self.hide()


class InfoPanelBorder(QWidget):

    def destroy(self):
        super().deleteLater()

    def paintEvent(self, event):

        # Initialize painter
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw decorations
        qp.fillRect(0, 0, self.screen_width, self.screen_height // 360, QBrush(QColor(144, 144, 144)))
        qp.fillRect(0, self.screen_height // 360, self.screen_width, self.screen_height // 360, QBrush(QColor(208, 208, 208)))
        
        # End paint event
        qp.end()

    def __init__(self, main):
        super().__init__(main.central_widget)
        self.screen_width = main.screen_width
        self.screen_height = main.screen_height
        self.setGeometry(0, self.screen_height // 20, self.screen_width, self.screen_height // 180)
        self.show()


class PauseButton(Button):

    def destroy(self):
        super().deleteLater()

    def pause_game(self):

        if self.paused:

            # Hide "pause game" controls
            self.board.pause_game_text.hide()
            self.board.show_settings_btn.hide()
            for tile in self.board.settings_name_tiles:
                tile.hide()
            for tile in self.board.settings_values_tiles:
                tile.hide()

            # Show all game controls
            self.board.call_set_btn.setEnabled(True)
            if len(self.board.sets) == 0 and self.board.deck:
                self.board.add_cards_btn.setEnabled(True)
            for card in self.board.current_board:
                card.show()
            if self.board.mode == "static":
                for card in self.board.found_cards:
                    card.show()
            if self.board.enable_hints:
                self.board.enable_hints.setEnabled(True)

            # Resume timer if in time trial mode
            if self.board.mode in ["static", "recycle", "xl", "time_trial"]:
                self.board.timer.start(100)

            # Start selection delay if active
            if self.board.selection_delay_timer_active:
                self.board.selection_delay_timer.start(self.board.main.settings["selection_delay"])

            # AI and Call Set button are not resumed until selection delay is over. Otherwise, resume immediately
            else:

                # Resume AI
                if self.board.mode == "ai":
                    self.board.ai.resume()

                # Resume Call Set button if active
                if self.board.call_set_btn.called:
                    if self.board.mode == "ai":
                        if not self.board.ai.in_selection:
                            self.board.call_set_btn.timer.start(100)
                    else:
                        self.board.call_set_btn.timer.start(100)

        else:
        
            # Hide controls while dialogue is up
            self.board.call_set_btn.setEnabled(False)
            for card in self.board.current_board:
                card.hide()
            if self.board.mode == "static":
                for card in self.board.found_cards:
                    card.hide()
            self.board.add_cards_btn.setEnabled(False)
            if self.board.enable_hints:
                self.board.enable_hints.setEnabled(False)

            # Show pause controls
            self.board.pause_game_text.show()
            self.board.show_settings_btn.show()
            if self.board.show_settings_btn.text() == "Hide Current Settings":
                for tile in self.board.settings_name_tiles:
                    tile.show()
                for tile in self.board.settings_values_tiles:
                    tile.show()
                
            # Pause Call Set button if active
            if self.board.call_set_btn.called:
                if self.board.ai:
                    if not self.board.ai.in_selection:
                        self.board.call_set_btn.timer.stop()
                else:
                    self.board.call_set_btn.timer.stop()

            # Stop selection delay if active
            if self.board.selection_delay_timer_active:
                self.board.selection_delay_timer.stop()

            # Pause timer if in time trial mode
            if self.board.mode in ["static", "recycle", "xl", "time_trial"]:
                self.board.timer.stop()

            # Pause AI
            if self.board.mode == "ai":
                self.board.ai.pause()

        # Toggle paused state
        self.paused = not self.paused
        
        # Update board buttons
        self.update()
        self.board.update_buttons()

    def paintEvent(self, event):

        # Call default paint event for button
        super().paintEvent(event)

        # Initialize painter
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Set brush color based on quit game menu status
        if self.board.quit_game_text.isHidden() and self.board.game_over_text.isHidden():
            color = QColor(0, 0, 0)
        else:
            color = QColor(120, 120, 120)

        # Create brush for drawing filled polygons
        brush = QBrush()
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        brush.setColor(color)
        qp.setBrush(brush)

        # Draw pause button icons
        if self.paused:

            # Play symbol
            qp.drawPolygon(QPolygon([
                QPoint(self.screen_width // 200, 2 * self.screen_height // 225),
                QPoint(self.screen_width // 200, 8 * self.screen_height // 225),
                QPoint(self.screen_width // 50, self.screen_height // 45)
            ]))
        
        else:

            # Pause symbol
            qp.fillRect(self.screen_width // 200, 2 * self.screen_height // 225, self.screen_width // 160, 6 * self.screen_height // 225, QBrush(color))
            qp.fillRect(11 * self.screen_width // 800, 2 * self.screen_height // 225, self.screen_width // 160, 6 * self.screen_height // 225, QBrush(color))
        
        # End paint event
        qp.end()

    def __init__(self, main, board):
        super().__init__(
            main = main,
            geometry = QRect(559 * main.screen_width // 640, main.screen_height // 360, main.screen_width // 40, 2 * main.screen_height // 45),
            connect = self.pause_game
        )
        self.screen_width = main.screen_width
        self.screen_height = main.screen_height
        self.board = board
        self.paused = False
        self.show()


class ScorePanelBorder(QWidget):

    def destroy(self):
        super().deleteLater()

    def paintEvent(self, event):

        # Initialize painter
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw decorations
        qp.fillRect(0, 0, self.screen_width // 640, 17 * self.screen_height // 18, QBrush(QColor(144, 144, 144)))
        qp.fillRect(self.screen_width // 640, 0, self.screen_width // 640, 17 * self.screen_height // 18, QBrush(QColor(208, 208, 208)))
        
        # End paint event
        qp.end()

    def __init__(self, main):
        super().__init__(main.central_widget)
        self.screen_width = main.screen_width
        self.screen_height = main.screen_height
        self.setGeometry(3 * self.screen_width // 20, self.screen_height // 18, self.screen_width // 320, 17 * self.screen_height // 18)
        self.show()


class Slider(QSlider):

    def arrow_navigation(self, up, down, alt_down = None):

        # Defines the neighboring widgets used for arrow key navigation
        self.up = up
        self.down = down
        self.alt_down = alt_down

    def enterEvent(self, event):
        self.update_style(shift = 20)
        return super().enterEvent(event)
    
    def keyPressEvent(self, event):

        # Go back a page on Esc
        if event.key() == Qt.Key.Key_Escape:
            self.main.settings_page.return_to_menu_btn.click()

        # Up arrow
        elif self.up and self.up.isEnabled() and event.key() == Qt.Key.Key_Up:
            self.clearFocus()
            self.up.setFocus()

        # Down arrow
        elif self.down and event.key() == Qt.Key.Key_Down:
            self.clearFocus()
            if self.down.isEnabled():
                self.down.setFocus()
            elif self.alt_down:
                self.alt_down.setFocus()

    def leaveEvent(self, event):
        self.update_style()
        return super().leaveEvent(event)
    
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

    def update_style(self, hex_code = None, shift = 0):

        if hex_code:
            self.color = hex_code

        self.setStyleSheet(f"""
            QSlider::handle {{
                background-color: {self.shift_color_lightness(self.color, shift)};
            }}
        """)

    def __init__(self, main, geometry, orientation, minimum, maximum, value, cursor):
        super().__init__(
            parent = main.central_widget,
            geometry = geometry,
            orientation = orientation,
            minimum = minimum,
            maximum = maximum,
            value = value,
            cursor = cursor
        )

        self.main = main

        self.hover = False
        self.color = main.settings["accent_color"]
        self.update_style(self.color)

        self.up = None
        self.down = None


class SpinBox(QSpinBox):

    def arrow_navigation(self, up, down, alt_up = None):

        # Defines the neighboring widgets used for arrow key navigation
        self.up = up
        self.down = down
        self.alt_up = alt_up

    def keyPressEvent(self, event):

        # Go back a page on Esc
        if event.key() == Qt.Key.Key_Escape:
            self.main.settings_page.return_to_menu_btn.click()

        # Left arrow
        elif event.key() == Qt.Key.Key_Left:
            v = self.value()
            self.setValue(v - 1)

        # Right arrow
        elif event.key() == Qt.Key.Key_Right:
            v = self.value()
            self.setValue(v + 1)

        # Up arrow
        elif self.up and event.key() == Qt.Key.Key_Up:
            self.clearFocus()
            if self.up.isEnabled():
                self.up.setFocus()
            elif self.alt_up:
                self.alt_up.setFocus()

        # Down arrow
        elif self.down and event.key() == Qt.Key.Key_Down:
            self.clearFocus()
            self.down.setFocus()

    def __init__(self, main, font, geometry, minimum, maximum, value, suffix, cursor, connect):
        super().__init__(
            parent = main.central_widget,
            font = font,
            geometry = geometry,
            minimum = minimum,
            maximum = maximum,
            value = value,
            suffix = suffix,
            cursor = cursor
        )

        self.valueChanged.connect(connect)
        self.main = main