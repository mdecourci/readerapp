# AI Assistant Platform
# Detailed Design Document (DDD)

**Version:** 1.0  
**Derived From:** Source Code Analysis and SID HLD Alignment  
**Purpose:** Maintenance and Enhancement Guide for Developers

---

# 1. Introduction

This document describes the detailed implementation architecture of the AI Assistant Platform.

Unlike the original SID High Level Design, this document focuses on the architecture that has actually been implemented in code.

The system is an Azure-native enterprise Retrieval Augmented Generation (RAG) platform that provides secure, citation-backed AI responses over consultation and programme-specific knowledge repositories.

---

# 2. System Purpose

The platform enables users to:

- Authenticate using Microsoft Entra ID
- Access authorised programmes
- Ask questions against consultation datasets
- Retrieve relevant content from Azure AI Search
- Generate AI responses using Azure OpenAI
- Receive responses with citations
- Store conversations and feedback
- Enforce governance and token controls

---

# 3. High Level Architecture

```text
+----------------------------------------------------+
|                    Client UI                       |
+--------------------------+-------------------------+
                           |
                           v
+----------------------------------------------------+
|                     FastAPI API                    |
+----------------------------------------------------+
                           |
                           v
+----------------------------------------------------+
|          Authentication / Authorization            |
+----------------------------------------------------+
                           |
                           v
+----------------------------------------------------+
|            Conversation Orchestration              |
+----------------------------------------------------+
            |                             |
            v                             v
+----------------------+    +--------------------------+
|   Azure AI Search    |    |      Azure OpenAI        |
+----------------------+    +--------------------------+
            |                             |
            +-------------+---------------+
                          |
                          v
               +----------------------+
               | PostgreSQL Storage   |
               +----------------------+
```

---

# 4. Architectural Principles

The implementation follows:

- Layered Architecture
- Service-Oriented Design
- Dependency Injection
- Attribute Based Access Control (ABAC)
- Retrieval Augmented Generation (RAG)
- Azure-Native Infrastructure
- Strong Separation of Concerns

---

# 5. Layered Architecture

```text
Presentation Layer
        |
Application Layer
        |
Domain Layer
        |
Infrastructure Layer
```

---

# 6. Presentation Layer

The Presentation Layer exposes REST APIs through FastAPI.

## Components

### Chat API

Responsibilities:

- Submit question
- Retrieve conversations
- Delete conversations
- Submit feedback

Dependencies:

```text
ChatService
ABACService
SessionManagerService
```

---

### User API

Responsibilities:

```text
Create User
Grant Access
Assign Programmes
Assign Actions
Retrieve Users
```

Dependencies:

```text
UserService
ABACService
```

---

### Program API

Responsibilities:

```text
List Programmes
Activate Programmes
Manage Programme Metadata
```

---

### Prompt API

Responsibilities:

```text
Prompt Administration
Prompt Versioning
Prompt Activation
Prompt Archiving
```

---

### Health API

Responsibilities:

```text
Health Monitoring
Readiness Checks
Liveness Checks
```

---

# 7. Authentication Architecture

Authentication uses Microsoft Entra ID (Azure AD).

## Authentication Flow

```text
User
 |
 v
Azure AD Login
 |
 v
Bearer JWT Token
 |
 v
Auth Service
 |
 v
Authenticated User
```

## Auth Service Responsibilities

- JWT validation
- Signature validation
- Issuer validation
- Audience validation
- OID extraction
- Scope validation

## Output

```python
AuthenticatedUser
```

Contains:

```text
OID
Username
Tenant
Scopes
Claims
```

---

# 8. Authorization Architecture

The solution implements Attribute Based Access Control (ABAC).

## ABAC Service

Central component responsible for all authorization decisions.

### Design Pattern

Chain of Responsibility

---

## ABAC Evaluation Flow

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

---

## User Active Handler

Checks:

```text
User Exists
User Active
```

