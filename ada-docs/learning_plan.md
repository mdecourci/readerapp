# AI Assistant Platform Learning Plan
## 12-Week Developer Onboarding Plan

### Goal

Become comfortable maintaining, debugging, testing, and enhancing the AI Assistant Platform independently.

### Suggested Effort

- 5-8 hours per week
- Mix of reading code, studying concepts, and hands-on experimentation

---

# Week 1 - Understand the Application

## Objective

Understand what the application does end-to-end.

## Learn

- Overall architecture
- RAG fundamentals
- FastAPI basics
- Request flow

## Read

```text
README.md
HLD.md
DDD.md

main.py
chat.py
dependencies.py
```

## Study

Understand this request flow:

```text
User
  |
FastAPI
  |
ABAC
  |
Chat Service
  |
Query Analysis
  |
AI Search
  |
OpenAI
  |
Database
```

## Deliverable

Draw the architecture from memory and explain the purpose of each component.

## Week 1 Checklist

- [ ] Read HLD and DDD
- [ ] Read main.py
- [ ] Read chat.py
- [ ] Read dependencies.py
- [ ] Understand request flow
- [ ] Draw architecture from memory
- [ ] Explain architecture to another developer

---

# Week 2 - Python Async Programming

## Objective

Become comfortable reading async code.

## Learn

```python
async
await
async def
async with
asyncio
```

## Read

```text
chat_service.py
open_ai_service.py
ai_search_service.py
postgres.py
```

## Practice

Create simple async examples using:

```python
asyncio.run()

await
```

## Deliverable

Explain:

```text
Why services are async
Why AsyncSession is used
Why Azure calls are async
```

## Week 2 Checklist

- [ ] Understand async/await
- [ ] Understand event loop basics
- [ ] Read chat_service.py
- [ ] Read open_ai_service.py
- [ ] Read ai_search_service.py
- [ ] Read postgres.py
- [ ] Create async sample program
- [ ] Explain async execution flow

---

# Week 3 - FastAPI Deep Dive

## Objective

Understand how requests enter the application.

## Learn

```text
Routers
Dependency Injection
Middleware
Pydantic Models
Authentication
```

## Read

```text
chat.py
users.py
programs.py
prompts.py
health_check.py
dependencies.py
```

## Deliverable

Trace the complete execution of:

```http
POST /chat
```

from API endpoint to response.

## Week 3 Checklist

- [ ] Understand FastAPI routers
- [ ] Understand dependency injection
- [ ] Understand middleware
- [ ] Understand request models
- [ ] Understand response models
- [ ] Trace POST /chat
- [ ] Trace program endpoint
- [ ] Trace user endpoint

---

# Week 4 - Authentication and Identity

## Objective

Understand how user identity is established.

## Learn

```text
JWT Tokens
Azure AD / Entra ID
OID Claims
Scopes
Managed Identity
```

## Read

```text
auth.py
auth_service.py
managed_identity_service.py
```

## Deliverable

Draw:

```text
User
  |
Azure AD
  |
JWT Token
  |
Auth Service
  |
Authenticated User
```

## Week 4 Checklist

- [ ] Understand JWT structure
- [ ] Understand claims
- [ ] Understand OID
- [ ] Understand scopes
- [ ] Read auth_service.py
- [ ] Read auth.py
- [ ] Read managed_identity_service.py
- [ ] Draw authentication flow

---

# Week 5 - ABAC Authorization

## Objective

Understand how access decisions are made.

## Learn

```text
RBAC vs ABAC
Policy Evaluation
Chain of Responsibility
```

## Read

```text
abac_service.py

user_active.py
token_quota.py
program_active.py
user_program.py
user_action.py
policy.py
```

## Deliverable

Draw the complete ABAC flow.

## Week 5 Checklist

- [ ] Understand RBAC
- [ ] Understand ABAC
- [ ] Read abac_service.py
- [ ] Read user_active.py
- [ ] Read token_quota.py
- [ ] Read program_active.py
- [ ] Read user_program.py
- [ ] Read user_action.py
- [ ] Read policy.py
- [ ] Draw authorization flow
- [ ] Explain why a request could be denied

---

# Week 6 - PostgreSQL and SQLAlchemy

## Objective

Understand how data is stored.

