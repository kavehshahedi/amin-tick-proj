"""
Authentication module for TicketAssist application.

This module provides authentication utilities and session management 
for the TicketAssist application.
"""
from typing import Callable, Dict, Optional, Tuple, Any
import streamlit as st

from utils.config import config


class Authenticator:
    """
    Authentication manager for TicketAssist application.
    
    Handles user authentication, session management, and related utilities.
    """
    
    def __init__(self) -> None:
        """Initialize the authenticator with default settings."""
        # Initialize session state if needed
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False
    
    def verify_credentials(self) -> None:
        """
        Verify provided credentials and update authentication state.
        
        This method checks if the provided username and password match 
        configured credentials and updates the session state accordingly.
        """
        # Get configured credentials from environment or Docker secrets
        valid_username = config.get("STREAMLIT_AUTH_USER", "admin")
        valid_password = config.get("STREAMLIT_AUTH_PASSWORD", "admin")
        
        if (st.session_state["user"].strip() == valid_username and 
            st.session_state["passwd"].strip() == valid_password):
            st.session_state["authenticated"] = True
        else:
            st.session_state["authenticated"] = False
            
            if not st.session_state["passwd"]:
                st.warning("Please enter password.")
            elif not st.session_state["user"]:
                st.warning("Please enter username.")
            else:
                st.error("Invalid Username/Password :face_with_raised_eyebrow:")
    
    def authenticate_user(self) -> bool:
        """
        Display authentication form and verify user credentials.
        
        Returns:
            bool: True if user is authenticated, False otherwise.
        """
        if "authenticated" not in st.session_state:
            st.text_input(label="Username :", value="", key="user")
            st.text_input(
                label="Password :", 
                value="", 
                key="passwd", 
                type="password", 
                on_change=self.verify_credentials
            )
            return False
        else:
            if st.session_state["authenticated"]:
                return True
            else:
                st.text_input(
                    label="Username :", 
                    value="", 
                    key="user", 
                    on_change=self.verify_credentials
                )
                st.text_input(
                    label="Password :", 
                    value="", 
                    key="passwd", 
                    type="password", 
                    on_change=self.verify_credentials
                )
                return False


class SessionManager:
    """
    Session manager for handling login state and navigation.
    
    Manages login/logout functionality and session state.
    """
    
    def __init__(self) -> None:
        """Initialize the session manager and setup session state."""
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False
    
    def login(self) -> None:
        """Handle the login action and update session state."""
        if st.button("Log in"):
            st.session_state.logged_in = True
            st.rerun()

    def logout(self) -> None:
        """Handle the logout action and update session state."""
        if st.button("Log out"):
            st.session_state.logged_in = False
            st.rerun()