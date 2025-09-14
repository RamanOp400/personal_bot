import streamlit as st
import time
import random
from datetime import datetime
import uuid

# Import our custom modules
from config import *
from database import ChatMemory
from openai_client import OpenAIClient
from image_handler import ImageHandler
from theme_handler import ThemeHandler

# Page configuration
st.set_page_config(
    page_title="Raman - AI Companion 🇮🇳",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the most adorable design ever! 🌸
st.markdown("""
<style>
    /* Import cute fonts */
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One:wght@400&family=Nunito:wght@300;400;600;700&display=swap');
    
    /* Main theme colors */
    :root {
        --primary-pink: #FF6B9D;
        --secondary-pink: #C44569;
        --accent-pink: #F8BBD9;
        --light-pink: #FFF0F5;
        --dark-text: #2D3436;
        --gradient-bg: linear-gradient(135deg, #FFF0F5 0%, #F8BBD9 100%);
    }
    
    /* Hide default Streamlit elements */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Custom header */
    .main-header {
        background: var(--gradient-bg);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(255, 107, 157, 0.2);
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .main-header h1 {
        font-family: 'Fredoka One', cursive;
        font-size: 3rem;
        color: var(--primary-pink);
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        background: linear-gradient(45deg, #FF6B9D, #C44569, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-header p {
        font-family: 'Nunito', sans-serif;
        font-size: 1.2rem;
        color: var(--dark-text);
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
           /* Chat container */
           .chat-container {
               background: transparent;
               border-radius: 20px;
               padding: 1.5rem;
               margin-bottom: 2rem;
               min-height: 500px;
               max-height: 600px;
               overflow-y: auto;
               display: flex;
               flex-direction: column;
               justify-content: flex-end;
           }
    
    /* WhatsApp style messages */
    .message-container {
        display: flex;
        flex-direction: column;
        gap: 15px;
        padding: 10px 0;
    }
    
    /* Message bubbles */
    .user-message {
        background: linear-gradient(135deg, #25D366, #128C7E);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 5px 18px;
        margin: 8px 0;
        margin-left: 25%;
        box-shadow: 0 2px 8px rgba(37, 211, 102, 0.3);
        font-family: 'Nunito', sans-serif;
        font-weight: 500;
        animation: slideInRight 0.3s ease-out;
        max-width: 70%;
        word-wrap: break-word;
        position: relative;
    }
    
    .bot-message {
        background: white;
        color: #2D3436;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 5px;
        margin: 8px 0;
        margin-right: 25%;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        font-family: 'Nunito', sans-serif;
        font-weight: 400;
        animation: slideInLeft 0.3s ease-out;
        border: 1px solid rgba(0, 0, 0, 0.1);
        max-width: 70%;
        word-wrap: break-word;
        position: relative;
    }
    
    .user-message::before {
        content: '';
        position: absolute;
        bottom: 0;
        right: -8px;
        width: 0;
        height: 0;
        border: 8px solid transparent;
        border-left-color: #25D366;
        border-bottom: none;
    }
    
    .bot-message::before {
        content: '';
        position: absolute;
        bottom: 0;
        left: -8px;
        width: 0;
        height: 0;
        border: 8px solid transparent;
        border-right-color: white;
        border-bottom: none;
    }
    
    /* Avatar styling */
    .avatar-container {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .avatar {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        border: 3px solid var(--primary-pink);
        box-shadow: 0 4px 15px rgba(255, 107, 157, 0.3);
        margin-right: 1rem;
        animation: bounce 2s infinite;
    }
    
    /* Input area */
    .stTextInput > div > div > input {
        border-radius: 25px !important;
        border: 2px solid var(--accent-pink) !important;
        padding: 0.75rem 1.5rem !important;
        font-family: 'Nunito', sans-serif !important;
        font-size: 1rem !important;
        background: transparent !important;
        color: #000000 !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-pink) !important;
        box-shadow: 0 0 0 3px rgba(255, 107, 157, 0.2) !important;
        color: #000000 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B9D, #C44569) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.75rem 2rem !important;
        font-family: 'Nunito', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 15px rgba(255, 107, 157, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 107, 157, 0.4) !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: var(--gradient-bg) !important;
    }
    
    /* Animations */
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-10px);
        }
        60% {
            transform: translateY(-5px);
        }
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(255, 107, 157, 0.7);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(255, 107, 157, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(255, 107, 157, 0);
        }
    }
    
    /* Loading animation */
    .loading-dots {
        display: inline-block;
    }
    
    .loading-dots::after {
        content: '';
        animation: dots 1.5s steps(5, end) infinite;
    }
    
    @keyframes dots {
        0%, 20% {
            content: '';
        }
        40% {
            content: '.';
        }
        60% {
            content: '..';
        }
        80%, 100% {
            content: '...';
        }
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .user-message, .bot-message {
            margin-left: 5% !important;
            margin-right: 5% !important;
        }
        
        .chat-container {
            padding: 1rem;
            min-height: 400px;
        }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    
    if 'current_avatar' not in st.session_state:
        st.session_state.current_avatar = ""
    
    if 'current_theme' not in st.session_state:
        st.session_state.current_theme = ""
    
    if 'bot_initialized' not in st.session_state:
        st.session_state.bot_initialized = False
    
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0
    
    if 'enter_pressed' not in st.session_state:
        st.session_state.enter_pressed = False

def display_message(message, is_user=True):
    """Display a chat message with beautiful styling"""
    if is_user:
        st.markdown(f"""
        <div class="user-message">
            <strong>You:</strong><br>
            {message}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bot-message">
            <strong>Raman:</strong><br>
            {message}
        </div>
        """, unsafe_allow_html=True)

def display_avatar_and_welcome():
    """Display avatar and welcome message"""
    image_handler = ImageHandler()
    
    # Get current avatar
    if not st.session_state.current_avatar:
        st.session_state.current_avatar = image_handler.get_random_avatar()
    
    avatar_b64 = image_handler.get_avatar_base64(st.session_state.current_avatar, (100, 100))
    
    if avatar_b64:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <img src="{avatar_b64}" class="avatar" style="width: 100px; height: 100px;">
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Initialize everything
    initialize_session_state()
    memory = ChatMemory()
    openai_client = OpenAIClient()
    image_handler = ImageHandler()
    theme_handler = ThemeHandler()
    
    # Apply amazing multi-image background by default
    theme_handler.apply_theme_to_page()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🇮🇳 Raman 🇮🇳</h1>
        <p>Your AI companion!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for settings
    with st.sidebar:
        st.markdown("### 🎨 Apna Experience Customize Karo")
        
        # User name input
        user_name = st.text_input("Tumhara Naam", value=st.session_state.user_name, placeholder="Apna naam enter karo...")
        if user_name != st.session_state.user_name:
            st.session_state.user_name = user_name
            memory.save_user_preferences(
                st.session_state.session_id,
                user_name=user_name,
                preferred_avatar=st.session_state.current_avatar
            )
        
        # Theme selection
        st.markdown("### 🎨 Apna Theme Choose Karo")
        new_theme = theme_handler.create_theme_selector(st.session_state.current_theme)
        if new_theme != st.session_state.current_theme:
            st.session_state.current_theme = new_theme
            st.rerun()
        
        # Avatar selection
        st.markdown("### 🖼️ Apna Avatar Choose Karo")
        new_avatar = image_handler.create_avatar_selector(st.session_state.current_avatar)
        if new_avatar != st.session_state.current_avatar:
            st.session_state.current_avatar = new_avatar
            memory.save_user_preferences(
                st.session_state.session_id,
                user_name=st.session_state.user_name,
                preferred_avatar=new_avatar
            )
        
        # Stats
        st.markdown("### 📊 Chat ki Stats")
        history = memory.get_conversation_history(st.session_state.session_id)
        st.metric("Messages", len(history))
        
        # Clear chat button
        if st.button("🗑️ Chat History Clear Karo", type="secondary"):
            # This would clear the database - implement if needed
            st.rerun()
    
    # Main chat area
    col1, col2, col3 = st.columns([1, 8, 1])
    
    with col2:
        # Display avatar
        display_avatar_and_welcome()
        
        # Chat container
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Welcome message will be shown in the message display section
        
        # Display messages in WhatsApp style
        st.markdown('<div class="message-container">', unsafe_allow_html=True)
        for message in st.session_state.messages:
            display_message(message["content"], message["role"] == "user")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Always show welcome message if no messages yet
        if not st.session_state.messages:
            welcome_msg = openai_client.generate_welcome_message(st.session_state.user_name)
            st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
            st.session_state.bot_initialized = True
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input with auto-clear functionality
        col_input1, col_input2, col_input3 = st.columns([1, 8, 1])
        with col_input2:
            user_input = st.text_input(
                "Message",
                placeholder="Type your message... 💭",
                key=f"user_input_{st.session_state.input_key}",
                value="",
                label_visibility="collapsed",
                on_change=lambda: setattr(st.session_state, 'enter_pressed', True) if st.session_state.get(f'user_input_{st.session_state.input_key}', '') else None
            )
        
        # Send button and Enter key functionality
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            send_clicked = st.button("Send Karo 💕", type="primary")
            
            # Check for Enter key press or button click
            if st.session_state.get('enter_pressed', False) or (send_clicked and user_input and user_input.strip()):
                # Reset enter_pressed flag
                st.session_state.enter_pressed = False
                # Store the message for processing
                message_to_send = user_input.strip()
                
                # Add user message
                st.session_state.messages.append({"role": "user", "content": message_to_send})
                
                # Get conversation history for context
                history = memory.get_conversation_history(st.session_state.session_id)
                user_prefs = memory.get_user_preferences(st.session_state.session_id)
                
                # Generate bot response
                with st.spinner("Raman soch raha hai..."):
                    bot_response = openai_client.generate_response(
                        message_to_send,
                        history,
                        user_prefs,
                        st.session_state.session_id
                    )
                
                # Add bot response
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                
                # Save to memory
                memory.save_conversation(
                    st.session_state.session_id,
                    message_to_send,
                    bot_response
                )
                
                # Clear the input field by changing the key
                st.session_state.input_key += 1
                st.rerun()
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; color: #666; font-family: 'Nunito', sans-serif;">
        <p>Made by Raman</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
