"""
Lead Agent
==========

Uses Google ADK's Agent class to orchestrate:
1. Scrape / enrich target leads.
2. Generate personalised outreach emails.
3. Publish an event so other agents (e.g. ContentAgent) can react.

Heavy lifting (scraping, enrichment, email) is delegated to *tools* so they
can be mocked in unit tests.
"""

from adk import Agent, Task, tool
from typing import List, Dict
from .tools.scraper_tool import scrape_and_enrich
from supabase import create_client
import os, json, datetime
from google.cloud import pubsub_v1

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
PUBSUB_TOPIC = os.getenv("PUBSUB_TOPIC_LEAD_CREATED", "lead-created")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(os.getenv("GCP_PROJECT"), PUBSUB_TOPIC)

class LeadAgent(Agent):
    """Collects and outreaches to leads."""

    @tool(name="scrape_leads")
    def scrape_leads(self, query: str, limit: int = 50) -> List[Dict]:
        """Searches the web for companies/people & enriches them."""
        return scrape_and_enrich(query, limit)

    def run(self, task: Task):
        target_query = task.input.get("query", "plumber houston tx")
        leads = self.scrape_leads(target_query, limit=task.input.get("limit", 50))

        # Store leads -> Supabase
        supabase.table("leads").insert(leads).execute()

        # Fire Pub/Sub event
        publisher.publish(topic_path, json.dumps({"query": target_query, "count": len(leads)}).encode())
        task.set_output({"stored": len(leads)})
