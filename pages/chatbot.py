"""
TicketAssist Chatbot Page

This module provides the chat interface for the TicketAssist application,
allowing users to interact with a Language Model for ticket assistance.
"""
from typing import Dict, List, Any, Optional
import streamlit as st
from streamlit_float import float_init
import extra_streamlit_components as stx
from streamlit_feedback import streamlit_feedback

# Import custom utilities
from utils.chat import ChatHistory, LlmService


class ChatbotUI:
    """
    User interface for the TicketAssist chatbot.
    
    Provides the UI components and interaction logic for the chat page.
    """
    
    # Constants for avatar icons
    USER_AVATAR = "🧑‍💻"
    BOT_AVATAR = "🤖"
    
    def __init__(self) -> None:
        """Initialize the chatbot UI components and services."""
        self.configure_page()
        self.chat_history = ChatHistory()
        self.llm_service = LlmService()
        
        # Initialize float feature for UI enhancements
        float_init()
        
        # Setup cookie manager
        self.cookie_manager = stx.CookieManager(key="cookie_manager")
        
        # Initialize or load chat history
        if "messages" not in st.session_state:
            st.session_state.messages = self.chat_history.load()
            if not st.session_state.messages:
                st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]
    
    def configure_page(self) -> None:
        """Configure the Streamlit page settings for the chatbot."""
        st.set_page_config(
            page_title="TicketAssist - Q/A",
            page_icon="💬",
            initial_sidebar_state="expanded",
        )
        
        st.title("💬 TicketAssist Chatbot")
    
    def setup_sidebar(self) -> Dict[str, Any]:
        """
        Setup the sidebar with model selection and parameters.
        
        Returns:
            Dict containing model parameters and API tokens
        """
        with st.sidebar:
            st.title('TicketAssist Chatbot')
            
            # API token configuration
            if 'REPLICATE_API_TOKEN' in st.secrets:
                st.success('Connected to ELI API', icon='✅')
                replicate_api = st.secrets['REPLICATE_API_TOKEN']
            else:
                replicate_api = st.text_input('Enter Replicate API token:', type='password')
                if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
                    st.warning('Please enter your credentials!', icon='⚠️')
                else:
                    st.success('Proceed to entering your prompt message!', icon='👉')
            
            # Model selection
            st.subheader('Models and parameters')
            selected_model = st.sidebar.selectbox(
                'Choose a model', 
                ['Llama3-8B', 'Llama2-13B'], 
                key='selected_model'
            )
            
            # Initialize model with a default value
            model = 'llama3.1:8b'
            
            if selected_model == 'Llama3-8B':
                model = 'llama3.1:8b'
                self.llm_service.model = model
            
            # Model parameters
            temperature = st.sidebar.slider(
                'temperature', 
                min_value=0.01, 
                max_value=5.0, 
                value=0.1, 
                step=0.01
            )
            
            top_p = st.sidebar.slider(
                'top_p', 
                min_value=0.01, 
                max_value=1.0, 
                value=0.9, 
                step=0.01
            )
            
            max_length = st.sidebar.slider(
                'max_length', 
                min_value=64, 
                max_value=4096, 
                value=512, 
                step=8
            )
            
            seed = st.number_input(
                'Seed', 
                min_value=0, 
                max_value=10000, 
                value=101, 
                step=1
            )
            
            st.markdown('📖 Learn more [here]()!')
            
            # Clear history button
            st.button('Clear Chat History', on_click=self.clear_chat_history)
            
            return {
                "api_token": replicate_api,
                "model": model,
                "temperature": temperature,
                "top_p": top_p,
                "max_length": max_length,
                "seed": seed
            }
    
    def clear_chat_history(self) -> None:
        """Clear the chat history and reset the conversation."""
        st.session_state.messages = self.chat_history.clear()
    
    def display_chat_messages(self) -> None:
        """Display the chat message history in the UI."""
        for message in st.session_state.messages:
            avatar = self.USER_AVATAR if message["role"] == "user" else self.BOT_AVATAR
            st.chat_message(message["role"], avatar=avatar).write(message["content"])
    
    def handle_user_input(self, api_token: str) -> None:
        """
        Process user input and generate responses.
        
        Args:
            api_token: API token for the LLM service
        """
        if prompt := st.chat_input("Ask anything", max_chars=150, disabled=not api_token):
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user", avatar=self.USER_AVATAR).write(prompt)
            
            # Generate assistant response
            with st.spinner("Thinking..."):
                st.session_state["full_message"] = ""
                
                # Stream the response
                st.chat_message("assistant", avatar=self.BOT_AVATAR).write_stream(
                    self.llm_service.generate_response
                )
                
                # Add complete response to history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": st.session_state["full_message"]
                })
            
            # Save chat history
            self.chat_history.save(st.session_state.messages)
    
    def display_feedback_widget(self) -> None:
        """Display the feedback widget for the last assistant message."""
        if st.session_state.messages and len(st.session_state.messages) > 1:
            feedback = streamlit_feedback(
                feedback_type="faces",
                optional_text_label="[Optional] Please provide an explanation",
                key=f"feedback_{len(st.session_state.messages)}",
            )
            
            if feedback:
                st.toast("Feedback recorded!", icon="📝")
                # Log the feedback
                feedback_type = "positive" if feedback.get("score", 0) > 0 else "negative"
                self.chat_history.log_feedback(feedback_type)
    
    def run(self) -> None:
        """
        Run the chatbot UI application.
        
        This method sets up the UI components and handles the interaction flow.
        """
        # Setup sidebar and get parameters
        params = self.setup_sidebar()
        
        # Display existing chat messages
        self.display_chat_messages()
        
        # Handle user input
        self.handle_user_input(params["api_token"])
        
        # Display feedback widget
        self.display_feedback_widget()


def main() -> None:
    """Main function to initialize and run the chatbot page."""
    chatbot = ChatbotUI()
    chatbot.run()


if __name__ == "__main__":
    main()