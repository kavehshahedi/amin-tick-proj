import streamlit as st
# Set page configuration as the first Streamlit command
st.set_page_config(layout="wide", page_title="5G Ticket Catalog2", page_icon="📱")

import pandas as pd
import json
from datetime import datetime
import random
import uuid
from unidecode import unidecode
import time  # Added for timestamp-based IDs

# Import the function to generate fake 5G tickets
def generate_fake_5g_tickets(count=5):
    projects = {
        "PCELS": {
            "project_name": "5G Policy Control",
            "project_id": "20001"
        },
        "PCTR": {
            "project_name": "5G Charging Trigger Router",
            "project_id": "20002"
        },
        "PCIFUS": {
            "project_name": "5G Network Function State Manager",
            "project_id": "20003"
        },
        "PCBP": { 
            "project_name": "5G Policy Control Data Repository",
            "project_id": "20004"
        }
    }

    base_url = "localhost:8080/browse"
    status_options = ["Open", "In Progress", "Verify", "Resolved"]
    priority_names = ["Minor", "Major", "Critical"]
    components_list = ["Compass", "The Cable Guys", "Service Engine", "Traffic Control", 
                      "Kubernetes Operator", "Network Slice Manager", "Cloud Native Functions"]  # Added new components
    comments_bank = [
        "Can you please check if this can be fixed in the next drop?",
        "Fix is mentioned but no details are shared. Can someone clarify?",
        "This will be delivered in Drop#93. Patch is ready and needs verification.",
        "Seeing the same issue in test environment, can we expedite this?",  # Added new comments
        "Similar issue was fixed in another project, can we reuse that solution?",
        "Is there a workaround for this until the permanent fix is deployed?"
    ]
    answer_categories = ["Bug Fix", "Root Cause Identified", "Performance Enhancement", "Design Limitation", 
                         "Configuration Change", "Architecture Update"]  # Added new categories

    short_titles = [
        "UPF crash during handover",
        "SMF timeout issue",
        "NRF registration fail",
        "Packet drop in edge site",
        "AMF restart loop",
        "PCF policy synchronization issues",  # Added new titles
        "UDM data corruption during failover",
        "Network slice isolation breach",
        "NSSF selection algorithm deadlock",
        "UPF data path congestion"
    ]

    short_descriptions = [
        "",
        "UPF failed after handover in a high-traffic zone.",
        "SMF didn't respond within expected time during session setup.",
        "NRF could not register NFs under high load.",
        "Edge site dropped packets intermittently.",
        "AMF pod restarted repeatedly after upgrade.",
        "PCF failing to synchronize policies across regions.",  # Added new descriptions
        "UDM data corruption observed during automated failover tests.",
        "Network slice isolation compromised during peak load.",
        "NSSF selection algorithm deadlocked with multiple concurrent requests.",
        "UPF data path experiencing congestion with specific traffic patterns."
    ]

    long_descriptions = [
        "UPF experienced a critical failure during handover processing. Log analysis indicates a service mesh routing conflict causing gRPC retries to hang. This is reproducible under peak conditions in edge deployments.",
        "NRF failed to register new network functions during orchestrated deployment. Load testing shows memory bottlenecks and long GC pauses that align with the failure window.",
        "Session setup flows failed between AMF and SMF due to missing N11 signaling. Investigation reveals timeout misconfigurations and container-level resource starvation.",
        "PCF policy synchronization failed between geographical redundant sites resulting in policy inconsistency. Investigation shows network latency spikes during synchronization windows.",  # Added new descriptions
        "Network slice resource allocation conflicts observed when concurrent slice creation requests are processed. Root cause appears to be race condition in the slice manager orchestrator."
    ]

    long_answers = [
        {
            "summary_of_analysis": "Root cause found in gRPC timeout and stale connection handling within UPF router module.",
            "planned_release": "v23.9.1",
            "answer_text": (
                "Upon detailed inspection, it was discovered that stale gRPC connections were not being reaped by the UPF control plane. "
                "This led to congestion in the listener thread pool, especially during gNB handovers. A fix was applied to include active timeout cleanup and connection recycling. "
                "Memory profiling confirmed improved behavior post-patch, and stress test under 10k sessions was passed successfully."
            ),
            "included_build": f"build_{random.randint(7000, 9999)}",
            "answer_code": f"FIX-{random.randint(10000, 99999)}",
            "answer_category": "Bug Fix"
        },
        {
            "summary_of_analysis": "AMF restart loop linked to excessive memory growth due to recursive state handler reinitialization.",
            "planned_release": "v24.2.0",
            "answer_text": (
                "AMF's internal state machine reentered a fault state loop under failed N2 setup scenarios. This recursive initialization consumed excess memory, "
                "eventually triggering container OOM kills. The fix includes a guard to detect retry exhaustion and gracefully drop the session. "
                "Tested under varied fail conditions and passed with stability for over 48h soak runs."
            ),
            "included_build": f"build_{random.randint(7000, 9999)}",
            "answer_code": f"FIX-{random.randint(10000, 99999)}",
            "answer_category": "Root Cause Identified"
        },
        {
            "summary_of_analysis": "NRF underload condition traced to missing index on Redis cache for NF heartbeat key lookups.",
            "planned_release": "v24.1.3",
            "answer_text": (
                "During NF discovery, NRF's heartbeat lookup times spiked. Redis queries lacked an index on the `nf-heartbeat-status` key set, leading to linear scans. "
                "Latency crossed 200ms on average, impacting all NF registration attempts. We added a sorted index, rewrote the lookup logic, and introduced back-pressure controls "
                "at the service mesh to prevent flood during failover. Confirmed 4x improvement in registration speed."
            ),
            "included_build": f"build_{random.randint(7000, 9999)}",
            "answer_code": f"FIX-{random.randint(10000, 99999)}",
            "answer_category": "Performance Enhancement"
        },
        {
            "summary_of_analysis": "Network slice isolation breach traced to improper QoS flow binding in the SMF.",
            "planned_release": "v24.3.0",
            "answer_text": (
                "Investigation revealed that QoS flow binding in the SMF wasn't properly enforcing slice isolation under high-load conditions. "
                "This allowed traffic from one slice to potentially impact another slice's performance. We implemented a dual-layer verification "
                "mechanism in both the SMF and UPF to ensure strict slice isolation is maintained even during peak loads. "
                "Validation testing under multiple slice configurations confirmed the fix effectiveness."
            ),
            "included_build": f"build_{random.randint(7000, 9999)}",
            "answer_code": f"FIX-{random.randint(10000, 99999)}",
            "answer_category": "Design Limitation"
        },
        {
            "summary_of_analysis": "PCF policy synchronization failures due to inconsistent distributed cache updates.",
            "planned_release": "v24.2.1",
            "answer_text": (
                "The PCF policy synchronization issues were traced to inconsistent updates in the distributed cache system. "
                "When policies were modified concurrently from multiple control nodes, the eventual consistency model caused temporary "
                "policy mismatches. We've implemented a consensus-based update protocol with version vectors to ensure "
                "all nodes converge to the same policy state. Additionally, a policy reconciliation job was added to "
                "detect and resolve any lingering inconsistencies during operation."
            ),
            "included_build": f"build_{random.randint(7000, 9999)}",
            "answer_code": f"FIX-{random.randint(10000, 99999)}",
            "answer_category": "Architecture Update"
        }
    ]

    project_options = list(projects.keys())  # Use all projects defined at the top
    tickets = {}

    for _ in range(count):
        project_key = random.choice(project_options)
        project_info = projects[project_key]
        project_name = project_info["project_name"]
        project_id = project_info["project_id"]

        numeric_ticket_id = str(random.randint(4000000, 9999999))
        issue_number = random.randint(80000, 99999)
        key_str = f"{project_key}-{issue_number}"
        created_dt = datetime.now().replace(microsecond=0)
        created_dt = created_dt - pd.Timedelta(days=random.randint(5, 30))
        updated_dt = created_dt + pd.Timedelta(days=random.randint(1, 5))

        description = random.choice(short_descriptions + long_descriptions)
        # description = random.choice(long_descriptions)
        # description = short_descriptions[0]
        title = random.choice(short_titles)
        status = random.choice(status_options)
        priority = random.choice(priority_names)
        answer = random.choice(long_answers)
        # answer = {
        #     "summary_of_analysis": "Root cause found ",
        #     "planned_release": "v23.9.1",
        #     "answer_text": ("", ""),
        #     "included_build": f"build_{random.randint(7000, 9999)}",
        #     "answer_code": f"FIX-{random.randint(10000, 99999)}",
        #     "answer_category": "Bug Fix"
        # }
        comments_list = random.sample(comments_bank, k=random.randint(1, 3))

        ticket = {
            "url": f"{base_url}/{key_str}",
            "key": key_str,
            "created": created_dt.strftime("%Y-%m-%dT%H:%M:%S.000+0200"),
            "last_updated": updated_dt.strftime("%Y-%m-%dT%H:%M:%S.000+0200"),
            "environment": None,
            "status_name": status,
            "labels": [],
            "project_id": project_id,
            "project_key": project_key,
            "project_name": project_name,
            "priority_id": str(10500 + priority_names.index(priority)),
            "priority_name": priority,
            "linked_issues": [],
            "components": random.sample(components_list, k=random.randint(1, 2)),
            "attachments": [],
            "title": title,
            "description": description,
            "detected_language": "en",
            "comments": [
                {
                    "detected_language": "en",
                    "content": comment,
                    "url": f"{base_url}/{key_str}?focusedId={random.randint(19000000, 19999999)}#comment-{random.randint(19000000, 19999999)}"
                }
                for comment in comments_list
            ],
            "Answer": answer,
            "project_options": project_options
        }

        tickets[numeric_ticket_id] = ticket

    return tickets

