# login.py
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QFormLayout, QHBoxLayout, QDialog, QComboBox
)
from PyQt5.QtGui import QFont, QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt
import pymysql

class SignupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("User Registration")
        self.setFixedSize(450, 500)

        self.setStyleSheet("""
            background-color: #00509d;
            border-radius: 15px;
        """)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Title
        title = QLabel("SIGN UP")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white;")

        # Form layout
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(15)

        input_style = "padding: 10px; background-color: white; border-radius: 8px;"

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name")
        self.name_input.setStyleSheet(input_style)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet(input_style)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(input_style)

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Age")
        self.age_input.setStyleSheet(input_style)

        self.gender_input = QComboBox()
        self.gender_input.addItems(["Select", "Male", "Female", "Other"])
        self.gender_input.setStyleSheet("padding: 10px; background-color: white; border-radius: 8px;")

        self.qualification_input = QLineEdit()
        self.qualification_input.setPlaceholderText("Qualification")
        self.qualification_input.setStyleSheet(input_style)

        form_layout.addRow(self.create_label("Full Name:"), self.name_input)
        form_layout.addRow(self.create_label("Username:"), self.username_input)
        form_layout.addRow(self.create_label("Password:"), self.password_input)
        form_layout.addRow(self.create_label("Age:"), self.age_input)
        form_layout.addRow(self.create_label("Gender:"), self.gender_input)
        form_layout.addRow(self.create_label("Qualification:"), self.qualification_input)

        # Register button
        self.submit_btn = QPushButton("Register")
        self.submit_btn.setCursor(Qt.PointingHandCursor)
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #38b000;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f7b801;
            }
        """)
        self.submit_btn.clicked.connect(self.accept)

        # Build layout
        main_layout.addWidget(title)
        main_layout.addSpacing(10)
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.submit_btn)

        self.setLayout(main_layout)

    def create_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("color: white; font-weight: bold;")
        return label

    def get_details(self):
        return {
            "name": self.name_input.text().strip(),
            "username": self.username_input.text().strip(),
            "password": self.password_input.text().strip(),
            "age": self.age_input.text().strip(),
            "gender": self.gender_input.currentText(),
            "qualification": self.qualification_input.text().strip()
        }

class LoginWindow(QWidget):
    def __init__(self,main_app):
        super().__init__()
        self.main_app = main_app
        self.setWindowTitle("Career Prediction Login")
        self.setWindowState(Qt.WindowMaximized)
        self.initUI()
        self.setBackground()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        card = QWidget()
        card.setStyleSheet("background-color:#00509d; border-radius: 15px; padding: 40px;")
        card_layout = QVBoxLayout()

        title = QLabel("LOGIN")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white;")

        form_layout = QFormLayout()
        self.username = QLineEdit()
        self.username.setPlaceholderText(" Username")
        self.username.setStyleSheet("padding: 10px; background-color: white; border-radius: 8px;")

        self.password = QLineEdit()
        self.password.setPlaceholderText(" Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("padding: 10px; background-color: white; border-radius: 8px;")

        form_layout.addRow(self.username)
        form_layout.addRow(self.password)

        self.login_btn = QPushButton("Login")
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #38b000;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f7b801;
            }
        """)

        self.signup_btn = QPushButton("Sign Up")
        self.signup_btn.setCursor(Qt.PointingHandCursor)
        self.signup_btn.setStyleSheet("""
            QPushButton {
                background-color: #e63946;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f7b801;
            }
        """)

        self.login_btn.clicked.connect(self.login)
        self.signup_btn.clicked.connect(self.signup)

        card_layout.addWidget(title)
        card_layout.addSpacing(10)
        card_layout.addLayout(form_layout)
        card_layout.addSpacing(20)
        card_layout.addWidget(self.login_btn)
        card_layout.addWidget(self.signup_btn)
        card.setLayout(card_layout)

        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(card)
        center_layout.addStretch()

        main_layout.addLayout(center_layout)
        self.setLayout(main_layout)

    def setBackground(self):
        bg_path = os.path.join(os.path.dirname(__file__), r"C:\Users\balac\Downloads\mini Project_Done\assert\back.jpg")
        if not os.path.exists(bg_path):
            print("⚠ Background image not found.")
            return
        pixmap = QPixmap(bg_path).scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.setBackground()

    def connect_db(self):
        return pymysql.connect(
            host="localhost", user="root", password="9632", database="career_predictor"
        )

    def login(self):
        user = self.username.text()
        pwd = self.password.text()

        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (user, pwd))
        result = cursor.fetchone()
        db.close()

        if result:
            QMessageBox.information(self, "Login", "Login Successful!")
            self.parent().go_to_dashboard(user)  # switches page in stacked widget
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")


    def signup(self):
        dialog = SignupDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_details()

            if not data["username"] or not data["password"] or data["gender"] == "Select":
                QMessageBox.warning(self, "Input Error", "Please fill all fields correctly.")
                return

            db = self.connect_db()
            cursor = db.cursor()
            try:
                cursor.execute("""
                    INSERT INTO users (name, username, password, age, gender, qualification)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (data["name"], data["username"], data["password"],
                      data["age"], data["gender"], data["qualification"]))
                db.commit()
                QMessageBox.information(self, "Signup", "Account created successfully!")
            except pymysql.err.IntegrityError:
                QMessageBox.warning(self, "Signup", "Username already exists.")
            db.close()

    def clear_fields(self):
        self.username.clear()
        self.password.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
