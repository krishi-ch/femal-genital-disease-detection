# model_training.py
# Trains a Random Forest classifier and saves model + SHAP explainer
# Validates workflow and clearly warns about synthetic dataset

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import shap
import matplotlib.pyplot as plt
import seaborn as sns
import sys

# 1. Load your symptoms CSV (must be in same folder)
try:
    df = pd.read_csv('womens_health_symptoms.csv')  # update filename if needed
except Exception as e:
    print(f"Error loading CSV: {e}")
    sys.exit(1)

# Validation: Check for missing values and duplicates
if df.isnull().sum().sum() > 0:
    print("Warning: Your dataset contains missing values!")
else:
    print("No missing values detected.")

num_dupes = df.duplicated().sum()
print(f"Number of duplicate rows: {num_dupes}")

print(df['diagnosis'].value_counts())

# 2. Prepare features (X) and labels (y)
X = df.drop(columns=['diagnosis'])
y = df['diagnosis']

# 3. Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Train Random Forest model
model = RandomForestClassifier(n_estimators=120, random_state=42)
model.fit(X_train, y_train)

# After you get model predictions:
y_pred = model.predict(X_test)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Confusion matrix for diagnosis spread
print("\nGenerating confusion matrix for additional validation...")
cm = confusion_matrix(y_test, y_pred, labels=model.classes_)

# For visual inspection (optional in review, but great for notebook)
try:
    plt.figure(figsize=(8, 8))
    sns.heatmap(cm, annot=False, xticklabels=model.classes_, yticklabels=model.classes_, cbar=False)
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.show()
except Exception as e:
    print("Could not display confusion matrix plot (likely headless environment).")

# 5. Print accuracy for documentation / reporting
train_acc = accuracy_score(y_train, model.predict(X_train))
test_acc = accuracy_score(y_test, y_pred)
print(f"\nTraining Accuracy: {train_acc:.2f}")
print(f"Test Accuracy: {test_acc:.2f}")

# Warning if accuracy is artificial
if test_acc > 0.95:
    print("\nWARNING: Extremely high accuracy detected — this is expected for a highly distinct synthetic dataset and is NOT realistic for real-world diagnosis.")
print("NOTE: Results on synthetic data do not reflect expected medical diagnostic model performance.")

# 6. Save trained model for Streamlit app integration
joblib.dump(model, 'wh_rf_model.pkl')
print("Model saved as wh_rf_model.pkl")

# 7. Create and save SHAP explainer for fast use in the app
explainer = shap.TreeExplainer(model)
joblib.dump(explainer, 'shap_explainer.pkl')
print("SHAP explainer saved as shap_explainer.pkl")

# Optionally: Test SHAP values on a sample input (for logs)
sample_row = X_test.iloc[[0]]
sample_explanation = explainer.shap_values(sample_row)
print("Sample SHAP explanation for first test sample:", sample_explanation)

