import sqlite3
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import pickle
from langchain.vectorstores import FAISS

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def load_vector_store(file_path):
    with open(file_path, "rb") as file:
        vector_store = pickle.load(file)
    return vector_store
def get_user_conversation_history(user_id):
    conn = sqlite3.connect("user_conversation.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    conversation_history = {}
    for row in cursor.execute("SELECT * FROM user_conversation WHERE user_id = ?", (user_id,)):
        conversation_history.append({"page_content": row[2], "metadata": {}})

    return conversation_history
def store_conversation_history(user_id, history):
    conn = sqlite3.connect("user_conversation.db")
    cursor = conn.cursor()
    for message in history:
        cursor.execute("INSERT INTO user_conversation (user_id, message) VALUES (?, ?)", (user_id, message))
    conn.commit()
    conn.close()


def user_input(user_question, conversation_history):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Perform question-answering
    prompt_template = """
       Answer the question as detailed as possible from the provided context, make sure to provide all the details if not available in context give it accordingly\n\n
       Context:\n {context}?\n
       Question: \n{question}\n

       Answer:
       """
    qa_prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    qa_chain = load_qa_chain(ChatGoogleGenerativeAI(model="gemini-pro"), chain_type="stuff", prompt=qa_prompt)

    if user_question and user_question.strip():
        # Add chunks to the conversation history to use as context
        vector_store = load_vector_store("vector_store.pkl")
        chunks = vector_store.similarity_search(user_question)

        processed_conversation_history = []
        for message in conversation_history:
            if isinstance(message, dict) and "text" in message:
                processed_conversation_history.append(
                    {"page_content": message["text"], "metadata": message.get("metadata", {})})
            elif isinstance(message, str):
                print(
                    f"Skipping unexpected message format: {message}")  # Print error for clarity without breaking execution
            elif isinstance(message, dict):
                processed_conversation_history.append(message)

        processed_conversation_history += chunks

        # Provide the required input key 'input_documents' along with its value
        input_data = {"input_documents": processed_conversation_history, "question": user_question}

        output = qa_chain(input_data)

        response = output["output_text"]

        return response
    else:
        print("User question is empty or contains only whitespace.")
        return ""
