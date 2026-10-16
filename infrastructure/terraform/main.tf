terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Cloud Run Service for FastAPI Backend
resource "google_cloud_run_v2_service" "backend" {
  name     = "claimguard-api"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = var.container_image
      resources {
        limits = {
          cpu    = "2"
          memory = "2Gi"
        }
      }
      env {
        name  = "GCP_PROJECT_ID"
        value = var.project_id
      }
      env {
        name  = "GCP_REGION"
        value = var.region
      }
    }
  }
}

# Cloud Storage Bucket for Claims Documents
resource "google_storage_bucket" "claims_bucket" {
  name          = "${var.project_id}-claims-documents"
  location      = var.region
  force_destroy = false

  uniform_bucket_level_access = true
}

# BigQuery Dataset for Claims Analytics
resource "google_bigquery_dataset" "claims_dataset" {
  dataset_id                  = "claimguard_demo"
  friendly_name               = "ClaimGuard Demo Analytics"
  description                 = "Synthetic claims dataset and repair estimate baselines"
  location                    = var.region
  default_table_expiration_ms = null
}
