provider "google" {
  project     = var.project
  region      = var.region
}

resource "google_pubsub_topic" "example" {
  name = "topic1"
}

resource "google_pubsub_subscription" "example" {
  name  = "subscription1"
  topic = google_pubsub_topic.example.name
}