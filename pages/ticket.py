"""
TicketAssist - 5G Ticket Management Page

This module provides a UI for viewing, filtering, and analyzing 5G-related tickets.
"""
from typing import Dict, List, Any, Optional, Tuple, Set
import random
import uuid
import time
from datetime import datetime

import streamlit as st
import pandas as pd
from unidecode import unidecode

# Import custom modules
from utils.ticket import TicketGenerator, TicketDisplay, TicketExporter
from utils.styles import load_ticket_css, load_card_interactions_js, dark_mode_toggle


class TicketPageUI:
    """
    User interface for the 5G ticket management page.
    
    Provides UI components and handlers for the ticket display page.
    """
    
    def __init__(self) -> None:
        """Initialize the ticket page UI components."""
        # Set page configuration
        st.set_page_config(layout="wide", page_title="5G Ticket Catalog", page_icon="📱")
        
        # Load CSS styles
        load_ticket_css()
        
        # Initialize session state for filters if needed
        if 'filters' not in st.session_state:
            st.session_state.filters = {
                'projects': [],
                'priority': [],
                'status': [],
                'search': ""
            }
        
        # Initialize selector keys for resetting
        if 'selectbox_project_key' not in st.session_state:
            st.session_state.selectbox_project_key = 10
            st.session_state.selectbox_priority_key = 20
            st.session_state.selectbox_status_key = 30
    
    def setup_sidebar(self, tickets_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Setup the sidebar with filtering and export options.
        
        Args:
            tickets_list: List of ticket dictionaries to filter
            
        Returns:
            Dictionary containing filter settings
        """
        # Data options section
        st.sidebar.markdown("## Data Options")
        
        # Number of tickets to display
        ticket_count = st.sidebar.slider("Number of tickets to display", 5, 50, 20, 5)
        
        # Export data option
        export_format = st.sidebar.selectbox("Export Format", ["CSV", "JSON", "Excel"])
        if st.sidebar.button("Export Data"):
            if export_format == "CSV":
                csv_data = TicketExporter.export_to_csv(tickets_list)
                st.sidebar.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name="5g_tickets_export.csv",
                    mime="text/csv"
                )
            st.sidebar.success(f"Data export in {export_format} format initiated!")
        
        # Filter options
        st.sidebar.write("## Filter Options")
        st.sidebar.write("")
        
        # Project type filter using multiselect
        available_projects = list(set([t["project_key"] for t in tickets_list]))
        selected_projects = st.sidebar.multiselect(
            label='Project Type',
            options=available_projects,
            default=available_projects  # Default to ALL project types
        )
        
        # Priority filter
        available_priorities = list(set([t["priority_name"] for t in tickets_list]))
        selected_priorities = st.sidebar.multiselect(
            label='Priority',
            options=available_priorities,
            default=[]  # No default selections
        )
        
        # Status filter
        available_statuses = list(set([t["status_name"] for t in tickets_list]))
        selected_statuses = st.sidebar.multiselect(
            label='Status',
            options=available_statuses,
            default=[]  # No default selections
        )
        
        # Store filter selections in session state
        st.session_state.filters['projects'] = selected_projects
        st.session_state.filters['priority'] = selected_priorities
        st.session_state.filters['status'] = selected_statuses
        
        # Detail view toggle
        cb_view_details = st.sidebar.checkbox('View Details', value=True)
        
        # Clear selections button
        if st.sidebar.button('Clear All Filters', on_click=self._reset_filters):
            pass  # Action handled by on_click
        
        # Dark mode toggle
        dark_mode_status = dark_mode_toggle()
        
        return {
            'ticket_count': ticket_count,
            'selected_projects': selected_projects,
            'selected_priorities': selected_priorities,
            'selected_statuses': selected_statuses,
            'view_details': cb_view_details,
            'dark_mode': dark_mode_status,
            'export_format': export_format
        }
    
    def _reset_filters(self) -> None:
        """Reset all filters to their default state."""
        st.session_state.selectbox_project_key = st.session_state.selectbox_project_key + 1
        st.session_state.selectbox_priority_key = st.session_state.selectbox_priority_key + 1
        st.session_state.selectbox_status_key = st.session_state.selectbox_status_key + 1
        # Reset all filters
        st.session_state.filters = {
            'projects': [],
            'priority': [],
            'status': [],
            'search': ""
        }
    
    def setup_search_bar(self) -> str:
        """
        Setup the search bar for filtering tickets.
        
        Returns:
            Search query string
        """
        c1, c2 = st.columns([6, 1])
        text_search = c1.text_input(
            label="Search", 
            value=st.session_state.filters.get('search', ""),
            max_chars=150,
            label_visibility='collapsed',
            placeholder="Search by title, description, or key"
        )
        text_search = unidecode(str(text_search).lower())
        st.session_state.filters['search'] = text_search
        
        # Search button
        c2.button(
            label="", 
            icon=":material/search:", 
            use_container_width=True, 
            type="primary", 
            on_click=None
        )
        
        return text_search
    
    def display_active_filters(self, available_projects: List[str], selected_projects: List[str], 
                              selected_priorities: List[str], selected_statuses: List[str]) -> None:
        """
        Display the currently active filters.
        
        Args:
            available_projects: List of all available project keys
            selected_projects: List of selected project keys
            selected_priorities: List of selected priorities
            selected_statuses: List of selected statuses
        """
        active_filters = []
        if selected_projects and len(selected_projects) < len(available_projects):
            active_filters.append(f"Projects: {', '.join(selected_projects)}")
        if selected_priorities:
            active_filters.append(f"Priority: {', '.join(selected_priorities)}")
        if selected_statuses:
            active_filters.append(f"Status: {', '.join(selected_statuses)}")
        
        if active_filters:
            st.markdown("**Active Filters:**")
            filter_html = ""
            for filter_text in active_filters:
                filter_html += f'<span class="filter-tag">{filter_text}</span>'
            st.markdown(f"""<div style="margin-bottom: 15px;">{filter_html}</div>""", unsafe_allow_html=True)
    
    def setup_sort_options(self) -> str:
        """
        Setup the sorting options for the tickets.
        
        Returns:
            Selected sort option
        """
        sort_options = [
            'Key A → Z', 
            'Key Z → A', 
            'Priority ↓', 
            'Priority ↑',
            'Status ↓', 
            'Status ↑', 
            'Created ↓', 
            'Created ↑', 
            'Updated ↓', 
            'Updated ↑'
        ]
        
        return st.sidebar.selectbox("Order By", sort_options)
    
    def display_advanced_filters(self) -> Dict[str, Any]:
        """
        Display advanced filtering options.
        
        Returns:
            Dictionary of advanced filter settings
        """
        with st.expander("Advanced Filters", expanded=False):
            col1, col2 = st.columns(2)
            
            # Filter by date range
            with col1:
                st.subheader("Date Filters")
                date_option = st.radio(
                    "Filter by date",
                    options=["All Dates", "Created Date", "Updated Date"]
                )
                
                if date_option != "All Dates":
                    date_range = st.date_input(
                        "Select date range",
                        value=(datetime.now() - pd.Timedelta(days=30), datetime.now()),
                        key="date_filter"
                    )
                else:
                    date_range = None
            
            # Filter by category
            with col2:
                st.subheader("Category Filters")
                categories = ["Bug Fix", "Root Cause Identified", "Performance Enhancement", 
                             "Design Limitation", "Configuration Error"]
                selected_categories = st.multiselect(
                    "Filter by category",
                    options=categories,
                    default=[]
                )
            
            return {
                "date_option": date_option,
                "date_range": date_range,
                "categories": selected_categories
            }
    
    def render_ticket_cards(self, tickets_list: List[Dict[str, Any]], view_details: bool) -> None:
        """
        Render the ticket cards with details.
        
        Args:
            tickets_list: List of filtered ticket dictionaries to display
            view_details: Whether to show detailed view or compact view
        """
        # Determine CSS classes based on details toggle
        if view_details:
            details_class = ""
            card_class = "card expanded"
        else:
            details_class = "details-hidden"
            card_class = "card compact"
        
        # Start the card container
        ticket_scorecard = """<div id="mydiv" class="ui centered cards">"""
        
        # Generate cards for each ticket
        for ticket in tickets_list:
            # Generate a unique ID for this ticket for DOM manipulation
            ticket_id = f"ticket_{time.time_ns()}_{uuid.uuid4().hex[:8]}"
            
            # Format dates for display
            created_date = datetime.strptime(ticket["created"], "%Y-%m-%dT%H:%M:%S.000+0200").strftime("%Y-%m-%d")
            updated_date = datetime.strptime(ticket["last_updated"], "%Y-%m-%dT%H:%M:%S.000+0200").strftime("%Y-%m-%d")
            
            # Format components for display
            components_str = ", ".join(ticket["components"])
            
            # Status and priority badges
            status_class = {
                "Open": "badge-open",
                "In Progress": "badge-progress",
                "Verify": "badge-verify",
                "Resolved": "badge-resolved"
            }.get(ticket["status_name"], "")
            
            priority_class = {
                "Critical": "badge-critical",
                "Major": "badge-major",
                "Minor": "badge-minor"
            }.get(ticket["priority_name"], "")
            
            # Calculate a progress percentage for the task (random for demonstration)
            progress_percentage = random.randint(10, 100)
            progress_color = {
                "Critical": '#d32f2f',
                "Major": '#f57c00',
                "Minor": '#0288d1'
            }.get(ticket["priority_name"], '#0288d1')
            
            # Create the card HTML with enhanced UI features
            ticket_scorecard += f"""
                <div class="{card_class}" id="{ticket_id}" data-url="{ticket['url']}">            
                <div class="content {TicketDisplay.priority_bg(ticket["priority_name"])}">
                    <div class="header smallheader">
                        <a href="{ticket['url']}" target="_blank" class="key-link">{ticket["key"]}</a>
                    </div>
                    <div class="meta smallheader">{ticket["title"]}</div>
                </div>
                <div class="content">
                    <div class="description"><br>
                        <div class="column kpi number">{ticket["project_key"]}<br>
                            <p class="kpi text">Project</p>
                        </div>
                        <div class="column kpi number tooltip">
                            <span class="ticket-badge {status_class}">{TicketDisplay.get_status_code(ticket["status_name"])}</span>
                            <span class="tooltiptext">{ticket["status_name"]}</span><br>
                            <p class="kpi text">Status</p>
                        </div>
                        <div class="column kpi number tooltip">
                            <span class="ticket-badge {priority_class}">{TicketDisplay.get_priority_code(ticket["priority_name"])}</span>
                            <span class="tooltiptext">{ticket["priority_name"]}</span><br>
                            <p class="kpi text">Priority</b>
                        </div>
                    </div>
                </div>
                <div class="extra content">
                    <div class="meta"><i class="tag icon"></i> <b>Category:</b> {ticket["Answer"]["answer_category"]}</div>
                    <div class="meta"><i class="code branch icon"></i> <b>Build:</b> {ticket["Answer"]["included_build"]}</div>
                    <div class="meta"><i class="calendar alternate outline icon"></i> <b>Created:</b> {created_date}</div>
                </div>
                <div class="extra content details-section {details_class}">
                    <div class="meta"><i class="info circle icon"></i> <b>Description:</b> {ticket["description"]}</div>
                    <div class="meta"><i class="edit icon"></i> <b>Updated:</b> {updated_date}</div>
                    <div class="meta"><i class="comment alternate outline icon"></i> <b>Comments:</b> {len(ticket["comments"])}</div>
                    <div class="meta"><i class="tags icon"></i> <b>Components:</b> {components_str}</div>
                    <div class="meta"><i class="clipboard check icon"></i> <b>Solution:</b>
                        <div class="solution-text">
                            {ticket["Answer"]["answer_text"]}
                        </div>
                    </div>
                    <div style="margin-top: 10px; text-align: center;">
                        <a href="{ticket['url']}" target="_blank" class="ui primary fluid button">
                            <i class="external alternate icon"></i> View Ticket Details
                        </a>
                    </div>
                </div>
            </div>"""
        
        ticket_scorecard += """</div>"""
        
        # Display the cards
        st.markdown(ticket_scorecard, unsafe_allow_html=True)
        
        # Add JavaScript for card interactions
        load_card_interactions_js()


class TicketManager:
    """
    Manager for ticket data handling and processing.
    
    Provides methods for filtering, sorting, and processing ticket data.
    """
    
    @staticmethod
    def apply_filters(tickets_list: List[Dict[str, Any]], filters: Dict[str, Any], 
                     text_search: str) -> List[Dict[str, Any]]:
        """
        Apply filters to the ticket list.
        
        Args:
            tickets_list: Original list of ticket dictionaries
            filters: Dictionary of filter settings
            text_search: Search query string
            
        Returns:
            Filtered list of tickets
        """
        filtered_tickets = tickets_list.copy()
        
        # Filter by selected projects if any are selected
        if filters.get('projects'):
            filtered_tickets = [t for t in filtered_tickets if t["project_key"] in filters['projects']]
        
        # Filter by selected priorities if any are selected
        if filters.get('priority'):
            filtered_tickets = [t for t in filtered_tickets if t["priority_name"] in filters['priority']]
        
        # Filter by selected statuses if any are selected
        if filters.get('status'):
            filtered_tickets = [t for t in filtered_tickets if t["status_name"] in filters['status']]

        # Filter by text search if provided
        if text_search:
            search_results = []
            for ticket in filtered_tickets:
                searchable_text = (
                    unidecode(ticket["title"].lower()) + " " +
                    unidecode(ticket["description"].lower()) + " " +
                    unidecode(ticket["key"].lower()) + " " +
                    unidecode(ticket["Answer"]["answer_category"].lower()) + " " +
                    unidecode(ticket["Answer"]["summary_of_analysis"].lower())
                )
                if text_search in searchable_text:
                    search_results.append(ticket)
            filtered_tickets = search_results
            
        return filtered_tickets
    
    @staticmethod
    def apply_sorting(tickets_list: List[Dict[str, Any]], sort_option: str) -> List[Dict[str, Any]]:
        """
        Apply sorting to the ticket list.
        
        Args:
            tickets_list: List of ticket dictionaries to sort
            sort_option: Selected sort option
            
        Returns:
            Sorted list of tickets
        """
        sorted_tickets = tickets_list.copy()
        
        if sort_option == 'Key A → Z':
            sorted_tickets.sort(key=lambda x: x["key"])
        elif sort_option == 'Key Z → A':
            sorted_tickets.sort(key=lambda x: x["key"], reverse=True)
        elif sort_option == 'Priority ↓':
            priority_order = {"Critical": 0, "Major": 1, "Minor": 2}
            sorted_tickets.sort(key=lambda x: priority_order.get(x["priority_name"], 3))
        elif sort_option == 'Priority ↑':
            priority_order = {"Critical": 0, "Major": 1, "Minor": 2}
            sorted_tickets.sort(key=lambda x: priority_order.get(x["priority_name"], 3), reverse=True)
        elif sort_option == 'Status ↓':
            status_order = {"Open": 0, "In Progress": 1, "Verify": 2, "Resolved": 3}
            sorted_tickets.sort(key=lambda x: status_order.get(x["status_name"], 4))
        elif sort_option == 'Status ↑':
            status_order = {"Open": 0, "In Progress": 1, "Verify": 2, "Resolved": 3}
            sorted_tickets.sort(key=lambda x: status_order.get(x["status_name"], 4), reverse=True)
        elif sort_option == 'Created ↓':
            sorted_tickets.sort(key=lambda x: x["created"], reverse=True)
        elif sort_option == 'Created ↑':
            sorted_tickets.sort(key=lambda x: x["created"])
        elif sort_option == 'Updated ↓':
            sorted_tickets.sort(key=lambda x: x["last_updated"], reverse=True)
        elif sort_option == 'Updated ↑':
            sorted_tickets.sort(key=lambda x: x["last_updated"])
        
        return sorted_tickets
    
    @staticmethod
    def calculate_statistics(tickets_list: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Calculate statistics about the tickets.
        
        Args:
            tickets_list: List of ticket dictionaries
            
        Returns:
            Dictionary of statistics
        """
        return {
            "open_count": sum(1 for t in tickets_list if t["status_name"] == "Open"),
            "in_progress_count": sum(1 for t in tickets_list if t["status_name"] == "In Progress"),
            "critical_count": sum(1 for t in tickets_list if t["priority_name"] == "Critical"),
            "major_count": sum(1 for t in tickets_list if t["priority_name"] == "Major"),
            "total_count": len(tickets_list)
        }


def main() -> None:
    """
    Main function to run the ticket management page.
    
    Orchestrates the different components and manages the overall application flow.
    """
    # Initialize UI
    ui = TicketPageUI()
    
    # Generate or load ticket data
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_tickets(count: int = 20) -> List[Dict[str, Any]]:
        tickets_dict = TicketGenerator.generate_fake_5g_tickets(count)
        return [ticket for _, ticket in tickets_dict.items()]

    # Start with default ticket count
    tickets_list = get_tickets(20)
    
    # Setup sidebar and get filter settings
    filters = ui.setup_sidebar(tickets_list)
    
    # Update tickets if count changed
    if filters['ticket_count'] != len(tickets_list):
        tickets_list = get_tickets(filters['ticket_count'])
    
    # Setup search bar
    text_search = ui.setup_search_bar()
    
    # Display active filters
    available_projects = list(set([t["project_key"] for t in tickets_list]))
    ui.display_active_filters(
        available_projects, 
        filters['selected_projects'], 
        filters['selected_priorities'], 
        filters['selected_statuses']
    )
    
    # Apply filters to tickets
    filtered_tickets = TicketManager.apply_filters(
        tickets_list, 
        st.session_state.filters, 
        text_search
    )
    
    # Setup sorting options
    sort_option = ui.setup_sort_options()
    
    # Apply sorting
    sorted_tickets = TicketManager.apply_sorting(filtered_tickets, sort_option)
    
    # Display advanced filters
    ui.display_advanced_filters()
    
    # Calculate statistics
    stats = TicketManager.calculate_statistics(sorted_tickets)
    
    # Display tickets
    ui.render_ticket_cards(sorted_tickets, filters['view_details'])


if __name__ == "__main__":
    main()