## Learn

```text
SQLAlchemy ORM
Relationships
AsyncSession
Entity Mapping
```

## Read

```text
postgres.py
pg_cache_service.py

conversation.py
message.py
feedback.py
retrieval_log.py
user.py
program.py
```

## Deliverable

Draw the entity relationship model.

## Week 6 Checklist

- [ ] Understand SQLAlchemy ORM
- [ ] Understand AsyncSession
- [ ] Read postgres.py
- [ ] Read pg_cache_service.py
- [ ] Read entity models
- [ ] Understand relationships
- [ ] Draw ERD
- [ ] Explain conversation storage

---

# Week 7 - Azure OpenAI

## Objective

Understand how AI responses are generated.

## Learn

```text
Embeddings
Chat Completions
Tokens
Temperature
System Prompts
```

## Read

```text
open_ai_service.py
model.py
```

## Deliverable

Explain:

```text
Embedding Generation

vs

Response Generation
```

## Week 7 Checklist

- [ ] Understand embeddings
- [ ] Understand completions
- [ ] Understand token usage
- [ ] Understand model selection
- [ ] Read open_ai_service.py
- [ ] Read model.py
- [ ] Trace OpenAI call flow
- [ ] Explain embedding lifecycle

---

# Week 8 - Azure AI Search

## Objective

Understand where answers come from.

## Learn

```text
Indexes
Documents
Semantic Search
Vector Search
Metadata Filters
```

## Read

```text
ai_search_service.py

registry.py

csnp.py
resp.py
rnp.py
tide.py
tresp.py
ssep_meeting_notes.py
ssep_feedback_log.py
ssep_methodology_consultation.py
```

## Deliverable

Explain how documents are retrieved.

## Week 8 Checklist

- [ ] Understand Azure AI Search
- [ ] Understand indexes
- [ ] Understand vector search
- [ ] Understand semantic search
- [ ] Read all strategy files
- [ ] Read registry.py
- [ ] Read ai_search_service.py
- [ ] Trace document retrieval

---

# Week 9 - RAG Architecture

## Objective

Understand Retrieval Augmented Generation.

## Learn

```text
RAG
Embeddings
Vector Search
Context Construction
Citation Generation
RRF
```

## Read

```text
chat_service.py
fusion_service.py
citation.py
retrieval_log.py
```

## Deliverable

Draw the complete RAG flow.

## Week 9 Checklist

- [ ] Understand RAG concepts
- [ ] Understand retrieval logs
- [ ] Understand Fusion Service
- [ ] Understand Citation Builder
- [ ] Understand context construction
- [ ] Read retrieval_log.py
- [ ] Draw RAG flow
- [ ] Explain source citations

---

# Week 10 - Prompt Engineering

## Objective

Understand how AI behaviour is controlled.

## Learn

```text
System Prompts
Planner Prompts
Synthesiser Prompts
Prompt Versioning
```

## Read

```text
prompt_service.py
prompt.py
08_seed_prompts.sql
```

## Deliverable

Explain the purpose of each prompt type.

## Week 10 Checklist

- [ ] Read prompt_service.py
- [ ] Read prompt.py
- [ ] Review prompt seed data
- [ ] Understand planner prompt
- [ ] Understand system prompt
- [ ] Understand synthesiser prompt
- [ ] Explain prompt versioning
- [ ] Map prompts to workflow

---

# Week 11 - Testing and Mocking

## Objective

Become productive at reading and creating tests.

## Learn

### Pytest

```text
Fixtures
conftest.py
pytest.mark.asyncio
parametrize
```

### Mocking

```python
Mock
MagicMock
AsyncMock
patch
monkeypatch
```

## Read

```text
test_chat_service.py
test_query_analyser_service.py
test_ai_search_service.py
test_open_ai_service.py
test_user_service.py
```

## Deliverable

Explain mocking strategy.

## Week 11 Checklist

- [ ] Understand pytest fixtures
- [ ] Understand monkeypatch
- [ ] Understand MagicMock
- [ ] Understand AsyncMock
- [ ] Read conftest.py
- [ ] Read top 5 service tests
- [ ] Create a simple unit test
- [ ] Create a simple mock
- [ ] Explain isolation testing

---

# Week 12 - Production Support and Troubleshooting

