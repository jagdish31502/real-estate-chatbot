from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.embedding_model import *
from utils.llm_model import *
from utils.helper_functions import *
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
CORS(app)

# Define the upload folder path
UPLOAD_FOLDER = 'uploaded_data'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# API for uploading files
@app.route('/file_upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                return jsonify({'error': 'No file part in the request'}), 400
            
            files = request.files.getlist('file')
            if not files:
                return jsonify({'error': 'No files uploaded'}), 400

            file_paths = []
            for file in files:
                if file.filename == '':
                    return jsonify({'error': 'No selected file'}), 400
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)
                file_paths.append(file_path)
                
            documents = load_documents(file_paths)
            save_to_chromadb(documents)
            return jsonify({'message': 'Documents are uploaded and processed successfully.'}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

# API for asking questions to the uploaded files.      
@app.route('/ask_question', methods=['POST'])
def ask_question():
    if request.method == 'POST':
        try:
            data = request.get_json()
            question = data['question']
            if not question:
                return jsonify({"error": "No question provided"}), 400
            index = load_from_chromadb()
            llm = llm_model()
            query_engine = index.as_query_engine(llm)
            answer = query_engine.query(question)
            return jsonify({"answer": answer.response}), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5000 , debug=False)
