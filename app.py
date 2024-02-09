# main.py
import streamlit as st
from chatbot import user_input, get_user_conversation_history, store_conversation_history
from database import init_database, register_user, authenticate_user, get_user_conversation_history, store_conversation_history
from langchain.vectorstores import FAISS

def main():
    init_database()
    st.markdown('<style>' + open('../../Minerva-main-20240208T074956Z-001/Minerva-main/styles.css').read() + '</style>', unsafe_allow_html=True)

    st.subheader("Ask me about mining laws!")

    # Sidebar authentication
    st.sidebar.image("minerva.png")
    st.sidebar.title("")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Register", key="register_button"):
        register_user(username, password)
        st.sidebar.success("User registered successfully!")

    if st.sidebar.button("Login", key="login_button"):
        user = authenticate_user(username, password)
        if user:
            st.session_state["authenticated"] = True
            st.session_state["user_id"] = user[0]
            st.sidebar.success(f"Logged in as {user[1]}")
        else:
            st.sidebar.warning("Invalid credentials")

    if "authenticated" not in st.session_state:
        st.write("Please log in to use the chatbot.")
        st.stop()

    # Main chatbot functionality
    st.subheader("Ask a question")
    user_question = st.text_area("You: ", key="user_input")

    if st.button("Send"):
        if user_question:
            response = user_input(user_question, get_user_conversation_history(st.session_state["user_id"]))
            st.write("Bot: ", response)

            conversation_history = get_user_conversation_history(st.session_state["user_id"])
            conversation_history.append(user_question)
            conversation_history.append(response)

            # Display the conversation history
            st.subheader("Conversation history")

            for message in conversation_history:
                st.write(message)

            # Store the conversation history
            store_conversation_history(st.session_state["user_id"], conversation_history)

if __name__ == "__main__":
    main()