import requests
import streamlit as st

def render_feedback(api_url, prompt, response):
    st.subheader("Was this response helpful?")

    with st.form("feedback_form"):
        rating = st.radio(
            "Select your feedback:",
            ["positive", "negative"],
            horizontal=True
        )

        comment = st.text_area(
            "Additional feedback (optional)"
        )

        submitted = st.form_submit_button("Submit Feedback")

    if submitted:
        try:
            result = requests.post(
                f"{api_url}/feedback",
                json={
                    "prompt": prompt,
                    "response": response,
                    "rating": rating,
                    "comment": comment
                },
                timeout=30
            )

            result.raise_for_status()
            st.success("Thank you for your feedback!")

        except requests.RequestException as e:
            st.error(f"Could not submit feedback: {e}")