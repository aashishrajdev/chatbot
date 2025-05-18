import streamlit as st
import google.generativeai as genai
import os

# Page configuration must be the first Streamlit command
st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* Base theme colors */
    :root {
        --background-color: var(--background-color);
        --text-color: var(--text-color);
        --user-message-bg: var(--user-message-bg);
        --assistant-message-bg: var(--assistant-message-bg);
    }

    /* Light mode (default) */
    [data-theme="light"] {
        --background-color: #FFFFFF;
        --text-color: #000000;
        --user-message-bg: #F0F2F6;
        --assistant-message-bg: #E3E6EA;
    }

    /* Dark mode */
    [data-theme="dark"] {
        --background-color: #0E1117;
        --text-color: #FFFFFF;
        --user-message-bg: #1E2132;
        --assistant-message-bg: #2D3347;
    }

    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #F0F2F6;
        color: #000000;
    }
    .assistant-message {
        background-color: #E3E6EA;
        color: #000000;
    }
    .stButton>button {
        border-radius: 20px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        background-color: var(--background-color);
        color: var(--text-color);
    }

    .stButton>button:hover {
        transform: scale(1.05);
        opacity: 0.9;
    }

    .stTextInput>div>div>input {
        border-radius: 20px;
        padding: 0.5rem 1rem;
        background-color: var(--background-color);
        color: var(--text-color);
    }

    .stSelectbox>div>div>div {
        border-radius: 20px;
        background-color: var(--background-color);
        color: var(--text-color);
    }

    /* Ensure text in chat messages is readable */
    .stChatMessageContent {
        color: var(--text-color);
    }
    </style>
""", unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = ""
    
if "model" not in st.session_state:
    st.session_state.model = None

with st.sidebar:
    st.header("Configuration")
    
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    
    if api_key:
        st.session_state.gemini_api_key = api_key
        try:
            genai.configure(api_key=api_key)
            
            models = [m.name for m in genai.list_models() if 'gemini' in m.name.lower()]
            
            if models:
                selected_model = st.selectbox("Select a model:", models)
                model = genai.GenerativeModel(selected_model)
                st.session_state.model = model
                st.success("API key is valid! Model selected.")
            else:
                st.error("No Gemini models found.")
                
        except Exception as e:
            st.error(f"Error with API key: {str(e)}")
    
    st.divider()
    st.markdown("© 2025 [rajaashishdev](https://github.com/aashishrajdev)")

st.title("Gemini AI Chatbot")
st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_prompt := st.chat_input("Ask something..."):
    if st.session_state.gemini_api_key and st.session_state.model:
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        with st.chat_message("user"):
            st.write(user_prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.model.generate_content(user_prompt)
                    response_text = response.text
                    st.write(response_text)
                    
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                except Exception as e:
                    error_message = f"Error generating response: {str(e)}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})
    else:
        st.error("Please enter a valid Gemini API key in the sidebar.")
