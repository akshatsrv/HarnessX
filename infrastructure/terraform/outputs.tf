output "backend_url" {
  value       = google_cloud_run_v2_service.backend.uri
  description = "The URL of the deployed FastAPI backend"
}

output "storage_bucket_name" {
  value       = google_storage_bucket.claims_bucket.name
  description = "Name of the Cloud Storage bucket for claim documents"
}

output "bigquery_dataset_id" {
  value       = google_bigquery_dataset.claims_dataset.dataset_id
  description = "BigQuery dataset ID for claims analytics"
}
