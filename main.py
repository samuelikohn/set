from challenges import Challenges
from ctypes import windll
from json import dump, load
from main_menu import MainMenu
from PyQt6.QtCore import QEvent, QObject, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from time_trial_page import TimeTrialPage

# Project stuffs
    # technical info and game features in README
    # screenshots/video demo


class Main:

    def go_to_challenges_page(self):
        self.challenges_page = Challenges(self)

    def go_to_main_menu(self):
        self.main_menu = MainMenu(self)

    def go_to_time_trial_page(self):
        self.time_trial_page = TimeTrialPage(self)

    def is_valid_settings(self, key, val, selected_shapes):

        all_shapes = ["circle", "square", "triangle", "diamond", "hourglass", "bowtie", "cross", "plus"]

        match key:
            case "num_traits":
                return val in [3, 4, 5]
            case "num_variations":
                return val in [3, 4, 5]
            case "selection_delay":
                return val in range(11)
            case "ai_difficulty":
                return val in [2, 1.5, 1, 0.5]
            case "show_num_sets":
                return val in [True, False]
            case "show_cards_left_in_deck":
                return val in [True, False]
            case "time_format":
                return val in ["numeric", "text", "raw"]
            case "enable_hints":
                return val in [True, False]
            case "accent_color":
                return self.validate_hex_code(val)
            case "colors":
                return isinstance(val, list) and len(val) == 5 and len(set(val)) == 5 and all(self.validate_hex_code(hex_code) for hex_code in val)
            case "custom_colors":
                return isinstance(val, list) and len(val) == len(set(val)) and all(self.validate_hex_code(hex_code) for hex_code in val)
            case "selected_shapes":
                return isinstance(val, list) and len(val) == 5 and len(set(val)) == 5 and all(shape in all_shapes for shape in val)
            case "not_selected_shapes":
                return isinstance(val, list) and len(val) == len(all_shapes) - 5 and len(set(val)) == len(all_shapes) - 5 and all(shape in set(all_shapes) - set(selected_shapes) for shape in val)

    def is_valid_times(self, val):

        # Time must be stored as a list, empty list is valid
        if not isinstance(val, list) or not val:
            return []
        
        # Times must only be positive ints
        i = 0
        while i < len(val):
            if isinstance(val[i], int) and val[i] > 0:
                i += 1
            else:
                val.pop(i)

        # Times must be sorted, max of 10
        val.sort()
        if len(val) > 10:
            val = val[:10]

        return val
    
    def load_settings(self):

        default_settings = {
            "num_traits": 4,
            "num_variations": 3,
            "selection_delay": 3,
            "ai_difficulty": 1.5,
            "show_num_sets": False,
            "show_cards_left_in_deck": False,
            "time_format": "numeric",
            "enable_hints": False,
            "accent_color": "#d9b9eb",
            "colors": [
                "#ea1c2d",
                "#14a750",
                "#662d91",
                "#1672f4",
                "#f8c326"
            ],
            "custom_colors": [],
            "selected_shapes": [
                "circle",
                "square",
                "triangle",
                "diamond",
                "hourglass"
            ],
            "not_selected_shapes": [
                "bowtie",
                "cross",
                "plus"
            ]
        }

        # Load from file
        try:
            with open('settings.json') as f:
                settings = load(f)

        # Replace with default settings if can't load
        except:
            settings = default_settings

        else:

            # If valid format, validate settings
            if isinstance(settings, dict):

                keys_to_remove = []
                for key in settings.keys():

                    # All keys must represent settings that exist
                    if key not in default_settings.keys():
                        keys_to_remove.append(key)

                    # All values must respresent valid values
                    elif not self.is_valid_settings(key, settings[key], settings["selected_shapes"]):
                        settings[key] = default_settings[key]

                # Remove invalid keys
                for key in keys_to_remove:
                    settings.pop(key, None)
                
                # All settings must be present
                for key in default_settings.keys():
                    if key not in settings.keys():
                        settings[key] = default_settings[key]

            # Replace with default settings if not valid format
            else:
                settings = default_settings

        self.settings = settings
        with open("settings.json", "w") as f:
            dump(self.settings, f, indent = 4)

    def load_times(self):

        default_times = {f"{mode}_{t}{v}": [] for mode in ["time_trial", "static", "recycle", "xl", "xs"] for t in [3, 4, 5] for v in [3, 4, 5]}

        # Load from file
        try:
            with open('times.json') as f:
                times = load(f)

        # Reset times if can't load
        except:
            times = default_times

        else:

            # If valid format, validate times
            if isinstance(times, dict):

                keys_to_remove = []
                for key in times.keys():

                    # All keys must represent valid trait/variation combos
                    if key not in default_times:
                        keys_to_remove.append(key)

                    # All values must be sorted lists of positive ints with max length of 10
                    else:
                        times[key] = self.is_valid_times(times[key])

                # Remove invalid keys
                for key in keys_to_remove:
                    times.pop(key, None)
                
                # All trait/variation combos must be present
                for key in default_times:
                    if key not in times.keys():
                        times[key] = []

            # Reset times if invalid format
            else:
                times = default_times

        self.times = times
        with open("times.json", "w") as f:
            dump(self.times, f, indent = 4)

    def translate_time(self, time):

        # Calculate time units
        tenths = time % 10
        total_seconds = (time - tenths) // 10
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        if self.settings["time_format"] == "numeric":

            # Build the time string based on numerical values of units
            if hours > 0:
                time_str = f"{hours}:{minutes:02}:{seconds:02}.{tenths}"
            else:
                time_str = f"{minutes:02}:{seconds:02}.{tenths}"

        elif self.settings["time_format"] == "text":

            # Depluralize text when value is 1
            if hours == 1:
                h = "hour"
            else:
                h = "hours"

            if minutes == 1:
                m = "minute"
            else:
                m = "minutes"

            # Build the time string based on text values of units
            if hours > 0:
                time_str = f"{hours} {h}, {minutes} {m}, {seconds}.{tenths} seconds"
            elif minutes > 0:
                time_str = f"{minutes} {m}, {seconds}.{tenths} seconds"
            else:
                time_str = f"{seconds}.{tenths} seconds"

        elif self.settings["time_format"] == "raw":
            time_str = str(time)

        return time_str
    
    def validate_hex_code(self, hex_code):
        return hex_code[0] == "#" and len(hex_code) == 7 and all(hex_code[i] in "0123456789abcdef" for i in range(1, 7))

    def __init__(self):

        # Get screen dimensions for placing widgets
        self.screen_width = windll.user32.GetSystemMetrics(0)
        self.screen_height = windll.user32.GetSystemMetrics(1)

        self.board = None
        
        # Configure parent window
        self.app = QApplication([])
        self.app.installEventFilter(SpaceEventFilter(self))
        self.window = QMainWindow(
            windowTitle = "SET",
            styleSheet = "background-color: #f3eef6",
            windowIcon = QIcon("icon.png")
        )
        self.window.showFullScreen()

        # Set central widget
        self.central_widget = QWidget(self.window)
        self.window.setCentralWidget(self.central_widget)

        # Load settings from file, replace any invalid settings with default values
        self.load_settings()

        # Load times from file, clear any invalid times
        self.load_times()

        # Init pages
        self.settings_page = None
        self.time_trial_page = None
        self.tutorial_page = None
        self.challenges_page = None
        self.go_to_main_menu()
        

# Hijack space bar press when board is active to trigger "Call SET" action
class SpaceEventFilter(QObject):
    
    def eventFilter(self, obj, event):
        if self.main.board and event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Space:
            self.main.board.call_set_btn.click()
            return True
        return super().eventFilter(obj, event)
    
    def __init__(self, main):
        super().__init__(parent = main.app)
        self.main = main


# Run application
if __name__ == "__main__":
    main = Main()
    main.window.show()
    main.app.exec()