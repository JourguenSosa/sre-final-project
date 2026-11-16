# SRE Final Project

Final project for the SRE Academy focused on containerization, Kubernetes orchestration, monitoring, visualization, and alerting using common Site Reliability Engineering practices.

## Project Overview

This project implements a Python/Flask application instrumented with Prometheus metrics and deployed to a local Kubernetes cluster using Minikube.

The monitoring stack includes Prometheus, Grafana, and Alertmanager.

## Architecture

The project follows this monitoring flow:

Client → Kubernetes Service → Flask Application → Prometheus → Grafana / Alertmanager

The Flask application exposes:

- `/`
- `/health`
- `/metrics`
- `/simulate-error`

## Technologies

- Python
- Flask
- prometheus-client
- Docker
- Kubernetes
- Minikube
- Prometheus
- Grafana
- Alertmanager
- Git
- GitHub
- GitHub Actions

## Application Endpoints

| Endpoint | Purpose |
|---|---|
| `/` | Returns basic application status |
| `/health` | Health endpoint used by Kubernetes probes |
| `/metrics` | Exposes application metrics for Prometheus |
| `/simulate-error` | Generates an intentional HTTP 500 error for testing |

## Custom Metrics

The application exposes three main custom metrics.

### HTTP Requests

`sre_http_requests_total`

Counts HTTP requests by endpoint.

### HTTP Errors

`sre_http_errors_total`

Counts simulated application errors.

### Request Latency

`sre_http_request_duration_seconds`

Histogram used to measure application request latency.

## Docker

The application is packaged as a Docker image.

### Build the image

```bash
cd app
docker build -t sre-final-app:1.0 .
```

### Run locally

```bash
docker run -d --name sre-final-app -p 5000:5000 sre-final-app:1.0
```

### Test the application

```bash
curl http://localhost:5000/health
curl http://localhost:5000/metrics
```

## Kubernetes

The application runs on a local Kubernetes cluster using Minikube.

### Start Minikube

```bash
minikube start --driver=docker
```

### Load the application image

```bash
minikube image load sre-final-app:1.0
```

### Deploy

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

### Verify

```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

The application Deployment includes:

- Two replicas
- Readiness probe using `/health`
- Liveness probe using `/health`
- CPU and memory requests
- CPU and memory limits
- Kubernetes Service

## Prometheus

Prometheus runs inside Kubernetes and periodically scrapes the application's `/metrics` endpoint.

During testing, the `sre-final-app` target appeared as **UP** in Prometheus.

Example PromQL queries:

```promql
sre_http_requests_total
```

```promql
sre_http_errors_total
```

```promql
rate(sre_http_requests_total[1m])
```

## Grafana

Grafana runs inside Kubernetes and uses Prometheus as its data source.

The internal Prometheus URL is:

`http://prometheus:9090`

The dashboard created for the project is:

**SRE Final Project - Application Monitoring**

It includes three panels:

### HTTP Request Rate

```promql
rate(sre_http_requests_total[1m])
```

### Total HTTP Errors

```promql
sre_http_errors_total
```

### Average Request Latency

```promql
rate(sre_http_request_duration_seconds_sum[1m])
/
rate(sre_http_request_duration_seconds_count[1m])
```

## Alertmanager

Alertmanager is deployed inside Kubernetes and connected to Prometheus.

Prometheus recognizes the Alertmanager service at:

`alertmanager:9093`

A custom Prometheus alert rule was created:

`SREApplicationErrors`

The rule uses:

```promql
sre_http_errors_total > 0
```

### Small Alertmanager note

I got Alertmanager deployed and connected to Prometheus, and the custom alert rule is being loaded correctly. The last piece I couldn't fully get working was seeing the simulated application error show up as a `Firing` alert in the Alertmanager UI. Rather than pretending it worked, I'm leaving this documented as one of the remaining improvements for the project.

## CI with GitHub Actions

As an additional feature, the project includes a GitHub Actions CI workflow.

The workflow is located at:

`.github/workflows/ci.yml`

The pipeline:

1. Checks out the repository.
2. Configures Python.
3. Installs the application dependencies.
4. Validates the Python application.
5. Builds the Docker image.

The workflow runs automatically on pushes and pull requests targeting the `main` branch.

## Repository Structure

```text
sre-final-project/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── kubernetes/
│   ├── deployment.yaml
│   └── service.yaml
├── monitoring/
│   ├── prometheus/
│   │   ├── prometheus.yaml
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── alerts.yaml
│   ├── grafana/
│   │   └── grafana.yaml
│   └── alertmanager/
│       └── alertmanager.yaml
├── screenshots/
├── .gitignore
├── README.md
├── LICENSE.md
└── CONTRIBUTING.md
```

## Troubleshooting Performed

Several real troubleshooting scenarios occurred during the project.

### Docker Port Conflict

A local Python/Flask process was already using port `5000`, preventing Docker from binding to the same port.

The process was identified and stopped before restarting the Docker container.

### Kubernetes Image Availability

The locally built image was loaded directly into Minikube:

```bash
minikube image load sre-final-app:1.0
```

This allowed Kubernetes to use the application image without requiring an external container registry.

### Grafana OOMKilled

Grafana initially had a memory limit of `256Mi`.

Kubernetes terminated the container with:

```text
OOMKilled
Exit Code: 137
```

The Grafana resources were increased to:

```text
Memory request: 256Mi
Memory limit: 512Mi
```

After updating the Deployment, Grafana successfully reached `1/1 Running`.

### Alertmanager Integration

Prometheus successfully loaded the `SREApplicationErrors` rule and detected the configured Alertmanager endpoint.

The final end-to-end `Firing` state was not successfully demonstrated and remains a future improvement.

## SRE Concepts Demonstrated

- Application instrumentation
- Health checks
- Containerization
- Kubernetes orchestration
- Multiple application replicas
- Readiness probes
- Liveness probes
- Resource requests and limits
- Prometheus metrics collection
- PromQL
- Grafana dashboards
- Prometheus alert rules
- Alertmanager deployment
- Git version control
- GitHub
- Continuous Integration
- Troubleshooting and observability

## Evidence

The `screenshots/` directory contains evidence from the implementation, including:

- Kubernetes workloads
- Prometheus targets
- Grafana dashboard
- Alertmanager

## Known Improvements

Future improvements include:

- Complete the Alertmanager end-to-end `Firing` test
- Configure external Alertmanager notifications
- Add persistent storage for Prometheus and Grafana
- Use Kubernetes-native Prometheus service discovery
- Use Kubernetes Secrets for sensitive configuration
- Add HTTPS/TLS
- Expand the CI pipeline with automated application tests

## License

This project is licensed under the MIT License. See `LICENSE.md`.

## Contributing

Contribution guidelines are available in `CONTRIBUTING.md`.

## Author

**Jourguen Sosa**

SRE Academy Final Project