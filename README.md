# Minerva
This repository contains the code for a Streamlit-based chatbot application that uses Langchain and Google Generative AI for question-answering. The application allows users to ask questions about mining laws and regulations by interacting with a conversational interface.

**Folder Structure
**
'app.py': The main Streamlit application file.
'chatbot.py': Contains functions for handling user input, conversation history, and question-answering.
'database.py': Contains functions for initializing and managing the SQLite database for storing user information and conversation history.
'processing.py': Contains functions for processing the mining laws PDF and generating a vector store for question-answering.
'storage.py': Contains functions for fetching conversation history from the database.
'style.css': Custom Streamlit application stylesheet.
'mining.pdf': The mining laws PDF file used as the knowledge base for the chatbot.
Dependencies
To run the application, make sure you have the following dependencies installed:

**Streamlit**
SQLite3
Langchain
Google Generative AI
Pandas
Numpy
PDF Plumber
Pickle
You can install these dependencies using the provided requirements.txt file:


pip install -r requirements.txt
In addition, you need to set up a Google API key to use the Google Generative AI model. Save the API key in a .env file with the variable name GOOGLE_API_KEY.

**Usage**
Run the application using the following command:

streamlit run app.py
The Streamlit application will open in your web browser. You can ask questions in the "Ask a question" text area and send them using the "Send" button.

The chatbot will display the answer to your question below the input area. The conversation history will also be displayed on the right side of the page.

To register a new user, enter a username and password in the sidebar and click the "Register" button.

To log in, enter the username and password in the sidebar and click the "Login" button.

**Folder Structure Explanation
**app.py is the main Streamlit application file. It initializes the database, loads the conversation history, and handles user input.
chatbot.py contains functions for handling user input, conversation history, and question-answering.
database.py contains functions for initializing and managing the SQLite database for storing user information and conversation history.
processing.py contains functions for processing the mining laws PDF and generating a vector store for question-answering.
storage.py contains functions for fetching conversation history from the database.
style.css is a custom Streamlit application stylesheet.
mining.pdf is the mining laws PDF file used as the knowledge base for the chatbot.
**License
**This project is licensed under the MIT License.
