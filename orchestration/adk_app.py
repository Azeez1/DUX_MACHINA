"""ADK Application entrypoint.

Registers the LeadAgent and ContentAgent and exposes them via REST-like
endpoints automatically through ADK's FastAPI integration.
"""
from adk import AdkApp
from agents.lead_agent.lead_agent import LeadAgent
from agents.content_agent.content_agent import ContentAgent

app = AdkApp(
    agents=[
        LeadAgent(name="lead_agent"),
        ContentAgent(name="content_agent")
    ]
)

# `app.fastapi` is a FastAPI instance that Cloud Run will serve.
fastapi_app = app.fastapi
