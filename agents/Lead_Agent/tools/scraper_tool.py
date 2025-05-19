"""Stub scraper tool.

In production swap this with Browserless + puppeteer-core or an external API like Serper.dev.
"""
from typing import List, Dict
import random, uuid, datetime

def scrape_and_enrich(query: str, limit: int = 50) -> List[Dict]:
    """Fake lead generator for early tests."""
    sample = []
    for _ in range(limit):
        sample.append({
            "id": str(uuid.uuid4()),
            "company": f"{query.title()} Corp {_}",
            "contact_name": "Jane Doe",
            "email": f"jane{_}@example.com",
            "source_query": query,
            "timestamp": datetime.datetime.utcnow().isoformat()
        })
    return sample
