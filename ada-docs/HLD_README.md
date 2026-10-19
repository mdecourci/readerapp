# AI Assistant Platform
## High Level Design (HLD)

Version: 1.0  
Generated From: Source Code Analysis Only  
Architecture Style: Azure-Native Enterprise Retrieval Augmented Generation (RAG) Platform

---

# 1. Executive Summary

The AI Assistant Platform is an enterprise-grade Retrieval Augmented Generation (RAG) solution built on Azure services.

The platform enables authenticated and authorised users to query multiple consultation and programme-specific knowledge repositories using natural language. Responses are generated using Azure OpenAI and enhanced through retrieval of relevant content from Azure AI Search indexes.

The solution implements:

- Azure AD / Entra ID authentication
- Attribute Based Access Control (ABAC)
- Retrieval Augmented Generation (RAG)
- Azure AI Search
- Azure OpenAI
- PostgreSQL persistence
- Prompt management
- Conversation management
- Token governance
- Feedback collection
- Citation generation
- Operational observability

The architecture demonstrates strong separation of concerns and follows modern cloud-native design principles.

---

# 2. System Context

```text
+-------------------------------------------------------+
|                       End User                        |
+--------------------------+----------------------------+
                           |
                           v
+-------------------------------------------------------+
|                     FastAPI APIs                      |
+-------------------------------------------------------+
                           |
                           v
+-------------------------------------------------------+
|            Authentication / Authorization            |
+-------------------------------------------------------+
                           |
                           v
+-------------------------------------------------------+
|                Chat Orchestration Layer              |
+-------------------------------------------------------+
             |                            |
             v                            v
+--------------------+      +--------------------------+
| Azure AI Search    |      | Azure OpenAI             |
| Semantic Search    |      | GPT Models              |
| Vector Search      |      | Embeddings              |
+---------+----------+      +------------+------------+
          |                              |
          +--------------+---------------+
                         |
                         v
              +----------------------+
              |  PostgreSQL Storage  |
              +----------------------+
```

---

# 3. Architectural Overview

The application follows a layered architecture.

```text
Presentation Layer
        |
Application Layer
        |
Domain Layer
        |
Infrastructure Layer
```

The design separates business logic from infrastructure concerns and allows external services to be replaced with minimal impact to business functionality.

---

# 4. Layered Architecture

## 4.1 Presentation Layer

Responsible for exposing REST APIs.

### Components

- Chat API
- User API
- Program API
- Prompt API
- Health Check API

### Responsibilities

- Request validation
- Authentication
- Dependency injection
- Response formatting

---

## 4.2 Application Layer

Responsible for orchestration and business workflows.

### Services

- Chat Service
- User Service
- Program Service
- Prompt Service
- ABAC Service
- Query Analyser Service
- AI Search Service
- OpenAI Service
- Session Manager Service
- APIM Key Service

---

## 4.3 Domain Layer

Contains business entities and business rules.

### Core Entities

```text
User
Program
Prompt
Conversation
Message
Feedback
Policy
Action
TokenLimit
RetrievalLog
```

---

## 4.4 Infrastructure Layer

Provides integrations with external systems.

### Infrastructure Services

```text
Azure OpenAI
Azure AI Search
Azure AD
Key Vault
Managed Identity
PostgreSQL
Azure API Management
Logging
Telemetry
```

---

# 5. Authentication Architecture

The platform authenticates users through Azure AD / Entra ID.

## Authentication Flow

```text
User
 |
 v
Azure AD Login
 |
 v
JWT Access Token
 |
 v
Authentication Service
 |
 v
Authenticated User
```

### Authentication Features

- JWT validation
- Issuer validation
- Signature validation
- Scope validation
- JWKS caching
- OID extraction

---

# 6. Authorization Architecture (ABAC)

The platform implements Attribute Based Access Control (ABAC).

Unlike simple role-based models, access decisions are calculated dynamically using user attributes, program membership, actions and policies.

