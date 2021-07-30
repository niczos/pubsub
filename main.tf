provider "google" {
  project     = var.project
  region      = var.region
}

resource "google_pubsub_topic" "demo" {
  name = "${var.project_name}-topic"
}

resource "google_pubsub_subscription" "demo" {
  name = "${var.project_name}-sub"
  topic = google_pubsub_topic.demo.name
}