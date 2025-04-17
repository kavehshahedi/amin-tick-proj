"""
TicketAssist - Main Application

This is the main entry point for the TicketAssist application, providing
authentication and core UI functionality.
"""
import streamlit as st
from utils.auth import Authenticator, SessionManager


def configure_page() -> None:
    """
    Configure the Streamlit page settings including title, icon, and layout.
    """
    st.set_page_config(
        page_title="Welcome - TicketAssist",
        page_icon=":wave:",
        initial_sidebar_state="collapsed",  # auto, expanded, and collapsed
        layout="centered",  # centered and wide
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "# This is a header. This is an *extremely* cool app!"
        }
    )


def display_welcome_content() -> None:
    """
    Display the welcome content on the main page.
    """
    st.write("# Welcome to TicketAssist! 👋")
    
    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
        
        **👈 Select a demo from the sidebar** to see some examples
        of what Streamlit can do!
        
        ### Want to learn more?
        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
            forums](https://discuss.streamlit.io)
        """
    )


def main() -> None:
    """
    Main function to run the TicketAssist application.
    
    Handles authentication and displays the main page content when authenticated.
    """
    # Initialize authentication
    auth = Authenticator()
    session = SessionManager()
    
    # Only configure page and display content if authenticated
    if auth.authenticate_user():
        configure_page()
        display_welcome_content()
        
        # Future implementation:
        # if st.session_state.logged_in:
        #     pg = st.navigation(
        #         {
        #             "Tools": [chat_bot_page, ticket_similarity_page],
        #             "Account": [logout_page],
        #         }
        #     )


if __name__ == "__main__":
    main()