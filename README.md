# 🛡️ AGENTGUARD — AI Control Tower for Autonomous Payment & Revenue Agents

> **Governance & Supervisory Layer above multiple autonomous financial agents.**
> *"LLM Recommends. Policy Engine Decides."*

---

#### 🚀 Overview

Modern merchants deploy multiple autonomous AI agents (Subscription Recovery, Payment Recovery, Abandoned Checkout, Invoicing/Receivables). Operating independently, these agents cause **customer fatigue, duplicate communications, competing financial discounts, and policy violations**. 

**AgentGuard** is an AI Supervisory Governance Layer built *above* multiple autonomous financial agents to detect collisions, enforce hard/soft policy guardrails, and provide human-in-the-loop oversight.

---

## 🛠️ Architecture

```
[Autonomous Agents] ──► [Conflict Detector] ──► [AI Supervisor (Gemini)] ──► [Policy Engine] ──► [ALLOW / REVIEW / STOP]
```

### Key Components:
- **4 Autonomous Agents:** Subscription Recovery, Payment Recovery, Checkout Recovery, Receivables Agent.
- **Inter-Agent Conflict Detector & Resolver:** Detects collisions (`DUPLICATE_ACTION`, `COMPETING_FINANCIAL`, `DUPLICATE_COMMUNICATION`, `PRIORITY_CLASH`) and resolves them deterministically based on agent priority.
- **AI Supervisor Layer:** Gemini 2.0 Flash integration using structured JSON output.
- **Deterministic Policy Engine:** Enforces hard rules (`CUSTOMER_OPT_OUT`, `MAX_RETRY_LIMIT`, `CONTACT_FREQUENCY_LIMIT`, `COST_BENEFIT_ANALYSIS`) and soft rules (`HIGH_VALUE_TRANSACTION`, `LOW_AI_CONFIDENCE`).
- **Interactive UI:** Built with React 19, Tailwind CSS v4, Recharts & `@xyflow/react` node canvas topology.

---

## ⚡ Quick Start

### 1. Backend Setup (FastAPI + SQLite WAL)
```bash
cd backend
pip install -r requirements.txt
python seed.py
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup (React 19 + Vite 6 + Tailwind v4)
```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser ..........

---

## 📜 License
MIT

