variable "project_id" {
  description = "GCP project ID"
  type        = string
  default     = "caesaraiapis"
}

variable "region" {
  description = "GCP region for Cloud Run"
  type        = string
  default     = "us-central1"
}

variable "image" {
  description = "Docker image for Cloud Run"
  type        = string
}

variable "service_name" {
  description = "Name of the Cloud Run service"
  type        = string
  default     = "blustoryappvideoconverter"
}
