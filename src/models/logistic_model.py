from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import csv
import numpy as np

with open("data/processed_data.csv") as f:
    reader = csv.DictReader(f)
    data = list(reader)

X = np.array([[float(row["fairOdds_prob"]), float(row["bookOdds_prob"]), float(row["bookOverUnder"]), float(row["fairOverUnder"]), float(row["odds_diff"]), float(row["side"]), float(row["is_half_point"])] for row in data])
y = np.array([int(row["label"]) for row in data])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(solver="liblinear",random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.4f}")