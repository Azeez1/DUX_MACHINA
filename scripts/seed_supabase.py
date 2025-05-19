"""Creates base tables in Supabase from your local machine.

Run:  python scripts/seed_supabase.py
"""
from supabase import create_client
import os, json, pathlib

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def create_tables():
    ddl = [
        """create table if not exists leads (
                id uuid primary key,
                company text,
                contact_name text,
                email text,
                source_query text,
                timestamp timestamptz
            );""",
        """create table if not exists social_queue (
                id serial primary key,
                copy text,
                image_url text,
                created_at timestamptz default now()
            );"""
    ]
    for q in ddl:
        supabase.postgrest.rpc("sql", dict(query=q)).execute()

if __name__ == "__main__":
    create_tables()
    print("✅ Supabase schema seeded")
