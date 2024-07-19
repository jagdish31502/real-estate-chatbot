import streamlit as st
import os
import requests
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

upload_folder = 'uploaded_data'
os.makedirs(upload_folder, exist_ok=True)

# Function for getting base64 image
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error(f"Error loading background image: {e}")
        return None
    
# Function for saving uploaded documents
def save_uploadedfile(uploaded_file):
    try:
        file_path = os.path.join(upload_folder, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        return file_path
    except Exception as e:
        st.error(f"Error saving uploaded file: {e}")
        return None
    
# Function for uploading documents
def upload_files(file_paths):
    url = "http://127.0.0.1:5000/file_upload"
    files = [('file', (os.path.basename(file_path), open(file_path, 'rb'), 'application/octet-stream')) for file_path in file_paths]
    try:
        response = requests.post(url, files=files)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while uploading the files: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None
    
# Function for document upload and processing
def document_upload_page():
    base64_image = get_base64_image(os.getenv("BACKGROUND_IMAGE"))
    if base64_image:
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: url(data:image/jpg;base64,{base64_image});
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    st.markdown("# Upload Documents 📎")
    uploaded_files = st.file_uploader('Upload multiple files', type=["pdf", "png", "jpg", "jpeg", "docx", "xlsx"], accept_multiple_files=True)

    if uploaded_files:
        file_paths = []
        for uploaded_file in uploaded_files:
            file_path = save_uploadedfile(uploaded_file)
            if file_path:
                file_paths.append(file_path)
        
        if st.button("Upload All 🚀"):
            with st.spinner("Uploading files..."):
                response = upload_files(file_paths)
                if response and 'message' in response:
                    st.success(response['message'])
                elif response and 'error' in response:
                    st.error(response['error'])
    else:
        st.write("Please upload files to proceed.")

# Function for asking questions to uploaded documents
def ask_question_page():
    st.markdown("## Real Estate Chatbot 🤖")
    st.markdown("#### ask anything from the uploaded documents")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to the user input
    if prompt := st.chat_input("Ask a question about the documents..."):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Call Flask API to get the response
        with st.spinner("Generating Answer..."):
            # Call Flask API to get the response
            try:
                response = requests.post("http://127.0.0.1:5000/ask_question", json={"question": prompt})
                response.raise_for_status()
                answer = response.json().get("answer", "No answer provided.")
            except requests.exceptions.RequestException as e:
                answer = f"An error occurred: {e}"
            except Exception as e:
                answer = f"Unexpected error: {e}"

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(answer)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": answer})

