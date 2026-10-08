import os

import requests
import streamlit as st
from dotenv import load_dotenv

from feedback_ui import render_feedback

load_dotenv()

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
API_KEY = os.getenv("API_SECURITY_KEY")

st.title("AI Text Assistant")

if not API_KEY:
    st.error("API_SECURITY_KEY is not configured.")
    st.stop()

headers = {"X-API-Key": API_KEY}

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
                headers=headers,
                json={"prompt": prompt},
                timeout=60,
            )
            response.raise_for_status()

            data = response.json()
            st.session_state.prompt = prompt
            st.session_state.response = data["response"]

        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 429:
                st.error("Rate limit exceeded. Please wait and try again.")
            elif e.response is not None and e.response.status_code == 401:
                st.error("API authentication failed.")
            else:
                st.error(f"API request failed: {e}")
        except requests.RequestException as e:
            st.error(f"Could not connect to the FastAPI backend: {e}")

if st.session_state.response:
    st.subheader("Response")
    st.write(st.session_state.response)

    render_feedback(
        API_URL,
        st.session_state.prompt,
        st.session_state.response,
        headers,
    )