# Helper function to get the appropriate background class based on priority
def priority_bg(priority):
    if priority == "Critical":
        return "criticalbackground"
    elif priority == "Major":
        return "majorbackground"
    elif priority == "Minor":
        return "minorbackground"
    else:
        return "minorbackground"

# Helper function to get shortened status code
def get_status_code(status):
    if status == "Open":
        return "O"
    elif status == "In Progress":
        return "IP"
    elif status == "Verify":
        return "V"
    elif status == "Resolved":
        return "R"
    else:
        return status[0]  # First letter as fallback

# Helper function to get shortened priority code
def get_priority_code(priority):
    if priority == "Critical":
        return "C"
    elif priority == "Major":
        return "M"
    elif priority == "Minor":
        return "m"
    else:
        return priority[0]  # First letter as fallback

# Helper function to format date for better display
def format_date(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.000+0200")
        return dt.strftime("%Y-%m-%d")
    except:
        return date_str

# Load CSS styles
def load_css():
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
    # .card {
    #     width: 300px !important;
    #     margin: 10px !important;
    #     transition: all 0.3s ease !important;
    #     box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
    #     cursor: pointer;
    #     overflow: hidden;
    #     border-radius: 8px !important;
    #     transition: all 0.3s ease;
    #     height: auto !important;
    #     display: flex;
    #     flex-direction: column;
    # }
    .card:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }
    # .card.expanded .details-section {
    #     max-height: 1000px !important; 
    #     overflow: visible !important;
    # }
    # .card .ui.button, .card a.button {
    #     cursor: pointer;
    #     z-index: 10;
    #     position: relative;
    # }

    .card .key-link {
        color: inherit;
        font-weight: bold;
        text-decoration: none;
        position: relative;
        z-index: 10;
    }

    # .card .key-link:hover {
    #     text-decoration: underline;
    #     color: #1e70bf;
    # }
    
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
    # .card-actions {
    #     display: flex;
    #     justify-content: space-between;
    #     margin-top: 10px;
    # }
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
    
    /* Dark mode toggle */
    # .dark-mode-toggle {
    #     position: fixed;
    #     bottom: 20px;
    #     right: 20px;
    #     z-index: 999;
    #     background: rgba(0,0,0,0.7);
    #     color: white;
    #     border: none;
    #     border-radius: 50%;
    #     width: 50px;
    #     height: 50px;
    #     display: flex;
    #     align-items: center;
    #     justify-content: center;
    #     cursor: pointer;
    #     box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    #     transition: all 0.3s;
    # }
    
    # .dark-mode-toggle:hover {
    #     background: rgba(0,0,0,0.9);
    #     transform: scale(1.1);
    # }
    # .dark-mode {
    #     background-color: #222 !important;
    #     color: #eee !important;
    # }
    # .dark-mode .card {
    #     background-color: #333 !important;
    #     color: #eee !important;
    #     border: 1px solid #444 !important;
    # }
    # .dark-mode .meta {
    #     color: #ddd !important;
    # }
    # .dark-mode .progress-bar {
    #     background-color: #444 !important;
    # }
    # .dark-mode .ui.statistic .value, 
    # .dark-mode .ui.statistic .label {
    #     color: #eee !important;
    # }
    
    # /* Responsive improvements */
    # @media (max-width: 768px) {
    #     .card {
    #         width: 100% !important;
    #     }
    #     .ui.statistics {
    #         display: flex;
    #         flex-wrap: wrap;
    #     }
    #     .ui.statistics .statistic {
    #         flex: 1 0 50%;
    #         margin-bottom: 10px !important;
    #     }
    # }
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

