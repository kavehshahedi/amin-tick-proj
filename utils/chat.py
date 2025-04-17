"""
Chat utilities for the TicketAssist application.

This module provides chat-related functionality for the TicketAssist chatbot.
"""
from typing import Dict, List, Iterator, Any, Optional
from datetime import datetime
import json
import logging
import shelve
from pathlib import Path

import ollama
import streamlit as st

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(encoding="UTF-8", level=logging.INFO)


class ChatHistory:
    """
    Manager for chat history persistence and manipulation.
    
    Handles loading, saving, and clearing of chat message history.
    """
    
    def __init__(self, data_path: str = "data/chat_history") -> None:
        """
        Initialize the chat history manager.
        
        Args:
            data_path: Path to the chat history storage file
        """
        self.data_path = data_path
        # Ensure the data directory exists
        Path(data_path).parent.mkdir(parents=True, exist_ok=True)
    
    def load(self) -> List[Dict[str, Any]]:
        """
        Load chat history from storage.
        
        Returns:
            List of message dictionaries containing chat history
        """
        try:
            with shelve.open(self.data_path) as db:
                return db.get("messages", [])
        except Exception as e:
            logger.error(f"Error loading chat history: {e}")
            return []
    
    def save(self, messages: List[Dict[str, Any]]) -> None:
        """
        Save chat history to storage.
        
        Args:
            messages: List of message dictionaries to save
        """
        try:
            with shelve.open(self.data_path) as db:
                db["messages"] = messages
        except Exception as e:
            logger.error(f"Error saving chat history: {e}")
    
    def clear(self) -> List[Dict[str, Any]]:
        """
        Clear chat history and return a fresh message list.
        
        Returns:
            A new list with just the initial assistant message
        """
        initial_message = [{"role": "assistant", "content": "How may I assist you today?"}]
        self.save([])
        return initial_message
    
    def log_feedback(self, feedback_type: str) -> None:
        """
        Log user feedback on messages.
        
        Args:
            feedback_type: Type of feedback (positive/negative)
        """
        try:
            # Retrieve the last question and answer
            last_messages = json.dumps(st.session_state["messages"][-2:])
            
            # Record the timestamp
            activity = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": "
            
            # Include feedback type and messages
            activity += feedback_type
            activity += ": " + last_messages
            
            # Log the activity
            logger.info(activity)
            
            # Display a confirmation to the user
            st.toast("Thanks for your feedback!", icon="👌")
        except Exception as e:
            logger.error(f"Error logging feedback: {e}")


class LlmService:
    """
    Service for interacting with Language Models.
    
    Handles communication with Ollama and other LLM providers.
    """
    
    def __init__(self, model: str = "llama3.1:8b") -> None:
        """
        Initialize the LLM service.
        
        Args:
            model: Name of the model to use
        """
        self.model = model
    
    def generate_response(self, messages: List[Dict[str, Any]]) -> Iterator[str]:
        """
        Generate streaming response from the LLM.
        
        Args:
            messages: List of message dictionaries to send to the LLM
            
        Yields:
            Tokens from the LLM response as they become available
        """
        try:
            response = ollama.chat(
                model=self.model, 
                stream=True, 
                messages=messages
            )
            
            for partial_resp in response:
                token = partial_resp["message"]["content"]
                # Update the full message in session state
                if "full_message" in st.session_state:
                    st.session_state["full_message"] += token
                yield token
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            yield f"I encountered an error: {str(e)}"