## Objective

Learn how to support the application.

## Learn

```text
Logging
Request Correlation
Startup Lifecycle
Health Checks
Exception Handling
```

## Read

```text
configure_logging.py
request_id.py
lifespan.py
exceptions.py
health_check.py
```

## Deliverable

Create a troubleshooting guide.

## Week 12 Checklist

- [ ] Read logging implementation
- [ ] Read request correlation code
- [ ] Read startup lifecycle
- [ ] Read exception hierarchy
- [ ] Review health checks
- [ ] Learn log locations
- [ ] Create troubleshooting guide
- [ ] Simulate support scenarios

---

# Suggested Daily Reading Order

```text
1. chat_service.py
2. abac_service.py
3. query_analyser_service.py
4. ai_search_service.py
5. open_ai_service.py
6. pg_cache_service.py
7. user_service.py
8. prompt_service.py
9. session_manager_service.py
10. fusion_service.py
```

## Daily Progress Checklist

- [ ] Read one service
- [ ] Trace service dependencies
- [ ] Identify inputs
- [ ] Identify outputs
- [ ] Identify tests
- [ ] Update notes

---

# Technology Learning Priority

```text
1. Pytest Fixtures and Mocking
2. Async Python
3. FastAPI
4. Azure AD / Authentication
5. ABAC Authorization
6. SQLAlchemy
7. Azure OpenAI
8. Azure AI Search
9. RAG Architecture
10. Prompt Engineering
11. Azure Key Vault
12. Azure Infrastructure
```

## Technology Mastery Checklist

### Pytest

- [ ] Fixtures
- [ ] Parametrize
- [ ] Async Tests
- [ ] Mocking

### FastAPI

- [ ] Routers
- [ ] Middleware
- [ ] Dependency Injection
- [ ] Security

### AI Search

- [ ] Indexes
- [ ] Vector Search
- [ ] Semantic Search
- [ ] Filters

### OpenAI

- [ ] Embeddings
- [ ] Completions
- [ ] Tokens
- [ ] Prompts

---

# Most Important Services to Understand

```text
ChatService
ABACService
QueryAnalyserService
AISearchService
OpenAIService
```

## Core Services Checklist

### ChatService

- [ ] Understand orchestration
- [ ] Understand persistence
- [ ] Understand citations

### ABACService

- [ ] Understand handler chain
- [ ] Understand policy evaluation
- [ ] Understand authorization failures

### QueryAnalyserService

- [ ] Understand planning prompts
- [ ] Understand filter creation
- [ ] Understand datasource selection

### AISearchService

- [ ] Understand search execution
- [ ] Understand strategies
- [ ] Understand search results

### OpenAIService

- [ ] Understand embeddings
- [ ] Understand response generation
- [ ] Understand retry logic

---

# Most Important Tests to Study

```text
1. test_chat_service.py
2. test_query_analyser_service.py
3. test_ai_search_service.py
4. test_open_ai_service.py
5. test_user_service.py
```

## Test Learning Checklist

- [ ] Understand fixtures
- [ ] Understand mocks
- [ ] Trace service under test
- [ ] Read assertions
- [ ] Understand expected behaviour

---

# End Goal

By the end of this learning plan you should be able to:

- [ ] Explain the architecture
- [ ] Understand request flow
- [ ] Debug authentication issues
- [ ] Debug authorization issues
- [ ] Troubleshoot retrieval problems
- [ ] Troubleshoot OpenAI issues
- [ ] Update prompts safely
- [ ] Add a datasource
- [ ] Add tests
- [ ] Support production incidents
- [ ] Explain the platform to another developer

---

# Final Mental Model

```text
User
  |
FastAPI
  |
Authentication
  |
ABAC
  |
Chat Service
  |
Query Analyser
  |
Azure AI Search
  |
Fusion
  |
Citation Builder
  |
Azure OpenAI
  |
PostgreSQL
  |
Response
```

## Final Success Checklist

- [ ] Can explain entire request flow
- [ ] Can debug ABAC issues
- [ ] Can debug search issues
- [ ] Can debug OpenAI issues
- [ ] Can trace data through the system
- [ ] Can modify a service safely
- [ ] Can create meaningful tests
- [ ] Ready to support production