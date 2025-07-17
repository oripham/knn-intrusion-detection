import csv
import joblib
from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors=3)

# Read data in from file
with open("df_train.csv") as f:
    reader = csv.reader(f)
    next(reader)

    data_train = []
    for row in reader:
        data_train.append({
            "evidence": row[4:-1],
            "label": "normal" if row[-1] == "normal" else "anomaly"
        })

# Separate data into training and testing groups
evidence = [row["evidence"] for row in data_train]
labels = [row["label"] for row in data_train]

# train model
model.fit(evidence, labels)

# Save the model
joblib.dump(model, "knn_model.pkl")