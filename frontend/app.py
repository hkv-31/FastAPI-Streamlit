import streamlit as st
import requests
from feedback_ui import render_feedback

API_URL = "http://127.0.0.1:8000"

st.title("AI Text Assistant")

if "prompt" not in st.session_state:
    st.session_state.prompt = ""

if "response" not in st.session_state:
    st.session_state.response = ""

prompt = st.text_area("Enter your question:", value=st.session_state.prompt)

if st.button("Generate"):
    if not prompt.strip():
        st.warning("Please enter a question.")
    else:
        try:
            response = requests.post(
                f"{API_URL}/generate",
                json={"prompt": prompt},
                timeout=60
            )
            response.raise_for_status()

            data = response.json()

            st.session_state.prompt = prompt
            st.session_state.response = data["response"]

        except requests.RequestException as e:
            st.error(f"Could not connect to the FastAPI backend: {e}")

if st.session_state.response:
    st.subheader("Response")
    st.write(st.session_state.response)

    render_feedback(
        API_URL,
        st.session_state.prompt,
        st.session_state.response
    )