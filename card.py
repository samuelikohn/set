from math import ceil
from PyQt6.QtCore import QPoint, QRect, Qt
from PyQt6.QtGui import QBrush, QColor, QPainter, QPen, QPolygon
from PyQt6.QtWidgets import QWidget


class Card(QWidget):

    def calc_position(self):
        y_pos = self.card_pos % self.board.board_height
        x_pos = (self.card_pos - y_pos) // self.board.board_height

        cx = 369 * self.board.main.screen_width // 640 # Center of the gameplay area
        cy = 19 * self.board.main.screen_height // 36

        width = ceil(len(self.board.current_board) / self.board.board_height) # Max cards per row in board

        w = self.board.card_length * width + (self.board.card_length // 20) * (width - 1)
        h = self.board.card_length * self.board.board_height + (self.board.card_length // 20) * (self.board.board_height - 1)

        x_coord = (cx - w // 2) + 21 * x_pos * self.board.card_length // 20
        y_coord = (cy - h // 2) + 21 * y_pos * self.board.card_length // 20

        self.setGeometry(x_coord, y_coord, self.board.card_length, self.board.card_length)

    def destroy(self):
        super().deleteLater()

    # On Click
    def mousePressEvent(self, event):

        # On left click, toggle card selection
        if self.board.mode == "ai":
            if not self.board.ai.in_selection and event.button() == Qt.MouseButton.LeftButton and self.board.call_set_btn.called and self.board.call_set_btn.time_left > 0:
                self.board.card_clicked(self, "player")
        elif event.button() == Qt.MouseButton.LeftButton and self.board.call_set_btn.called and self.board.call_set_btn.time_left > 0:
            self.board.card_clicked(self, "player")

        # On right click, toggle card marker
        if event.button() == Qt.MouseButton.RightButton:
            self.has_marker = not self.has_marker
            self.update()

    # Define shapes to draw on card
    def paintEvent(self, event):

        # Initialize painter
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background white square
        qp.fillRect(0, 0, self.board.card_length, self.board.card_length, QBrush(QColor(255, 255, 255)))
        
        # Configure pen and brush
        pen = QPen()
        brush = QBrush()
        pen.setWidth(self.board.card_length // 60)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)

        # Set Color
        pen.setColor(QColor(self.color))
        brush.setColor(QColor(self.color))

        # Set Fill
        match self.fill:
            case "solid":
                brush.setStyle(Qt.BrushStyle.SolidPattern)
            case "empty":
                brush.setStyle(Qt.BrushStyle.NoBrush)
            case "striped":
                brush.setStyle(Qt.BrushStyle.HorPattern)
            case "crossed":
                brush.setStyle(Qt.BrushStyle.DiagCrossPattern)
            case "dense":
                brush.setStyle(Qt.BrushStyle.Dense4Pattern)

        # Set Shape Positions Based on Number
        match self.number:
            case 1:
                points = [
                    (3 * self.board.card_length // 8, 3 * self.board.card_length // 8)
                ]
            case 2:
                points = [
                    (7 * self.board.card_length // 32, 3 * self.board.card_length // 8),
                    (17 * self.board.card_length // 32, 3 * self.board.card_length // 8)
                ]
            case 3:
                points = [
                    (3 * self.board.card_length // 8, 7 * self.board.card_length // 32),
                    (7 * self.board.card_length // 32, 17 * self.board.card_length // 32),
                    (17 * self.board.card_length // 32, 17 * self.board.card_length // 32)
                ]
            case 4:
                points = [
                    (7 * self.board.card_length // 32, 7 * self.board.card_length // 32),
                    (17 * self.board.card_length // 32, 7 * self.board.card_length // 32),
                    (7 * self.board.card_length // 32, 17 * self.board.card_length // 32),
                    (17 * self.board.card_length // 32, 17 * self.board.card_length // 32)
                ]
            case 5:
                points = [
                    (7 * self.board.card_length // 32, 7 * self.board.card_length // 32),
                    (17 * self.board.card_length // 32, 7 * self.board.card_length // 32),
                    (self.board.card_length // 16, 17 * self.board.card_length // 32),
                    (3 * self.board.card_length // 8, 17 * self.board.card_length // 32),
                    (11 * self.board.card_length // 16, 17 * self.board.card_length // 32)
                ]

        # Draw Shape
        qp.setPen(pen)
        qp.setBrush(brush)

        match self.shape:
            case "square":
                for point in points:
                    qp.drawRect(point[0], point[1], self.board.card_length // 4, self.board.card_length // 4)
                    qp.fillRect(QRect(point[0], point[1], self.board.card_length // 4, self.board.card_length // 4), brush)

            case "diamond":
                for point in points:
                    qp.drawPolygon(QPolygon([
                        QPoint(point[0], point[1] + self.board.card_length // 8),
                        QPoint(point[0] + self.board.card_length // 8, point[1]),
                        QPoint(point[0] + self.board.card_length // 4, point[1] + self.board.card_length // 8),
                        QPoint(point[0] + self.board.card_length // 8, point[1] + self.board.card_length // 4)
                    ]))
                    
            case "triangle":
                for point in points:
                    qp.drawPolygon(QPolygon([
                        QPoint(point[0], point[1] + self.board.card_length // 4),
                        QPoint(point[0] + self.board.card_length // 8, point[1]),
                        QPoint(point[0] + self.board.card_length // 4, point[1] + self.board.card_length // 4)
                    ]))
                    
            case "circle":
                for point in points:
                    qp.drawEllipse(point[0], point[1], self.board.card_length // 4, self.board.card_length // 4)

            case "hourglass":
                for point in points:
                    qp.drawPolygon(QPolygon([
                        QPoint(point[0], point[1]),
                        QPoint(point[0] + self.board.card_length // 4, point[1]),
                        QPoint(point[0], point[1] + self.board.card_length // 4),
                        QPoint(point[0] + self.board.card_length // 4, point[1] + self.board.card_length // 4)
                    ]))
                    
            case "plus":
                for point in points:
                    qp.drawPolygon(QPolygon([
                        QPoint(point[0] + self.board.card_length // 12, point[1]),
                        QPoint(point[0] + self.board.card_length // 6, point[1]),
                        QPoint(point[0] + self.board.card_length // 6, point[1] + self.board.card_length // 12),
                        QPoint(point[0] + self.board.card_length // 4, point[1] + self.board.card_length // 12),
                        QPoint(point[0] + self.board.card_length // 4, point[1] + self.board.card_length // 6),
                        QPoint(point[0] + self.board.card_length // 6, point[1] + self.board.card_length // 6),
                        QPoint(point[0] + self.board.card_length // 6, point[1] + self.board.card_length // 4),
                        QPoint(point[0] + self.board.card_length // 12, point[1] + self.board.card_length // 4),
                        QPoint(point[0] + self.board.card_length // 12, point[1] + self.board.card_length // 6),
                        QPoint(point[0], point[1] + self.board.card_length // 6),
                        QPoint(point[0], point[1] + self.board.card_length // 12),
                        QPoint(point[0] + self.board.card_length // 12, point[1] + self.board.card_length // 12)
                    ]))
                    
            case "bowtie":
                for point in points:
                    qp.drawPolygon(QPolygon([
                        QPoint(point[0], point[1]),
                        QPoint(point[0], point[1] + self.board.card_length // 4),
                        QPoint(point[0] + self.board.card_length // 4, point[1]),
                        QPoint(point[0] + self.board.card_length // 4, point[1] + self.board.card_length // 4)
                    ]))

            case "cross":
                for point in points:
                    qp.drawPolygon(QPolygon([
                        QPoint(point[0], point[1]),
                        QPoint(point[0] + self.board.card_length // 8, point[1] + self.board.card_length // 16),
                        QPoint(point[0] + self.board.card_length // 4, point[1]),
                        QPoint(point[0] + 3 * self.board.card_length // 16, point[1] + self.board.card_length // 8),
                        QPoint(point[0] + self.board.card_length // 4, point[1] + self.board.card_length // 4),
                        QPoint(point[0] + self.board.card_length // 8, point[1] + 3 * self.board.card_length // 16),
                        QPoint(point[0], point[1] + self.board.card_length // 4),
                        QPoint(point[0] + self.board.card_length // 16, point[1] + self.board.card_length // 8)
                    ]))
                
        # Draw corners
        match self.corner:
            case "none":
                pass
            case "top_left":
                qp.drawPolygon(QPolygon([
                    QPoint(0, 0),
                    QPoint(0, self.board.card_length // 4),
                    QPoint(self.board.card_length // 4, 0)
                ]))

            case "top_right":
                qp.drawPolygon(QPolygon([
                    QPoint(self.board.card_length, 0),
                    QPoint(3 * self.board.card_length // 4, 0),
                    QPoint(self.board.card_length, self.board.card_length // 4)
                ]))

            case "bottom_left":
                qp.drawPolygon(QPolygon([
                    QPoint(0, 3 * self.board.card_length // 4),
                        QPoint(0, self.board.card_length),
                        QPoint(self.board.card_length // 4, self.board.card_length)
                    ]))
                
            case "bottom_right":
                qp.drawPolygon(QPolygon([
                    QPoint(3 * self.board.card_length // 4, self.board.card_length),
                    QPoint(self.board.card_length, self.board.card_length),
                    QPoint(self.board.card_length, 3 * self.board.card_length // 4)
                ]))

        # Do not draw decorations on tutorial cards
        if str(type(self.board)) != "<class 'dummy.DummyBoard'>":

            # Draw Border
            if self.has_border:
                qp.setPen(QPen(QColor(self.shift_color_lightness(self.board.main.settings["accent_color"], -25)), 3))
                qp.setBrush(Qt.BrushStyle.NoBrush)
                qp.drawRect(self.rect().adjusted(1, 1, -1, -1))

            # Draw marker
            if self.has_marker:
                qp.setPen(QPen(QColor(0, 0, 0), 0))
                qp.setBrush(QBrush(QColor(0, 0, 0)))
                qp.drawPolygon(QPolygon([
                    QPoint(7 * self.board.card_length // 15, self.board.card_length // 9),
                    QPoint(22 * self.board.card_length // 45, 2 * self.board.card_length // 15),
                    QPoint(8 * self.board.card_length // 15, 4 * self.board.card_length // 45),
                    QPoint(19 * self.board.card_length // 36, self.board.card_length // 12),
                    QPoint(22 * self.board.card_length // 45, 11 * self.board.card_length // 90),
                    QPoint(17 * self.board.card_length // 36, 19 * self.board.card_length // 180)
                ]))

        # End paint event
        qp.end()

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
    
    def __lt__(self, other):
        
        all_properties = {
            "color": self.board.main.settings["colors"],
            "shape": self.board.main.settings["selected_shapes"],
            "number": [1, 2, 3, 4, 5],
            "fill": ["solid", "empty", "striped", "crossed", "dense"],
            "corner": ["none", "top_left", "top_right", "bottom_left", "bottom_right"]
        }

        for trait in all_properties:
            self_var = all_properties[trait].index(getattr(self, trait))
            other_var = all_properties[trait].index(getattr(other, trait))
            if self_var > other_var:
                return False
            elif self_var < other_var:
                return True
            
        return False

    def __init__(self, color, shape, number, fill, corner, card_pos, board, geometry = None):
        super().__init__(board.main.central_widget)
        self.board = board
        self.color = color
        self.shape = shape
        self.number = number
        self.fill = fill
        self.corner = corner
        self.has_border = False
        self.has_marker = False
        self.card_pos = card_pos

        if geometry:
            self.setGeometry(geometry)

        # Display card
        self.show()