from math import ceil
from PyQt6.QtCore import QPoint, QRect, Qt
from PyQt6.QtGui import QBrush, QColor, QCursor, QFont, QPainter, QPen, QPolygon
from PyQt6.QtWidgets import QLabel, QScrollArea, QWidget
from ui import Button


class ShapeSelect:

    def destroy(self):
        self.scroller.deleteLater()
        self.choose_panel.deleteLater()
        self.choose_text.deleteLater()
        self.selected_panel.deleteLater()
        self.selected_text.deleteLater()
        self.reset.deleteLater()
        for wid in self.selected_shapes:
            wid.deleteLater()
        for wid in self.not_selected_shapes:
            wid.deleteLater()
        for wid in self.selection_borders:
            wid.deleteLater()

    def hide(self):
        self.scroller.hide()
        self.choose_panel.hide()
        self.choose_text.hide()
        self.selected_panel.hide()
        self.selected_text.hide()
        self.reset.hide()
        for wid in self.selected_shapes:
            wid.hide()
        for wid in self.not_selected_shapes:
            wid.hide()
        for wid in self.selection_borders:
            wid.hide()

    def place_shape(self, shape, i):
        length = 7 * self.main.screen_width // 64

        self.not_selected_shapes.append(ShapeDisplay(
            self.main,
            self,
            shape,
            self.save_btn,
            length // 16 + (i % 6) * 5 * length // 16,
            length // 16 + (i // 6) * 5 * length // 16,
            length // 4,
            length // 4,
            right_pos = i
        ))
        self.choose_panel.setGeometry(133 * self.main.screen_width // 192, 7 * self.main.screen_height // 12, 43 * self.main.screen_width // 192, ceil(len(self.not_selected_shapes) / 6) * 5 * length // 16)
        self.scroller.takeWidget()
        self.scroller.setWidget(self.choose_panel)

    def reset_shapes(self):
        default_shapes = ["circle", "square", "triangle", "diamond", "hourglass"]
        length = 7 * self.main.screen_width // 64
        x_offset = 83 * self.main.screen_width // 144
        y_offset = 7 * self.main.screen_height // 12
        points = [
            (7 * length // 32, length // 16),
            (17 * length // 32, length // 16),
            (length // 16, 3 * length // 8),
            (3 * length // 8, 3 * length // 8),
            (11 * length // 16, 3 * length // 8)
        ]
        
        # Remove all selected shapes
        while self.selected_shapes:
            self.selected_shapes[0].unselect()

        # Add selected shapes in order
        i = 0
        for c in default_shapes:
            for d in self.not_selected_shapes:
                if d.shape == c:
                    d.select()
                    break
            else:
                self.selected_shapes.append(ShapeDisplay(
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
                self.settings["selected_shapes"].append(c)

            i += 1

        self.save_btn.setText("Save Current Settings")

    def show(self):
        self.scroller.show()
        self.choose_panel.show()
        self.choose_text.show()
        self.selected_panel.show()
        self.selected_text.show()
        self.reset.show()
        for wid in self.selected_shapes:
            wid.show()
        for wid in self.not_selected_shapes:
            wid.show()
        for wid in self.selection_borders:
            wid.show()
        
    def __init__(self, main, settings, save_btn, tooltips):

        self.main = main
        self.settings = settings
        self.save_btn = save_btn
        self.not_selected_shapes = []
        length = 7 * main.screen_width // 64

        # Choose Panel
        self.choose_panel = QWidget(
            parent = main.central_widget,
            geometry = QRect(133 * self.main.screen_width // 192, 7 * self.main.screen_height // 12, 43 * self.main.screen_width // 192, ceil(len(self.not_selected_shapes) / 6) * 5 * length // 16)
        )
        self.choose_panel.show()

        # Scroller for custom shapes
        self.scroller = QScrollArea(
            parent = main.central_widget,
            verticalScrollBarPolicy = Qt.ScrollBarPolicy.ScrollBarAlwaysOn,
            horizontalScrollBarPolicy = Qt.ScrollBarPolicy.ScrollBarAlwaysOff,
            styleSheet = "QScrollArea {border: 2px inset gray;}",
            geometry = QRect(133 * main.screen_width // 192, 7 * main.screen_height // 12, 43 * main.screen_width // 192, 77 * main.screen_height // 576)
        )
        self.scroller.setWidget(self.choose_panel)
        self.scroller.show()

        # Draw not selected shapes
        i = 0
        for shape in self.settings["not_selected_shapes"]:
            self.place_shape(shape, i)
            i += 1

        # Selected Panel
        self.selected_panel = QLabel(
            parent = main.central_widget,
            styleSheet = "border: 2px inset gray;",
            geometry = QRect(83 * main.screen_width // 144, 7 * main.screen_height // 12, 7 * main.screen_width // 64, 77 * main.screen_height // 576)
        )
        self.selected_panel.show()

        # Selected Text
        self.selected_text = QLabel(
            parent = main.central_widget,
            text = "Current Shapes",
            font = QFont("Trebuchet MS", main.screen_height // 90),
            geometry = QRect(83 * main.screen_width // 144, 13 * main.screen_height // 18, 7 * main.screen_width // 64, main.screen_height // 30),
            alignment = Qt.AlignmentFlag.AlignCenter
        )
        self.selected_text.show()

        # Choose Text
        self.choose_text = QLabel(
            parent = main.central_widget,
            text = "Choose Shapes",
            font = QFont("Trebuchet MS", main.screen_height // 60),
            geometry = QRect(83 * main.screen_width // 144, 19 * main.screen_height // 36, 49 * main.screen_width // 144, main.screen_height // 18),
            alignment = Qt.AlignmentFlag.AlignCenter,
            toolTip = tooltips["choose_shape"]
        )
        self.choose_text.show()

        # Reset button
        self.reset = Button(
            main = main,
            text = "Reset to Default Shapes",
            font = QFont("Trebuchet MS", main.screen_height // 90),
            geometry = QRect(483 * main.screen_width // 640, 13 * main.screen_height // 18, main.screen_width // 10, main.screen_height // 30),
            connect = self.reset_shapes
        )
        self.reset.show()

        # Selected shapes locations
        x_offset = 83 * main.screen_width // 144
        y_offset = 7 * main.screen_height // 12
        points = [
            (7 * length // 32, length // 16),
            (17 * length // 32, length // 16),
            (length // 16, 3 * length // 8),
            (3 * length // 8, 3 * length // 8),
            (11 * length // 16, 3 * length // 8)
        ]

        # Borders for selected shapes
        self.selection_borders = []
        for i in range(5):
            self.selection_borders.append(QWidget(
                main.central_widget,
                geometry = QRect(points[i][0] + x_offset, points[i][1] + y_offset, length // 4, length // 4),
                styleSheet = "border: 2px outset gray;"
            ))
            self.selection_borders[i].show()
  
        # Create labels for the selected shapes
        self.selected_shapes = []
        for i in range(5):
            self.selected_shapes.append(ShapeDisplay(
                main,
                self,
                self.settings["selected_shapes"][i],
                self.save_btn,
                points[i][0] + x_offset,
                points[i][1] + y_offset,
                length // 4,
                length // 4,
                left_pos = i
            ))


class ShapeDisplay(QLabel):

    def destroy(self):
        super().deleteLater()

    def mousePressEvent(self, event):

        # On left click, move to opposite side if able
        if event.button() == Qt.MouseButton.LeftButton:

            # If selected, unselect
            if self.left_pos != None:
                self.unselect()

            # If not selected and less than 5 shapes selected, select
            elif len(self.shape_select.selected_shapes) < 5:
                self.select()

    def paintEvent(self, event):

        # Initialize painter
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Configure pen and brush
        pen = QPen()
        brush = QBrush()
        length = 7 * self.main.screen_width // 256
        pen.setWidth(length // 60)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)

        # Set Color
        pen.setColor(QColor("#000000"))
        brush.setColor(QColor("#000000"))

        # Set Fill
        brush.setStyle(Qt.BrushStyle.SolidPattern)

        # Draw Shape
        qp.setPen(pen)
        qp.setBrush(brush)

        match self.shape:
            case "square":
                qp.drawRect(0, 0, length, length)
                qp.fillRect(QRect(0, 0, length, length), brush)

            case "diamond":
                qp.drawPolygon(QPolygon([
                    QPoint(0, length // 2),
                    QPoint(length // 2, 0),
                    QPoint(length, length // 2),
                    QPoint(length // 2, length)
                ]))
                    
            case "triangle":
                qp.drawPolygon(QPolygon([
                    QPoint(0, length),
                    QPoint(length // 2, 0),
                    QPoint(length, length)
                ]))
                    
            case "circle":
                qp.drawEllipse(0, 0, length, length)

            case "hourglass":
                qp.drawPolygon(QPolygon([
                    QPoint(0, 0),
                    QPoint(length, 0),
                    QPoint(0, length),
                    QPoint(length, length)
                ]))
                    
            case "plus":
                qp.drawPolygon(QPolygon([
                    QPoint(length // 3, 0),
                    QPoint(2 * length // 3, 0),
                    QPoint(2 * length // 3, length // 3),
                    QPoint(length, length // 3),
                    QPoint(length, 2 * length // 3),
                    QPoint(2 * length // 3, 2 * length // 3),
                    QPoint(2 * length // 3, length),
                    QPoint(length // 3, length),
                    QPoint(length // 3, 2 * length // 3),
                    QPoint(0, 2 * length // 3),
                    QPoint(0, length // 3),
                    QPoint(length // 3, length // 3)
                ]))
                    
            case "bowtie":
                qp.drawPolygon(QPolygon([
                    QPoint(0, 0),
                    QPoint(0, length),
                    QPoint(length, 0),
                    QPoint(length, length)
                ]))
                
            case "cross":
                qp.drawPolygon(QPolygon([
                    QPoint(0, 0),
                    QPoint(length // 2, length // 4),
                    QPoint(length, 0),
                    QPoint(3 * length // 4, length // 2),
                    QPoint(length, length),
                    QPoint(length // 2, 3 * length // 4),
                    QPoint(0, length),
                    QPoint(length // 4, length // 2)
                ]))

        # End paint event
        qp.end()

    def select(self):
        length = 7 * self.main.screen_width // 64
        x_offset = 83 * self.main.screen_width // 144
        y_offset = 7 * self.main.screen_height // 12
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

        # Find first instance of empty space in selected shapes
        positions = [shape.left_pos for shape in self.shape_select.selected_shapes]
        for i in range(5):
            if i not in positions:

                # Update position values
                p = self.right_pos
                self.right_pos = None
                self.left_pos = i

                # Change assigned list
                self.shape_select.selected_shapes.insert(i, self)
                self.shape_select.not_selected_shapes.remove(self)

                # Use new position value to change placement
                self.setGeometry(points[i][0] + x_offset, points[i][1] + y_offset, length // 4, length // 4)

                # Update settings
                self.shape_select.settings["selected_shapes"].insert(i, self.shape)
                self.shape_select.settings["not_selected_shapes"].remove(self.shape)
                
                # Reorder existing not selected shapes
                for shape_display in self.shape_select.not_selected_shapes:
                    if shape_display.right_pos > p:
                        shape_display.setGeometry(length // 16 + ((shape_display.right_pos - 1) % 6) * 5 * length // 16, length // 16 + ((shape_display.right_pos - 1) // 6) * 5 * length // 16, length // 4, length // 4)
                        shape_display.right_pos -= 1
                        self.shape_select.choose_panel.setGeometry(133 * self.main.screen_width // 192, 7 * self.main.screen_height // 12, 43 * self.main.screen_width // 192, ceil(len(self.shape_select.not_selected_shapes) / 6) * 5 * length // 16)
                        self.shape_select.scroller.takeWidget()
                        self.shape_select.scroller.setWidget(self.shape_select.choose_panel)

                self.save_btn.setText("Save Current Settings")

                break

    def unselect(self):

        # Change parent widget
        self.setParent(self.shape_select.choose_panel)
        self.show()
        
        # Update position values
        i = len(self.shape_select.not_selected_shapes)
        self.right_pos = i
        self.left_pos = None

        # Change assigned list
        self.shape_select.selected_shapes.remove(self)
        self.shape_select.not_selected_shapes.append(self)

        # Update settings
        self.shape_select.settings["selected_shapes"].remove(self.shape)
        self.shape_select.settings["not_selected_shapes"].append(self.shape)

        # Update position
        length = 7 * self.main.screen_width // 64
        self.setGeometry(length // 16 + (i % 6) * 5 * length // 16, length // 16 + (i // 6) * 5 * length // 16, length // 4, length // 4)
        self.shape_select.choose_panel.setGeometry(133 * self.main.screen_width // 192, 7 * self.main.screen_height // 12, 43 * self.main.screen_width // 192, ceil(len(self.shape_select.not_selected_shapes) / 6) * 5 * length // 16)
        self.shape_select.scroller.takeWidget()
        self.shape_select.scroller.setWidget(self.shape_select.choose_panel)

        self.save_btn.setText("Save Current Settings")

    def __init__(self, main, shape_select, shape, save_btn, x, y, w, h, left_pos = None, right_pos = None):

        # Custom shapes are children of the scroll area
        if right_pos != None:
            super().__init__(shape_select.choose_panel)

        # Selected shapes are children of the main window
        else:
            super().__init__(main.central_widget)
            
        self.main = main
        self.shape_select = shape_select
        self.shape = shape
        self.save_btn = save_btn
        self.left_pos = left_pos
        self.right_pos = right_pos
        self.setGeometry(x, y, w, h)
        self.setStyleSheet("border: 2px outset gray;")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.show()