# Function to create export button
def create_export_button(tickets_list):
    if st.button("Export Tickets to CSV"):
        # Create a flattened dataframe
        export_data = []
        for ticket in tickets_list:
            flat_ticket = {
                "key": ticket["key"],
                "title": ticket["title"],
                "description": ticket["description"],
                "status": ticket["status_name"],
                "priority": ticket["priority_name"],
                "project": ticket["project_name"],
                "created": format_date(ticket["created"]),
                "updated": format_date(ticket["last_updated"]),
                "components": ", ".join(ticket["components"]),
                "category": ticket["Answer"]["answer_category"],
                "solution": ticket["Answer"]["answer_text"],
                "planned_release": ticket["Answer"]["planned_release"],
                "build": ticket["Answer"]["included_build"]
            }
            export_data.append(flat_ticket)
        
        export_df = pd.DataFrame(export_data)
        
        # Convert dataframe to CSV
        csv = export_df.to_csv(index=False)
        
        # Create download button
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="5g_tickets_export.csv",
            mime="text/csv"
        )

# Function to display advanced filtering options
def display_advanced_filters():
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
            "date_range": date_range if date_option != "All Dates" else None,
            "categories": selected_categories
        }

# Dark mode toggle function
def dark_mode_toggle():
    """Create a toggle for dark mode"""
    
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

