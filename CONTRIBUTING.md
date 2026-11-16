Contributing
Thanks for your interest in the SRE Final Project.

Development Workflow
Fork or clone the repository.
Create a new branch.
Make and test your changes.
Keep infrastructure and application changes separated when possible.
Commit using clear commit messages.
Open a pull request describing the change.
Local Testing
Before submitting changes, verify:

The Python application starts successfully.
/health returns HTTP 200.
/metrics exposes Prometheus metrics.
The Docker image builds successfully.
Kubernetes manifests pass kubectl apply --dry-run=client.
Kubernetes Pods reach the Running state.
Commit Style
Examples:

feat: add application metrics
fix: update Kubernetes health probe
docs: improve deployment instructions
monitoring: add Prometheus alert rule
Security
Do not commit passwords, tokens, private SSH keys, .env files, or other secrets.
