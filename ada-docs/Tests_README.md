# 32. Test Analysis and Coverage Guide

This section explains what each test file verifies, which component it tests, and why the test is important.

The goal is to help maintainers understand:

- What behaviour is protected by tests
- How confident we can be when making code changes
- Which architectural components are covered by tests
- Which components require additional testing

---

# 33. Test Architecture Overview

The test suite broadly mirrors the application architecture.

```text
API Tests
│
├── Chat API
├── User API
├── Program API
├── Prompt API
└── Health API

Service Tests
│
├── Authentication
├── Search
├── OpenAI
├── Query Analysis
├── User Management
├── Prompt Management
├── Session Management
├── Fusion
└── Persistence

Infrastructure Tests
│
├── PostgreSQL
├── Key Vault
├── APIM
└── Application Startup
```

---

# 34. Test Infrastructure

## conftest.py

### Purpose

Provides reusable fixtures and common test setup used throughout the test suite.

### What Is Being Verified

- Shared test configuration
- Dependency injection support
- Mock infrastructure setup
- Fixture management

### Component Under Test

```text
Test Framework Infrastructure
```

### Why It Matters

This file establishes the test environment and removes duplication across test files.

---

# 35. API Tests

API tests verify the FastAPI endpoints exposed by the application.

---

## test_health_check.py

### Purpose

Verifies the application's health endpoint.

### What Is Being Tested

- Health endpoint responds successfully
- Application reports healthy state

### Component Under Test

```text
Health API
```

### Business Requirement Validated

```text
Operational Monitoring
Application Readiness
Health Reporting
```

### Test Classification

```text
API Test
```

---

## test_chat.py

### Purpose

Validates chat REST endpoints.

### What Is Being Tested

- Request processing
- Response formatting
- Dependency wiring
- Endpoint behaviour

### Component Under Test

```text
Chat API
```

### Business Requirement Validated

```text
Question Answering
Conversation Access
Response Delivery
```

### Test Classification

```text
API Test
```

---

## test_programs.py

### Purpose

Validates programme-related endpoints.

### What Is Being Tested

- Program retrieval
- Program administration operations
- Endpoint responses

### Component Under Test

```text
Program API
```

### Business Requirement Validated

```text
Programme Management
Programme Discovery
Multi-Programme Support
```

### Test Classification

```text
API Test
```

---

## test_prompts.py

### Purpose

Validates prompt management endpoints.

### What Is Being Tested

- Prompt retrieval
- Prompt administration
- Prompt response handling

### Component Under Test

```text
Prompt API
```

### Business Requirement Validated

```text
Prompt Management
Prompt Versioning
Prompt Lifecycle
```

### Test Classification

```text
API Test
```

---

## test_users.py

### Purpose

Validates user management endpoints.

### What Is Being Tested

- User retrieval
- User administration
- Access assignment requests

### Component Under Test

```text
User API
```

### Business Requirement Validated

```text
User Provisioning
Access Management
Security Administration
```

### Test Classification

```text
API Test
```

---

# 36. Service Tests

Service tests validate business logic independently from API endpoints.

---

## test_auth_service.py

### Purpose

Verifies authentication logic.

### What Is Being Tested

- JWT validation
- Claims extraction
- Authenticated user construction
- Identity validation

### Component Under Test

```text
AuthService
```

### Business Requirement Validated

```text
Azure AD Authentication
Identity Verification
```

### Why This Test Exists

Protects the primary entry point into the platform.

### Test Classification

```text
Unit Test
```

---

## test_apim_key_service.py

### Purpose

Validates APIM key management.

### What Is Being Tested

- Secret retrieval
- Cache creation
- Cache invalidation
- Repeated key requests

### Component Under Test

```text
APIMKeyService
```

### Business Requirement Validated

```text
Secure Configuration
Secret Management
```

### Test Classification

```text
Unit Test
```

---

## test_ai_search_service.py

### Purpose

Validates the Azure AI Search integration layer.

### What Is Being Tested

- Search execution
- Search strategy selection
- Client caching
- Retry handling
- Resource cleanup
- Search result processing