Failure Result:

```text
Access Denied
```

---

## Token Quota Handler

Checks:

```text
Daily Token Limit
Monthly Token Limit
```

Sources:

```text
Conversation History
Message History
User Limits
```

---

## Program Active Handler

Checks:

```text
Program Exists
Program Active
```

---

## User Program Handler

Checks:

```text
User Assigned To Programme
```

Example:

```text
User
 |
 +-- SSEP
 +-- RESP

Denied:
 |
 +-- TIDE
```

---

## User Action Handler

Supported Actions:

```text
READ
WRITE
EXPORT
```

---

## Policy Handler

Evaluates:

```text
Policy Conditions
Allow Effect
Deny Effect
```

---

# 9. Core Application Components

---

# 9.1 Chat Service

The Chat Service is the primary orchestration component.

## Responsibilities

```text
Conversation Creation
Conversation Retrieval
Authorization Integration
Prompt Selection
Query Planning
Search Execution
Response Generation
Persistence
```

## Inputs

```text
User Question
Conversation ID
Authenticated User
```

## Outputs

```text
AI Response
Conversation Updates
Retrieved Citations
```

---

# 9.2 Session Manager Service

Maintains active conversations.

## Responsibilities

```text
Create Session
Retrieve Session
Update Session
Delete Session
Cleanup Sessions
```

## Storage

```text
In-Memory Session Store
```

Purpose:

```text
Reduce repeated database reads
Maintain active conversation context
```

---

# 10. Query Analysis Layer

The platform performs intelligent query planning before retrieval.

---

## Query Analyser Service

### Purpose

Convert natural language into retrieval instructions.

### Input

```text
What did Scottish Local Authorities
say about regional planning?
```

### Output

```json
{
  "datasources":["RESP","SSEP"],
  "region":"Scotland",
  "stakeholder":"Local Authority"
}
```

---

## Benefits

```text
Improved Precision
Reduced Noise
Better Retrieval Results
```

---

## Planner Prompt

Uses OpenAI before search execution.

Flow:

```text
Question
 |
Planner Prompt
 |
GPT Analysis
 |
Structured Search Request
```

---

# 11. Retrieval Architecture

The platform uses Retrieval Augmented Generation (RAG).

---

## End-to-End RAG Flow

```text
Question
    |
    v
Query Planning
    |
    v
Datasource Selection
    |
    v
Search
    |
    v
Fusion
    |
    v
Citation Building
    |
    v
Prompt Assembly
    |
    v
OpenAI Generation
    |
    v
Response
```

---

# 12. AI Search Service

Central integration point for Azure AI Search.

## Responsibilities

```text
Vector Search
Semantic Search
Filtering
Search Index Querying
Document Retrieval
```

## Security

Uses:

```text
Managed Identity
```

---

# 13. Registry Pattern

Used for datasource resolution.

## Flow

```text
Datasource
      |
      v
Registry
      |
      v
Strategy
```

Benefits:

```text
Loose Coupling
Easy Extension
No Chat Service Changes Required
```

---

# 14. Search Strategy Components

Every datasource is represented by a strategy.

---

## CSNP Strategy

```text
CSNP Consultation Data
```

---

## RESP Strategy

```text
RESP Consultation Responses
```

---

## RNP Strategy

```text
RNP Consultation Responses
```

---

## TIDE Strategy

```text
TIDE Consultation Data
```

---

## TRESP Strategy

```text
Regional Energy Strategic Plans
```

---

## SSEP Strategies

Support:

```text
Meeting Notes
Feedback Logs
Methodology Consultations
```

---

# 15. Fusion Service

Combines retrieval results from multiple indexes.

## Algorithm

Reciprocal Rank Fusion (RRF)

---

## Flow

```text
Search A
      \
       \
Search B ---> Fusion ---> Ranked Results
       /
      /
Search C
```

Benefits:

