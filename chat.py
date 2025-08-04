import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QLineEdit,
    QPushButton, QMessageBox, QHBoxLayout, QSizePolicy
)
from PyQt5.QtGui import QFont, QTextCursor, QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from sentence_transformers import SentenceTransformer, util
import re

class AnswerThread(QThread):
    result_ready = pyqtSignal(str)
    
    def __init__(self, user_input, qa_list, question_embeddings, model):
        super().__init__()
        self.user_input = user_input
        self.qa_list = qa_list
        self.question_embeddings = question_embeddings
        self.model = model

    def run(self):
        user_input = self.user_input.strip().lower()

        # ✅ Handle flexible greetings
        greeting_patterns = [
            r"\bhi+\b",                                # hi, hii, hiiiii
            r"\bhello+\b",                             # hello, helloooo
            r"\bhey+\b",                               # hey, heyyy
            r"\bhey\s+\w+",                            # hey dude, hey there
            r"\bgood\s+(morning|evening|afternoon)",  # good morning, good evening
            r"\bhowdy\b",                              # howdy
            r"\byo+\b",                                # yo, yoooo
            r"\bwhat('?| i)s\s+up\b"                   # what's up, what is up
        ]

        if any(re.search(pattern, user_input) for pattern in greeting_patterns):
            self.result_ready.emit("👋 Hello! Ask me anything about careers, technology, or education.")
            return
        farewell_patterns = [r"\bbye+\b", r"\bgoodbye\b", r"\bsee\s+(you|ya)\b", r"\blater\b", r"\bcatch\s+you\s+later\b"]
        if any(re.search(pattern, user_input) for pattern in farewell_patterns):
            self.result_ready.emit("👋 Goodbye! Have a great day and keep learning!")
            return


        elif user_input in ["thanks", "thank you", "tnx", "ok", "okay"]:
            self.result_ready.emit("👍 Got it! Feel free to ask your next question about careers or tech.")
            return


        try:
            query_embedding = self.model.encode(user_input, convert_to_tensor=True)
            scores = util.pytorch_cos_sim(query_embedding, self.question_embeddings)[0]

            best_score = float(scores.max())
            best_index = int(scores.argmax())

            if best_score >= 0.75:
                self.result_ready.emit(self.qa_list[best_index]["answer"])
            elif best_score >= 0.50:
                suggestion = self.qa_list[best_index]["question"]
                self.result_ready.emit(f"❌ I couldn't find a good answer.<br>❓ Did you mean: “{suggestion}”?")
            else:
                self.result_ready.emit("🧠 The model is in training mode right now. We’ll update this soon.<br>💬 Let’s continue with other career-related questions!")
        except Exception as e:
            self.result_ready.emit(f"⚠️ Error during processing: {e}")

class ChatbotPage(QWidget):
    def __init__(self, stacked_widget,dashboard_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.dashboard_widget = dashboard_widget
        self.stacked_widget = stacked_widget
        self.background_path = r"C:\Users\balac\Downloads\mini Project_Done\assert\career.png"
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.setAutoFillBackground(True)
        self.set_background()

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        self.label = QLabel("🤖 SparkBot - Ask me anything about careers, tech, or education!")
        self.label.setFont(QFont("Times New Roman", 18, QFont.Bold))
        self.label.setStyleSheet("color: #003366; background: transparent;")
        layout.addWidget(self.label)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 0.85);
                padding: 14px;
                border: 2px solid #ccc;
                border-radius: 12px;
                font-size: 15pt;
                font-family: "Times New Roman";
            }
        """)
        layout.addWidget(self.chat_display)

        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your question and press Enter...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                border: 2px solid #003366;
                padding: 10px;
                border-radius: 10px;
                font-size: 14pt;
                font-family: "Times New Roman";
            }
        """)
        self.input_field.returnPressed.connect(self.handle_input)
        self.input_field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #0077b6;
                color: white;
                padding: 10px 25px;
                border-radius: 10px;
                font-size: 14pt;
                font-family: "Times New Roman";
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #023e8a;
            }
        """)
        self.send_button.clicked.connect(self.handle_input)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)

        self.back_button = QPushButton("🔙 Back to Home")
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #e63946;
                color: white;
                padding: 10px 20px;
                border-radius: 10px;
                font-size: 13pt;
                font-family: "Times New Roman";
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f77f00;
            }
        """)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button, alignment=Qt.AlignRight)

        self.setLayout(layout)
        self.load_data()

    def set_background(self):
        pixmap = QPixmap(self.background_path)
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        self.setPalette(palette)

    def resizeEvent(self, event):
        self.set_background()
        super().resizeEvent(event)
        
    def load_data(self):
        try:
            with open(r"C:\Users\balac\Downloads\mini Project_Done\datas\combined_chat_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.qa_list = data["qa_data"]
                self.questions = [item["question"].lower() for item in self.qa_list]
                self.question_embeddings = self.model.encode(self.questions, convert_to_tensor=True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load chatbot data:\n{e}")
            self.qa_list = []
            self.questions = []
            self.question_embeddings = []

    def handle_input(self):
        user_text = self.input_field.text().strip()
        if not user_text:
            return

        if user_text.lower() in ["clear", "clear chat", "clear window", "cls"]:
            self.chat_display.clear()
            self.input_field.clear()
            return

        self.chat_display.append(f"<p style='color: #1d3557; font-weight: bold;'>🧑‍💻 You: {user_text}</p>")
        self.chat_display.moveCursor(QTextCursor.End)
        self.input_field.clear()

        if user_text.lower() == "exit":
            self.chat_display.append("<p style='color: #6c757d;'>🤖 SparkBot: Goodbye! 👋 Stay curious.</p>")
            return

        # ✅ Use the optimized thread version
        self.thread = AnswerThread(user_text, self.qa_list, self.question_embeddings, self.model)
        self.thread.result_ready.connect(self.display_response)
        self.thread.start()

    def display_response(self, response):
        self.chat_display.append(f"<p style='color: #000000; margin-left: 20px;'>🤖 SparkBot: {response}</p>")
        self.chat_display.moveCursor(QTextCursor.End)

    def go_back(self):
        self.stacked_widget.setCurrentWidget(self.dashboard_widget)