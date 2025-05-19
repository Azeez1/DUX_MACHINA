# Dux Machina — MVP Skeleton (v0.1)

This repo contains the minimal, fully‑commented scaffolding to run the **Lead Agent**, **Content Agent**, and the ADK orchestrator on Google Cloud Run.

```
dux-machina/
├── agents/
│   ├── lead_agent/
│   │   ├── tools/
│   │   └── lead_agent.py
│   └── content_agent/
│       ├── tools/
│       └── content_agent.py
├── orchestration/
│   └── adk_app.py
├── api/
│   └── main.py
├── infra/
│   └── terraform/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── scripts/
│   └── seed_supabase.py
└── Makefile
```

## n8n Flow (concept)

```mermaid
flowchart LR
    subgraph Lead_Agent
        A1[New Lead CSV Uploaded] --> A2[Scraper + Enricher]
        A2 --> A3[Personalised Email Tool]
        A3 --> A4[Publish "lead-created" Pub/Sub Topic]
    end

    subgraph Content_Agent
        B1["lead-created" Subscription] --> B2[Generate Social Post]
        B2 --> B3[Schedule via Meta/LinkedIn]
    end
```

*In `n8n`, you will create two separate workflows mirroring the above.  The Pub/Sub trigger subscribes to
`lead-created`; the Content Agent webhook URL is called with the new lead’s context.*
