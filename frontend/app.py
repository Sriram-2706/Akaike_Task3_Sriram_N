import streamlit as st
import requests 

st.set_page_config(page_title="QA chatbot", layout="centered")
st.title("Upload pdf or text file and ask only questions related to that file")

if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False


with st.sidebar:
    st.header("Upload Document")
    file = st.file_uploader("Choose a text file", type="pdf")
    if file:
        res = requests.post("http://localhost:5000/upload", files={"file": file})
        if res.ok:
            st.session_state.file_uploaded = True
            st.success("File uploaded and processed!")

if st.session_state.file_uploaded:
    st.subheader("Ask a question")
    query = st.text_input("Your question")
    if st.button("Submit") and query:
        response = requests.post("http://localhost:5000/ask", json={"query": query})
        if response.ok:
            st.success(response.json()["response"])
        else:
            st.error("Error: " + response.json().get("error", "Unknown error"))

