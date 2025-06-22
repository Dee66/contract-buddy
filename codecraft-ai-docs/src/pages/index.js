codecraft-ai-docs/src/pages/index.js

import React from 'react';
import Layout from '@theme/Layout';
import { useDocusaurusContext } from '@docusaurus/core';

const Home = () => {
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout
      title={siteConfig.title}
      description="A fully custom, AWS-native, production-grade AI platform. Portfolio showcase for enterprise-ready, secure, and scalable AI solutions."
    >
      <header className="hero hero--primary">
        <div className="container">
          <h1 className="hero__title">{siteConfig.title}</h1>
          <p className="hero__subtitle">
            A living demonstration of how to deliver secure, scalable, and business-aligned AI solutions at an enterprise level.<br />
            Architected, engineered, and deployed to production on AWS.
          </p>
          <div className="hero__buttons">
            <a className="button button--secondary button--lg" href="/docs/introduction">
              Get Started
            </a>
          </div>
        </div>
      </header>
      <main>
        <div className="container margin-vert--lg">
          <section>
            <h2>Welcome to CodeCraft AI</h2>
            <p>
              <strong>CodeCraft AI</strong> is a fully custom, end-to-end AI platform, meticulously architected, engineered, and deployed to production (also dev & staging) on AWS.
              This is no theoretical exercise or boilerplate demo. This is a living testament to architecting and deploying truly custom AI solutions that are not just functional, but uncompromisingly robust, intrinsically secure, infinitely scalable, and operationally mature.
            </p>
            <p>
              Experience the mastery of a full-stack, cloud-native AI implementation: from automated password rotation and Dockerized services to a hardened CI/CD pipeline (GitHub Actions) rigorously validating code and deploying across a rich AWS ecosystem—including S3, ALB, Secrets Manager, IAM, IaC (CDK), ECR, ECS, and Fargate.
              CodeCraft AI showcases the rigorous engineering principles vital for transforming groundbreaking AI into tangible, battle-ready business impact. This is how I turn vision into a deployable reality.
            </p>
          </section>

          <hr />

          <section>
            <h2>🚀 Why CodeCraft AI?</h2>
            <ul>
              <li>
                <strong>Enterprise-Grade, Not a Toy:</strong><br />
                CodeCraft AI is a real, production-hardened platform—battle-tested in live AWS environments, not a classroom exercise or a copy-paste demo. Every feature is engineered for real-world reliability, scale, and business impact.
              </li>
              <li>
                <strong>AWS-Native, Cloud-First Engineering:</strong><br />
                The architecture is deeply integrated with AWS best practices, leveraging the full spectrum of cloud-native services—S3, ECS on Fargate, ALB, SageMaker, ECR, IAM, Secrets Manager, SSM Parameter Store, and more. Infrastructure is defined as code (CDK, Python) for repeatable, auditable, and secure deployments.
              </li>
              <li>
                <strong>Business Value at the Core:</strong><br />
                Every technical decision is mapped directly to measurable business outcomes—whether it’s reducing operational overhead, accelerating delivery, or enabling new revenue streams. This is AI with a purpose, not just AI for its own sake.
              </li>
              <li>
                <strong>Operational Excellence, Proven in Production:</strong><br />
                Zero-downtime hot-reloads, atomic model and data updates, automated rollbacks, and cost-optimized, serverless infrastructure. The platform is designed for continuous delivery, rapid iteration, and operational resilience—no manual interventions, no surprises.
              </li>
              <li>
                <strong>Security as a Foundation, Not an Afterthought:</strong><br />
                End-to-end security is woven into every layer: OIDC-based passwordless deployments, least-privilege IAM, automated secret rotation, private networking, and rigorous compliance with the AWS Well-Architected Framework. Secrets and configs are never hardcoded—always managed via AWS Secrets Manager and SSM.
              </li>
              <li>
                <strong>Relentless Focus on Automation and Quality:</strong><br />
                From multi-stage Docker builds and automated CI/CD (GitHub Actions) to proactive vulnerability scanning, code linting (Ruff), and pre-commit hooks, every step is automated for consistency, security, and speed.
              </li>
              <li>
                <strong>Transparent, Developer-First Experience:</strong><br />
                Centralized logging (CloudWatch), real-time dashboards, and Docusaurus-powered documentation ensure that every aspect of the system is observable, explainable, and easy to onboard for new engineers.
              </li>
            </ul>
            <blockquote>
              <em>
                CodeCraft AI is not just a project—it's a living demonstration of how to deliver secure, scalable, and business-aligned AI solutions at an enterprise level. This is what modern, cloud-native AI engineering looks like in practice.
              </em>
            </blockquote>
          </section>

          <hr />

          <section>
            <h2>✨ My Blueprint: The AI Solutions "Recipe" for Uncompromising Success</h2>
            <p>
              Every high-performing AI solution begins with a solid foundation. CodeCraft AI unveils my systematic, MLOps-driven methodology — a battle-tested "recipe" that ensures every AI initiative I lead is designed for unwavering success:
            </p>
            <ul>
              <li>
                <strong>🎯 Business-Centric Foundations:</strong><br />
                Start with the business problem, user pain points, and ROI. Every solution is mapped to measurable, strategic value.<br />
                <em>(From: Business problem & value, Objective defined, Initial cost model)</em>
              </li>
              <li>
                <strong>📐 Architectural Rigor & Data Governance:</strong><br />
                Design for scalability, security, and maintainability from day one. Architecture blueprints, clear I/O specs, and privacy/compliance are embedded throughout.<br />
                <em>(From: Architecture blueprint, Input/output specification, Data privacy & compliance, Model strategy, Risk & constraints)</em>
              </li>
              <li>
                <strong>⚙️ Flawless Operational Excellence:</strong><br />
                Full lifecycle automation and continuous optimization. Modular, testable data pipelines, reproducible environments, and rigorous benchmarking with cost tracking.<br />
                <em>(From: Dev environment, Data pipeline, Experimentation, Benchmarking & optimization, Cost tracking, Evaluation plan)</em>
              </li>
              <li>
                <strong>🔒 Production Readiness & Security:</strong><br />
                Secure, reliable deployments with model versioning, rollback, and proactive risk mitigation.<br />
                <em>(From: Model versioning & rollback, Risk & constraints)</em>
              </li>
            </ul>
          </section>

          <hr />

          <section>
            <h2>🌟 Impact Highlights</h2>
            <ul>
              <li><strong>Zero-downtime model and data updates</strong> via atomic hot-reloading of vector stores from S3.</li>
              <li><strong>Automated, auditable deployments</strong> with full rollback support and environment parity.</li>
              <li><strong>Cost-optimized, serverless infrastructure</strong> — no idle compute, pay only for what you use.</li>
              <li><strong>End-to-end security:</strong> OIDC, least-privilege IAM, automated secret rotation, and private subnets.</li>
              <li><strong>Comprehensive observability:</strong> Centralized logging, dashboards, and proactive alerting.</li>
            </ul>
          </section>

          <hr />

          <section>
            <h2>🏗️ Engineering Excellence in Action</h2>
            <h3>☁️ Resilient Cloud-Native Architecture</h3>
            <ul>
              <li>
                <strong>AWS CDK (Python) for Infrastructure-as-Code:</strong><br />
                All AWS resources are defined in code for repeatable, auditable deployments. Stateful (S3, ECR) and stateless (ECS, ALB) resources are managed separately for clarity and lifecycle control.
              </li>
              <li>
                <strong>Highly available, serverless compute:</strong><br />
                ECS on Fargate runs API (FastAPI) and ingestion services, fronted by ALB for seamless scaling and traffic management.
              </li>
              <li>
                <strong>Security posture:</strong><br />
                Private subnets, passwordless OIDC deployment, least-privilege IAM, AWS Secrets Manager, and SSM Parameter Store for config/secrets.
              </li>
            </ul>
            <h3>🧠 Advanced AI & ML Pipeline</h3>
            <ul>
              <li>
                <strong>Retrieval-Augmented Generation (RAG):</strong><br />
                FAISS vector search + Hugging Face Transformers + AWS Bedrock for contextual, robust AI interactions.
              </li>
              <li>
                <strong>Fine-Tuning & PEFT:</strong><br />
                Rapid, cost-effective model specialization with robust versioning and rollback.
              </li>
              <li>
                <strong>Self-healing, idempotent ingestion:</strong><br />
                Full S3-to-FAISS sync, atomic hot-reloading, and thread-safe updates — no service restarts required.
              </li>
            </ul>
            <h3>🚀 Automated MLOps & CI/CD</h3>
            <ul>
              <li>
                <strong>End-to-end ML lifecycle automation:</strong><br />
                Model training, inference, and monitoring via AWS SageMaker.
              </li>
              <li>
                <strong>GitHub Actions CI/CD:</strong><br />
                Multi-stage Docker builds, automated tests (Pytest), security scans (Dependabot, pip-audit), and direct deployment to AWS.
              </li>
              <li>
                <strong>Quality gates:</strong><br />
                Linting (Ruff), pre-commit hooks, and automated code quality enforcement.
              </li>
            </ul>
            <h3>📊 Transparent Operations & Developer Experience</h3>
            <ul>
              <li>
                <strong>Observability:</strong><br />
                Centralized structured logging (CloudWatch), dashboards, and alerting on key metrics.
              </li>
              <li>
                <strong>Deterministic environments:</strong><br />
                Reproducible builds with pip-tools lockfiles.
              </li>
              <li>
                <strong>Documentation-driven:</strong><br />
                Docusaurus-powered docs, API references, model cards, and architecture diagrams.
              </li>
              <li>
                <strong>Developer productivity:</strong><br />
                Makefile-driven local setup and deployment.
              </li>
            </ul>
          </section>

          <hr />

          <section>
            <h2>🗺️ Your Journey into Engineering Excellence Starts Here</h2>
            <p>
              This page offers a strategic overview of CodeCraft AI. For a deeper dive into the architecture, design decisions, and operational innovations, explore the full documentation:
            </p>
            <ul>
              <li><strong>Deep Dive into Architecture & Design</strong> — Modular, secure, and scalable foundations, with ADRs and MLOps diagrams.</li>
              <li><strong>Understanding the AI Core & Optimization</strong> — Strategic AI patterns, robust data engineering, and benchmarking.</li>
              <li><strong>MLOps & CI/CD Pipeline Explained</strong> — Automation, testing, and secure deployment.</li>
              <li><strong>Getting Started: Run the Project Locally</strong> — Experience the developer workflow.</li>
              <li><strong>Full Technology Stack</strong> — Review the comprehensive set of tools and AWS services.</li>
            </ul>
          </section>

          <hr />

          <section>
            <h2>Connect with Me</h2>
            <p>
              I'm passionate about architecting secure, scalable, and impactful AI solutions that drive real business value.<br />
              <strong>CodeCraft AI</strong> is more than a technical showcase — it's a blueprint for delivering secure, scalable, and business-aligned AI in the cloud. Every decision, from architecture to deployment, reflects an unwavering commitment to operational maturity, security, and real-world impact.
            </p>
          </section>
        </div>
      </main>
    </Layout>
  );
};

export default Home;
