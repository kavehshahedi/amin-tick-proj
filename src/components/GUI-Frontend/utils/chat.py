"""
Chat utilities for the TicketAssist application.

This module provides chat-related functionality for the TicketAssist chatbot.
"""
from typing import Dict, List, Iterator, Any, Optional
from datetime import datetime
import json
import logging
import shelve
import os
from pathlib import Path
import requests
import time

import ollama
import streamlit as st

from utils.config import config

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
    
    def __init__(self, model: Optional[str] = None) -> None:
        """
        Initialize the LLM service.
        
        Args:
            model: Name of the model to use, defaults to the configured model
        """
        self.model = model or config.get("LLM_MODEL", "llama3.1:8b")
        self.temperature = config.get("LLM_TEMPERATURE", 0.1)
        self.max_tokens = config.get("LLM_MAX_TOKENS", 512)
        self.top_p = config.get("LLM_TOP_P", 0.9)
        
        # Configure Ollama API host if specified
        ollama_api_host = config.get("OLLAMA_API_HOST")
        if ollama_api_host:
            os.environ["OLLAMA_HOST"] = ollama_api_host
            logger.info(f"Using custom Ollama API host: {ollama_api_host}")

    # Add this code to utils/chat.py in the LlmService class

    def wait_for_ollama(self, max_retries=10, retry_interval=5):
        """
        Wait for Ollama service to be available.
        
        Args:
            max_retries: Maximum number of connection attempts
            retry_interval: Seconds to wait between retries
            
        Returns:
            bool: True if Ollama is available, False otherwise
        """
        ollama_url = os.environ.get("OLLAMA_API_HOST", "http://localhost:11434")
        health_url = f"{ollama_url}/api/version"
        
        logger.info(f"Checking Ollama availability at {health_url}")
        
        for attempt in range(max_retries):
            try:
                response = requests.get(health_url, timeout=5)
                if response.status_code == 200:
                    logger.info(f"Ollama is available: {response.json()}")
                    return True
            except Exception as e:
                logger.warning(f"Attempt {attempt+1}/{max_retries}: Ollama not available yet. Error: {e}")
            
            logger.info(f"Waiting {retry_interval} seconds before next attempt...")
            time.sleep(retry_interval)
        
        logger.error(f"Failed to connect to Ollama after {max_retries} attempts")
        return False

    def generate_response(self, messages: List[Dict[str, Any]]) -> Iterator[str]:
        """
        Generate streaming response from the LLM.
        
        Args:
            messages: List of message dictionaries to send to the LLM
            
        Yields:
            Tokens from the LLM response as they become available
        """
        # Try to ensure Ollama is available
        if not self.wait_for_ollama():
            yield "I'm having trouble connecting to the language model service. Please try again in a few moments."
            return
        
        try:
            logger.info(f"Generating response with model={self.model}, temp={self.temperature}")
            
            response = ollama.chat(
                model=self.model, 
                stream=True, 
                messages=messages,
                options={
                    "temperature": self.temperature,
                    "top_p": self.top_p,
                    "num_predict": self.max_tokens
                }
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