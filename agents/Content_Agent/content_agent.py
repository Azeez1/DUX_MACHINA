"""Content Agent

Listens for 'lead-created' events and prepares social media posts referencing the
freshly-scraped lead cohort.

Note: For v0.1 we assume manual trigger (CLI / HTTP). In v0.2 you'll bind a
Pub/Sub push subscription to `/api/content-agent/webhook`.
"""

from adk import Agent, Task, tool
from typing import Dict
import os, json, random
from .tools.image_tool import generate_visual
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

POST_TEMPLATES = [
    "Need more qualified leads but short on time? 🚀 Our AI just scraped {count} fresh prospects so you don't have to. #GrowthHacks",
    "We love saving SMBs time—{count} new contacts queued for outreach. Let the bots handle prospecting while you close deals! 💼🤖"
]

class ContentAgent(Agent):
    """Generates & schedules social posts."""

    @tool(name="generate_post")
    def generate_post(self, count: int) -> Dict:
        """Returns copy + generated image URL."""
        copy = random.choice(POST_TEMPLATES).format(count=count)
        image_url = generate_visual(copy)
        return {"copy": copy, "image_url": image_url}

    def run(self, task: Task):
        lead_count = task.input.get("count", 100)
        post = self.generate_post(lead_count)
        supabase.table("social_queue").insert(post).execute()
        task.set_output(post)
