import streamlit as st
import requests  # Sends the calculations back to your Google Form

st.set_page_config(page_title="Self-Esteem Assessment", layout="centered")
st.title("Rosenberg Self-Esteem Scale Component")
st.write("Please select the response that best describes how you feel about each statement.")
st.write("---")

# The 10 standard research questions
questions = [
    "1. I feel that I am a person of worth, at least on an equal plane with others.",
    "2. I feel that I have a number of good qualities.",
    "3. All in all, I am inclined to feel that I am a failure.",
    "4. I am able to do things as well as most other people.",
    "5. I feel I do not have much to be proud of.",
    "6. I take a positive attitude toward myself.",
    "7. On the whole, I am satisfied with myself.",
    "8. I wish I could have more respect for myself.",
    "9. I certainly feel useless at times.",
    "10. At times I think I am no good at all."
]

options = ["Strongly Disagree", "Disagree", "Agree", "Strongly Agree"]
score_map = {"Strongly Disagree": 0, "Disagree": 1, "Agree": 2, "Strongly Agree": 3}
reverse_indices = {2, 4, 7, 8, 9}

user_responses = {}

with st.form("rosenberg_form"):
    for i, question in enumerate(questions):
        st.write(f"**{question}**")
        choice = st.radio(
            label=f"Select your response for question {i+1}",
            options=options,
            index=None,
            key=f"q_{i}",
            label_visibility="collapsed"
        )
        user_responses[i] = choice
        st.write("")

    submit_button = st.form_submit_button(label="Submit Answers & Record Score", type="primary")

if submit_button:
    if None in user_responses.values():
        st.error("⚠️ Please answer all 10 questions before submitting!")
    else:
        total_score = 0
        for i, choice in user_responses.items():
            numerical_value = score_map[choice]
            if i in reverse_indices:
                scored_points = 3 - numerical_value
            else:
                scored_points = numerical_value
            total_score += scored_points

        # Determine the evaluation range
        if total_score < 15:
            interpretation = "Low self-esteem"
        elif 15 <= total_score <= 25:
            interpretation = "Normal/Average range"
        else:
            interpretation = "High self-esteem"

        # --- SUBMIT DIRECTLY TO REBECCA'S GOOGLE FORM DATABASE ---
        form_url = "https://google.com"
        
        # Mapping calculated values to your exact form entries
        form_data = {
            "entry.103888205": f"{total_score} / 30",
            "entry.787960835": interpretation
        }
        
        try:
            # Secretly posts the Rosenberg results to your Google Form
            requests.post(form_url, data=form_data)
            st.success("🎉 Your Rosenberg Score has been securely calculated and logged!")
        except Exception:
            st.error("⚠️ Connection error. Score calculated locally but could not upload.")

        # Show visual confirmation on screen
        st.write("---")
        st.metric(label="Your Total Rosenberg Score", value=f"{total_score} / 30")
        st.info(f"**Interpretation:** {interpretation}")
        st.write("Thank you! You can close this window now.")
