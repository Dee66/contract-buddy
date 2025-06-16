# 📚 Data Sourcing Strategy

## Purpose

Define the sources, licensing considerations, and ingestion process for all data used in Contract Buddy’s Retrieval-Augmented Generation (RAG) and model fine-tuning.

---

## 1. Foundational Model

- **Provider:**  
  Use a reputable foundational LLM (e.g., OpenAI GPT-4, Anthropic Claude, or open-source models like Llama 3).
- **Usage:**  
  The foundational model provides general code understanding and generation capabilities.

---

## 2. Supplemental Data for RAG

- **Primary Sources:**
  - Official documentation (language/framework docs, API references)
  - Curated open-source repositories (with permissive licenses, e.g., MIT, Apache 2.0)
  - Public Q&A (e.g., Stack Overflow), subject to licensing and terms of service
  - Internal/company codebases (if applicable and with explicit permission)
- **Selection Criteria:**
  - High signal-to-noise ratio (quality, relevance, recency)
  - Clear, permissive licensing or explicit permission for use
  - Diversity of examples and coverage across supported stacks

---

## 3. Licensing & Compliance

- **Due Diligence:**
  - Review and document the license for every data source.
  - Avoid sources with restrictive or unclear terms (e.g., GPL, proprietary code, Stack Overflow without explicit permission).
  - Maintain a data provenance log for auditability.
- **Attribution:**
  - Where required, provide attribution for code snippets or documentation used in RAG responses.
- **User Data:**
  - Do not ingest or store user-submitted code or prompts without explicit consent.

---

## 4. Ingestion & Indexing Pipeline

- **Automated Scripts:**
  - Scripts provided to fetch, preprocess, and index data for local development and CI.
- **Data Storage:**
  - Use local volumes or cloud object storage for indexed datasets.
- **Update Frequency:**
  - Schedule regular updates for external sources to keep the RAG index current.

---

## 5. Local Development

- **Sample Data:**
  - Provide a small, legally-cleared sample dataset for development and testing.
- **Configuration:**
  - Data source paths and credentials managed via environment variables.

---

## 6. Future Expansion

- **Pluggable Sources:**
  - Architecture supports adding/removing data sources as licensing or business needs evolve.
- **Legal Review:**
  - All new sources undergo legal and compliance review before production use.

---

## 7. Model Selection Options

### Option 1: Development (Local/Resource-Constrained)

- **Recommended Model:**
  - **StarCoder2 3B** or **Phi-3 Mini**
- **Why:**
  - Lightweight, fast inference on consumer hardware or small cloud instances.
  - Good code generation quality for prototyping and testing.
  - Easy to fine-tune or extend for specific languages.
- **How to Use:**
  - Pull from Hugging Face and run via Docker or local Python environment.
  - Example:
    ```sh
    pip install transformers
    from transformers import AutoModelForCausalLM, AutoTokenizer
    model = AutoModelForCausalLM.from_pretrained("bigcode/starcoder2-3b")
    tokenizer = AutoTokenizer.from_pretrained("bigcode/starcoder2-3b")
    ```

---

### Option 2: Production (High-Quality, Scalable)

- **Recommended Model:**
  - **Code Llama 70B Instruct** or **DeepSeek Coder 33B**
- **Why:**
  - State-of-the-art performance for code generation and completion.
  - Supports multiple languages and complex tasks.
  - Suitable for scalable, containerized, or cloud-based inference.
- **How to Use:**
  - Deploy on GPU-enabled cloud infrastructure (AWS, Azure, GCP) or use managed inference endpoints.
  - Example:
    ```sh
    # Using Hugging Face Inference Endpoints or custom deployment
    from transformers import AutoModelForCausalLM, AutoTokenizer
    model = AutoModelForCausalLM.from_pretrained("meta-llama/CodeLlama-70b-Instruct-hf")
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/CodeLlama-70b-Instruct-hf")
    ```

---

## 8. Model Evaluation & Benchmarking

- **Why:**  
  Regular benchmarking ensures the chosen model meets quality, latency, and cost targets as the use case evolves.
- **How:**
  - Use open code generation benchmarks (e.g., HumanEval, MBPP, MultiPL-E).
  - Track metrics: code correctness, test pass rate, response time, and resource usage.
  - Document results and revisit model selection periodically.

---

## 9. Monitoring & Feedback Loops

- **Why:**  
  Continuous monitoring and user feedback are essential for maintaining and improving code generation quality.
- **How:**
  - Log model outputs and user interactions (with consent) for analysis.
  - Implement feedback mechanisms (e.g., thumbs up/down, error reporting).
  - Use feedback data to retrain or fine-tune models and update retrieval sources.

---

## 10. Security & Privacy Considerations

- **Why:**  
  Protecting user data and intellectual property is critical in code generation applications.
- **How:**
  - Ensure all data in transit and at rest is encrypted.
  - Do not store user code or prompts unless explicitly permitted.
  - Regularly audit data pipelines for compliance with privacy regulations.

---

## 11. Cost Management

- **Why:**  
  Model inference costs can scale rapidly in production.
- **How:**
  - Monitor and log inference usage and associated costs.
  - Use quantization or model distillation for efficiency where possible.
  - Set up alerts for unusual usage patterns or cost spikes.

---

## 12. Documentation & Provenance

- **Why:**  
  Clear documentation of data and model sources is essential for transparency and compliance.
- **How:**
  - Maintain a data and model provenance log (source, license, date ingested, version).
  - Update documentation with every new data/model addition or change.

---

> **Professional Insight:**  
> “Select a model that matches the environment: lightweight for dev, state-of-the-art for production. Always validate licensing and resource requirements before deployment.”
>
> **Sage Wisdom:**  
> “A robust data sourcing strategy is not just about what you use, but how you evaluate, monitor, and govern it. This is what sets apart a mature, production-ready AI solution.”
