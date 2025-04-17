import streamlit_authenticator as stauth
import streamlit as st


# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

def creds_entered():
    if st.session_state["user"].strip() == "admin" and st.session_state["passwd"].strip() == "admin":
        st.session_state["authenticated"] = True
    else:
        st.session_state["authenticated"] = False
        
        if not st.session_state["passwd"]:
            st.warning("Please enter password.")
        elif not st.session_state["user"]:
            st.warning("Please enter username.")
        else:
            st.error("Invalid Username/Password :face_with_raised_eyebrow:")
        
    
def authenticate_user():
    if "authenticated" not in st.session_state:
        st.text_input(label="Username :", value="", key="user")
        st.text_input(label="Password :", value="", key="passwd", type="password", on_change=creds_entered)
        return False
    else:
        if st.session_state["authenticated"]:
            return True
        else:
            st.text_input(label="Username :", value="", key="user", on_change=creds_entered)
            st.text_input(label="Password :", value="", key="passwd", type="password", on_change=creds_entered)
            return False

def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

# login_page = st.Page(login, title="Log in", icon=":material/login:")
# logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

# chat_bot_page = st.Page("ch.py", title="Q/A", icon=":material/forum:")
# ticket_similarity_page = st.Page("sm.py", title="Ticket Similarity", icon=":material/compare_arrows:")

if authenticate_user():

    # https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
    st.set_page_config(
        page_title="Welcome - TicketAssist",
        page_icon=":wave:",
        initial_sidebar_state="collapsed", # auto, expanded ,and collapsed
        layout="centered", # centered and wide
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "# This is a header. This is an *extremely* cool app!"
        }
    )

    # if st.session_state.logged_in:
    #     pg = st.navigation(
    #         {
    #             # "Reports": [dashboard, bugs, alerts],
    #             "Tools": [chat_bot_page, ticket_similarity_page],
    #             "Account": [logout_page],
    #         }
    #     )
    # else:
    #     pg = st.navigation([login_page])
        
    st.write("# Welcome to TicketAssist! 👋")

    # st.sidebar.success("Select a demo above.")
    # st.sidebar.markdown("Select a demo above.")

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

    # pg = st.navigation([chat_bot_page, ticket_similarity_page])

    # pg.run()
    