### Component Under Test

```text
AISearchService
```

### Business Requirement Validated

```text
Document Retrieval
Azure AI Search Integration
RAG Search Layer
```

### Why This Test Exists

Protects search functionality and document retrieval.

### Test Classification

```text
Service Unit Test
```

---

## test_keyvault_client.py

### Purpose

Validates Azure Key Vault access.

### What Is Being Tested

- Secret retrieval
- Access token acquisition
- Error handling
- Cleanup operations

### Component Under Test

```text
KeyVaultClient
```

### Business Requirement Validated

```text
Infrastructure Security
Secret Storage
```

### Test Classification

```text
Infrastructure Test
```

---

## test_open_ai_service.py

### Purpose

Validates Azure OpenAI integration.

### What Is Being Tested

- Embedding generation
- Chat completions
- OpenAI communication
- Error handling

### Component Under Test

```text
OpenAIService
```

### Business Requirement Validated

```text
Response Generation
Embedding Generation
LLM Integration
```

### Why This Test Exists

Protects the platform's AI capabilities.

### Test Classification

```text
Service Unit Test
```

---

## test_prompt_service.py

### Purpose

Validates prompt lifecycle management.

### What Is Being Tested

- Prompt loading
- Prompt caching
- Prompt retrieval
- Prompt version selection

### Component Under Test

```text
PromptService
```

### Business Requirement Validated

```text
Prompt Lifecycle
Prompt Administration
Prompt Versioning
```

### Test Classification

```text
Service Unit Test
```

---

## test_query_analyser_service.py

### Purpose

Validates query planning functionality.

### What Is Being Tested

- Planner prompt execution
- JSON parsing
- Search filter construction
- Datasource identification
- Query analysis caching

### Component Under Test

```text
QueryAnalyserService
```

### Business Requirement Validated

```text
Query Planning
Search Optimisation
Datasource Selection
Filter Construction
```

### Why This Test Exists

The quality of retrieval depends on the quality of query analysis.

### Test Classification

```text
Service Unit Test
```

---

## test_session_manager_service.py

### Purpose

Validates active conversation management.

### What Is Being Tested

- Session creation
- Session retrieval
- Session updates
- Session deletion
- Cleanup operations

### Component Under Test

```text
SessionManagerService
```

### Business Requirement Validated

```text
Conversation Continuity
Context Management
```

### Test Classification

```text
Unit Test
```

---

## test_user_service.py

### Purpose

Validates user provisioning and access management.

### What Is Being Tested

- User creation
- Program assignment
- Action assignment
- Access grants
- Identity resolution
- Error handling

### Component Under Test

```text
UserService
```

### Business Requirement Validated

```text
User Provisioning
Programme Assignment
Authorization Administration
```

### Test Classification

```text
Service Unit Test
```

---

## test_chat_service.py

### Purpose

Validates the primary orchestration service.

### What Is Being Tested

- Conversation creation
- Message persistence
- Session integration
- Citation generation
- Response generation
- Storage integration

### Component Under Test

```text
ChatService
```

### Business Requirement Validated

```text
Question Answering
Conversation Storage
Citation Support
Response Generation
```

### Why This Test Exists

This is one of the most important tests in the codebase because Chat Service orchestrates the entire request flow.

### Test Classification

```text
Service Integration Test
```

---

## test_fusion_service.py

### Purpose

Validates document ranking logic.

### What Is Being Tested

- Reciprocal Rank Fusion (RRF)
- Result merging
- Result ordering
- Duplicate handling

### Component Under Test

```text
FusionService
```

### Business Requirement Validated

```text
Multi-Source Retrieval
Result Ranking
Search Quality
```

### Why This Test Exists

Directly impacts response quality by determining which documents reach the LLM.

### Test Classification

```text
Algorithm Test
```

---

## test_pg_cache_service.py

### Purpose

Validates persistence operations.

### What Is Being Tested

- Conversation storage
- Message persistence
- Conversation retrieval
- Token calculations

### Component Under Test

```text
PGCacheService
```

### Business Requirement Validated

