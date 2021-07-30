provider "google" {
  project     = var.project
  region      = var.region
}

resource "google_pubsub_topic" "demo" {
  #name ="${google_pubsub_topic.demo.name}-topic"
  name = "demo-topic"
}

resource "google_pubsub_subscription" "demo" {
  #name  = "${google_pubsub_subscription.name}-subscription"
  name = "demo-sub"
  topic = google_pubsub_topic.demo.name
}
