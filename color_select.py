from math import ceil
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtWidgets import QColorDialog, QLabel, QMessageBox, QScrollArea, QWidget
from ui import Button

class ColorSelect:

    def add_color(self, color):
        
        self.color_dialogue = None

        # Convert from tuple into formatted string
        hex_code = self.rgb_to_hex(color.getRgb())

        # Check if color already exists
        if hex_code in self.settings["colors"] or hex_code in self.settings["custom_colors"]:
            color_dupe = QMessageBox(
                parent = self.main.central_widget,
                text = "This color already exists!"
            )
            color_dupe.setWindowTitle("Duplicate Color")
            color_dupe.show()

        # If not in settings, add
        else:
        
            # Add to display
            self.place_custom_color(hex_code, len(self.settings["custom_colors"]))
            
            # Add to settings
            self.settings["custom_colors"].append(hex_code)

            self.save_btn.setText("Save Current Settings")

    def custom_color(self):

        # If no color dialogue exists, open one for color selection
        if not self.color_dialogue:
            self.color_dialogue = ColorDialogue(self)
            self.color_dialogue.colorSelected.connect(self.add_color)
            self.color_dialogue.show()

    def destroy(self):
        if self.color_dialogue:
            self.color_dialogue.deleteLater()
        self.scroller.deleteLater()
        self.choose_panel.deleteLater()
        self.choose_text.deleteLater()
        self.selected_panel.deleteLater()
        self.selected_text.deleteLater()
        self.custom_color_btn.deleteLater()
        self.reset.deleteLater()
        for wid in self.selected_colors:
            wid.deleteLater()
        for wid in self.not_selected_colors:
            wid.deleteLater()
        for wid in self.selection_borders:
            wid.deleteLater()

    def hide(self):
        if self.color_dialogue:
            self.color_dialogue.deleteLater()
        self.scroller.hide()
        self.choose_panel.hide()
        self.choose_text.hide()
        self.selected_panel.hide()
        self.selected_text.hide()
        self.custom_color_btn.hide()
        self.reset.hide()
        for wid in self.selected_colors:
            wid.hide()
        for wid in self.not_selected_colors:
            wid.hide()
        for wid in self.selection_borders:
            wid.hide()

    def place_custom_color(self, color, i):
        length = 7 * self.main.screen_width // 64

        self.not_selected_colors.append(ColorDisplay(
            self.main,
            self,
            color,
            self.save_btn, 
            length // 16 + (i % 6) * 5 * length // 16,
            length // 16 + (i // 6) * 5 * length // 16,
            length // 4,
            length // 4,
            right_pos = i
        ))
        self.choose_panel.setGeometry(133 * self.main.screen_width // 192, 7 * self.main.screen_height // 36, 43 * self.main.screen_width // 192, ceil(len(self.not_selected_colors) / 6) * 5 * length // 16)
        self.scroller.takeWidget()
        self.scroller.setWidget(self.choose_panel)

    def reset_colors(self):
        
        default_colors = ["#ea1c2d", "#14a750", "#662d91", "#1672f4", "#f8c326"]
        length = 7 * self.main.screen_width // 64
        x_offset = 83 * self.main.screen_width // 144
        y_offset = 43 * self.main.screen_height // 144
        points = [
            (7 * length // 32, length // 16),
            (17 * length // 32, length // 16),
            (length // 16, 3 * length // 8),
            (3 * length // 8, 3 * length // 8),
            (11 * length // 16, 3 * length // 8)
        ]
        
        # Remove all selected colors
        while self.selected_colors:
            self.selected_colors[0].unselect()

        # Add selected colors in order
        i = 0
        for c in default_colors:
            for d in self.not_selected_colors:
                if d.color == c:
                    d.select()
                    break
            else:
                self.selected_colors.append(ColorDisplay(
                    self.main,
                    self,
                    c,
                    self.save_btn,
                    points[i][0] + x_offset,
                    points[i][1] + y_offset,
                    length // 4,
                    length // 4,
                    left_pos = i
                ))
                self.settings["colors"].append(c)

            i += 1

        self.save_btn.setText("Save Current Settings")

    def rgb_to_hex(self, color):
        return "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])

    def show(self):
        self.scroller.show()
        self.choose_panel.show()
        self.choose_text.show()
        self.selected_panel.show()
        self.selected_text.show()
        self.custom_color_btn.show()
        self.reset.show()
        for wid in self.selected_colors:
            wid.show()
        for wid in self.not_selected_colors:
            wid.show()
        for wid in self.selection_borders:
            wid.show()
        
    def __init__(self, main, settings, save_btn, tooltips):

        self.main = main
        self.settings = settings
        self.save_btn = save_btn
        self.color_dialogue = None
        self.not_selected_colors = []
        length = 7 * main.screen_width // 64

        # Choose Panel
        self.choose_panel = QWidget(
            parent = main.central_widget,
            geometry = QRect(133 * main.screen_width // 192, 43 * main.screen_height // 144, 43 * main.screen_width // 192, ceil(len(self.not_selected_colors) / 6) * 5 * length // 16)
        )
        self.choose_panel.show()

        # Scroller for custom colors
        self.scroller = QScrollArea(
            parent = main.central_widget,
            verticalScrollBarPolicy = Qt.ScrollBarPolicy.ScrollBarAlwaysOn,
            horizontalScrollBarPolicy = Qt.ScrollBarPolicy.ScrollBarAlwaysOff,
            geometry = QRect(133 * main.screen_width // 192, 43 * main.screen_height // 144, 43 * main.screen_width // 192, 77 * main.screen_height // 576),
            styleSheet = "QScrollArea {border: 2px inset gray;}"
        )
        self.scroller.setWidget(self.choose_panel)
        self.scroller.show()

        # Draw existing custom colors
        i = 0
        for color in self.settings["custom_colors"]:
            self.place_custom_color(color, i)
            i += 1

        # Selected Panel
        self.selected_panel = QLabel(
            parent = main.central_widget,
            geometry = QRect(83 * main.screen_width // 144, 43 * main.screen_height // 144, 7 * main.screen_width // 64, 77 * main.screen_height // 576),
            styleSheet = "border: 2px inset gray;"
        )
        self.selected_panel.show()

        # Selected Text
        self.selected_text = QLabel(
            parent = main.central_widget,
            text = "Current Colors",
            font = QFont("Trebuchet MS", main.screen_height // 90),
            geometry = QRect(83 * main.screen_width // 144, 7 * main.screen_height // 16, 7 * main.screen_width // 64, main.screen_height // 30),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.selected_text.show()

        # Choose Text
        self.choose_text = QLabel(
            parent = main.central_widget,
            text = "Choose Colors",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(83 * main.screen_width // 144, 35 * main.screen_height // 144, 49 * main.screen_width // 144, main.screen_height // 18),
            alignment = Qt.AlignmentFlag.AlignCenter,
            toolTip = tooltips["choose_color"]
        )
        self.choose_text.show()

        # Custom color button
        self.custom_color_btn = Button(
            main = main,
            text = "Add Custom Color",
            font = QFont("Trebuchet MS", main.screen_height // 90),
            geometry = QRect(7 * main.screen_width // 10, 7 * main.screen_height // 16, main.screen_width // 10, main.screen_height // 30),
            connect = self.custom_color
        )
        self.custom_color_btn.show()

        # Reset button
        self.reset = Button(
            main = main,
            text = "Reset to Default Colors",
            font = QFont("Trebuchet MS", main.screen_height // 90),
            geometry = QRect(311 * main.screen_width // 384, 7 * main.screen_height // 16, main.screen_width // 10, main.screen_height // 30),
            connect = self.reset_colors
        )
        self.reset.show()

        # Selected colors locations
        x_offset = 83 * main.screen_width // 144
        y_offset = 43 * main.screen_height // 144
        points = [
            (7 * length // 32, length // 16),
            (17 * length // 32, length // 16),
            (length // 16, 3 * length // 8),
            (3 * length // 8, 3 * length // 8),
            (11 * length // 16, 3 * length // 8)
        ]

        # Borders for selected colors
        self.selection_borders = []
        for i in range(5):
            self.selection_borders.append(QWidget(
                main.central_widget,
                geometry = QRect(points[i][0] + x_offset, points[i][1] + y_offset, length // 4, length // 4),
                styleSheet = "border: 2px outset gray;"
            ))
            self.selection_borders[i].show()
  
        # Create labels for the selected colors
        self.selected_colors = []
        for i in range(5):
            self.selected_colors.append(ColorDisplay(
                main,
                self,
                self.settings["colors"][i],
                self.save_btn,
                points[i][0] + x_offset,
                points[i][1] + y_offset,
                length // 4,
                length // 4,
                left_pos = i
            ))


class ColorDialogue(QColorDialog):

    def closeEvent(self, event):
        self.color_select.color_dialogue = None
        return super().closeEvent(event)

    def reject(self):
        self.color_select.color_dialogue = None
        return super().reject()
    
    def __init__(self, color_select):
        super().__init__(color_select.main.central_widget)
        self.color_select = color_select


class ColorDisplay(QLabel):

    def delete_color(self):

        # Remove from custom colors
        self.color_select.settings["custom_colors"].remove(self.color)
        self.color_select.not_selected_colors.remove(self)

        # Reorder existing colors
        length = 7 * self.main.screen_width // 64
        for color_display in self.color_select.not_selected_colors:
            if color_display.right_pos > self.right_pos:
                color_display.setGeometry(length // 16 + ((color_display.right_pos - 1) % 6) * 5 * length // 16, length // 16 + ((color_display.right_pos - 1) // 6) * 5 * length // 16, length // 4, length // 4)
                color_display.right_pos -= 1
                self.color_select.choose_panel.setGeometry(133 * self.main.screen_width // 192, 7 * self.main.screen_height // 36, 43 * self.main.screen_width // 192, ceil(len(self.color_select.not_selected_colors) / 6) * 5 * length // 16)
                self.color_select.scroller.takeWidget()
                self.color_select.scroller.setWidget(self.color_select.choose_panel)

        self.color_select.save_btn.setText("Save Current Settings")

        # Destroy all widgets
        self.delete_color_button.destroy()
        self.off_click_detect.destroy()
        self.destroy()

    def destroy(self):
        super().deleteLater()

    def mousePressEvent(self, event):

        # On left click, move to opposite side if able
        if event.button() == Qt.MouseButton.LeftButton:

            # If selected, unselect
            if self.left_pos != None:
                self.unselect()

            # If not selected and less than 5 colors selected, select
            elif len(self.color_select.selected_colors) < 5:
                self.select()
        
        # On right click, if not currently selected, create Delete button
        elif event.button() == Qt.MouseButton.RightButton and self.right_pos != None:
            self.off_click_detect = OffClickDetect(self.main, self)
            self.delete_color_button = DeleteColorButton(self.main)
            self.delete_color_button.clicked.connect(self.delete_color)

    def select(self):
        length = 7 * self.main.screen_width // 64
        x_offset = 83 * self.main.screen_width // 144
        y_offset = 43 * self.main.screen_height // 144
        points = [
            (7 * length // 32, length // 16),
            (17 * length // 32, length // 16),
            (length // 16, 3 * length // 8),
            (3 * length // 8, 3 * length // 8),
            (11 * length // 16, 3 * length // 8)
        ]

        # Change parent widget
        self.setParent(self.main.central_widget)
        self.show()

        # Find first instance of empty space in selected colors
        positions = [color.left_pos for color in self.color_select.selected_colors]
        for i in range(5):
            if i not in positions:

                # Update position values
                p = self.right_pos
                self.right_pos = None
                self.left_pos = i

                # Change assigned list
                self.color_select.selected_colors.insert(i, self)
                self.color_select.not_selected_colors.remove(self)

                # Use new position value to change placement
                self.setGeometry(points[i][0] + x_offset, points[i][1] + y_offset, length // 4, length // 4)

                # Update settings
                self.color_select.settings["colors"].insert(i, self.color)
                self.color_select.settings["custom_colors"].remove(self.color)
                
                # Reorder existing not selected colors
                for color_display in self.color_select.not_selected_colors:
                    if color_display.right_pos > p:
                        color_display.setGeometry(length // 16 + ((color_display.right_pos - 1) % 6) * 5 * length // 16, length // 16 + ((color_display.right_pos - 1) // 6) * 5 * length // 16, length // 4, length // 4)
                        color_display.right_pos -= 1
                        self.color_select.choose_panel.setGeometry(133 * self.main.screen_width // 192, 7 * self.main.screen_height // 36, 43 * self.main.screen_width // 192, ceil(len(self.color_select.not_selected_colors) / 6) * 5 * length // 16)
                        self.color_select.scroller.takeWidget()
                        self.color_select.scroller.setWidget(self.color_select.choose_panel)

                self.save_btn.setText("Save Current Settings")

                break

    def unselect(self):

        # Change parent widget
        self.setParent(self.color_select.choose_panel)
        self.show()
        
        # Update position values
        i = len(self.color_select.not_selected_colors)
        self.right_pos = i
        self.left_pos = None

        # Change assigned list
        self.color_select.selected_colors.remove(self)
        self.color_select.not_selected_colors.append(self)

        # Update settings
        self.color_select.settings["colors"].remove(self.color)
        self.color_select.settings["custom_colors"].append(self.color)

        # Update position
        length = 7 * self.main.screen_width // 64
        self.setGeometry(length // 16 + (i % 6) * 5 * length // 16, length // 16 + (i // 6) * 5 * length // 16, length // 4, length // 4)
        self.color_select.choose_panel.setGeometry(133 * self.main.screen_width // 192, 7 * self.main.screen_height // 36, 43 * self.main.screen_width // 192, ceil(len(self.color_select.not_selected_colors) / 6) * 5 * length // 16)
        self.color_select.scroller.takeWidget()
        self.color_select.scroller.setWidget(self.color_select.choose_panel)

        self.save_btn.setText("Save Current Settings")

    def __init__(self, main, color_select, color, save_btn, x, y, w, h, left_pos = None, right_pos = None):

        # Custom colors are children of the scroll area
        if right_pos != None:
            super().__init__(color_select.choose_panel)

        # Selected colors are children of the main window
        else:
            super().__init__(main.central_widget)
        self.main = main
        self.color_select = color_select
        self.color = color
        self.save_btn = save_btn
        self.left_pos = left_pos
        self.right_pos = right_pos
        self.setStyleSheet(f"background-color: {color}")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setGeometry(x, y, w, h)
        self.show()


class DeleteColorButton(Button):

    def destroy(self):
        super().deleteLater()

    def __init__(self, main):
        cursor_pos = main.central_widget.mapFromGlobal(QCursor.pos())
        super().__init__(
            main,
            text = "Delete Color",
            font = QFont("Trebuchet MS", main.screen_height // 90),
            geometry = QRect(cursor_pos.x(), cursor_pos.y() - main.screen_height // 30, main.screen_width // 18, main.screen_height // 30)
        )
        self.show()


class OffClickDetect(QWidget):

    def destroy(self):
        super().deleteLater()

    def mousePressEvent(self, event):
        self.destroy()
        self.color_display.delete_color_button.destroy()

    def __init__(self, main, color_display):
        super().__init__(main.central_widget)
        self.color_display = color_display
        self.setGeometry(0, 0, main.screen_width, main.screen_height)
        self.show()