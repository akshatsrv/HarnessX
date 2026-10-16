variable "project_id" {
  type        = string
  description = "The Google Cloud Project ID"
}

variable "region" {
  type        = string
  description = "The GCP region for deployments"
  default     = "us-central1"
}

variable "container_image" {
  type        = string
  description = "Container image URI for the FastAPI backend"
  default     = "gcr.io/google-samples/hello-app:1.0"
}
