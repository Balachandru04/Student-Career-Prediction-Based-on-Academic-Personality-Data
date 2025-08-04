import sys, json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QGridLayout, QStackedWidget, QScrollArea, QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt


class LearningDetailPage(QWidget):
    def __init__(self, stacked_widget, learning_page):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.learning_page = learning_page

        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap("assert/career.png"))
        self.bg_label.setScaledContents(True)
        self.bg_label.lower()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 30, 40, 30)

        # ✅ Only Heading Title at Top
        self.title_label_top = QLabel("")
        self.title_label_top.setAlignment(Qt.AlignCenter)
        self.title_label_top.setFont(QFont("Arial", 30, QFont.Bold))
        self.title_label_top.setStyleSheet("color: #001845; margin-bottom: 10px;")
        self.layout.addWidget(self.title_label_top)

        # Scrollable content
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self.content = QWidget()
        self.content.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.93);
                border-radius: 20px;
                padding: 30px;
            }
        """)
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setSpacing(25)

        # ❌ Removed old title_label here

        self.detail_label = QLabel("")
        self.detail_label.setObjectName("DetailLabel")
        self.detail_label.setWordWrap(True)
        self.detail_label.setOpenExternalLinks(True)

        self.detail_label.setTextFormat(Qt.RichText)
        self.detail_label.setStyleSheet("""
            QLabel#DetailLabel {
                font-size: 17px;
                color: #002855;
                line-height: 1.8em;
            }
        """)

        self.back_button = QPushButton("🔙 Back to Learning Path")
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #e63946;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #ba1b1d;
            }
        """)
        self.back_button.clicked.connect(self.go_back)

        # Add only detail label to scroll area
        self.content_layout.addWidget(self.detail_label)
        self.scroll.setWidget(self.content)

        self.layout.addWidget(self.scroll)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

    def resizeEvent(self, event):
        self.bg_label.resize(self.size())

    def go_back(self):
        self.stacked_widget.setCurrentWidget(self.learning_page)

    def display_details(self, field_name, info):
        emoji = self.learning_page.fields_with_emojis.get(field_name, "📘")

        # Set top fixed title
        self.title_label_top.setText(f"{emoji} {field_name}")

        # HTML section builders
        def section_title(icon, title):
            return f"<h3 style='color:#0a1172; font-size:20px; margin-bottom:6px;'> {icon} {title}</h3>"

        def bullet_list(items):
            return "<ul style='margin-left:20px; font-size:16px;'>" + "".join(
                [f"<li style='margin-bottom:5px;'>{item}</li>" for item in items]
            ) + "</ul>"

        def comma_list(items):
            return "<p style='font-size:16px; margin-top:0px; margin-bottom:20px;'>" + ", ".join(items) + "</p>"

        # Only the content (without repeating heading)
        html = f"""
            {section_title("📝", "Description")}
            <p style='font-size:16px; color:#002855;'>{info['description']}</p>

            {section_title("🗺️", "Roadmap")}
            {bullet_list(info['roadmap'])}

            {section_title("🧠", "Skills")}
            {comma_list(info['skills'])}

            {section_title("🛠️", "Tools")}
            {comma_list(info['tools'])}

            {section_title("📚", "Resources")}
            {bullet_list(info['resources'])}
        """

        self.detail_label.setTextFormat(Qt.RichText)
        self.detail_label.setText(html)


class LearningPage(QWidget):
   
    def __init__(self, stacked_widget, dashboard_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.dashboard_widget = dashboard_widget
        # self.detail_label.setOpenExternalLinks(True)


        # Background image
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap("assert/career.png"))
        self.bg_label.setScaledContents(True)
        self.bg_label.lower()

        # Set stylesheet
        self.setStyleSheet("""
            QLabel#HeaderTitle {
                color: #001845;
                font-size: 36px;
                font-weight: bold;
                font-family: "Times New Roman";
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }

            QPushButton#CardBtn {
                background-color: rgba(255, 255, 255, 0.85);
                color: #001f54;
                font-size: 16px;
                font-weight: 600;
                padding: 20px;
                border-radius: 18px;
                border: 2px solid #0077b6;
                text-align: center;
            }

            QPushButton#CardBtn:hover {
                background-color: #0077b6;
                color: white;
                border: 2px solid #023e8a;
            }

            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #00509d;
                background: transparent;
            }
        """)

        # Header title (NO box)
        self.title = QLabel("📘 Learning Path Recommendations")
        self.title.setObjectName("HeaderTitle")
        self.title.setAlignment(Qt.AlignCenter)

        # Fields with emojis
        self.fields_with_emojis = {
            "📊": "Data Science",
            "🧠": "Artificial Intelligence",
            "🔍": "Machine Learning",
            "🛡️": "Cyber Security",
            "📈": "Data Analyst",
            "☁️": "Cloud Computing",
            "🧑‍💻": "Full Stack Developer",
            "🌐": "Web Development",
            "🎨": "UI/UX",
            "📱": "App Development",
            "📶": "IoT",
            "🤖": "Robotics",
            "🔧": "DevOps",
            "⛓️": "Blockchain",
            "🕶️": "AR/VR & Metaverse"
        }
        self.fields = list(self.fields_with_emojis.keys())

        # Grid layout for buttons
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(30)

        for i, emoji in enumerate(self.fields):
            field_name = self.fields_with_emojis[emoji]
            btn = QPushButton(f"{emoji}  {field_name}")
            btn.setFixedSize(250, 80)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setObjectName("CardBtn")
            btn.clicked.connect(lambda _, f=field_name: self.open_learning_detail(f))
            row, col = divmod(i, 3)
            self.grid_layout.addWidget(btn, row, col, alignment=Qt.AlignCenter)

        # Back button
        self.back_btn = QPushButton("🔙 Back to Home")
        self.back_btn.setFixedSize(180, 45)
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #e63946;
                color: white;
                font-weight: bold;
                font-size: 16px;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #ba1b1d;
            }
        """)
        self.back_btn.clicked.connect(self.go_back)

        # Learning detail page
        self.detail_page = LearningDetailPage(self.stacked_widget, self)
        self.stacked_widget.addWidget(self.detail_page)

        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(40)
        layout.addWidget(self.title)
        layout.addLayout(self.grid_layout)
        layout.addWidget(self.back_btn, alignment=Qt.AlignCenter)
        self.setLayout(layout)



    def resizeEvent(self, event):
        self.bg_label.resize(self.size())

    def open_learning_detail(self, field_name):
        try:
            with open(r"C:\Users\balac\Downloads\mini Project_Done\datas\learning_details.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            if field_name in data:
                self.detail_page.display_details(field_name, data[field_name])
                self.stacked_widget.setCurrentWidget(self.detail_page)
            else:
                QMessageBox.warning(self, "Not Found", f"No learning path found for '{field_name}'.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unable to load learning details:\n{str(e)}")

    def go_back(self):
        self.stacked_widget.setCurrentWidget(self.dashboard_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()

    dashboard = QLabel("🏠 Dashboard Placeholder")
    dashboard.setAlignment(Qt.AlignCenter)
    dashboard.setFont(QFont("Arial", 24))
    stacked_widget.addWidget(dashboard)

    learning_page = LearningPage(stacked_widget, dashboard)
    stacked_widget.addWidget(learning_page)

    stacked_widget.setCurrentWidget(learning_page)
    stacked_widget.showFullScreen()
    sys.exit(app.exec_())
