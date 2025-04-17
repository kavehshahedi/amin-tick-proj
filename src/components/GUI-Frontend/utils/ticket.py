"""
Ticket management utilities for the TicketAssist application.

This module provides ticket data generation, formatting, and display functionality.
"""
from typing import Dict, List, Any, Optional, Union
import random
import uuid
import time
from datetime import datetime
from pathlib import Path
import json

import pandas as pd
from pydantic import BaseModel, Field


class Project(BaseModel):
    """Model representing a project in the ticket system."""
    project_name: str
    project_id: str


class TicketComment(BaseModel):
    """Model representing a comment on a ticket."""
    detected_language: str = "en"
    content: str
    url: str


class TicketAnswer(BaseModel):
    """Model representing an answer or solution for a ticket."""
    summary_of_analysis: str
    planned_release: str
    answer_text: str
    included_build: str
    answer_code: str
    answer_category: str


class Ticket(BaseModel):
    """Model representing a ticket in the system."""
    url: str
    key: str
    created: str
    last_updated: str
    environment: Optional[str] = None
    status_name: str
    labels: List[str] = Field(default_factory=list)
    project_id: str
    project_key: str
    project_name: str
    priority_id: str
    priority_name: str
    linked_issues: List[str] = Field(default_factory=list)
    components: List[str]
    attachments: List[str] = Field(default_factory=list)
    title: str
    description: str
    detected_language: str = "en"
    comments: List[TicketComment]
    Answer: TicketAnswer
    project_options: List[str]


