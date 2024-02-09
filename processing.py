import pickle
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import pdfplumber
from langchain.vectorstores import FAISS
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
def save_vector_store(vector_store, file_path):
    with open(file_path, "wb") as file:
        pickle.dump(vector_store, file)


def get_pdf_text(pdf_path):
    text=""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text



def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    return vector_store


pdf_path = r"C:\Users\USER\Downloads\Chat-Gemini-master\Chat-Gemini-master\mining.pdf"
text=get_pdf_text(pdf_path)
chunks=get_text_chunks(text)
vector_store=get_vector_store(chunks)
save_vector_store(vector_store,"vector_store.pkl")
