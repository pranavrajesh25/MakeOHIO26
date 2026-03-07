# 1. IMPORT
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 2. LOAD DATA
df = pd.read_csv("data/your_file.csv")
print(df.head())

# 3. EXPLORE
print(df.shape)
print(df.describe())
df.hist()
plt.show()

# 4. PREPARE
X = df.drop("target", axis=1)   # features
y = df["target"]                 # label

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 5. TRAIN
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train, y_train)

# 6. EVALUATE
predictions = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, predictions))

# 7. SAVE MODEL
import pickle
pickle.dump(model, open("models/model.pkl", "wb"))
