terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">=5.0"
    }
  }
  required_version = ">= 1.5.0"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_service_account" "adk_runner" {
  account_id   = "adk-runner"
  display_name = "ADK Cloud Run Service Account"
}

resource "google_cloud_run_v2_service" "adk" {
  name     = "dux-machina-adk"
  location = var.region
  template {
    service_account = google_service_account.adk_runner.email
    containers {
      image = var.container_image  # built via Cloud Build or GH Actions
      env {
        name  = "SUPABASE_URL"
        value = var.supabase_url
      }
      env {
        name  = "SUPABASE_KEY"
        value = var.supabase_service_key
      }
    }
  }
}

resource "google_pubsub_topic" "lead_created" {
  name = "lead-created"
}

output "cloud_run_url" {
  value = google_cloud_run_v2_service.adk.uri
}