```text
Improved Ranking
Cross-Domain Retrieval
Higher Recall
```

---

# 16. Citation Service

Responsible for creating evidence references.

---

## Input

```text
Retrieved Documents
```

## Output

```text
[S1]
[S2]
[S3]
```

---

## Purpose

Supports:

```text
Traceability
Responsible AI
Evidence-Based Responses
```

---

# 17. OpenAI Service

Provides Azure OpenAI abstraction.

---

## Responsibilities

```text
Embedding Generation
Chat Completion
Retry Logic
Error Translation
Timeout Handling
```

---

## Input

```text
Prompt
Conversation History
Retrieved Context
```

---

## Output

```text
Generated Answer
```

---

# 18. Component Interaction Diagram

This diagram shows the runtime interaction between all major components.

```text
+------------------+
|      User        |
+---------+--------+
          |
          | Ask Question
          v
+------------------+
|     Chat API     |
+---------+--------+
          |
          | Authorize Request
          v
+------------------+
|   ABAC Service   |
+---------+--------+
          |
          +--------------------------------+
          |                                |
          v                                |
+------------------+                       |
| User Active      |                       |
+------------------+                       |
          |                                |
          v                                |
+------------------+                       |
| Token Quota      |                       |
+------------------+                       |
          |                                |
          v                                |
+------------------+                       |
| Program Active   |                       |
+------------------+                       |
          |                                |
          v                                |
+------------------+                       |
| User Program     |                       |
+------------------+                       |
          |                                |
          v                                |
+------------------+                       |
| User Action      |                       |
+------------------+                       |
          |                                |
          v                                |
+------------------+                       |
| Policy Handler   |                       |
+---------+--------+                       |
          | Allowed                        |
          +--------------------------------+
          |
          v
+--------------------------+
|       Chat Service       |
+-----------+--------------+
            |
            | Retrieve / Create Session
            v
+--------------------------+
| Session Manager Service  |
+--------------------------+
            |
            v
+--------------------------+
| Query Analyser Service   |
+-----------+--------------+
            |
            | Uses Planner Prompt
            v
+--------------------------+
|     OpenAI Service       |
| (Query Planning Phase)   |
+-----------+--------------+
            |
            | Structured Search Request
            v
+--------------------------+
|    AI Search Service     |
+-----------+--------------+
            |
            v
+--------------------------+
|     Registry Service     |
+-----------+--------------+
            |
            +-------------------------------+
            |                               |
            v                               v
+------------------+             +------------------+
| CSNP Strategy    |             | RESP Strategy    |
+------------------+             +------------------+
            |                               |
            +-----------+-------------------+
                        |
                        v
               +------------------+
               | Other Strategies |
               | RNP / TIDE /     |
               | TRESP / SSEP     |
               +--------+---------+
                        |
                        | Search Results
                        v
               +------------------+
               | Fusion Service   |
               |   (RRF Merge)    |
               +--------+---------+
                        |
                        v
               +------------------+
               | Citation Builder |
               +--------+---------+
                        |
                        | Context + Sources
                        v
               +------------------+
               | OpenAI Service   |
               | Response Gen     |
               +--------+---------+
                        |
                        | AI Response
                        v
               +------------------+
               | PostgreSQL Cache |
               | Service          |
               +--------+---------+
                        |
                        +--> Save Conversation
                        |
                        +--> Save Message
                        |
                        +--> Save Retrieval Logs
                        |
                        +--> Save Token Usage
                        |
                        v
               +------------------+
               |   Chat Service   |
               +--------+---------+
                        |
                        v
               +------------------+
               |     Chat API     |
               +--------+---------+
                        |
                        v
               +------------------+
               |       User       |
               +------------------+
```

---

# 19. Persistence Architecture

## PostgreSQL Manager

Responsibilities:

```text
Connection Pooling
Session Management
Managed Identity Authentication
```

---

## PostgreSQL Cache Service

Responsibilities:

