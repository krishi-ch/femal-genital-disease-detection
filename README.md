
# Code Pink: Women's Health Anonymous Diagnosis 💗

## Project Overview
A Streamlit-based prototype application for anonymous women's health symptom diagnosis with accessibility support for blind and deaf users.

## Features
- 🩺 Symptom-based diagnosis using machine learning models
- 👩‍🦯 Accessibility modes for blind (screen reader + audio instructions) and deaf (sign language video) users
- 📊 Risk probability visualization
- 💬 AI assistant for help
- 📥 Downloadable diagnosis results
- 🎨 Pink-themed UI

## Disclaimer
**IMPORTANT**: This project is a prototype using a synthetic dataset for educational purposes only. Results are NOT actual medical advice. Always consult a healthcare professional for medical concerns.

## Installation
1. Clone or download this repository
2. Create and activate a virtual environment (recommended)
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. First, generate the synthetic dataset and train the models:
   ```bash
   python generate_dataset.py
   python model_training.py
   ```
2. Run the app with:
   ```bash
   streamlit run app.py
   ```

## Project Files
- `app.py`: Main Streamlit application
- `diagnosis_module.py`: Diagnosis prediction and explanation logic
- `assistant_module.py`: AI assistant functionality
- `model_training.py`: Model training script
- `generate_dataset.py`: Synthetic dataset generator
- `requirements.txt`: Dependencies list
- `static/`: Audio and video files for accessibility
- `.pkl` files (not included in repo, generated locally): Trained ML models and explainer

## Author
Krishi Chintala

