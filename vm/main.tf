provider "google" {
    project = var.project
}

resource "google_compute_instance" "syslog" {
  name         = "syslog"
  machine_type = "e2-small"
  zone         = "europe-central2-a"


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
