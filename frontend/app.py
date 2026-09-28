import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/generate"

st.title("AI Text Assistant")
prompt = st.text_area("Enter your question:")

if st.button("Generate"):
    if not prompt.strip():
        st.warning("Please enter a question.")
    else:
        try:
            response = requests.post(API_URL, json={"prompt": prompt}, timeout=60)
            response.raise_for_status()
            data = response.json()
            st.subheader("Response")
            st.write(data["response"])
        except requests.RequestException as e:
            st.error(f"Could not connect to the FastAPI backend: {e}")
