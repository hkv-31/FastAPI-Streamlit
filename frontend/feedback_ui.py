import requests
import streamlit as st


def render_feedback(api_url, prompt, response, headers):
    st.subheader("Was this response helpful?")

    with st.form("feedback_form"):
        rating = st.radio(
            "Select your feedback:",
            ["positive", "negative"],
            horizontal=True,
        )
        comment = st.text_area("Additional feedback (optional)")
        submitted = st.form_submit_button("Submit Feedback")

    if submitted:
        try:
            result = requests.post(
                f"{api_url}/feedback",
                headers=headers,
                json={
                    "prompt": prompt,
                    "response": response,
                    "rating": rating,
                    "comment": comment,
                },
                timeout=30,
            )
            result.raise_for_status()
            st.success("Thank you for your feedback!")

        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 429:
                st.error("Rate limit exceeded. Please wait and try again.")
            elif e.response is not None and e.response.status_code == 401:
                st.error("API authentication failed.")
            else:
                st.error(f"Feedback request failed: {e}")
        except requests.RequestException as e:
            st.error(f"Could not submit feedback: {e}")
