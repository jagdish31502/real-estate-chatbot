from utils.streamlit_functions import *
import streamlit as st

# Main function for the app
def main():
    st.sidebar.title("Real Estate Chat bot")
    page = st.sidebar.radio("Go to...", ["Upload Documents 📂", "Ask a Question ❓"])

    st.sidebar.title("Chat Options")
    if st.sidebar.button("Clear Chat History 🧹"):
        st.session_state.messages = []
    if st.sidebar.button("New Chat 🆕"):
        st.session_state.messages = []
        st.sidebar.success("Started a new chat.")
    if st.sidebar.button("Previous Chat History ⏮️"):
        st.sidebar.markdown("### Previous Chats")
        for message in st.session_state.get("messages", []):
            st.sidebar.write(f"{message['role'].capitalize()}: {message['content']}")

    if page == "Upload Documents 📂":
        document_upload_page()
    elif page == "Ask a Question ❓":
        ask_question_page()

if __name__ == '__main__':
    main()
