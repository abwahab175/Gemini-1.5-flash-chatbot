import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Initialize the Generative Model
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to get response from the model
# Gemini uses 'model' for assistant; Streamlit uses 'assistant'


def role_to_streamlit(role):
    if role == "model":
        return "assistant"
    else:
        return role


# Add a Gemini Chat history object to Streamlit session state
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Display Form Title
st.title("Chat with Google Gemini-1.5-flash!")

# Display chat messages from history above current input box
for message in st.session_state.chat.history:
    with st.chat_message(role_to_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Accept user's next message, add to context, resubmit context to Gemini
if prompt := st.chat_input("I possess a well of knowledge. What would you like to know?"):
    # Display user's last message
    st.chat_message("user").markdown(prompt)

    # Send user entry to Gemini and read the response
    response = st.session_state.chat.send_message(prompt)

    # Display last
    with st.chat_message("assistant"):
        st.markdown(response.text)
