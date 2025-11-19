
# -----------------------------------
# Create Cloud Run service account
# -----------------------------------
resource "google_service_account" "cloud_run_sa" {
  account_id   = "cloud-run-sa"
  display_name = "Cloud Run Service Account"
}


