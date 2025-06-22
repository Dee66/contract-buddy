# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability, please open an issue or contact the maintainers directly. We will respond promptly and coordinate remediation.

## Automated Security Scanning

This project enforces security best practices via:
- **Dependabot:** Automated dependency and GitHub Actions workflow updates.
- **pip-audit:** Python dependency vulnerability scanning on every PR, push, and nightly.
- **Trivy:** Container image vulnerability scanning for all Docker images.
- **Gitleaks:** Automated secrets detection in all code and PRs.
- **Branch Protection:** Security scan jobs are required for merging and deployment.

## Required Branch Protection

The following status checks **must be required** in your GitHub branch protection rules to ensure no insecure code is merged:
- Python Dependency Vulnerability Scan
- Trivy Container Vulnerability Scan
- Gitleaks Secrets Detection

## Security Scan Failures: Triage & Remediation

If a security scan fails in CI:
1. **Review the CI logs** for details on the vulnerability or secret detected.
2. **For dependency vulnerabilities:**
   - Update the affected package to a secure version, or apply a patch if available.
   - If a fix is not available, document the risk and mitigation in the PR.
3. **For container image vulnerabilities:**
   - Update the base image or affected system packages.
   - Rebuild and rescan the image.
4. **For secrets detection:**
   - Remove the secret from code and rotate it in AWS or your secret manager.
   - Force-push removal if necessary and document the incident.
5. **Re-run the CI pipeline** to confirm remediation.

## Container Build Caching

For faster CI, consider enabling Docker layer caching in your GitHub Actions workflows using the `actions/cache` or `docker/build-push-action` cache features. This reduces build times and cost, especially for large images.

## Optional: Centralized Security Alerting

For enterprise environments, integrate with AWS Security Hub or your SIEM of choice to forward vulnerability and secrets alerts for centralized monitoring and incident response.

## Disclosure Policy

We follow responsible disclosure and will credit reporters in release notes if desired.