## Authorization Pipeline

```text
Request
  |
  v
UserActiveHandler
  |
  v
TokenQuotaHandler
  |
  v
ProgramActiveHandler
  |
  v
UserProgramHandler
  |
  v
UserActionHandler
  |
  v
PolicyHandler
  |
  v
ALLOW / DENY
```

## Supported Actions

```text
READ
WRITE
EXPORT
```

## Policy Effects

```text
ALLOW
DENY
```

---

# 7. Conversation Management

The platform is centred around persisted conversations.

## Conversation Model

```text
User
 |
 +---- Conversation
           |
           +---- Message
                     |
                     +---- Feedback
                     |
                     +---- RetrievalLog
```

### Conversation Responsibilities

- Chat history management
- Archiving
- Token tracking
- Model tracking
- Retrieval auditing
- Feedback collection

---

# 8. Retrieval Augmented Generation (RAG)

The platform implements a sophisticated Retrieval Augmented Generation architecture.

## End-to-End Flow

```text
User Question
      |
      v
Query Analysis
      |
      v
Datasource Selection
      |
      v
Azure AI Search
      |
      v
Fusion Service
      |
      v
Citation Builder
      |
      v
OpenAI Prompt Assembly
      |
      v
Azure OpenAI
      |
      v
Generated Response
```

---

# 9. Query Analysis Layer

Before any search is performed, the platform analyses the user question using an LLM planner.

## Query Planning Flow

```text
Question
     |
     v
Planner Prompt
     |
     v
GPT Analysis
     |
     +---- Datasources
     |
     +---- Regions
     |
     +---- Organisations
     |
     +---- Categories
     |
     +---- Date Filters
     |
     v
Search Instructions
```

This approach significantly improves retrieval quality.

---

# 10. Search Architecture

Azure AI Search is used as the primary retrieval engine.

Both semantic search and vector search are supported.

## Search Flow

```text
Question
   |
   v
Embedding Generation
   |
   v
Azure AI Search
   |
   +---- Vector Search
   |
   +---- Semantic Search
   |
   v
Retrieved Documents
```

---

# 11. Strategy Pattern Implementation

The retrieval subsystem implements the Strategy Pattern.

Each datasource corresponds to a dedicated search strategy.

## Search Strategy Architecture

```text
Datasource Registry
        |
        +---- CSNP
        |
        +---- RESP
        |
        +---- RNP
        |
        +---- TIDE
        |
        +---- TRESP
        |
        +---- SSEP
```

### Benefits

- Extensible design
- Low coupling
- Easy onboarding of new consultation repositories
- Independent search configurations

---

# 12. Fusion Architecture

Multiple search indexes can be queried for a single request.

Results are merged using Reciprocal Rank Fusion (RRF).

## Fusion Flow

```text
Search Index A
        \
         \
Search Index B -----> Fusion Service
         /
        /
Search Index C
        |
        v
Unified Ranked Results
```

### Advantages

- Improved relevance
- Better result coverage
- Reduced bias toward a single datasource

---

# 13. Citation Architecture

Responses are generated with supporting citations.

## Citation Flow

```text
Retrieved Documents
         |
         v
Citation Builder
         |
         +---- S1
         +---- S2
         +---- S3
         |
         v
Response Context
         |
         v
Generated Response
```

### Benefits

- Explainable AI
- Traceability
- Source verification

---

# 14. Session Management

The platform maintains both active and persistent state.

## Session Architecture

```text
Session Manager
       |
       +---- Active Session Cache

PostgreSQL
       |
       +---- Persistent Conversation Store
```

### Responsibilities

- Session tracking
- Message history
- Cleanup
- Persistence coordination

---

# 15. Database Model

## High-Level ER Diagram

```text
User
 |
 +---- UserProgram
 |
 +---- UserAction
 |
 +---- UserTokenLimit
 |
 +---- Conversation
            |
            +---- Message
                     |
                     +---- Feedback
                     |
                     +---- RetrievalLog

Program
 |
 +---- Policy
 |
 +---- Conversations

Prompt
 |
 +---- Prompt Versions
```

