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

resource "google_compute_instance" "syslog" {
  name         = "syslog"
  machine_type = "e2-small"
  zone         = "us-central1-b"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-10"
    }
  }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral IP
    }
  }

  metadata_startup_script = file("${path.module}/init.sh")

}