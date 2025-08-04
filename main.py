import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from login import LoginWindow
from PyQt5.QtCore import Qt
import sys

from career_dashboard import DashboardWindow

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Career Prediction System")
        self.setWindowState(Qt.WindowMaximized)

        # Pages
        self.login_page = LoginWindow(self)
        self.dashboard_page = None  # Will be set after login

        self.addWidget(self.login_page)   # Index 0
        self.setCurrentWidget(self.login_page)

    def go_to_dashboard(self, username):
        self.dashboard_page = DashboardWindow(username, self,self)
        self.addWidget(self.dashboard_page)  # Index 1
        self.setCurrentWidget(self.dashboard_page)

    def logout(self):
        self.setCurrentWidget(self.login_page)
        self.login_page.clear_fields()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
