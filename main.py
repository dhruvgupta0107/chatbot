import streamlit as st
from openai import OpenAI

# Initialize the OpenAI client for Hugging Face API
client = OpenAI(
    base_url="https://api-inference.huggingface.co/v1/",
    api_key="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"  # Replace with your Hugging Face API key
)

# Function to send message to the Hugging Face API
def send_message(user_input):
    if user_input:
        # Add user message to the chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Send the message to the Hugging Face API
        try:
            stream = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
                messages=st.session_state.messages,
                max_tokens=500,
                stream=True
            )
            
            # Collect the bot's response
            bot_response = ""
            for chunk in stream:
                chunk_content = chunk.choices[0].delta.content
                if chunk_content:
                    bot_response += chunk_content
            
            # Add bot response to the chat history
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Streamlit UI
st.title("Chatbot Web App")
st.write("Welcome to the chatbot! Type your message below.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("Type your message here...")

# Send message when user inputs something
if user_input:
    send_message(user_input)
    # Rerun the app to update the chat history
    st.rerun()
