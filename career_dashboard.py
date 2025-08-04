from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QApplication
)
from PyQt5.QtGui import QFont, QPixmap, QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt
import sys
from model import PredictionPage
from learningpage import LearningPage

bg_image = r"C:\Users\balac\Downloads\mini Project_Done\assert\career.png"
chat_icon = r"C:\Users\balac\Downloads\mini Project_Done\assert\chat.png"
predict_icon = r"C:\Users\balac\Downloads\mini Project_Done\assert\predict.png"
learning_icon = r"C:\Users\balac\Downloads\mini Project_Done\assert\history.png"

class DashboardWindow(QWidget):

    def __init__(self, username, login_window, stacked_widget):
        super().__init__()
        self.username = username
        self.login_window = login_window
        self.stacked_widget = stacked_widget
        self.setWindowTitle("Career Prediction Dashboard")
        self.setWindowState(Qt.WindowMaximized)

        self.bg = QPixmap(bg_image)

        self.title = QLabel("🎓 Career Prediction System")
        self.title.setFont(QFont("Arial", 24, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #00509d; margin-top: 30px; background: transparent;")

        self.label = QLabel(f"Welcome, {self.username}!")
        self.label.setFont(QFont("Arial", 14, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #333333; margin-bottom: 30px; background: transparent;")

        # Create buttons with icons on top
        prediction_widget, self.btn_prediction = self.create_button_with_image(predict_icon, "Career Prediction")
        learning_widget, self.btn_learning = self.create_button_with_image(learning_icon, "Learning Path")
        chatbot_widget, self.btn_chatbot = self.create_button_with_image(chat_icon, "Career Chatbot")

        # Add LearningPage to stacked widget
        self.learning_widget = LearningPage(self.stacked_widget, self)
        self.stacked_widget.addWidget(self.learning_widget)

        # Connect button clicks
        self.btn_prediction.clicked.connect(self.open_prediction)
        self.btn_learning.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.learning_widget))
        self.btn_chatbot.clicked.connect(self.open_chatbot)

        # Logout button
        self.btn_logout = QPushButton("🔴 Logout")
        self.btn_logout.setFixedSize(100, 35)
        self.btn_logout.setStyleSheet("""
            QPushButton {
                background-color: #e63946;
                color: white;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #f7b801;
            }
        """)
        self.btn_logout.clicked.connect(self.logout)

        # Layouts
        top_layout = QVBoxLayout()
        top_layout.addWidget(self.title)
        top_layout.addWidget(self.label)
        top_layout.setAlignment(Qt.AlignTop)

        horizontal_buttons = QHBoxLayout()
        horizontal_buttons.setSpacing(40)
        horizontal_buttons.setAlignment(Qt.AlignCenter)
        horizontal_buttons.addWidget(prediction_widget)
        horizontal_buttons.addWidget(learning_widget)
        horizontal_buttons.addWidget(chatbot_widget)

        logout_layout = QHBoxLayout()
        logout_layout.addStretch()
        logout_layout.addWidget(self.btn_logout)
        logout_layout.setContentsMargins(0, 20, 20, 20)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addStretch()
        main_layout.addLayout(horizontal_buttons)
        main_layout.addStretch()
        main_layout.addLayout(logout_layout)

        self.setLayout(main_layout)

        # Add PredictionPage to stacked_widget
        self.prediction_page = PredictionPage(self.stacked_widget, self)
        self.stacked_widget.addWidget(self.prediction_page)

    def open_prediction(self):
        self.stacked_widget.setCurrentWidget(self.prediction_page)

    def create_button_with_image(self, image_path, text):
        container = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)  # Balanced spacing

        # Image Label
        image_label = QLabel()
        pixmap = QPixmap(image_path).scaled(110, 110, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setFixedSize(120, 120)  # Container box
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setStyleSheet("""
            background-color: white;
            border: 2px solid #ffffff;
            border-radius: 15px;
            padding: 8px;
        """)

        # Button
        button = QPushButton(text)
        button.setFixedSize(160, 38)
        button.setStyleSheet("""
            QPushButton {
                background-color: #0077b6;
                color: white;
                font-size: 13px;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #00b4d8;
            }
        """)
        button.setCursor(Qt.PointingHandCursor)

        # Add to layout
        layout.addWidget(image_label)
        layout.addWidget(button)
        container.setLayout(layout)

        return container, button

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.bg)

    def open_chatbot(self):
        from chat import ChatbotPage
        self.chatbot_page = ChatbotPage(self.stacked_widget, self)  # Pass self
        self.stacked_widget.addWidget(self.chatbot_page)
        self.stacked_widget.setCurrentWidget(self.chatbot_page)

    def open_history(self):
        from learningpage import HistoryPage
        self.history_page = HistoryPage(self.username, self.stacked_widget, self)  # Pass dashboard reference
        self.stacked_widget.addWidget(self.history_page)
        self.stacked_widget.setCurrentWidget(self.history_page)

    def logout(self):
        reply = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )

        if reply == QMessageBox.Yes:
            # QMessageBox.information(self, "Logout", "You have been logged out.")
            self.stacked_widget.logout()
        else:
            QMessageBox.information(self, "Logout Cancelled", "You are still logged in.")


if __name__ == '__main__':
    from login import LoginWindow
    from PyQt5.QtWidgets import QStackedWidget

    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()
    fake_login = LoginWindow(stacked_widget)
    dashboard = DashboardWindow("TestUser", fake_login, stacked_widget)

    stacked_widget.addWidget(dashboard)
    stacked_widget.setCurrentWidget(dashboard)
    stacked_widget.showMaximized()
    
    sys.exit(app.exec_())