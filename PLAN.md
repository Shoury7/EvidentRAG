# EvidentRAG — Production-Grade Retrieval Augmented Generation System

## 🚀 Overview

**EvidentRAG** is a production-oriented Retrieval Augmented Generation (RAG) system built to demonstrate real-world AI infrastructure and retrieval engineering practices.

Unlike demo-level RAG pipelines, EvidentRAG emphasizes:

- grounded, citation-backed responses
- hybrid retrieval for high recall and precision
- cross-encoder reranking
- automated faithfulness evaluation
- CI-enforced quality gates

The system is designed to mirror how modern enterprise knowledge assistants are built and validated.

---

## 🎯 Objectives

- Build a trustworthy RAG pipeline with verifiable citations
- Minimize hallucinations via explicit citation enforcement
- Improve retrieval quality using hybrid search + reranking
- Continuously measure answer faithfulness offline
- Simulate production best practices (CI/CD, versioned prompts, API serving)

---

## 🧠 System Architecture

### Phase 1 — Foundations

**Capabilities**

- Document ingestion pipeline
- Intelligent chunking (500–800 tokens, 100 token overlap)
- Embedding generation and vector indexing (Chroma / Weaviate)
- Top-k semantic retrieval
- Answer generation with source citations

**Outcome:** End-to-end working grounded RAG pipeline.

---

### Phase 2 — Production Hardening

#### Hybrid Retrieval

Combines:

- BM25 keyword search
- Dense vector semantic search

**Rationale:** Dense retrieval captures semantic intent, while BM25 preserves exact-term recall.

---

#### Cross-Encoder Reranking

- Query–chunk pairwise scoring
- Reorders initial candidates for higher precision
- Reduces retrieval noise

---

#### Citation Enforcement Guardrail

- System abstains when evidence is insufficient
- Prevents unsupported or hallucinated answers
- Ensures every claim is grounded in retrieved context

---

#### Prompt Versioning

- Prompts stored as versioned YAML artifacts
- Treated as first-class components of the system
- Enables reproducibility and controlled iteration

**Outcome:** Production-quality, reliability-focused retrieval pipeline.

---

### Phase 3 — Faithfulness Evaluation

#### Golden Evaluation Set

- 50–200 manually curated Q&A pairs
- Domain-grounded verification
- Used for regression testing

---

#### Offline Evaluation Pipeline

- RAGAS-based faithfulness measurement
- Claim-level grounding checks
- Retrieval and answer quality metrics

---

#### CI Quality Gate

- GitHub Actions evaluation on every PR
- Automatic failure if metrics regress below threshold
- Prevents silent quality degradation

**Outcome:** Continuously validated, measurable RAG system.

---

## 🛠️ Technology Stack

**Orchestration**

- LangChain / LangGraph

**Retrieval**

- ChromaDB / Weaviate
- BM25 (sparse retrieval)
- Cohere Rerank or SBERT Cross-Encoder

**Evaluation**

- RAGAS

**Serving & Infra**

- FastAPI
- Docker
- GitHub Actions CI

---

## 📊 Why EvidentRAG Stands Out

- Moves beyond toy RAG demos
- Implements hybrid retrieval + reranking
- Enforces grounded answer generation
- Includes automated faithfulness evaluation
- Demonstrates production-minded AI system design

---

## 🔮 Future Work

- Query rewriting and expansion
- Multi-hop retrieval
- Streaming responses
- Retrieval observability (LangSmith)
- Semantic caching layer
- Multi-tenant indexing

---

## 👤 Author

Built to demonstrate production-grade AI system design, retrieval engineering, and evaluation rigor.
