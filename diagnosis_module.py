import pandas as pd
import joblib
import shap

# Load trained Random Forest model and SHAP explainer
model = joblib.load('wh_rf_model.pkl')
explainer = shap.TreeExplainer(model)

def predict_and_explain(input_dict):
    """
    Given input_dict with symptoms, returns diagnosis and SHAP values.
    """
    input_df = pd.DataFrame([input_dict])
    pred_proba = model.predict_proba(input_df)[0]
    classes = model.classes_
    shap_values = explainer.shap_values(input_df)[0][0]
    result = dict(zip(classes, pred_proba))
    pred_diagnosis = classes[pred_proba.argmax()]
    shap_explanation = dict(zip(input_df.columns, shap_values))
    return pred_diagnosis, result, shap_explanation
