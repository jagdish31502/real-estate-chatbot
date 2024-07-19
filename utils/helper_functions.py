import os
import pandas as pd
import fitz
from .embedding_model import *
from .llm_model import *
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.node_parser import SentenceSplitter
from llama_index.readers.file import (DocxReader, PDFReader, FlatReader, PagedCSVReader)
from llama_index.core import Document
import chromadb
from PIL import Image
import pytesseract

# Set up pytesseract for OCR
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Function for reading .xlsx file
def read_xlsx(filepath):
    try:
        df = pd.read_excel(filepath)
        return df.to_string() 
    except Exception as e:
        print(f"Failed to read Excel file {filepath} with error: {e}")
        return ""

# Function to extract text from images using pytesseract
def extract_text_from_images_pytesseract(filepath):
    try:
        text_content = " "
        if filepath.lower().endswith(('.jpg', '.jpeg', '.png')):
            response = pytesseract.image_to_string(Image.open(filepath))
            text_content += response + "\n"
        return text_content
    
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return f"Error extracting text from image: {e}"

# Function to process files in a directory
def load_documents(file_paths):
    try:
        all_documents = []
        for filepath in file_paths:
            file_extension = os.path.splitext(filepath)[1].lower()
            filename = os.path.basename(filepath)
            
            # Loading PDF, DOCX file, CSV files
            if file_extension in [".pdf",".docx",".csv"]:
                documents = SimpleDirectoryReader(
                    input_files=[filepath], required_exts=[".pdf",".docx",".csv"]
                ).load_data()
                all_documents.extend(documents)
            
            # Loading JPG, JPEG, and PNG files
            if file_extension in [".jpg", ".jpeg", ".png"]:
                image_text = extract_text_from_images_pytesseract(filepath)
                document = [Document(
                        text=image_text,
                        metadata={
                            "file_name": filename,
                            "file_path": filepath,
                            "author": "LlamaIndex",
                        },
                        excluded_llm_metadata_keys=[filepath],
                        metadata_seperator="::",
                        metadata_template="{key}=>{value}",
                        text_template="Metadata: {metadata_str}\n-----\nContent: {content}",
                    )]
                all_documents.extend(document)
            
            # Loading excel files
            if file_extension == ".xlsx":
                xlsx_text = read_xlsx(filepath)
                document = Document(
                        text=xlsx_text,
                        metadata={
                            "file_name": filename,
                            "file_path": filepath,
                            "author": "LlamaIndex",
                        },
                        excluded_llm_metadata_keys=[filepath],
                        metadata_seperator="::",
                        metadata_template="{key}=>{value}",
                        text_template="Metadata: {metadata_str}\n-----\nContent: {content}",
                    )
                all_documents.append(document)
        return all_documents
    except Exception as e:
        print(f"Failed to load documents from {filepath} with error: {e}")
        return f"Failed to load documents from {filepath} with error: {e}"

# saving embeddings into Chromadb
def save_to_chromadb(documents, persist_dir="./chroma_db"):
    try:
        embed_model = embedding_model()
        chroma_client = chromadb.PersistentClient(path=persist_dir)
        chroma_collection = chroma_client.get_or_create_collection(name='real_estate_embeddings')
        node_parser = SentenceSplitter(chunk_size=1000, chunk_overlap=200)
        vector_store = ChromaVectorStore(chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, embed_model=embed_model, node_parser=node_parser, persist_dir=persist_dir)
        index.storage_context.persist(persist_dir)
    
    except Exception as e:
        print(f"Failed to save embeddings to Chromadb with error: {e}")
        return f"Failed to save embeddings to Chromadb with error: {e}"

# retrieving indexing from the chromadb
def load_from_chromadb():
    try:
        db = chromadb.PersistentClient(path="./chroma_db")
        chroma_collection = db.get_or_create_collection("real_estate_embeddings")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        index = VectorStoreIndex.from_vector_store(
            vector_store,
            embed_model=embedding_model(),
        )
        return index
    
    except Exception as e:
        print(f"Failed to load embeddings from Chromadb with error: {e}")
        return f"Failed to load embeddings from Chromadb with error: {e}"