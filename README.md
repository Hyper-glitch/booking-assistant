# Booking Assistant AI Agent

This project demonstrates a **stateful, tool-based conversational agent** built with **LangGraph** that handles user requests related to booking modifications (rescheduling, cancellation, or keeping the original booking).  

> ⚠️ **Important**: This is a **synthetic demo** — all business logic, external APIs, and data are **mocked** for illustrative purposes.

---

## What This Agent Does

The agent simulates a customer support assistant for a hotel booking service.

The agent:
- Understands user intent from natural language
- Retrieves booking details
- Guides the user through decision flows (change/cancel/keep)
- Enforces strict state transitions via tool calls
- Escalates to a human operator when needed

---

## Key Features

- **Stateful conversation flow** using `LangGraph` and `Pydantic` state
- **Tool-based decision making**: every action (confirm/reject/transfer) is a tool call
- **Structured logging & error handling**
- **In-memory caching** for external API endpoint `get_booking`.
- **Human-in-the-loop escalation**

---

## Technical Stack

| Component | Technology |
|---------|------------|
| Core Framework | LangGraph + LangChain |
| LLM | **Qwen3-30B-Instruct** |
| Runtime | Python 3.13 + Poetry |
| State Management | Pydantic + `add_messages` reducer |
| Persistence | PostgreSQL (`AsyncPostgresSaver`) |
| Deployment | Docker + Docker Compose |

> 🔒 **Model Access**: The LLM is only accessible through **VPN**. External users cannot run this demo without internal credentials.

---

## Project Structure

```text
src/
├── agent/               # Core agent logic
│   ├── booking/         # Booking-specific graph, tools, state
│   └── common/          # Shared abstractions (runner, service, decorators)
├── api/                 # FastAPI application (v1 endpoints)
├── integration/         # Mocked external API client & interfaces
├── main.py              # Entry point
├── usage.py             # CLI interactive mode
└── settings.py          # Configuration (LLM, DB, logging)
```

## Quick Start

### Prerequisites:
- Python 3.13+
- Docker + Docker Compose

### Install dependencies:
```bash
poetry install
```

### Start services:
```bash
docker-compose up -d
```

### Run interactive mode:
```bash
python src/usage.py
```

#### Example input:
`"I want to change my booking time"`

### TODO
- **CI/CD Pipeline**: GitHub Actions for linting, type checking, testing and deployment
- **Integration Tests**: Validate end-to-end flows (happy path, edge cases)
- **Regression Tests**: Ensure state transitions remain consistent after changes
- **Observability**: Add structured logging, metrics, and tracing
