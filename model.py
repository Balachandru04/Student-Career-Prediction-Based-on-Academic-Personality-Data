from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit,
    QComboBox, QMessageBox, QHBoxLayout,QComboBox, QListView,QScrollArea
)
from PyQt5.QtGui import QFont,QMouseEvent,QPixmap
from PyQt5.QtCore import Qt
import joblib
import pandas as pd
from tensorflow.keras.models import load_model

class PredictionPage(QWidget):

    def __init__(self, stacked_widget, dashboard_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.dashboard_widget = dashboard_widget

        # === Background ===
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap("assert/career.png"))
        self.bg_label.setScaledContents(True)
        self.bg_label.lower()

        # === Title ===
        title = QLabel("🎯 Career Prediction Form")
        title.setFont(QFont("Times New Roman", 36, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #001d3d;")

        # === Styling Helpers ===
        def styled_lineedit(placeholder):
            le = QLineEdit()
            le.setPlaceholderText(placeholder)
            le.setFont(QFont("Times New Roman", 15))
            le.setFixedHeight(38)
            return le

        def styled_combobox(items):
            cb = QComboBox()
            cb.addItems(items)
            cb.setFont(QFont("Times New Roman", 15))
            cb.setFixedHeight(38)
            return cb

        def field_row(label_text, widget):
            label = QLabel(label_text)
            label.setFont(QFont("Times New Roman", 16, QFont.Bold))
            label.setFixedWidth(220)
            row = QHBoxLayout()
            row.addWidget(label)
            row.addWidget(widget)
            return row

        # === Inputs ===
        self.sslc_input = styled_lineedit("e.g., 88.5")
        self.hsc_input = styled_lineedit("e.g., 90.2")
        self.ug_cgpa = styled_lineedit("e.g., 9.0")
        self.pg_cgpa = styled_lineedit("e.g., 8.6")
        self.tech_skills = styled_lineedit("e.g., 8")
        self.soft_skills = styled_lineedit("e.g., 7")

        self.hsc_stream = styled_combobox(["Science", "Commerce", "Arts"])
        # self.ug_degree = styled_combobox([
        #     "B.Com", "BCA", "BA-English", "B.Sc-CS", "B.E-ECE", "B.E-EEE", "B.Tech-CSE", "B.Tech-IT"
        # ])
        self.ug_degree = styled_combobox(["B.Com", "BCA", "BA-English", "B.Sc-CS",
            "B.E-ECE", "B.E-EEE", "B.Tech-CSE", "B.Tech-IT"])
        
        # self.pg_degree = styled_combobox(["None", "MCA", "MBA", "MSc", "MA"])
        self.pg_degree = styled_combobox(['None',"MCA", "MBA", "MSc", "MA"])
        self.project_done = styled_combobox(["Yes", "No"])
        self.project_exp = styled_combobox(["None", "Beginner", "Intermediate", "Advanced"])
        self.internship = styled_combobox(["Yes", "No"])

        self.interested_field = CheckableComboBox()

        self.interested_field.addItems(["Data Science", "Web Development", "Full Stack Developer", "AI", 
            "Machine Learning", "Data Analyst", "Cyber Security", 
            "App Development", "Cloud Computing", "UI/UX", "IoT", "Robotics"])
        
        self.interested_field.setFont(QFont("Times New Roman", 15))
        self.interested_field.setFixedHeight(38)

        self.known_lang = CheckableComboBox()
        self.known_lang.addItems(["Python", "Java", "C++", "SQL", "JavaScript", "R", "Go", "C#", "Ruby"])
        
        self.known_lang.setFont(QFont("Times New Roman", 15))
        self.known_lang.setFixedHeight(38)

        self.known_tools = CheckableComboBox()
        self.known_tools.addItems(["Excel", "Power BI", "Tableau", "Git", "VS Code", "Jupyter", "React Native", "Flutter"])
        self.known_tools.setFont(QFont("Times New Roman", 15))
        self.known_tools.setFixedHeight(38)

        # === Form Sections ===
        form_layout = QVBoxLayout()
        form_layout.setSpacing(20)

        def add_section(title):
            section_label = QLabel(title)
            section_label.setFont(QFont("Times New Roman", 20, QFont.Bold))
            form_layout.addWidget(section_label)

        def add_field(label_text, widget):
            form_layout.addLayout(field_row(label_text, widget))

        add_section("\t \t \t\t\t🎓 Education")
        add_field("SSLC Percentage:", self.sslc_input)
        add_field("HSC Percentage:", self.hsc_input)
        add_field("HSC Stream:", self.hsc_stream)
        add_field("UG Degree:", self.ug_degree)
        add_field("UG CGPA:", self.ug_cgpa)
        add_field("PG Degree:", self.pg_degree)
        add_field("PG CGPA:", self.pg_cgpa)

        add_section("\t \t \t\t\t💡 Skills & Interests")
        add_field("Interested Fields:", self.interested_field)
        add_field("Known Languages:", self.known_lang)
        add_field("Known Tools:", self.known_tools)
        add_field("Technical Skills (0-10):", self.tech_skills)
        add_field("Soft Skills (0-10):", self.soft_skills)

        add_section("\t \t \t\t\t🛠 Experience & Projects")
        add_field("Project Done?", self.project_done)
        add_field("Project Experience:", self.project_exp)
        add_field("Internship Done?", self.internship)

        # === Buttons ===
        self.predict_btn = QPushButton("🎯 Predict Now")
        self.back_btn = QPushButton("🔙 Back")
        for btn in [self.predict_btn, self.back_btn]:
            btn.setFixedHeight(42)
            btn.setFont(QFont("Times New Roman", 16, QFont.Bold))
            btn.setCursor(Qt.PointingHandCursor)

            self.back_btn.setStyleSheet("""
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
            
            self.predict_btn.setStyleSheet("""
            QPushButton {
                background-color: #0077b6;
                color: white;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #f7b801;
            }
            """)

        self.predict_btn.clicked.connect(self.run_prediction)
        self.back_btn.clicked.connect(self.go_back)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(30)
        btn_layout.addStretch()
        btn_layout.addWidget(self.back_btn)
        btn_layout.addWidget(self.predict_btn)
        btn_layout.addStretch()

        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)
        self.result_label.setFont(QFont("Times New Roman", 14))
        self.result_label.setAlignment(Qt.AlignCenter)

        # === Form Card ===
        card = QWidget()
        card.setStyleSheet("background-color: rgba(255, 255, 255, 0.97); border-radius: 16px;")
        card.setMinimumWidth(700)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(50, 40, 50, 40)
        card_layout.setSpacing(25)
        card_layout.addLayout(form_layout)
        card_layout.addLayout(btn_layout)
        card_layout.addWidget(self.result_label)

        # === Scroll Area ===
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent;")
        scroll.setWidget(card)

        scroll_container = QHBoxLayout()
        scroll_container.setContentsMargins(80, 0, 80, 0)
        scroll_container.addWidget(scroll)

        # === Main Layout ===
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 20, 40, 60)
        main_layout.setSpacing(30)
        main_layout.addWidget(title)
        main_layout.addLayout(scroll_container)
        self.setLayout(main_layout)

        # === Styles ===
        self.setStyleSheet("""
            QLineEdit, QComboBox {
                background-color: #f0f8ff;
                border: 1.5px solid #999;
                border-radius: 6px;
                padding: 6px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #0077b6;
                color: white;
                padding: 8px 18px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #023e8a;
            }
            QLabel {
                color: #001d3d;
            }
        """)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.bg_label.resize(self.size())

    def split_items(self, x):
        return [item.strip() for item in str(x).split(';') if item.strip()]

    def run_prediction(self):
        try:
            sample_input = {
                'SSLC_Percentage': float(self.sslc_input.text()),
                'HSC_Stream': self.hsc_stream.currentText().strip(),
                'HSC_Percentage': float(self.hsc_input.text()),
                'UG_Degree': self.ug_degree.currentText().strip(),
                'UG_CGPA': float(self.ug_cgpa.text()),
                'PG_Degree': self.pg_degree.currentText().strip(),
                'PG_CGPA': float(self.pg_cgpa.text()),
                'Interested_Field': ";".join(self.interested_field.checkedItems()),
                'Project_Done': self.project_done.currentText().strip(),
                'Project_Experience_Level': self.project_exp.currentText().strip(),
                'Internship': self.internship.currentText().strip(),
                'Known_Languages': ';'.join(self.known_lang.checkedItems()),
                'Known_Tools': ';'.join(self.known_tools.checkedItems()),
                'Technical_Skills': int(self.tech_skills.text()),
                'Soft_Skills': int(self.soft_skills.text())
            }

            result = self.predict_ann(sample_input)
            self.result_label.setText(result.replace("\n", "<br>").replace("🎓", "<b>🎓</b>").replace("🎯", "<b>🎯</b>").replace("✅", "<b>✅</b>"))

        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", str(e))

    def go_back(self):
        self.stacked_widget.setCurrentWidget(self.dashboard_widget)

    def predict_ann(self, sample_input):
        


        # Mapping interests to recommended skills/tools
        interest_skill_guide = {
            'AI': ['Python', 'NumPy', 'Pandas', 'TensorFlow', 'Scikit-learn'],
            'Data Science': ['Python', 'SQL', 'Pandas', 'Power BI', 'Matplotlib'],
            'Web Development': ['HTML', 'CSS', 'JavaScript', 'React', 'Node JS'],
            'Cloud Computing': ['AWS', 'Azure', 'Docker', 'Linux'],
            'Machine Learning': ['Python', 'Scikit-learn', 'Jupyter', 'TensorFlow'],
            'Full Stack Developer': ['React', 'Node JS', 'MongoDB', 'Express JS', 'Git'],
            'UI/UX Design': ['Figma', 'Adobe XD', 'Creativity']
        }

        # Helpers from training
        def normalize_value(val):
            replacements = {
                "Bca": "BCA", "Bsc": "BSc", "B.Sc": "BSc", "B.Tech": "BTech", "Btech": "BTech",
                "Mca": "MCA", "Msc": "MSc", "M.Sc": "MSc", "M.Tech": "MTech", "Mtech": "MTech",
                "None": "None", "Arts": "Arts", "Science": "Science", "Commerce": "Commerce",
                "Yes": "Yes", "No": "No"
            }
            val = str(val).strip().title()
            return replacements.get(val, val)

        def split_items(x):
            replacements = {
                "SQL": "SQL", "MYSQL": "MySQL", "C++": "C++", "AI": "AI",
                "NODEJS": "Node JS", "NODE JS": "Node JS",
                "POWERBI": "Power BI", "POWER BI": "Power BI",
                "REACTNATIVE": "React Native", "REACT NATIVE": "React Native",
                "FLUTTER": "Flutter",
                "HIGH": "High", "INTERMEDIATE": "Intermediate", "BEGINNER": "Beginner",
                "BCA": "BCA", "BSC": "BSc", "BSC CS": "BSc CS", "BE": "BE", "B.TECH": "B.Tech"
            }
            items = [i.strip().upper() for i in str(x).split(';') if i.strip()]
            return [replacements.get(i, i.title()) for i in items]

        # Load models and encoders
        scaler = joblib.load("saved_models/scaler.pkl")
        ann_model = load_model("saved_models/ann_model.h5")
        input_columns = joblib.load("saved_models/input_columns.pkl")

        categorical_cols = ['HSC_Stream', 'UG_Degree', 'PG_Degree', 'Project_Done', 'Internship', 'Final_Career']
        multi_label_fields = ['Known_Languages', 'Known_Tools', 'Interested_Field', 'Project_Experience_Level']

        encoders = {col: joblib.load(f"saved_models/encoder_{col}.pkl") for col in categorical_cols}
        mlbs = {field: joblib.load(f"saved_models/mlb_{field}.pkl") for field in multi_label_fields}

        # Normalize and encode categorical fields
        for col in categorical_cols:
            if col in sample_input:
                val = normalize_value(sample_input[col])
                le = encoders[col]
                if val in le.classes_:
                    sample_input[col] = le.transform([val])[0]
                else:
                    sample_input[col] = le.transform(['None'])[0]

        # Encode multi-label fields and save original values
        multilabel_encoded_parts = []
        multilabel_raw_values = {}

        for field in multi_label_fields:
            raw = sample_input[field]
            multilabel_raw_values[field] = raw  # Save for later tips
            items = split_items(raw)
            mlb = mlbs[field]
            transformed = mlb.transform([items])
            columns = [f"{field}_{cls}" for cls in mlb.classes_]
            multilabel_encoded_parts.append(pd.DataFrame(transformed, columns=columns))
            sample_input.pop(field, None)  # Remove from main dict

        # Combine input
        df_input = pd.DataFrame([sample_input])
        final_input = pd.concat([df_input] + multilabel_encoded_parts, axis=1)

        # Ensure all expected columns are present
        for col in input_columns:
            if col not in final_input:
                final_input[col] = 0
        final_input = final_input[input_columns]

        # Predict
        input_scaled = scaler.transform(final_input)
        prediction = ann_model.predict(input_scaled)[0]
        top3 = prediction.argsort()[-3:][::-1]

        target_encoder = encoders['Final_Career']
        careers = target_encoder.inverse_transform(top3)

        # Generate learning tips based on interests
        user_skills = set(
            split_items(multilabel_raw_values.get('Known_Languages', '')) +
            split_items(multilabel_raw_values.get('Known_Tools', '')) +
            split_items(multilabel_raw_values.get('Project_Experience_Level', ''))
        )
        interest_items = split_items(multilabel_raw_values.get('Interested_Field', ''))

        learning_tips = []
        for field in interest_items:
            required = set(interest_skill_guide.get(field, []))
            missing = required - user_skills
            if missing:
                tip = f"📘 Since you're interested in {field}, consider learning: {', '.join(missing)}"
                learning_tips.append(tip)

        # Build result string

        result = f"""
        🎯 Predicted Career: {careers[0]}
        ✅ Confidence: {prediction[top3[0]] * 100:.2f}%""".strip()

        if learning_tips:
            result += "\n\n🎓 Learning Suggestions:\n" + "\n".join(learning_tips)

        return result.strip()


class CheckableComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setView(QListView())
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().setPlaceholderText("Select multiple...")
        self.setInsertPolicy(QComboBox.NoInsert)
        self.view().viewport().installEventFilter(self)
        self._popup_shown = False

    def addItems(self, items):
        for item in items:
            self.addItem(item)
            index = self.model().index(self.count() - 1, 0)
            self.model().setData(index, Qt.Unchecked, Qt.CheckStateRole)

    def eventFilter(self, obj, event):
        if isinstance(event, QMouseEvent) and event.type() == QMouseEvent.MouseButtonRelease:
            index = self.view().indexAt(event.pos())
            if index.isValid():
                current_state = self.model().data(index, Qt.CheckStateRole)
                new_state = Qt.Unchecked if current_state == Qt.Checked else Qt.Checked
                self.model().setData(index, new_state, Qt.CheckStateRole)
                self.update_display()
                return True  # Prevent closing
        return super().eventFilter(obj, event)

    def showPopup(self):
        self._popup_shown = True
        super().showPopup()

    def hidePopup(self):
        if self._popup_shown:
            # Override hide unless forced
            self._popup_shown = False
        else:
            super().hidePopup()

    def checkedItems(self):
        return [self.itemText(i) for i in range(self.count())
                if self.model().data(self.model().index(i, 0), Qt.CheckStateRole) == Qt.Checked]

    def update_display(self):
        selected = self.checkedItems()
        self.lineEdit().setText("; ".join(selected))
