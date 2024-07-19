# Real Estate Chatbot

## Overview

This project is a chatbot designed for a real estate website. It allows users to upload documents in various formats such as `.pdf`, `.docx`, `.xlsx`, `.jpg`, `.jpeg`, and `.png`, and interact with the content through a chat interface.

## Technology Used

- **LlamaIndex**: For indexing and querying document chunks.
- **Gemini Model**: For generating responses.
- **Huggingface Embedding Model**: For creating embeddings of document chunks.
- **Pytesseract**: For extracting text from images.
- **Flask**: For backend API services.
- **ChromaDB**: For storing embeddings.
- **Streamlit**: For frontend interface.

## How It Works

1. **Document Upload**: Users upload documents using Streamlit at the frontend.
2. **Document Processing**: The backend (Flask API) processes these documents, converts them into chunks, and creates embeddings using the Huggingface embedding model.
3. **Embedding Storage**: The embeddings are stored in ChromaDB.
4. **Query Handling**: When a user asks a question, the system retrieves relevant embeddings from ChromaDB using a retriever and query engine, and generates a response using the Gemini model.

## API Endpoints

- **/file_upload**: Endpoint to upload documents.
- **/ask_question**: Endpoint to ask questions and get responses based on the uploaded documents.

## Setup Instructions

    create .env file that contains:
    ``` bash
    # Huggingface embedding model
    EMBED_MODEL = "sentence-transformers/all-mpnet-base-v2"

    # GOOGLE
    GOOGLE_API_KEY = "google api key" 
    GEMINI_MODEL = "models/gemini-pro"

    # Background Image
    BACKGROUND_IMAGE = "utils\images\bg-image.jpg"
    ```

### Pytesseract Setup

For processing images, ensure Pytesseract is installed and properly configured.

1. **Download Pytesseract**:
   - Download Pytesseract from [here](https://github.com/UB-Mannheim/tesseract/wiki).

2. **Configure Pytesseract**:
   - Add the following line in your code to call Pytesseract on your machine:
     ```python
     pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
     ```

### Installation

**Clone the repository**:
```bash
git clone git@github.com:jagdish31502/real-estate-chatbot.git
cd real-estate-chatbot
```

**Install dependencies:**

``` bash
pip install -r requirements.txt
```

**Run the application:**

``` bash
streamlit run stramlit.py
python run app.py
```
**NOTE:** both server are running in different terminal (Flask for backend, and streamlit for frontend.)

**Usage**

**Upload Documents:**

- Go to the Streamlit interface and upload documents in any supported format.

**Ask Questions:**

- Use the chat interface to ask questions about the uploaded documents.