# Cache ticket data across reruns
# @st.cache_data(ttl=300)  # Cache for 5 minutes
def get_tickets(count=20):
    return generate_fake_5g_tickets(count)

# Main application
def main():
    
    # Load CSS
    load_css()
    
    if 'filters' not in st.session_state:
        st.session_state.filters = {
            'projects': [],
            'priority': [],
            'status': [],
            'search': ""
        }
    
    # Generate fake tickets (you can adjust the count)
    tickets = get_tickets(1)
    
    # Convert to a list for easier manipulation
    tickets_list = [ticket for _, ticket in tickets.items()]
    
    # Sidebar - Data options
    st.sidebar.markdown("## Data Options")
    
    # Number of tickets to display
    ticket_count = st.sidebar.slider("Number of tickets to display", 5, 50, 20, 5)
    if ticket_count != len(tickets_list):
        tickets = get_tickets(ticket_count)
        tickets_list = [ticket for _, ticket in tickets.items()]
    
    # Export data option
    export_format = st.sidebar.selectbox("Export Format", ["CSV", "JSON", "Excel"])
    if st.sidebar.button("Export Data"):
        st.sidebar.success(f"Data export in {export_format} format initiated!")
        
    # Sidebar filters
    st.sidebar.write("## Filter Options")
    st.sidebar.write("")
    
    # Toggle dark mode
    dark_mode_toggle()
    
    # Project type filter using multiselect
    available_projects = list(set([t["project_key"] for t in tickets_list]))
    selected_projects = st.sidebar.multiselect(
        label='Which project type you are looking for?',
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
    
    # Store filter selections
    st.session_state.filters['projects'] = selected_projects
    st.session_state.filters['priority'] = selected_priorities
    st.session_state.filters['status'] = selected_statuses
    
    # Display active filters at the top of main content area
    active_filters = []
    if selected_projects and len(selected_projects) < len(available_projects):
        active_filters.append(f"Projects: {', '.join(selected_projects)}")
    if selected_priorities:
        active_filters.append(f"Priority: {', '.join(selected_priorities)}")
    if selected_statuses:
        active_filters.append(f"Status: {', '.join(selected_statuses)}")
        

    # Advanced filters
    display_advanced_filters()
    
    # Apply filters to tickets list
    filtered_tickets = tickets_list.copy()
    
    # Filter by selected projects if any are selected
    if selected_projects:
        tickets_list = [t for t in tickets_list if t["project_key"] in selected_projects]
    
    # Search bar
    c1, c2 = st.columns([6, 1])
    text_search = c1.text_input(
        label="Search", 
        value=st.session_state.filters.get('search', ""),
        max_chars=150,
        label_visibility='collapsed',
        placeholder="Search by title, description, or key"
    )
    text_search = unidecode(text_search.lower())
    st.session_state.filters['search'] = text_search
    
    # Search button
    c2.button(
        label="", 
        icon=":material/search:", 
        use_container_width=True, 
        type="primary", 
        on_click=None
    )
    
    # Active filters display
    if active_filters:
        st.markdown("**Active Filters:**")
        filter_html = ""
        for filter_text in active_filters:
            filter_html += f'<span class="filter-tag">{filter_text}</span>'
        st.markdown(f"""<div style="margin-bottom: 15px;">{filter_html}</div>""", unsafe_allow_html=True)
    
    # Filter by selected projects if any are selected
    if selected_projects:
        tickets_list = [t for t in tickets_list if t["project_key"] in selected_projects]
    
    # Filter by selected priorities if any are selected
    if selected_priorities:
        tickets_list = [t for t in tickets_list if t["priority_name"] in selected_priorities]
    
    # Filter by selected statuses if any are selected
    if selected_statuses:
        tickets_list = [t for t in tickets_list if t["status_name"] in selected_statuses]

    # Filter by text search if provided
    if text_search:
        filtered_tickets = []
        for ticket in tickets_list:
            searchable_text = (
                unidecode(ticket["title"].lower()) + " " +
                unidecode(ticket["description"].lower()) + " " +
                unidecode(ticket["key"].lower()) + " " +
                unidecode(ticket["Answer"]["answer_category"].lower()) + " " +
                unidecode(ticket["Answer"]["summary_of_analysis"].lower())
            )
            if text_search in searchable_text:
                filtered_tickets.append(ticket)
        tickets_list = filtered_tickets
        
    # Additional sidebar filters
    cb_view_details = st.sidebar.checkbox('View Details', value=True)
        
    # Use classes instead of inline styles for better control
    if cb_view_details:
        details_class = ""
        card_class = "card expanded"
    else:
        details_class = "details-hidden"
        card_class = "card compact"
    
    # Sorting options
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
    
    selectbox_orderby = st.sidebar.selectbox("Order By", sort_options)
    
    # Clear selections button
    if 'selectbox_project_key' not in st.session_state:
        st.session_state.selectbox_project_key = 10
        st.session_state.selectbox_priority_key = 20
        st.session_state.selectbox_status_key = 30
    
    def reset_button():
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
    
    clear_button = st.sidebar.button(
        label='Clear All Filters', on_click=reset_button
    )
    
    # Apply sorting based on selection
    if selectbox_orderby == 'Key A → Z':
        tickets_list.sort(key=lambda x: x["key"])
    elif selectbox_orderby == 'Key Z → A':
        tickets_list.sort(key=lambda x: x["key"], reverse=True)
    elif selectbox_orderby == 'Priority ↓':
        priority_order = {"Critical": 0, "Major": 1, "Minor": 2}
        tickets_list.sort(key=lambda x: priority_order.get(x["priority_name"], 3))
    elif selectbox_orderby == 'Priority ↑':
        priority_order = {"Critical": 0, "Major": 1, "Minor": 2}
        tickets_list.sort(key=lambda x: priority_order.get(x["priority_name"], 3), reverse=True)
    elif selectbox_orderby == 'Status ↓':
        status_order = {"Open": 0, "In Progress": 1, "Verify": 2, "Resolved": 3}
        tickets_list.sort(key=lambda x: status_order.get(x["status_name"], 4))
    elif selectbox_orderby == 'Status ↑':
        status_order = {"Open": 0, "In Progress": 1, "Verify": 2, "Resolved": 3}
        tickets_list.sort(key=lambda x: status_order.get(x["status_name"], 4), reverse=True)
    elif selectbox_orderby == 'Created ↓':
        tickets_list.sort(key=lambda x: x["created"], reverse=True)
    elif selectbox_orderby == 'Created ↑':
        tickets_list.sort(key=lambda x: x["created"])
    elif selectbox_orderby == 'Updated ↓':
        tickets_list.sort(key=lambda x: x["last_updated"], reverse=True)
    elif selectbox_orderby == 'Updated ↑':
        tickets_list.sort(key=lambda x: x["last_updated"])
    
    # Ticket statistics
    open_count = sum(1 for t in tickets_list if t["status_name"] == "Open")
    in_progress_count = sum(1 for t in tickets_list if t["status_name"] == "In Progress")
    critical_count = sum(1 for t in tickets_list if t["priority_name"] == "Critical")
    major_count = sum(1 for t in tickets_list if t["priority_name"] == "Major")

    st.write("")
    
    ticket_scorecard = """<div id="mydiv" class="ui centered cards">"""
    
    # Generate cards for each ticket
    for ticket in tickets_list:
        # Generate a unique ID for this ticket for DOM manipulation
        # Use timestamp-based ID to ensure uniqueness
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
            <div class="content {priority_bg(ticket["priority_name"])}">
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
                        <span class="ticket-badge {status_class}">{get_status_code(ticket["status_name"])}</span>
                        <span class="tooltiptext">{ticket["status_name"]}</span><br>
                        <p class="kpi text">Status</p>
                    </div>
                    <div class="column kpi number tooltip">
                        <span class="ticket-badge {priority_class}">{get_priority_code(ticket["priority_name"])}</span>
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
                    
                    // No expand button handling needed
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
    
# Run the main application
if __name__ == "__main__":
    main()
