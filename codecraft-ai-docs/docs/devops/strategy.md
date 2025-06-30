[⬅ Back](../index.md)

# DevOps & Developer Experience Strategy – CodeCraft AI

This document outlines a production-grade, AWS-native, and Clean Architecture-aligned approach for managing the complexity of a modern AI portfolio project. It is designed to help senior engineers and teams maintain operational clarity, scalability, and developer happiness as the project grows.

---

## 1. **Principles**

- **Single Source of Truth:** All configuration, dependencies, and scripts are version-controlled and documented.
- **Automation First:** Manual steps are minimized via Makefile targets, CI/CD pipelines, and IaC.
- **Environment Parity:** Local, staging, and production environments are as similar as possible.
- **Security & Governance:** Secrets are never hardcoded; use AWS Secrets Manager, SSM, or `.env` (for local only).
- **Observability:** Logging, monitoring, and error reporting are built-in from the start.

---

## 2. **Key Tools & Their Roles**

| Tool/Script          | Purpose                                         | How to Use                                                                                                           |
| -------------------- | ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Nox**              | One-command, cross-platform developer workflows | `nox -s <session>`                                                                                                   |
| **requirements/\***  | Python dependency management (pip-tools)        | `nox -s sync_deps` / `nox -s install`                                                                                |
| **Docker**           | Build, test, and run in isolated environments   | `nox -s docker_build_api`, `nox -s docker_build_ingestion`, `nox -s docker_test_api`, `nox -s docker_test_ingestion` |
| **AWS CDK**          | Infrastructure as Code (IaC)                    | `nox -s cdk_deploy`                                                                                                  |
| **pytest**           | Automated testing                               | `nox -s test` or `pytest`                                                                                            |
| **Jupyter Notebook** | Interactive demos & rapid prototyping           | Open in VS Code or JupyterLab                                                                                        |
| **Git**              | Version control                                 | `git add/commit/push`                                                                                                |

---

## 3. **Recommended Workflow**

### **A. Local Development**

1. **Clone the repo and create a virtual environment:**

   ```sh
   git clone <repo-url>
   cd codecraft-ai
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install nox
   ```

2. **Install dev dependencies:**

   ```sh
   nox -s install
   ```

3. **Sync dependencies if you change any `.in` files:**

   ```sh
   nox -s sync_deps
   ```

4. **Run the API locally:**

   ```sh
   nox -s run_api_dev
   ```

5. **Run tests:**

   ```sh
   nox -s test
   ```

6. **Use the notebook:**
   - Start the API server.
   - Open `notebooks/ai_demo.ipynb` in VS Code or JupyterLab.
   - Run cells to interact with your AI system.

### **B. Staging & Production Deployment**

1. **Ensure code is merged to `main` and passes all tests.**
2. **Deploy to AWS:**
   ```sh
   nox -s cdk_deploy
   ```
3. **Monitor logs and performance metrics.**
4. **Run smoke tests to verify deployment.**

---

## 4. **Directory Structure**

```
/codecraft-ai
|-- /app                  # Application code
|   |-- __init__.py
|   |-- main.py           # Entry point
|   |-- api.py            # API definitions
|   |-- model.py          # AI/ML model code
|   |-- service.py        # Business logic
|   |-- repository.py     # Data access
|
|-- /notebooks            # Jupyter notebooks for demos & prototyping
|   |-- ai_demo.ipynb
|
|-- /tests                # Unit and integration tests
|   |-- __init__.py
|   |-- test_api.py
|   |-- test_model.py
|
|-- /infrastructure       # Infrastructure as Code (IaC)
|   |-- app.py            # CDK app
|   |-- lambda_stack.py   # Lambda function stack
|   |-- api_gateway.py    # API Gateway configuration
|
|-- requirements.txt      # Python package dependencies
|-- README.md             # Project documentation
|-- Makefile              # Makefile for automation
```

---

## 5. **CI/CD Pipeline Overview**

1. **Code is pushed to the repository.**
2. **CI pipeline is triggered:**
   - Install dependencies
   - Run linters
   - Execute tests
3. **CD pipeline is triggered on `main` branch:**
   - Build Docker image
   - Push image to ECR
   - Deploy CloudFormation stack
4. **Post-deployment:**
   - Run smoke tests
   - Notify team of successful deployment

---

## 6. **Troubleshooting Common Issues**

- **Dependency conflicts:** Ensure all dependencies are specified in `requirements.in` and run `nox -s sync_deps`.
- **Docker issues:** Ensure Docker Desktop is running. Use `docker-compose down` to stop containers.
- **AWS permissions:** Ensure your AWS credentials have the necessary permissions. Use `aws sts get-caller-identity` to check.
- **CDK issues:** Ensure you have the latest AWS CDK version. Run `npm install -g aws-cdk` to update.

---

## 7. **Further Reading & Resources**

- **AWS Well-Architected Framework:** Best practices for architecting on AWS.
- **12-Factor App Methodology:** Principles for building modern, scalable web applications.
- **Clean Architecture:** A software design philosophy that emphasizes separation of concerns and testability.
- **Docker Documentation:** Official documentation for Docker.
- **AWS CDK Documentation:** Official documentation for AWS Cloud Development Kit.

---

## 8. **Appendix**

- **A. Environment Variables**
  - `AWS_ACCESS_KEY_ID`: AWS access key
  - `AWS_SECRET_ACCESS_KEY`: AWS secret key
  - `AWS_DEFAULT_REGION`: AWS region (e.g., `us-west-2`)
  - `DOCKER_USERNAME`: Docker Hub username
  - `DOCKER_PASSWORD`: Docker Hub password
  - `SLACK_WEBHOOK_URL`: Slack webhook URL for notifications

- **B. Makefile Targets**
  - `make install`: Install Python dependencies
  - `make sync-deps`: Sync dependencies from `requirements.in`
  - `make run-api-dev`: Run the API in development mode
  - `make test`: Run tests
  - `make lint`: Run linters
  - `make docker-build`: Build the Docker image
  - `make docker-run`: Run the Docker container
  - `make cdk-deploy`: Deploy the CDK stack
  - `make cdk-destroy`: Destroy the CDK stack

---

## 9. **Changelog**

- **v1.0.0** - Initial release
  - Defined principles, key tools, and recommended workflow
  - Established directory structure and CI/CD pipeline overview
  - Documented troubleshooting tips and further reading resources

---

## 10. **Feedback & Contributions**

We welcome feedback and contributions to this document and the project. Please open an issue or submit a pull request with your suggestions.

---
