import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler, MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical

# ========== Step 1: Setup ========== #
os.makedirs("saved_models", exist_ok=True)

# ========== Step 2: Load Data ========== #
# df = pd.read_csv(r"C:\Users\balac\Downloads\mini Project\final_realistic_career_dataset.csv")
df = pd.read_csv(r"C:\Users\balac\Downloads\mini Project_Done\datas\final_realistic_career_dataset.csv")
df = df[df['Final_Career'].notnull()]

# ========== Step 3: Normalization Helpers ========== #
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
    # Normalize all values to uppercase for consistency
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
    normalized = [replacements.get(i, i.title()) for i in items]
    return normalized


# ========== Step 4: Label Encode Categorical ========== #
categorical_cols = ['HSC_Stream', 'UG_Degree', 'PG_Degree', 'Project_Done', 'Internship', 'Final_Career']
label_encoders = {}
for col in categorical_cols:
    df[col] = df[col].fillna("None").apply(normalize_value)
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le
    joblib.dump(le, f"saved_models/encoder_{col}.pkl")

# ========== Step 5: MultiLabel Fields ========== #
multi_label_fields = ['Known_Languages', 'Known_Tools', 'Interested_Field', 'Project_Experience_Level']
mlb_dict = {}
for field in multi_label_fields:
    df[field] = df[field].fillna('')
    mlb = MultiLabelBinarizer()
    encoded = mlb.fit_transform(df[field].map(split_items))
    encoded_df = pd.DataFrame(encoded, columns=[f"{field}_{cls}" for cls in mlb.classes_])
    df = pd.concat([df, encoded_df], axis=1)
    df.drop(columns=[field], inplace=True)
    mlb_dict[field] = mlb
    joblib.dump(mlb, f"saved_models/mlb_{field}.pkl")

# ========== Step 6: Features & Target ========== #
X = df.drop('Final_Career', axis=1).fillna(0)
y = df['Final_Career']
input_columns = X.columns.tolist()
joblib.dump(input_columns, "saved_models/input_columns.pkl")

# ========== Step 7: Scale ========== #
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
joblib.dump(scaler, "saved_models/scaler.pkl")

# ========== Step 8: Split ========== #
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# ========== Step 9: Train Models ========== #
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
joblib.dump(rf, "saved_models/random_forest.pkl")

log_model = LogisticRegression(max_iter=1000)
log_model.fit(X_train, y_train)
joblib.dump(log_model, "saved_models/logistic_regression.pkl")

num_classes = len(np.unique(y))
y_train_cat = to_categorical(y_train, num_classes)
ann = Sequential([
    Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dense(num_classes, activation='softmax')
])
ann.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
ann.fit(X_train, y_train_cat, epochs=25, batch_size=32, verbose=0)
ann.save("saved_models/ann_model.h5")

print("✅ All models trained and saved.")

# ========== Step 10: Prediction Function ========== #
def predict_ann(sample_input):
    scaler = joblib.load("saved_models/scaler.pkl")
    ann_model = load_model("saved_models/ann_model.h5")
    input_columns = joblib.load("saved_models/input_columns.pkl")

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

    # Process multi-label fields
    multilabel_encoded_parts = []
    for field in multi_label_fields:
        raw = sample_input.pop(field, "")
        items = split_items(raw)
        mlb = mlbs[field]
        transformed = mlb.transform([items])
        columns = [f"{field}_{cls}" for cls in mlb.classes_]
        multilabel_encoded_parts.append(pd.DataFrame(transformed, columns=columns))

    df_input = pd.DataFrame([sample_input])
    final_input = pd.concat([df_input] + multilabel_encoded_parts, axis=1)

    for col in input_columns:
        if col not in final_input:
            final_input[col] = 0
    final_input = final_input[input_columns]

    input_scaled = scaler.transform(final_input)
    prediction = ann_model.predict(input_scaled)[0]
    top3 = prediction.argsort()[-3:][::-1]

    target_encoder = encoders['Final_Career']
    careers = target_encoder.inverse_transform(top3)

    print("\n🎯 Predicted Career:", careers[0])
    print(f"✅ Confidence: {prediction[top3[0]] * 100:.2f}%")
    print("\n🔝 Top 3 Career Suggestions:")
    for i in range(3):
        print(f"{i+1}. {careers[i]} ({prediction[top3[i]] * 100:.2f}%)")

# ========== Step 11: Sample Prediction ========== #
sample_input = {
    'SSLC_Percentage': 88.5,
    'HSC_Stream': 'Science',
    'HSC_Percentage': 90.7,
    'UG_Degree': 'BCA',
    'UG_CGPA': 9.7,
    'PG_Degree': 'None',
    'PG_CGPA': 0.0,
    'Interested_Field': 'Data Science;Data Analyst;Full Stack Developer',
    'Project_Done': 'Yes',
    'Project_Experience_Level': 'Advanced;',
    'Internship': 'Yes',
    'Known_Languages': 'Python;SQL;Java',
    'Known_Tools': 'Power BI;Tableau;Excel;Git;React Native;Flutter',
    'Technical_Skills': 8,
    'Soft_Skills': 7
}

predict_ann(sample_input)