```text
Save Conversation
Save Message
Retrieve Conversations
Retrieve Messages
Compute Token Usage
```

---

# 20. Domain Model

```text
User
 |
 +-- UserPrograms
 |
 +-- UserActions
 |
 +-- UserTokenLimits
 |
 +-- Conversations
         |
         +-- Messages
                 |
                 +-- Feedback
                 |
                 +-- RetrievalLogs

Program
 |
 +-- Policies

Prompt
 |
 +-- Versions
```

---

# 21. Domain Entity Descriptions

## User

Stores:

```text
OID
Username
Email
Active Flag
```

---

## Program

Stores:

```text
Programme Metadata
Status
Description
```

---

## Conversation

Stores:

```text
Title
Owner
Programme
Created Date
Archived State
```

---

## Message

Stores:

```text
Role
Content
Prompt Tokens
Completion Tokens
Model Used
Latency
```

---

## Retrieval Log

Stores:

```text
Retrieved Document
Rank
Score
Datasource
Citation
```

---

## Feedback

Stores:

```text
Feedback Type
Comments
Associated Message
```

---

## Prompt

Stores:

```text
Name
Version
Status
Content
```

---

# 22. Infrastructure Components

## Managed Identity Service

Provides:

```text
Azure Access Tokens
```

Used for:

```text
Azure Search
PostgreSQL
Key Vault
```

---

## Key Vault Client

Provides:

```text
Secret Retrieval
```

---

## APIM Key Service

Provides:

```text
Secret Caching
APIM Key Retrieval
```

---

## Logging Service

Provides:

```text
Structured Logging
Error Logging
Operational Metrics
```

---

## Request ID Middleware

Provides:

```text
Request Traceability
Correlation IDs
```

---

# 23. Startup Sequence

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
Load Active Prompts
        |
        v
Load Active Programmes
        |
        v
Retrieve APIM Key
        |
        v
Build OpenAI Client
        |
        v
Validate OpenAI Connection
        |
        v
Application Ready
```

---

# 24. Design Patterns Used

## Layered Architecture

```text
Presentation
Application
Domain
Infrastructure
```

## Service Layer

```text
ChatService
UserService
ProgramService
PromptService
```

## Chain of Responsibility

```text
ABAC Handler Chain
```

## Strategy Pattern

```text
Search Strategy Framework
```

## Registry Pattern

```text
Datasource Registry
```

## Singleton Pattern

```text
PostgreSQL Manager
```

## Dependency Injection

```text
FastAPI Dependencies
```

## Middleware Pattern

```text
Logging
Request IDs
Authentication
```

---

# 25. Maintenance Guidance

## Adding a New Data Source

1. Create new Search Strategy.
2. Register strategy in Registry.
3. Add datasource mapping.
4. Update query analyser prompts.
5. Validate citations.

---

## Adding New Authorization Rules

1. Create new Handler.
2. Implement `handle()`.
3. Insert in ABAC chain.
4. Add tests.

---

## Adding New Prompt Types

1. Add Prompt Type.
2. Seed Prompt.
3. Load during startup.
4. Update Prompt Service.

---

## Troubleshooting Chat Responses

Investigate in order:

```text
1. Authentication
2. Authorization
3. Query Analysis
4. Search Retrieval
5. Fusion
6. Citation Builder
7. OpenAI Response
8. Persistence
```

---

# 26. Architectural Assessment

## Strengths

- Strong security model
- Governance built into architecture
- Extensible search framework
- Explainable AI responses
- Clear separation of concerns
- Highly maintainable service boundaries

## Risks

- Authorization complexity as policies grow
- Strategy growth for new datasources
- Prompt-engineering dependency
- Dual state management (memory + database)

---

---

# 27. Service Deep Dive

This section provides a maintenance-focused view of each service, what it does, when it is called, and how data flows through the system.

The objective is to help new developers understand:

- Which service owns which responsibility
- How requests move through the system
- Where to debug issues
- Which services are business-critical

---

# 27.1 Chat Service

## Purpose

The Chat Service is the central orchestration component.

Almost every user request passes through this service.

It coordinates:

- Authorization
- Sessions
- Query Analysis
- Search
- Fusion
- Citation Generation
- OpenAI
- Persistence

## Flow

```text
User Question
      |
      v
