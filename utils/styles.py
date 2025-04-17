"""
Styling utilities for the TicketAssist application.

This module provides CSS styling and UI enhancement functions.
"""
import streamlit as st


def load_ticket_css() -> None:
    """
    Load CSS styles for the ticket display page.
    
    Injects custom CSS into the Streamlit application for enhanced ticket visualization.
    """
    st.markdown("""
    <style>
    /* Add a specific class for hidden details */
    .details-hidden {
        display: none !important;
    }
    
    /* Improved scrollable section for card details */
    .details-section {
        max-height: 250px !important;
        overflow-y: auto !important; /* Force scrollbar to appear when needed */
        overflow-x: hidden !important;
        padding: 10px !important;
        margin: 0 !important;
        border-top: 1px solid rgba(0,0,0,0.1) !important;
        display: block !important; /* Ensure display is block */
    }

    /* Custom scrollbar styling */
    .details-section::-webkit-scrollbar {
        width: 6px !important;
        display: block !important;
    }

    .details-section::-webkit-scrollbar-track {
        background: #f1f1f1 !important;
        border-radius: 10px !important;
    }

    .details-section::-webkit-scrollbar-thumb {
        background: #888 !important;
        border-radius: 10px !important;
    }

    .details-section::-webkit-scrollbar-thumb:hover {
        background: #555 !important;
    }
    
    /* Card structure and expansion handling */
    .card {
        width: 300px !important;
        margin: 10px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
        cursor: pointer !important;
        overflow: visible !important; /* Allow scrollbar to be visible */
        border-radius: 8px !important;
        display: flex !important;
        flex-direction: column !important;
    }

    /* Default card with fixed height when details are hidden */
    .card:not(.expanded) {
        height: auto !important;
        max-height: 280px !important; /* Default height when compact */
    }

    /* Expanded card when details are shown */
    .card.expanded {
        height: auto !important;
        max-height: 530px !important; /* Maximum height when expanded */
    }

    /* Force details section to have correct scroll behavior */
    .card .extra.content.details-section {
        flex: 1 1 auto !important;
        overflow-y: auto !important;
        max-height: 250px !important;
        display: none !important; /* Hidden by default */
    }

    /* When card is expanded, show the details section */
    .card.expanded .extra.content.details-section {
        display: block !important;
    }

    /* Improve text formatting in scrollable area */
    .details-section .meta {
        margin-bottom: 12px !important;
        word-break: break-word !important;
    }

    .details-section .solution-text {
        padding: 5px !important;
        background-color: rgba(0,0,0,0.02) !important;
        border-radius: 4px !important;
        margin-top: 8px !important;
        word-break: break-word !important;
    }
    .criticalbackground {
        background: linear-gradient(135deg, #e53935 0%, #d32f2f 100%) !important;
        color: white !important;
        border-bottom: 3px solid #b71c1c !important;
    }
    .majorbackground {
        background: linear-gradient(135deg, #fb8c00 0%, #f57c00 100%) !important;
        color: white !important;
        border-bottom: 3px solid #ef6c00 !important;
    }
    .minorbackground {
        background: linear-gradient(135deg, #039be5 0%, #0288d1 100%) !important;
        color: white !important;
        border-bottom: 3px solid #0277bd !important;
    }
    .tablebackground {
        background: linear-gradient(135deg, #1e88e5 0%, #1976d2 100%) !important;
        color: white !important;
        border-bottom: 3px solid #1565c0 !important;
    }
    .viewbackground {
        background: linear-gradient(135deg, #4fc3f7 0%, #29b6f6 100%) !important;
        color: white !important;
        border-bottom: 3px solid #039be5 !important;
    }
    .mvbackground {
        background: linear-gradient(135deg, #ffd54f 0%, #ffca28 100%) !important;
        color: white !important;
        border-bottom: 3px solid #ffb300 !important;
    }
    
    .smallheader {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 250px;
        font-weight: 600 !important;
    }
    .description {
        display: flex;
        justify-content: space-between;
    }
    .kpi.number {
        font-size: 1.5em;
        text-align: center;
        display: inline-block;
        margin: 0 10px;
        width: 70px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .kpi.text {
        font-size: 0.7em;
        margin-top: 0;
        text-align: center;
    }
    #mydiv {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .card:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }

    .card .key-link {
        color: inherit;
        font-weight: bold;
        text-decoration: none;
        position: relative;
        z-index: 10;
    }
    
    .details-section {
        max-height: 250px;
        overflow: hidden;
        transition: max-height 0.5s ease-in-out;
    }
    .expandable {
        cursor: pointer;
    }
    .solution-text {
        max-height: none !important;
        white-space: normal !important;
        overflow: visible !important;
        word-wrap: break-word !important; 
        word-break: normal !important;
        line-height: 1.5 !important;
        margin-top: 5px !important;
    }
    .meta {
        white-space: normal !important;
        overflow: visible !important;
        word-wrap: break-word !important;
        margin-bottom: 8px !important;
        line-height: 1.4 !important;
    }
    .ticket-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.9em;
        font-weight: bold;
        margin-right: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .badge-critical {
        background: linear-gradient(135deg, #e53935 0%, #d32f2f 100%);
        color: white;
    }
    .badge-major {
        background: linear-gradient(135deg, #fb8c00 0%, #f57c00 100%);
        color: white;
    }
    .badge-minor {
        background: linear-gradient(135deg, #039be5 0%, #0288d1 100%);
        color: white;
    }
    .badge-open {
        background: linear-gradient(135deg, #43a047 0%, #388e3c 100%);
        color: white;
    }
    .badge-progress {
        background: linear-gradient(135deg, #1e88e5 0%, #1976d2 100%);
        color: white;
    }
    .badge-verify {
        background: linear-gradient(135deg, #7cb342 0%, #689f38 100%);
        color: white;
    }
    .badge-resolved {
        background: linear-gradient(135deg, #78909c 0%, #607d8b 100%);
        color: white;
    }
    div.stButton > button {
        width: 100%;
    }
    .ui.cards {
        padding-bottom: 30px;
    }
    .ui.statistics {
        margin-bottom: 30px !important;
    }
    .ui.statistic .value {
        font-size: 2.5rem !important;
    }
    .ui.small.statistics .statistic .value {
        font-size: 2rem !important;
    }
    .progress-bar {
        height: 10px;
        background-color: #f3f3f3;
        border-radius: 5px;
        margin: 10px 0;
    }
    .progress-value {
        height: 10px;
        border-radius: 5px;
    }
    
    /* Tooltips */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 120px;
        background-color: rgba(0, 0, 0, 0.8);
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 0.8em;
        font-weight: normal;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Improve expand button */
    .ui.mini.button {
        background: linear-gradient(135deg, #78909c 0%, #607d8b 100%) !important;
        color: white !important;
        font-weight: bold !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
        border-radius: 20px !important;
    }
    .ui.mini.button:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Improve header section */
    .content.header-section {
        padding: 15px !important;
    }
    
    /* Added styles for filter tags */
    .filter-tag {
        display: inline-block;
        background: #e0e0e0;
        border-radius: 15px;
        padding: 5px 12px;
        margin-right: 8px;
        margin-bottom: 8px;
        font-size: 0.85em;
        color: #333;
    }
    .filter-tag .close {
        margin-left: 5px;
        cursor: pointer;
        color: #666;
    }
    .filter-tag .close:hover {
        color: #d32f2f;
    }
    .filter-tags-container {
        margin: 10px 0;
        display: flex;
        flex-wrap: wrap;
    }
    
    /* Added styles for category badges */
    .category-badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        margin-right: 5px;
        background: #e0e0e0;
        color: #333;
    }
    .category-Bug-Fix {
        background: #d1c4e9;
        color: #4527a0;
    }
    .category-Root-Cause {
        background: #c8e6c9;
        color: #2e7d32;
    }
    .category-Performance {
        background: #bbdefb;
        color: #0d47a1;
    }
    .category-Design {
        background: #ffecb3;
        color: #ff6f00;
    }
    .category-Configuration {
        background: #ffccbc;
        color: #bf360c;
    }
    
    /* Added styles for card actions */
    .action-button {
        flex: 1;
        text-align: center;
        padding: 5px;
        border-radius: 4px;
        margin: 0 3px;
        cursor: pointer;
        font-size: 0.8em;
        transition: all 0.2s;
    }
    .action-button:hover {
        background: rgba(0,0,0,0.05);
    }
    .action-button i {
        margin-right: 3px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Load Semantic UI CSS from CDN
    st.markdown(
        """
        <link href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
        """,
        unsafe_allow_html=True
    )


def load_card_interactions_js() -> None:
    """
    Load JavaScript for card interactions.
    
    Injects JavaScript to handle card click events and UI interactions.
    """
    st.markdown("""
    <script type="text/javascript">
        document.addEventListener('DOMContentLoaded', function() {
            function setupCardInteractions() {
                // Set up click handlers for each card
                document.querySelectorAll('.card').forEach(function(card) {
                    // Store the URL from the data attribute
                    var cardUrl = card.getAttribute('data-url');
                    
                    // Add click event to the card (except for buttons)
                    card.addEventListener('click', function(e) {
                        // Only open URL if not clicking a button or link
                        if (!e.target.closest('.ui.button') && !e.target.closest('a')) {
                            window.open(cardUrl, '_blank');
                        }
                    });
                });
                
                console.log("Card interactions initialized");
            }
            
            // Initial setup
            setupCardInteractions();
            
            // Also try after a delay to catch any dynamic content
            setTimeout(setupCardInteractions, 1000);
        });
    </script>
    """, unsafe_allow_html=True)


def dark_mode_toggle() -> bool:
    """
    Create a toggle for dark mode.
    
    Returns:
        bool: True if dark mode is enabled, False otherwise
    """
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
        
    dark_mode_status = st.sidebar.checkbox("Dark Mode")
        
    if dark_mode_status:
        st.session_state.dark_mode = True
        st.markdown("""
        <style>
        .main {
            background-color: #121212;
            color: #e0e0e0;
        }
        .css-1kyxreq, .css-12oz5g7 {
            background-color: #1e1e1e;
            color: #e0e0e0;
        }
        .st-c8, .st-bd, .st-ae, .st-af {
            color: #e0e0e0;
        }
        .st-bq {
            background-color: #2d2d2d;
        }
        .card {
            background-color: #2d2d2d !important;
            color: #e0e0e0 !important;
        }
        .meta, .header, .description {
            color: #e0e0e0 !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.session_state.dark_mode = False
        
    return dark_mode_status