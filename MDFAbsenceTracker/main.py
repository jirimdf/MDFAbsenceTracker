import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMainWindow, QGridLayout
from PyQt5.QtGui import QFont, QFontDatabase, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
import os


class CustomButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFixedSize(200, 50)
        self.setStyleSheet(
            """
            QPushButton {
                background-color: #FF0000;
                color: #FFFFFF;
                border-radius: 25px;
                border: 2px solid #000000;
            }
            QPushButton:hover {
                background-color: #990000;
            }
            QPushButton:pressed {
                background-color: #660000;
            }
            """
        )

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setGeometry(300, 300, 220, 50)

        self.max_percent_label = QLabel("Max % absence:", self)
        self.max_percent_input = QLineEdit(self)
        self.max_percent_input.setText("25")
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_settings)

        layout = QVBoxLayout()
        layout.addWidget(self.max_percent_label)
        layout.addWidget(self.max_percent_input)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def save_settings(self):
        try:
            max_percent = int(self.max_percent_input.text())
            if 0 <= max_percent <= 100:
                self.save_settings_to_file(max_percent)
                print(f"Saved: The maximum percentage of absent is now {max_percent}%.")
                self.update_main_window(max_percent)
                self.update_main_window(max_percent)
                self.close()
            else:
                print("Error: Please enter a number between 0 and 100.")
        except ValueError:
            print("Error: Please enter a whole number.")

    def update_main_window(self, max_percent):
        main_window = QApplication.instance().activeWindow()
        if isinstance(main_window, MainWindow):
            main_window.update_max_percent(max_percent)

    def save_settings_to_file(self, max_percent):
        with open("settings.txt", "w") as file:
            file.write(str(max_percent))

    def load_settings_from_file(self):
        try:
            with open("settings.txt", "r") as file:
                max_percent = int(file.read())
                self.max_percent_input.setText(str(max_percent))
                self.update_main_window(max_percent)
        except FileNotFoundError:
            self.max_percent_input.setText("25")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.create_settings_file_if_not_exists()

        QFontDatabase.addApplicationFont("Azonix.otf")
        QFontDatabase.addApplicationFont("FredokaOne-Regular.otf")

        self.setWindowIcon(QIcon("logo.png"))

        window_width = 400
        window_height = 450

        self.setMinimumSize(window_width, window_height)
        self.setMaximumSize(window_width, window_height)

        pixmap = QPixmap("background.jpg").scaled(window_width, window_height)
        background_label = QLabel(self)
        background_label.setPixmap(pixmap)
        background_label.resize(window_width, window_height)

        self.overlay = QWidget(self)
        self.overlay.setGeometry(0, 0, window_width, window_height)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 50);")
        self.title_label = QLabel("MDF Absence", self)
        self.title_label.setFont(QFont("Azonix", 23))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #FFFFFF;")
        self.total_hours_label = QLabel("Total hours:", self)
        self.total_hours_label.setFont(QFont("Fredoka One", 11))
        self.total_hours_label.setStyleSheet("color: #FFFFFF;")
        self.total_hours_input = QLineEdit(self)
        self.total_hours_input.setStyleSheet("background-color: #333333; color: #FFFFFF; border: 2px solid #FFFFFF; border-radius: 10px; padding: 5px;")


        self.absent_hours_label = QLabel("Hours of absence:", self)
        self.absent_hours_label.setFont(QFont("Fredoka One", 11))
        self.absent_hours_label.setStyleSheet("color: #FFFFFF;")
        self.absent_hours_input = QLineEdit(self)
        self.absent_hours_input.setStyleSheet("background-color: #333333; color: #FFFFFF; border: 2px solid #FFFFFF; border-radius: 10px; padding: 5px;")

        self.calculate_button = CustomButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_percent)

        self.result_label = QLabel(self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("color: #FFFFFF; font-size: 14px;")

        self.additional_result_label = QLabel(self)
        self.additional_result_label.setAlignment(Qt.AlignCenter)
        self.additional_result_label.setStyleSheet("color: #FFFFFF; font-size: 14px;")

        self.third_result_label = QLabel(self)
        self.third_result_label.setAlignment(Qt.AlignCenter)
        self.third_result_label.setStyleSheet("color: #FFFFFF; font-size: 14px;")

        self.settings_button = QPushButton(self)
        self.settings_button.setIcon(QIcon("settings.png"))
        self.settings_button.setIconSize(QSize(20, 20))
        self.settings_button.setFixedSize(30, 30)
        self.settings_button.setStyleSheet(
            """
            background-color: transparent;
            border: none;
            """
        )
        self.settings_button.clicked.connect(self.show_settings)

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.total_hours_label)
        layout.addWidget(self.total_hours_input)
        layout.addWidget(self.absent_hours_label)
        layout.addWidget(self.absent_hours_input)

        self.future_absent_hours_label = QLabel("Planning to miss:", self)
        self.future_absent_hours_label.setFont(QFont("Fredoka One", 11))
        self.future_absent_hours_label.setStyleSheet("color: #FFFFFF;")
        self.future_absent_hours_input = QLineEdit(self)
        self.future_absent_hours_input.setStyleSheet("background-color: #333333; color: #FFFFFF; border: 2px solid #FFFFFF; border-radius: 10px; padding: 5px;")

        layout.addWidget(self.future_absent_hours_label)
        layout.addWidget(self.future_absent_hours_input)
        layout.addWidget(self.calculate_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.result_label)
        layout.addWidget(self.additional_result_label)
        layout.addWidget(self.third_result_label)

        grid_layout = QGridLayout()
        grid_layout.addLayout(layout, 0, 0, Qt.AlignTop)
        grid_layout.addWidget(self.settings_button, 1, 0, Qt.AlignRight | Qt.AlignBottom)

        container = QWidget()
        container.setLayout(grid_layout)
        self.setCentralWidget(container)
        self.setWindowTitle("MDF absence calculator")
        self.setGeometry(100, 100, window_width, window_height)

    def calculate_percent(self):
        try:
            total_hours = int(self.total_hours_input.text())
            absent_hours = int(self.absent_hours_input.text())
            future_absent_hours = int(self.future_absent_hours_input.text())

            if total_hours < 0 or absent_hours < 0 or future_absent_hours < 0:
                raise ValueError

            if hasattr(self, 'settings_window') and self.settings_window is not None:
                max_percent = int(self.settings_window.max_percent_input.text())
            else:
                max_percent = 25

            max_absent_hours = total_hours * (int(max_percent) / 100)
            remaining_hours = max(0, max_absent_hours - absent_hours - future_absent_hours)
            rounded_max_absent_hours = round(remaining_hours)

            percent = (absent_hours / total_hours) * 100
            rounded_percent = round(percent, 2)

            total_hours_with_future_absent = total_hours + future_absent_hours
            future_percent = ((absent_hours + future_absent_hours) / total_hours_with_future_absent) * 100
            rounded_future_percent = round(future_percent, 2)

            max_hours_text = f"The maximum hours you can miss is: {rounded_max_absent_hours}"
            current_absence_text = f"Current absence: {rounded_percent}%"
            future_percent_text = f"After planned absence: {rounded_future_percent}%"
            self.result_label.setText(max_hours_text + "\n" + current_absence_text + "\n" + future_percent_text)

        except ValueError:
            self.result_label.setText("Error: Please enter a positive whole number.")

    def show_settings(self):
        self.settings_window = SettingsWindow()
        self.settings_window.load_settings_from_file()
        self.settings_window.show()

    def create_settings_file_if_not_exists(self):
        if not os.path.exists("settings.txt"):
            with open("settings.txt", "w") as file:
                file.write("25")

    def update_max_percent(self, max_percent):
        self.settings_window.max_percent_input.setText(str(max_percent))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