Authorization Passed
      |
      v
Load/Create Conversation
      |
      v
Query Analysis
      |
      v
Search Documents
      |
      v
Merge Results
      |
      v
Build Citations
      |
      v
Generate AI Response
      |
      v
Save Conversation
      |
      v
Return Response
```

## Debug Here When

```text
Incorrect Responses
Conversation Issues
Missing Citations
Search Not Executed
```

---

# 27.2 ABAC Service

## Purpose

Central authorization engine.

Every request must pass through ABAC before any search or AI processing occurs.

## Flow

```text
Request
    |
    v
Build Context
    |
    v
User Active Check
    |
    v
Token Quota Check
    |
    v
Program Active Check
    |
    v
User Program Check
    |
    v
User Action Check
    |
    v
Policy Check
    |
    v
ALLOW / DENY
```

## Debug Here When

```text
Access Denied
Missing Permissions
Program Access Problems
Authorization Failures
```

---

# 27.3 User Service

## Purpose

Manages users and access assignments.

## Responsibilities

```text
Create User
Update User
Assign Programs
Assign Actions
Grant Access
Retrieve User Data
```

## Flow

```text
Admin Request
      |
      v
Validate User
      |
      v
Create/Update User
      |
      v
Assign Programs
      |
      v
Assign Actions
      |
      v
Persist To Database
```

## Debug Here When

```text
User Missing
Incorrect Access
Provisioning Problems
```

---

# 27.4 Program Service

## Purpose

Maintains programme metadata and active programme cache.

## Responsibilities

```text
Load Programs
Cache Programs
Retrieve Programs
Validate Programs
Check Active Status
```

## Flow

```text
Program Request
      |
      v
Read Active Program Cache
      |
      v
Validate Program
      |
      v
Return Program
```

## Debug Here When

```text
Program Not Found
Program Inactive
Program Metadata Issues
```

---

# 27.5 Prompt Service

## Purpose

Manages prompt lifecycle.

## Responsibilities

```text
Load Prompts
Version Prompts
Activate Prompts
Archive Prompts
```

## Flow

```text
Startup
    |
    v
Load Active Prompts
    |
    v
Cache Prompts
    |
    v
Provide Prompt On Request
```

## Prompt Types

```text
System
Planner
Synthesiser
```

## Debug Here When

```text
Bad AI Responses
Prompt Changes
Prompt Version Issues
```

---

# 27.6 Query Analyser Service

## Purpose

Converts natural language into structured retrieval instructions.

This is the first AI stage.

## Example

Input:

```text
What concerns did Scottish local
authorities raise about energy planning?
```

Output:

```json
{
  "region": "Scotland",
  "stakeholder":"Local Authority",
  "program":"SSEP"
}
```

## Flow

```text
Question
    |
    v
Planner Prompt
    |
    v
OpenAI Analysis
    |
    v
Extract Filters
    |
    v
Build Search Request
```

## Debug Here When

```text
Wrong Search Results
Bad Filtering
Incorrect Program Selection
```

---

# 27.7 AI Search Service

## Purpose

Provides Azure AI Search integration.

## Responsibilities

```text
Vector Search
Semantic Search
Filtering
Index Selection
```

## Flow

```text
Search Request
       |
       v
Get Strategy
       |
       v
Build Search Query
       |
       v
Azure AI Search
       |
       v
Retrieved Documents
```

## Debug Here When

```text
No Search Results
Incorrect Results
Search Performance Problems
```

---

# 27.8 Registry Service

## Purpose

Maps Datasource to Search Strategy.

## Flow

```text
Datasource
    |
    v