class TicketGenerator:
    """
    Generator for creating fake 5G-related tickets for demonstration purposes.
    """
    
    # Static data for ticket generation
    PROJECTS = {
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
    
    STATUS_OPTIONS = ["Open", "In Progress", "Verify", "Resolved"]
    PRIORITY_NAMES = ["Minor", "Major", "Critical"]
    COMPONENTS_LIST = [
        "Compass", "The Cable Guys", "Service Engine", "Traffic Control", 
        "Kubernetes Operator", "Network Slice Manager", "Cloud Native Functions"
    ]
    
    COMMENTS_BANK = [
        "Can you please check if this can be fixed in the next drop?",
        "Fix is mentioned but no details are shared. Can someone clarify?",
        "This will be delivered in Drop#93. Patch is ready and needs verification.",
        "Seeing the same issue in test environment, can we expedite this?",
        "Similar issue was fixed in another project, can we reuse that solution?",
        "Is there a workaround for this until the permanent fix is deployed?"
    ]
    
    ANSWER_CATEGORIES = [
        "Bug Fix", "Root Cause Identified", "Performance Enhancement", 
        "Design Limitation", "Configuration Change", "Architecture Update"
    ]
    
    SHORT_TITLES = [
        "UPF crash during handover",
        "SMF timeout issue",
        "NRF registration fail",
        "Packet drop in edge site",
        "AMF restart loop",
        "PCF policy synchronization issues",
        "UDM data corruption during failover",
        "Network slice isolation breach",
        "NSSF selection algorithm deadlock",
        "UPF data path congestion"
    ]
    
    SHORT_DESCRIPTIONS = [
        "",
        "UPF failed after handover in a high-traffic zone.",
        "SMF didn't respond within expected time during session setup.",
        "NRF could not register NFs under high load.",
        "Edge site dropped packets intermittently.",
        "AMF pod restarted repeatedly after upgrade.",
        "PCF failing to synchronize policies across regions.",
        "UDM data corruption observed during automated failover tests.",
        "Network slice isolation compromised during peak load.",
        "NSSF selection algorithm deadlocked with multiple concurrent requests.",
        "UPF data path experiencing congestion with specific traffic patterns."
    ]
    
    LONG_DESCRIPTIONS = [
        "UPF experienced a critical failure during handover processing. Log analysis indicates a service mesh routing conflict causing gRPC retries to hang. This is reproducible under peak conditions in edge deployments.",
        "NRF failed to register new network functions during orchestrated deployment. Load testing shows memory bottlenecks and long GC pauses that align with the failure window.",
        "Session setup flows failed between AMF and SMF due to missing N11 signaling. Investigation reveals timeout misconfigurations and container-level resource starvation.",
        "PCF policy synchronization failed between geographical redundant sites resulting in policy inconsistency. Investigation shows network latency spikes during synchronization windows.",
        "Network slice resource allocation conflicts observed when concurrent slice creation requests are processed. Root cause appears to be race condition in the slice manager orchestrator."
    ]
    
    LONG_ANSWERS = [
        {
            "summary_of_analysis": "Root cause found in gRPC timeout and stale connection handling within UPF router module.",
            "planned_release": "v23.9.1",
            "answer_text": (
                "Upon detailed inspection, it was discovered that stale gRPC connections were not being reaped by the UPF control plane. "
                "This led to congestion in the listener thread pool, especially during gNB handovers. A fix was applied to include active timeout cleanup and connection recycling. "
                "Memory profiling confirmed improved behavior post-patch, and stress test under 10k sessions was passed successfully."
            ),
            "included_build": lambda: f"build_{random.randint(7000, 9999)}",
            "answer_code": lambda: f"FIX-{random.randint(10000, 99999)}",
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
            "included_build": lambda: f"build_{random.randint(7000, 9999)}",
            "answer_code": lambda: f"FIX-{random.randint(10000, 99999)}",
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
            "included_build": lambda: f"build_{random.randint(7000, 9999)}",
            "answer_code": lambda: f"FIX-{random.randint(10000, 99999)}",
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
            "included_build": lambda: f"build_{random.randint(7000, 9999)}",
            "answer_code": lambda: f"FIX-{random.randint(10000, 99999)}",
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
            "included_build": lambda: f"build_{random.randint(7000, 9999)}",
            "answer_code": lambda: f"FIX-{random.randint(10000, 99999)}",
            "answer_category": "Architecture Update"
        }
    ]
    
    @classmethod
    def generate_fake_5g_tickets(cls, count: int = 5) -> Dict[str, Any]:
        """
        Generate a specified number of fake 5G tickets.
        
        Args:
            count: Number of tickets to generate
            
        Returns:
            Dictionary of generated tickets with numeric IDs as keys
        """
        project_options = list(cls.PROJECTS.keys())
        tickets = {}
        
        for _ in range(count):
            # Select random project
            project_key = random.choice(project_options)
            project_info = cls.PROJECTS[project_key]
            project_name = project_info["project_name"]
            project_id = project_info["project_id"]
            
            # Generate ticket identifiers
            numeric_ticket_id = str(random.randint(4000000, 9999999))
            issue_number = random.randint(80000, 99999)
            key_str = f"{project_key}-{issue_number}"
            
            # Generate dates
            created_dt = datetime.now().replace(microsecond=0)
            created_dt = created_dt - pd.Timedelta(days=random.randint(5, 30))
            updated_dt = created_dt + pd.Timedelta(days=random.randint(1, 5))
            
            # Select random content
            description = random.choice(cls.SHORT_DESCRIPTIONS + cls.LONG_DESCRIPTIONS)
            title = random.choice(cls.SHORT_TITLES)
            status = random.choice(cls.STATUS_OPTIONS)
            priority = random.choice(cls.PRIORITY_NAMES)
            
            # Process answer template
            answer_template = random.choice(cls.LONG_ANSWERS)
            answer = {
                "summary_of_analysis": answer_template["summary_of_analysis"],
                "planned_release": answer_template["planned_release"],
                "answer_text": answer_template["answer_text"],
                "included_build": answer_template["included_build"]() if callable(answer_template["included_build"]) else answer_template["included_build"],
                "answer_code": answer_template["answer_code"]() if callable(answer_template["answer_code"]) else answer_template["answer_code"],
                "answer_category": answer_template["answer_category"]
            }
            
            # Generate random comments
            comments_list = random.sample(cls.COMMENTS_BANK, k=random.randint(1, 3))
            base_url = "localhost:8080/browse"
            
            # Create ticket object
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
                "priority_id": str(10500 + cls.PRIORITY_NAMES.index(priority)),
                "priority_name": priority,
                "linked_issues": [],
                "components": random.sample(cls.COMPONENTS_LIST, k=random.randint(1, 2)),
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


class TicketDisplay:
    """
    Utilities for displaying tickets and related UI elements.
    """
    
    @staticmethod
    def priority_bg(priority: str) -> str:
        """
        Get the appropriate CSS background class based on priority.
        
        Args:
            priority: The priority name (Critical, Major, Minor)
            
        Returns:
            CSS class name for styling
        """
        if priority == "Critical":
            return "criticalbackground"
        elif priority == "Major":
            return "majorbackground"
        elif priority == "Minor":
            return "minorbackground"
        else:
            return "minorbackground"
    
    @staticmethod
    def get_status_code(status: str) -> str:
        """
        Get shortened status code for display.
        
        Args:
            status: The status name (Open, In Progress, Verify, Resolved)
            
        Returns:
            Short code representation of the status
        """
        status_codes = {
            "Open": "O",
            "In Progress": "IP",
            "Verify": "V",
            "Resolved": "R"
        }
        return status_codes.get(status, status[0])
    
    @staticmethod
    def get_priority_code(priority: str) -> str:
        """
        Get shortened priority code for display.
        
        Args:
            priority: The priority name (Critical, Major, Minor)
            
        Returns:
            Short code representation of the priority
        """
        priority_codes = {
            "Critical": "C",
            "Major": "M",
            "Minor": "m"
        }
        return priority_codes.get(priority, priority[0])
    
    @staticmethod
    def format_date(date_str: str) -> str:
        """
        Format date string for better display.
        
        Args:
            date_str: The date string in ISO format
            
        Returns:
            Formatted date string (YYYY-MM-DD)
        """
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.000+0200")
            return dt.strftime("%Y-%m-%d")
        except Exception:
            return date_str


class TicketExporter:
    """
    Utilities for exporting ticket data in various formats.
    """
    
    @staticmethod
    def export_to_csv(tickets: List[Dict[str, Any]]) -> str:
        """
        Export tickets to CSV format.
        
        Args:
            tickets: List of ticket dictionaries
            
        Returns:
            CSV data as string
        """
        # Create a flattened dataframe
        export_data = []
        for ticket in tickets:
            flat_ticket = {
                "key": ticket["key"],
                "title": ticket["title"],
                "description": ticket["description"],
                "status": ticket["status_name"],
                "priority": ticket["priority_name"],
                "project": ticket["project_name"],
                "created": TicketDisplay.format_date(ticket["created"]),
                "updated": TicketDisplay.format_date(ticket["last_updated"]),
                "components": ", ".join(ticket["components"]),
                "category": ticket["Answer"]["answer_category"],
                "solution": ticket["Answer"]["answer_text"],
                "planned_release": ticket["Answer"]["planned_release"],
                "build": ticket["Answer"]["included_build"]
            }
            export_data.append(flat_ticket)
        
        export_df = pd.DataFrame(export_data)
        return export_df.to_csv(index=False)