---

# 16. Prompt Architecture

Prompts are managed independently of application code.

## Prompt Types

```text
SYSTEM
PLANNER
SYNTHESISER
```

## Prompt Lifecycle

```text
Draft
   |
   v
Active
   |
   v
Archived
```

---

# 17. Startup Sequence

The application performs controlled startup validation.

## Startup Flow

```text
Application Start
        |
        v
Configure Logging
        |
        v
Connect PostgreSQL
        |
        v
Load Prompts
        |
        v
Load Programs
        |
        v
Retrieve APIM Key
        |
        v
Create OpenAI Client
        |
        v
Validate OpenAI Connectivity
        |
        v
Application Ready
```

---

# 18. Azure Services

The platform integrates heavily with Azure.

## Identity

- Azure AD / Entra ID
- Managed Identity

## AI Services

- Azure OpenAI
- Azure AI Search

## Security

- Azure Key Vault
- Azure API Management

## Persistence

- Azure PostgreSQL

---

# 19. Logging and Observability

The platform contains a comprehensive operational monitoring layer.

## Capabilities

- Structured logging
- Request correlation IDs
- Health checks
- Startup validation
- Exception hierarchy
- Retry policies

## Request Correlation

```text
Request
   |
   +---- X-Request-ID
   |
   v
Application Logs
```

---

# 20. Resilience Architecture

The platform implements retry and resilience patterns.

## Retry Conditions

```text
HTTP 429
HTTP 5xx
```

Retries are used for:

- Azure AI Search
- Azure OpenAI
- Key Vault access

---

# 21. Design Patterns Identified

## Layered Architecture

```text
API
 |
Service
 |
Domain
 |
Infrastructure
```

---

## Dependency Injection

FastAPI dependency providers are used throughout the application.

---

## Service Layer Pattern

Business workflows are isolated inside service classes.

---

## Chain of Responsibility

Used by the ABAC engine.

```text
Handler
  ->
Handler
  ->
Handler
```

---

## Strategy Pattern

Used by datasource search strategies.

```text
Datasource
     |
     v
Search Strategy
```

---

## Registry Pattern

Used to resolve search strategies dynamically.

---

## Singleton Pattern

Used by PostgreSQL infrastructure components.

---

## Middleware Pattern

Used for:

- Request correlation
- Authentication
- Logging

---

# 22. Architectural Strengths

## Security

- Azure AD integration
- ABAC authorization
- Policy-driven access control

## Scalability

- Datasource strategy framework
- Multi-index search
- Extensible retrieval architecture

## Maintainability

- Strong separation of concerns
- Service abstraction
- Domain isolation

## Governance

- Token quotas
- Program access controls
- Retrieval logging

## Explainability

- Citation framework
- Retrieval audit history

---

# 23. Risks and Technical Debt

## Authorization Complexity

The ABAC chain may become increasingly complex as new policy rules are introduced.

## Datasource Growth

Each new datasource requires strategy registration and maintenance.

## Prompt Dependency

Retrieval quality depends on planner prompt effectiveness.

## Dual State Management

State is maintained both:

```text
In Memory
and
PostgreSQL
```

requiring careful synchronisation.

---

# 24. Architectural Conclusion

The platform can be described as:

> An enterprise Azure-native Retrieval Augmented Generation (RAG) platform providing secure, citation-backed AI assistance over multiple consultation and programme knowledge repositories.

The strongest architectural characteristics are:

- Robust ABAC security model
- Multi-source retrieval architecture
- Query planning capability
- Reciprocal Rank Fusion search
- Evidence-backed responses
- Clean separation between API, application, domain and infrastructure layers

Overall, the design demonstrates a mature and extensible enterprise AI architecture suitable for regulated environments requiring governance, auditability, and explainable AI responses.