Registry
    |
    v
Return Strategy
```

Example:

```text
SSEP
 ->
SSEP Strategy

RESP
 ->
RESP Strategy
```

## Debug Here When

```text
Datasource Not Found
Strategy Registration Issues
```

---

# 27.9 Fusion Service

## Purpose

Combines search results from multiple sources.

## Algorithm

```text
Reciprocal Rank Fusion (RRF)
```

## Flow

```text
Search Result Set A
          \
           \
Search Result Set B
           /
          /
Search Result Set C
          |
          v
       Fusion
          |
          v
 Ranked Results
```

## Debug Here When

```text
Poor Ranking
Unexpected Result Order
```

---

# 27.10 Citation Service

## Purpose

Creates citations for AI responses.

## Example

```text
[S1]
[S2]
[S3]
```

## Flow

```text
Retrieved Documents
        |
        v
Generate Citations
        |
        v
Return Sources
```

## Debug Here When

```text
Missing Citations
Incorrect Sources
Bad Traceability
```

---

# 27.11 OpenAI Service

## Purpose

Abstraction layer over Azure OpenAI.

## Responsibilities

```text
Generate Embeddings
Generate Responses
Retry Failures
Handle Errors
```

## Flow

```text
Prompt
    |
    v
Azure OpenAI
    |
    v
AI Response
```

## Used By

```text
Query Analyser
Chat Service
```

## Debug Here When

```text
Model Errors
Rate Limits
Unexpected Responses
```

---

# 27.12 PostgreSQL Cache Service

## Purpose

Primary persistence service.

## Responsibilities

```text
Store Conversations
Store Messages
Store Retrieval Logs
Store Token Metrics
```

## Flow

```text
Conversation Update
       |
       v
Persist Objects
       |
       v
Database
```

## Debug Here When

```text
Missing Conversations
Data Persistence Issues
Token Calculation Problems
```

---

# 27.13 Session Manager Service

## Purpose

Maintains active conversation state.

## Flow

```text
Create Session
      |
      v
Add Messages
      |
      v
Retrieve Session
      |
      v
Delete Session
```

## Debug Here When

```text
Context Lost
Conversation State Issues
```

---

# 27.14 Authentication Service

## Purpose

Validates Azure AD tokens.

## Flow

```text
JWT Token
     |
     v
Validate Signature
     |
     v
Validate Issuer
     |
     v
Validate Audience
     |
     v
Create Authenticated User
```

## Debug Here When

```text
401 Errors
Login Issues
Token Errors
```

---

# 27.15 Managed Identity Service

## Purpose

Obtains Azure access tokens.

## Flow

```text
Application
      |
      v
Managed Identity
      |
      v
Azure Token
```

Used By:

```text
AI Search
PostgreSQL
Key Vault
```

---

# 27.16 Key Vault Client

## Purpose

Retrieve secrets securely.

## Flow

```text
Secret Name
      |
      v
Key Vault
      |
      v
Secret Value
```

---

# 27.17 APIM Key Service

## Purpose

Retrieve and cache APIM keys.

## Flow

```text
APIM Secret Name
        |
        v
Key Vault
        |
        v
Cache Result
        |
        v
