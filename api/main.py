"""Thin adapter so Cloud Run can serve the ADK fastapi instance."""
import importlib

# Lazy-load to avoid circular deps during local tests
adk_module = importlib.import_module("orchestration.adk_app")
app = adk_module.fastapi_app