```text
Conversation History
Persistence
Auditability
```

### Test Classification

```text
Service Integration Test
```

---

# 37. Infrastructure Tests

---

## test_postgres.py

### Purpose

Validates PostgreSQL infrastructure.

### What Is Being Tested

- Database initialization
- Engine creation
- Session management
- Singleton behaviour

### Component Under Test

```text
Postgres Manager
```

### Business Requirement Validated

```text
Data Persistence
Database Connectivity
```

### Test Classification

```text
Infrastructure Test
```

---

## test_lifespan.py

### Purpose

Validates application startup and shutdown behaviour.

### What Is Being Tested

- Prompt loading
- Program loading
- OpenAI initialization
- Dependency creation
- Startup sequence execution

### Component Under Test

```text
Application Lifespan
```

### Business Requirement Validated

```text
Application Startup
Readiness Validation
Operational Stability
```

### Why This Test Exists

Protects against deployment-time failures and startup regressions.

### Test Classification

```text
Infrastructure Integration Test
```

---

# 38. Test Coverage by Architecture Layer

## Presentation Layer

Covered By:

```text
test_health_check.py
test_chat.py
test_users.py
test_programs.py
test_prompts.py
```

Coverage Assessment:

```text
Excellent
```

---

## Security Layer

Covered By:

```text
test_auth_service.py
test_user_service.py
```

Coverage Assessment:

```text
Good
```

Known Gap:

```text
ABAC Service is not directly tested.
```

---

## Query Planning Layer

Covered By:

```text
test_query_analyser_service.py
```

Coverage Assessment:

```text
Excellent
```

---

## Search Layer

Covered By:

```text
test_ai_search_service.py
test_fusion_service.py
```

Coverage Assessment:

```text
Excellent
```

---

## OpenAI Layer

Covered By:

```text
test_open_ai_service.py
```

Coverage Assessment:

```text
Good
```

---

## Chat Orchestration Layer

Covered By:

```text
test_chat_service.py
```

Coverage Assessment:

```text
Good
```

---

## Persistence Layer

Covered By:

```text
test_pg_cache_service.py
test_postgres.py
```

Coverage Assessment:

```text
Excellent
```

---

## Infrastructure Layer

Covered By:

```text
test_apim_key_service.py
test_keyvault_client.py
test_lifespan.py
```

Coverage Assessment:

```text
Excellent
```

---

# 39. Coverage Gaps

The following architectural components appear untested or only partially tested.

## ABAC Service

Missing Coverage:

```text
Complete ALLOW path
Complete DENY path
Policy evaluation
Full handler chain execution
```

Recommended Test:

```text
test_abac_service.py
```

Priority:

```text
HIGH
```

---

## Authorization Handlers

Missing Coverage:

```text
test_user_active.py
test_program_active.py
test_token_quota.py
test_user_program.py
test_user_action.py
```

Priority:

```text
HIGH
```

---

## Citation Service

Missing Coverage:

```text
test_citation.py
```

Priority:

```text
MEDIUM
```

---

## Program Service

Missing Coverage:

```text
test_program_service.py
```

Priority:

```text
MEDIUM
```

---

# 40. Recommended Reading Order for New Developers

If you are new to the application, read the following tests first:

```text
1. test_chat_service.py
2. test_query_analyser_service.py
3. test_ai_search_service.py
4. test_open_ai_service.py
5. test_user_service.py
6. test_fusion_service.py
7. test_pg_cache_service.py
8. test_auth_service.py
9. test_lifespan.py
```

This sequence mirrors the runtime flow through the application.

---

# 41. Most Valuable Tests In The Solution

The five most useful tests for understanding the architecture are:

```text
test_chat_service.py
test_query_analyser_service.py
test_ai_search_service.py
test_open_ai_service.py
test_user_service.py
```

Together these describe approximately 80% of the business workflow:

```text
User
  |
Authentication
  |
Authorization
  |
Query Analysis
  |
Azure Search
  |
Fusion
  |
OpenAI
  |
Persistence
  |
Response
```

Understanding these tests is one of the fastest ways to understand how the platform works.