Return Key
```

---

# 28. Detailed ABAC Flow

The following flowchart shows the complete authorization decision process.

```text
                    +--------------------+
                    |  User Request      |
                    | Program = SSEP     |
                    | Action = READ      |
                    +---------+----------+
                              |
                              v
                  +------------------------+
                  | Build AbacContext      |
                  +-----------+------------+
                              |
                              v

                  +------------------------+
                  | User Active Handler    |
                  +-----------+------------+
                              |
                       User Active?
                         /      \
                       No       Yes
                       |          |
                       v          v
                    DENY     Continue

                              |
                              v

                  +------------------------+
                  | Token Quota Handler    |
                  +-----------+------------+
                              |
                     Quota Available?
                       /          \
                     No           Yes
                     |              |
                     v              v
                  DENY        Continue

                              |
                              v

                  +------------------------+
                  | Program Active Handler |
                  +-----------+------------+
                              |
                     Program Active?
                       /          \
                     No           Yes
                     |              |
                     v              v
                  DENY        Continue

                              |
                              v

                  +------------------------+
                  | User Program Handler   |
                  +-----------+------------+
                              |
                    User Assigned?
                       /        \
                     No         Yes
                     |            |
                     v            v
                  DENY      Continue

                              |
                              v

                  +------------------------+
                  | User Action Handler    |
                  +-----------+------------+
                              |
                   Action Assigned?
                       /       \
                      No       Yes
                      |          |
                      v          v
                   DENY     Continue

                              |
                              v

                  +------------------------+
                  | Policy Handler         |
                  +-----------+------------+
                              |
                      Policy Result
                       /         \
                   DENY         ALLOW
                     |             |
                     v             v
                 Access      Access
                 Denied      Granted
```

---

# 29. Program Catalogue

Programs represent business knowledge domains.

A Program controls:

- What data can be searched
- What conversations can be created
- Which users may access information
- Which search strategies are available

---

## CSNP

### Description

Represents consultation and stakeholder information related to the CSNP programme.

### Data Sources

```text
Consultation Responses
Stakeholder Feedback
Programme Documentation
```

### Typical Questions

```text
What concerns were raised?
Which themes appeared most often?
```

---

## RESP

### Description

Represents consultation responses associated with RESP initiatives.

### Data Sources

```text
Formal Responses
Public Consultation Data
```

### Typical Questions

```text
What did local authorities say?
What objections were submitted?
```

---

## RNP

### Description

Represents Reformed National Pricing related consultation material.

### Data Sources

```text
Consultation Responses
Stakeholder Representations
Pricing Discussions
```

### Typical Questions

```text
What pricing concerns were raised?
Which stakeholder groups supported the proposal?
```

---

## TIDE

### Description

Represents Transformation to Integrate Distributed Energy consultation information.

### Data Sources

```text
Distributed Energy Feedback
Consultation Responses
Stakeholder Commentary
```

### Typical Questions

```text
What concerns exist around distributed energy?
Which recommendations were proposed?
```

---

## TRESP

### Description

Represents Transitional Regional Energy Strategic Planning consultation material.

### Data Sources

```text
Regional Planning Responses
Energy Strategy Feedback
Consultation Documents
```

### Typical Questions

```text
What regional concerns were identified?
Which themes were most common?
```

---

## SSEP

### Description

Strategic Spatial Energy Planning programme.

This appears to be one of the largest knowledge domains in the platform.

### Data Sources

```text
Meeting Notes
Feedback Logs
Methodology Consultations
Stakeholder Engagement Records
```

### Typical Questions

```text
What feedback was received?
What actions were agreed?
Which organisations raised concerns?
```

---

# 30. Maintenance Starting Point

If you are new to the solution, focus on understanding these services first:

```text
ChatService
    |
ABACService
    |
QueryAnalyserService
    |
AISearchService
    |
OpenAIService
```

These five services form the core execution path of the entire platform.

Everything else exists to support, secure, monitor or persist that workflow.

# 31. Conclusion

This solution is best described as:

> An Azure-native, enterprise Retrieval Augmented Generation (RAG) platform that provides secure, auditable, citation-backed AI assistance across multiple consultation and programme knowledge repositories.

The most important component for maintainers to understand is the **Chat Service**, as it orchestrates the complete workflow:

```text
Authorization
    →
Session Management
    →
Query Analysis
    →
Search Retrieval
    →
Result Fusion
    →
Citation Generation
    →
OpenAI Generation
    →
Persistence
```

Nearly all future enhancements and support activities will intersect with this processing pipeline.