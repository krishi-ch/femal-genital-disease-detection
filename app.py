import streamlit as st
from diagnosis_module import predict_and_explain
from assistant_module import get_assistant_response

# --- ENHANCED STYLE/PINK THEME FOR ALL LABELS ---
st.markdown("""
    <style>
        html, body, .stApp { background-color: #ffe6ef !important; }
        .css-18e3th9, .css-1d391kg { background-color: #ffe6ef !important; color: #d6336c !important; }
        .stButton>button { color: white !important; background-color: #d6336c !important; }
        label, .stRadio label, .stCheckbox label, .stTextInput label, .stSelectbox label, .stSlider label, .stForm label { color: #d6336c !important; }
        .css-10trblm, .css-1c7y2kd, .css-1dxn15k, .css-1v0mbdj { color: #d6336c !important; }
        h1, h2, h3, h4, h5, h6, .stMarkdown, .stCaption, .caption { color: #d6336c !important; }
        .st-bw, .stInfo { color: #d6336c !important; }
    </style>
""", unsafe_allow_html=True)

# --- MODES ---
ACCESS_MODES = {"Blind": "blind", "Deaf": "deaf", "Normal": "normal"}

# --- Landing page ---
def show_landing():
    st.title("code pink: Women's Health Anonymous Diagnosis 💗")
    st.markdown('#### Select your accessibility mode:')
    mode = st.radio("", list(ACCESS_MODES.keys()))
    st.session_state['mode'] = ACCESS_MODES[mode]
    st.markdown(
        'Note: This project is a prototype! Results are educational and NOT actual medical advice.',
    )
    st.markdown(
        'Your feedback helps improve future versions.',
    )
    # Simple feedback (landing page)
    if st.button("Continue"):
        st.session_state['page'] = "diagnosis"
    st.markdown("---")
    if st.button("🤔 Was the intro/info clear?"):
        st.success("Thanks for your feedback!")

# --- User accessible interface ---
def show_diagnosis():
    st.header("Health Diagnosis Test")
    mode = st.session_state.get('mode', "normal")
    st.write(f"Accessibility mode: **{mode.capitalize()}**")

    # Accessibility blocks (only once!)
    if mode == "blind":
        st.audio("static/voice_instructions.mp3")
        st.info(
            "This app is compatible with all major screen readers. "
            "Use the Tab key to move between questions. Press Enter to select options. "
            "You may use your OS's built-in screen reader for full audio navigation."
        )
    if mode == "deaf":
        st.video("static/signlanguage.mp4")
        st.caption("Sign language introduction and accessibility support. For more, contact help.")

    # Validation/warning about synthetic dataset
    st.warning("Important: This app uses a synthetic, highly separable dataset for demonstration only. Model accuracy here does NOT reflect real-world medical performance.")

    # Symptom fields (match to your CSV header/features!)
    fields = [
        "age","itching","discharge","abdominal_pain","rash","bleeding",
        "ulcer","swelling","lump","odor","painful_urination"
    ]
    form = st.form("symptom_form")
    user_input = {}
    user_input['age'] = form.slider("Age", 13, 85, 30)
    for field in fields[1:]:
        label = field.replace('_',' ').capitalize()
        if mode == "blind":
            user_input[field] = form.radio(label, ['No', 'Yes'], index=0, key=field+"radio")
        else:
            user_input[field] = form.selectbox(label, ['No', 'Yes'], index=0, key=field+"select")
        user_input[field] = user_input[field] == "Yes"
    extra_details = form.text_area("Describe any extra symptoms (optional):")
    form_submit = form.form_submit_button("Submit for Diagnosis")

    if form_submit:
        predicted, proba, explanation = predict_and_explain(user_input)
        st.success(f"Most Likely Diagnosis: {predicted}")
        # ---- Improved Risk Display ----
        import pandas as pd
        top_risks = sorted(proba.items(), key=lambda x: x[1], reverse=True)[:5]
        st.markdown("#### Top 5 Risk Probabilities:")
        for disease, prob in top_risks:
            st.write(f"- {disease}: {prob*100:.1f}%")

        st.markdown("#### Risk Profile (Bar Chart):")
        st.bar_chart(pd.Series(dict(top_risks)))
        st.caption(f"Diagnosis is based on symptoms entered: {', '.join([k.replace('_',' ') for k,v in user_input.items() if v])}")

        # --- Explanation section ---
        st.markdown("#### Explanation (symptom influence):")
        st.markdown(
            "These values show which symptoms most influenced the result (positive means more risk, negative means less risk):"
        )
        for feature, val in explanation.items():
            st.write(f"- {feature.replace('_',' ').capitalize()}: {val:.2f}")

        st.download_button(
            "Download your result",
            f"Diagnosis: {predicted}\n\nRisk Profile: {proba}\n\nExplanation: {explanation}",
            file_name="diagnosis_result.txt"
        )

        st.info("If your diagnosis is unclear or symptoms are severe, please consult a doctor. This tool is not a substitute for medical examination.")

    # --- Feedback and Help ---
    st.markdown("#### Need help from AI Assistant?")
    msg = st.text_input("Ask the assistant a question or type 'help':")
    if msg:
        response = get_assistant_response(msg, mode)
        st.write("Assistant:", response)

    st.markdown("---")
    if st.button("👍 Was this page helpful?"):
        st.success("Thanks for your feedback!")

# --- Routing logic ---
if "page" not in st.session_state:
    st.session_state["page"] = "landing"
if "mode" not in st.session_state:
    st.session_state["mode"] = "normal"

if st.session_state["page"] == "landing":
    show_landing()
else:
    show_diagnosis()

st.caption("This website is anonymous, accessible, and does not store personal data. For education only. 💗")
