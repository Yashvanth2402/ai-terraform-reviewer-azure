🤖 AI Terraform Reviewer for Azure (Production-Grade)

An AI-assisted, deterministic Terraform Pull Request reviewer that analyzes Azure infrastructure changes, reasons about risk like a Staff Platform Engineer, and posts explainable, actionable feedback directly on GitHub Pull Requests.

This project intentionally combines:

Deterministic infrastructure analysis (source of truth)

Azure-aware domain knowledge

Historical memory

LLM-assisted explanations (Azure OpenAI)

Rules decide. LLM explains. Humans approve.

🚀 Why This Project Exists

Most Terraform review tools suffer from one of these problems:

❌ Only lint syntax (no real risk analysis)
❌ Stateless (forget past incidents and PRs)
❌ Over-trust LLMs (hallucinations, inconsistent risk)
❌ Unsafe for production (non-deterministic decisions)

This project solves those problems by designing an AI governance system, not a chatbot.

🧠 Core Design Principles

Determinism First

Same Terraform plan → same risk → every time

LLMs Are Not Decision Makers

LLMs only explain decisions already made

Explainability Over Cleverness

Every risk can be traced to a rule

Production Safety

LLM failure must never block CI

Human Authority

AI advises, humans decide

🏗️ High-Level Architecture
Pull Request
   ↓
GitHub Actions
   ↓
Terraform Plan (facts)
   ↓
Context Enrichment
   ↓
Deterministic Risk Engine
   ↓
Historical Memory Lookup
   ↓
LLM Explanation (Azure OpenAI)
   ↓
PR Comment (Explainable + Actionable)

📂 Repository Structure
ai-terraform-reviewer-azure/
│
├── terraform/
│   └── environments/
│       └── dev/                 # Sample Terraform environment
│
├── ai/
│   ├── context/
│   │   ├── enrich.py             # Converts terraform plan → enriched context
│   │   ├── tfplan.json           # Terraform plan (JSON)
│   │   └── enriched_context.json # Classified infra context
│   │
│   ├── reasoning/
│   │   ├── review.py             # Deterministic AI risk engine
│   │   ├── llm_enrichment.py     # Safe Azure OpenAI integration
│   │   ├── post_comment.py       # GitHub PR comment publisher
│   │   └── ai_review.json        # Final AI review output
│   │
│   ├── llm/
│   │   ├── llm_client.py         # Azure OpenAI client (controlled)
│   │   └── prompts.py            # Strict prompt contracts
│   │
│   └── memory/
│       ├── memory_store.py       # Historical PR memory engine
│       └── pr_memory.json        # (Ignored) runtime memory store
│
├── .github/
│   └── workflows/
│       └── terraform-ai-review.yml
│
└── README.md

🔍 What the AI Actually Does
Deterministic (Rules-Based)

The AI always detects:

Shared infrastructure changes

Azure networking changes (VNet, subnet)

Production vs non-production escalation

Large change sets (blast radius)

Repeated risky patterns (historical memory)

This logic lives in:

ai/reasoning/review.py

LLM-Assisted (Azure OpenAI)

The LLM is used only to:

Explain why a change is risky

Improve human readability

Maintain professional tone

The LLM:
❌ Cannot change risk
❌ Cannot block PRs
❌ Cannot invent resources

If Azure OpenAI fails → system still works.

🧠 Example PR Comment (Real Output)
🤖 AI Terraform Review (Azure)

Environment: dev
Risk Level: HIGH
Confidence: 85%

Why this change is risky:
- Shared Azure infrastructure is being modified
- Azure networking resources are being modified

Recommended Actions:
- Run during maintenance window
- Ensure rollback plan
- Validate in lower environment

AI Reasoning (LLM-Assisted):
The proposed Terraform changes carry a high risk due to modifications
to shared Azure networking components...

🧠 Why Not “Only LLM”?

Using only an LLM would cause:

Non-reproducible decisions

Hallucinated risks

No audit trail

Loss of trust

This project uses a hybrid architecture:

Component	Responsibility
Rules	Decide risk
Memory	Learn from past
LLM	Explain clearly
Human	Approve

This is how real production systems work.

🔐 Security & Compliance

No secrets committed

Azure OpenAI keys stored in GitHub Secrets

LLM never sees codebase or credentials

All decisions are auditable

CI never fails due to AI

🧪 How to Run Locally (Learning Mode)
terraform init
terraform plan -out=tfplan
terraform show -json tfplan > tfplan.json

python ai/context/enrich.py tfplan.json enriched_context.json
python ai/reasoning/review.py enriched_context.json ai_review.json

🔄 How CI Works

On every Pull Request:

Terraform plan runs

Context is enriched

Deterministic risk is computed

LLM explanation is added (if available)

PR comment is posted

PR is recorded into historical memory