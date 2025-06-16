[⬅ Back to Solution Foundation Overview](README.md)

# 📦 Solution Foundation Deliverables

> **What you'll walk away with from this step:**

---

- **📄 Comprehensive Business Case Summary:**  
  Clearly outlines the problem, solution, target users, and quantified impact for Contract Buddy.

  - _Acceptance Criteria:_ Reviewed and approved by project sponsor.

- **🗺️ High-Level MLOps Flow Diagram:**  
  Visualizes the end-to-end lifecycle from data ingestion and retrieval to code generation, delivery, and monitoring.

  - _Acceptance Criteria:_ Diagram reviewed by architect and aligns with blueprint.

- **📝 Initial Risk Log:**  
  Documents identified technical, ethical, and operational risks with mitigation strategies.

  - _Acceptance Criteria:_ Risks ranked by severity and reviewed by team.

- **💸 Initial Cost Model:**  
  Baseline estimate for infrastructure, cloud usage, and model/API costs.

  - _Acceptance Criteria:_ Estimates validated against cloud provider calculators.

- **📚 Architectural Decision Records (ADRs):**  
  Captures key technical and strategic decisions for future reference.
  - _Acceptance Criteria:_ ADRs follow template and are version-controlled.

---

## 📄 Templates & References

- [ADR Template](https://github.com/joelparkerhenderson/architecture_decision_record)
- [Risk Log Example](https://www.projectmanagementdocs.com/template/project-documents/risk-register/)
- [AWS Cost Calculator](https://calculator.aws.amazon.com/)

---

# 💸 Initial Cost Model

> **Purpose:**  
> Provide a realistic, transparent estimate of the infrastructure, cloud, and operational costs for Contract Buddy, using current (2025) market rates and best practices.  
> **All costs are estimated in South African Rand (ZAR).**  
> _(Assume 1 USD ≈ 18 ZAR for 2025 estimates.)_

---

## Cost Profiles

You can toggle between **Production** and **Development** cost estimates below, depending on the usage scenario.

---

<details>
<summary><strong>Production (24/7, always-on, ready for scale)</strong></summary>

### 1. Cloud Compute & Model Hosting

- **Model Inference (LLM):**

  - **OpenAI GPT-4 API:** ZAR 12,150–24,300/month (see detailed calculation above).
  - **Self-hosted OSS Model:** ZAR 18,660/month (24/7 GPU + storage).

- **Retrieval/Vector Database:** ZAR 1,260–1,800/month.

### 2. API & Web Hosting

- ZAR 1,800/month.

### 3. Storage & Data Transfer

- ZAR 5/month.

### 4. Monitoring & Logging

- ZAR 360–540/month.

### 5. CI/CD & DevOps

- ZAR 180–360/month.

### 6. Security & Compliance

- ZAR 900/month.

**Total Estimated Monthly Cost:**

- **Managed/Cloud API:** ZAR 17,015–29,125
- **Self-Hosted OSS:** ZAR 23,705

</details>

---

<details open>
<summary><strong>Development (on-demand, pay-as-you-go, dormant when not in use)</strong></summary>

### 1. Cloud Compute & Model Hosting

- **Model Inference (LLM):**

  - **OpenAI GPT-4 API:**
    - Assume 100 requests/day × 1,500 tokens/request × 22 workdays ≈ 3.3M tokens/month
    - ZAR 270–540 per 1M tokens → **ZAR 891–1,782/month**
  - **Self-hosted OSS Model:**
    - Run GPU instance only during dev/testing (e.g., 4 hours/day × 22 days = 88 hours/month)
    - ZAR 21.60/hour × 88 ≈ **ZAR 1,900/month**
    - Add 20% for storage, bandwidth, and backups: ≈ **ZAR 2,280/month**

- **Retrieval/Vector Database:**
  - ZAR 300–500/month (smaller instance, less storage).

### 2. API & Web Hosting

- ZAR 200–400/month (smaller container, lower traffic).

### 3. Storage & Data Transfer

- ZAR 2/month.

### 4. Monitoring & Logging

- ZAR 50–100/month (basic or open source).

### 5. CI/CD & DevOps

- ZAR 50–100/month.

### 6. Security & Compliance

- ZAR 0–200/month.

**Total Estimated Monthly Cost:**

- **Managed/Cloud API:** ZAR 1,493–3,024
- **Self-Hosted OSS:** ZAR 2,582–3,382

</details>

---

## How to Use This Template

- **For production:** Use the 24/7 always-on estimates for budgeting and scaling.
- **For development:** Use the on-demand estimates to minimize costs while building and testing.
- **Tip:**
  - Use cloud provider cost calculators for the region.
  - Monitor actual usage and adjust estimates monthly.

---

## 📊 Cost Summary Tables

### Production Cost Summary (ZAR/month)

| Category              | Estimated Cost (Managed/Cloud API) | Estimated Cost (Self-Hosted OSS) |
| --------------------- | :--------------------------------: | :------------------------------: |
| Model Inference       |          R12,150–R24,300           |             R18,660              |
| Vector Database       |               R1,260               |              R1,800              |
| API & Web Hosting     |               R1,800               |              R1,800              |
| Storage & Bandwidth   |                 R5                 |                R5                |
| Monitoring & Logging  |             R360–R540              |               R360               |
| CI/CD & DevOps        |             R180–R360              |               R180               |
| Security & Compliance |                R900                |               R900               |
| **Total**             |        **R17,015–R29,125**         |           **R23,705**            |

---

### Development Cost Summary (ZAR/month)

| Category              | Estimated Cost (Managed/Cloud API) | Estimated Cost (Self-Hosted OSS) |
| --------------------- | :--------------------------------: | :------------------------------: |
| Model Inference       |            R891–R1,782             |              R2,280              |
| Vector Database       |             R300–R500              |               R500               |
| API & Web Hosting     |             R200–R400              |               R400               |
| Storage & Bandwidth   |                 R2                 |                R2                |
| Monitoring & Logging  |              R50–R100              |               R50                |
| CI/CD & DevOps        |              R50–R100              |               R50                |
| Security & Compliance |              R0–R200               |               R200               |
| **Total**             |         **R1,493–R3,024**          |        **R2,582–R3,382**         |

---

> **Managerial Overview:**
>
> - **Production:** Budget for **R17,000–R29,000/month** (managed) or **R24,000/month** (self-hosted) for a 24/7, scalable solution.
> - **Development:** Expect **R1,500–R3,000/month** (managed) or **R2,500–R3,400/month** (self-hosted) for on-demand, cost-efficient development and testing.
> - **Key Drivers:** Model inference and GPU hosting are the largest costs; optimize by scaling resources to actual usage.
