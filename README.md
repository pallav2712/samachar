# 📰 Samachar

> **An AI-powered personalized news digest system that collects, summarizes, and delivers the news that matters to you.**

Samachar is a backend-focused application that automates the complete news consumption workflow.

Users configure the topics they care about through a **Telegram Bot**. Samachar collects relevant news through a **News API**, persists and manages the data in **PostgreSQL**, processes the collected articles using **LLM integration**, and delivers a concise personalized digest back to the user.

The system can be triggered manually through Telegram or automatically through a **scheduled daily job**, creating a complete end-to-end pipeline from **news collection → data persistence → AI processing → user delivery**.

---

# 🚀 Overview

Following news across multiple topics every day can be time-consuming. Samachar turns this into an automated workflow that collects relevant stories, removes unnecessary repetition, summarizes the important information, and delivers it in a format that is easy to consume.

The **FastAPI backend acts as the central orchestrator** of the application.

```text
                         ┌──────────────┐
                         │     User     │
                         └──────┬───────┘
                                │
                           Telegram Bot
                                │
                                ▼
                     ┌────────────────────┐
                     │   FastAPI Backend  │
                     │    Orchestrator    │
                     └──────┬─────┬───────┘
                            │     │
                ┌───────────┘     └───────────┐
                ▼                             ▼
         ┌─────────────┐               ┌─────────────┐
         │   News API  │               │ LLM Service │
         └──────┬──────┘               └──────┬──────┘
                │                             │
                ▼                             │
         ┌─────────────┐                      │
         │ PostgreSQL  │──────────────────────┘
         └─────────────┘
                │
                ▼
          News Digest
                │
                ▼
            Telegram
```

### Core Workflow

```text
User Preferences
       ↓
News Collection
       ↓
Article Processing
       ↓
PostgreSQL
       ↓
LLM Integration
       ↓
Digest Generation
       ↓
Telegram Delivery
```

The application is designed around **separation of responsibilities, reusable services, persistent state, external API resilience, and automated background processing**.

---

# ✨ Key Features

## 📰 Personalized News Collection

Users can choose the topics they are interested in.

Examples:

```text
technology
science
business
sports
politics
health
programming
```

The selected topics are persisted and used by the news pipeline when collecting articles.

---

## 🤖 LLM Integration

LLM integration is a core component of Samachar.

Instead of sending raw articles directly to the user, the application processes the collected articles through an LLM to generate a concise and readable digest.

The summarization pipeline:

```text
Articles
   ↓
Group by Topic
   ↓
Prompt Construction
   ↓
LLM
   ↓
Concise Digest
```

The prompt is designed to instruct the model to:

* produce concise bullet points
* organize stories by topic
* combine multiple articles about the same story
* avoid unnecessary repetition
* use only information present in the supplied articles
* avoid inventing facts
* focus on important information

This makes the output suitable for a daily news digest rather than a raw AI response.

---

## 🛡️ Multi-Provider LLM Fallback

The LLM layer is designed to avoid depending on a single AI provider.

Samachar uses a fallback chain:

```text
              LLM Request
                   │
                   ▼
                 Groq
                   │
              ┌────┴────┐
              │         │
           Success    Failure
              │         │
              ▼         ▼
           Digest   OpenRouter
                        │
                   ┌────┴────┐
                   │         │
                Success    Failure
                   │         │
                   ▼         ▼
                Digest    Gemini
                              │
                         ┌────┴────┐
                         │         │
                      Success    Failure
                         │         │
                         ▼         ▼
                      Digest   Application
                                 Error
```

### Provider Priority

| Priority | Provider      | Role             |
| -------- | ------------- | ---------------- |
| 1        | Groq          | Primary provider |
| 2        | OpenRouter    | First fallback   |
| 3        | Google Gemini | Final fallback   |

If one provider fails because of a temporary outage, rate limit, API error, or other external failure, Samachar automatically attempts the next provider.

This introduces **fault tolerance at the LLM integration layer** and reduces the impact of a single provider becoming unavailable.

---

# 📱 Telegram Bot

Telegram provides the user-facing interface for Samachar.

Users do not need to interact directly with the backend API for normal usage.

The bot allows users to:

* start using Samachar
* view available commands
* subscribe to topics
* unsubscribe from topics
* request a digest manually

### Commands

```text
/start
/help
/subscribe <topic>
/unsubscribe <topic>
/digest
```

Example:

```text
User:
/subscribe technology

Samachar:
You are subscribed to technology.
```

The Telegram layer is kept separate from the core business logic. Command handlers delegate operations to the application's service layer instead of implementing database and news logic directly.

---

# ⏰ Automated Daily Digest

Samachar supports automated daily digest generation using a task scheduler.

The scheduled job runs at **8:00 AM** and executes the same core pipeline used by the manual digest workflow.

```text
                  8:00 AM
                     │
                     ▼
              Scheduled Job
                     │
                     ▼
              Fetch Latest News
                     │
                     ▼
                PostgreSQL
                     │
                     ▼
             Retrieve Unread News
                     │
                     ▼
               LLM Processing
                     │
                     ▼
               Generate Digest
                     │
                     ▼
                Telegram
```

The scheduler does not maintain a separate news-processing implementation.

Instead, it reuses the application's existing pipeline:

```text
Fetch → Persist → Summarize → Deliver
```

This keeps manual and automated digest generation consistent.

---

# 🔄 End-to-End Architecture

Samachar has three main triggers.

## 1. Scheduled Trigger

The automated daily workflow:

```text
Scheduler
   ↓
Fetch News
   ↓
Save to Database
   ↓
Retrieve Relevant Articles
   ↓
LLM Summarization
   ↓
Save Digest
   ↓
Telegram
```

---

## 2. Manual Trigger

The user can request a digest through Telegram:

```text
/digest
   ↓
Telegram
   ↓
FastAPI
   ↓
News Pipeline
   ↓
LLM
   ↓
Digest
   ↓
Telegram
```

---

## 3. Configuration Trigger

Users can update their preferences:

```text
/subscribe technology
        ↓
Telegram
        ↓
FastAPI / Service Layer
        ↓
PostgreSQL
```

This allows the news pipeline to adapt to the user's selected topics.

---

# 📰 News API Integration

Samachar uses **Currents News API** as its news provider.

The integration is isolated inside the news service and communicates with the provider through HTTP requests.

The application retrieves topic-specific news using the provider's latest-news endpoint.

Conceptually:

```text
Topic
  ↓
News Service
  ↓
Currents API
  ↓
Articles
```

The news service is responsible for:

* API authentication
* topic-based requests
* HTTP communication
* response processing
* handling API failures
* handling network failures
* handling empty responses

Keeping the provider-specific logic inside its own service means the rest of the application does not need to know how the external API works.

---

# 🔄 News Processing Pipeline

The news collection process is orchestrated by a dedicated pipeline service.

```text
Get Topics
    ↓
For Each Topic
    ↓
Fetch News
    ↓
Process Articles
    ↓
Check for Duplicates
    ↓
Save Articles
    ↓
Create Topic Relationships
```

This prevents the FastAPI route from becoming responsible for every individual step.

Instead:

```text
Route
  ↓
Pipeline
  ↓
Services
  ↓
Database / External APIs
```

---

# ♻️ Article Deduplication

The application prevents the same article from being stored multiple times.

The article URL acts as the unique identifier.

```text
Incoming Article
       ↓
Check URL
       │
   ┌───┴────┐
   │        │
 Exists   New
   │        │
   ▼        ▼
 Reuse    Create
 Article  Article
```

There are two levels of protection:

### Application-Level

The article service checks whether the URL already exists before creating a new record.

### Database-Level

The `articles.url` column has a **unique constraint**.

This provides defense at both the application and database layers.

---

# 📖 Read / Unread Article Tracking

Articles maintain a read state.

New articles are stored as:

```text
is_read = False
```

During digest generation, Samachar retrieves today's unread articles.

After they have successfully been included in a digest:

```text
is_read = True
```

The lifecycle becomes:

```text
New Article
     ↓
Unread
     ↓
Included in Digest
     ↓
Read
```

This prevents already processed articles from continuously appearing in future digests.

---

# 🧠 Article Selection

For digest generation, the application:

1. Retrieves the configured topics.
2. Looks for articles associated with each topic.
3. Restricts results to the current day.
4. Filters out already-read articles.
5. Orders articles by fetch time.
6. Limits the number of articles processed per topic.

The per-topic limit also helps control the amount of context sent to the LLM.

```text
Topic
  ↓
Today's Articles
  ↓
Unread Only
  ↓
Latest Articles
  ↓
Top 5
  ↓
LLM
```

This is particularly useful when working with LLM context limits and keeping the generated digest focused.

---

# 🌍 Timezone Handling

Samachar explicitly uses the **Asia/Kolkata** timezone when determining daily article boundaries and digest timestamps.

This is important because "today" should represent the application's intended local day rather than blindly relying on the server's timezone.

```text
Asia/Kolkata
      ↓
Start of Day
      ↓
Today's Articles
      ↓
Digest Generation
```

The same timezone is used when recording:

* article fetch timestamps
* digest generation timestamps
* daily scheduling

---

# 🗄️ Database Design

Samachar uses **PostgreSQL** with **SQLAlchemy**.

The database contains four primary entities:

```text
Topic
Article
TopicArticle
Digest
```

### Relationship

```text
┌─────────────┐
│    Topic    │
└──────┬──────┘
       │
       ▼
┌────────────────┐
│ TopicArticle   │
└───────┬────────┘
        │
        ▼
┌─────────────┐
│   Article   │
└─────────────┘


┌─────────────┐
│   Digest    │
└─────────────┘
```

---

## Topic

Stores the available topics.

```text
id
name
```

Topic names are unique.

---

## Article

Stores collected news articles.

```text
id
headline
url
content
fetched_at
is_read
```

The URL is unique to prevent duplicate articles.

---

## TopicArticle

Represents the relationship between topics and articles.

```text
topic_id
article_id
```

Both fields form a composite primary key.

This prevents the same article-topic relationship from being inserted more than once.

---

## Digest

Stores generated digests.

```text
id
content
generated_at
```

Persisting digests allows generated results to remain available as application data rather than existing only as temporary LLM responses.

---

# 🏗️ Application Architecture

The project follows a service-oriented structure:

```text
app/
│
├── core/
│   └── config.py
│
├── models/
│   ├── article.py
│   ├── digest.py
│   ├── topic.py
│   └── topic_article.py
│
├── routes/
│   └── news.py
│
├── services/
│   ├── articles.py
│   ├── llm.py
│   ├── news.py
│   ├── pipeline.py
│   └── topics.py
│
├── telegram/
│   ├── bot.py
│   └── handlers.py
│
├── database.py
└── main.py
```

### Responsibilities

| Component              | Responsibility                                            |
| ---------------------- | --------------------------------------------------------- |
| `core/config.py`       | Application configuration                                 |
| `database.py`          | Database engine and session management                    |
| `models/`              | SQLAlchemy database models                                |
| `routes/`              | FastAPI API endpoints                                     |
| `services/news.py`     | News API integration                                      |
| `services/articles.py` | Article persistence and retrieval                         |
| `services/topics.py`   | Topic management                                          |
| `services/pipeline.py` | News pipeline orchestration                               |
| `services/llm.py`      | Prompt generation, LLM calls, fallback, digest generation |
| `telegram/bot.py`      | Telegram application setup                                |
| `telegram/handlers.py` | Telegram command handling                                 |

---

# 🔌 API Layer

FastAPI exposes the core backend operations.

## `POST /news/fetch`

Triggers the news collection pipeline.

```text
POST /news/fetch
```

Flow:

```text
Topics
 ↓
News API
 ↓
Deduplication
 ↓
PostgreSQL
```

---

## `POST /news/digest`

Triggers digest generation.

```text
POST /news/digest
```

Flow:

```text
Topics
 ↓
Today's Unread Articles
 ↓
Prompt Construction
 ↓
LLM Fallback Chain
 ↓
Mark Articles Read
 ↓
Save Digest
 ↓
Return Digest
```

FastAPI also provides interactive API documentation through Swagger UI.

```text
/docs
```

---

# 🔐 Configuration Management

Samachar uses **Pydantic Settings** to manage application configuration.

Sensitive values are loaded from environment variables rather than being hardcoded into the application.

Example:

```env
CURRENTS_API_KEY=...
GROQ_API_KEY=...
OPENROUTER_API_KEY=...
GEMINI_API_KEY=...
TELEGRAM_BOT_TOKEN=...
DATABASE_URL=...
```

This keeps credentials separate from application code and makes the same codebase usable across different environments.

---

# ⚠️ Error Handling

External services are treated as unreliable dependencies.

## News API

The news service handles:

* authentication failures
* missing endpoints
* server-side failures
* other HTTP errors
* network/request failures
* empty news responses

Provider-specific exceptions are converted into application-level errors inside the news service.

---

## LLM

LLM failures trigger the fallback chain:

```text
Groq
 ↓ failure
OpenRouter
 ↓ failure
Gemini
 ↓ failure
RuntimeError
```

This prevents provider-specific failures from being tightly coupled to the rest of the application.

---

# 🐳 Dockerization

Samachar is containerized using **Docker**.

The deployment uses Docker Compose to run the application and PostgreSQL together.

```text
┌─────────────────────────────────────┐
│          Docker Compose             │
│                                     │
│  ┌───────────────────────────────┐  │
│  │         FastAPI App           │  │
│  └───────────────┬───────────────┘  │
│                  │                  │
│  ┌───────────────▼───────────────┐  │
│  │          PostgreSQL           │  │
│  └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

A persistent database volume ensures that PostgreSQL data survives container restarts.

The complete application can therefore be started with a single Docker Compose command.

---

# ⏱️ Task Scheduling

The automated digest is implemented using **APScheduler**.

The scheduler is configured for:

```text
Every day
8:00 AM
Asia/Kolkata
```

The scheduled job invokes the same core processing pipeline used by the manual digest workflow.

```text
APScheduler
     ↓
Fetch News
     ↓
Save Articles
     ↓
Generate Digest
     ↓
Send Telegram Message
```

This avoids maintaining separate business logic for scheduled and manual execution.

---

# 🛠️ Tech Stack

| Technology              | Purpose                              |
| ----------------------- | ------------------------------------ |
| **Python 3.12+**        | Application language                 |
| **FastAPI**             | Backend/API framework                |
| **Uvicorn**             | ASGI server                          |
| **PostgreSQL**          | Relational database                  |
| **SQLAlchemy 2.x**      | ORM                                  |
| **psycopg**             | PostgreSQL driver                    |
| **Pydantic Settings**   | Configuration management             |
| **HTTPX**               | HTTP client                          |
| **Currents News API**   | News provider                        |
| **python-telegram-bot** | Telegram Bot integration             |
| **Groq**                | Primary LLM provider                 |
| **OpenRouter**          | LLM fallback                         |
| **Google Gemini**       | LLM fallback                         |
| **APScheduler**         | Task scheduling                      |
| **Docker**              | Containerization                     |
| **Docker Compose**      | Application + database orchestration |
| **uv**                  | Python dependency management         |

---

# 📁 Project Structure

```text
samachar/
│
├── app/
│   ├── core/
│   │   └── config.py
│   │
│   ├── models/
│   │   ├── article.py
│   │   ├── digest.py
│   │   ├── topic.py
│   │   └── topic_article.py
│   │
│   ├── routes/
│   │   └── news.py
│   │
│   ├── services/
│   │   ├── articles.py
│   │   ├── llm.py
│   │   ├── news.py
│   │   ├── pipeline.py
│   │   └── topics.py
│   │
│   ├── telegram/
│   │   ├── bot.py
│   │   └── handlers.py
│   │
│   ├── database.py
│   └── main.py
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── .gitignore
├── kanban.md
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# ⚙️ Getting Started

## Prerequisites

* Python 3.12+
* Docker & Docker Compose
* PostgreSQL (for local non-Docker development)
* Telegram Bot Token
* Currents API Key
* Groq API Key
* OpenRouter API Key
* Gemini API Key

---

## 1. Clone the Repository

```bash
git clone https://github.com/pallav2712/samachar.git
cd samachar
```

---

## 2. Configure Environment Variables

Create a `.env` file:

```env
CURRENTS_API_KEY=your_currents_api_key
GROQ_API_KEY=your_groq_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
GEMINI_API_KEY=your_gemini_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=your_database_url
```

---

## 3. Run with Docker

```bash
docker compose up --build
```

This starts the application and PostgreSQL database together.

---

## 4. Run Locally

Install dependencies using `uv`:

```bash
uv sync
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

Run the Telegram bot:

```bash
python -m app.telegram.bot
```

---

# 🧪 Example Usage

### Subscribe to a Topic

```text
/subscribe technology
```

### Remove a Topic

```text
/unsubscribe technology
```

### Request a Digest

```text
/digest
```

### Automated Digest

```text
8:00 AM
   ↓
News Collection
   ↓
Database
   ↓
LLM
   ↓
Telegram
```

---

# 🧠 Key Engineering Decisions

## 1. Central Orchestration

FastAPI acts as the central coordination layer instead of allowing individual external services to communicate directly.

```text
Telegram
    ↕
FastAPI
    ↕
Services
    ↕
External Systems
```

This keeps the application's business logic centralized.

---

## 2. Service Separation

News fetching, article management, topic management, LLM processing, and pipeline orchestration are separated into dedicated services.

This improves:

* maintainability
* readability
* testability
* extensibility

---

## 3. Multi-Provider AI Reliability

The LLM fallback mechanism prevents one provider failure from immediately breaking digest generation.

```text
Primary → Fallback → Final Fallback
```

---

## 4. Persistent State

The database stores not only news articles but also their processing state.

```text
Article
   ↓
Unread
   ↓
Digest Generated
   ↓
Read
```

This allows the system to reason about which content has already been processed.

---

## 5. Reusable Pipeline

Manual and scheduled execution use the same underlying pipeline.

```text
Manual Trigger ───┐
                  ├──→ Common Pipeline
Scheduled Job ────┘
```

This avoids duplicated business logic and keeps both workflows consistent.

---

## 6. LLM Context Control

Only a limited number of recent unread articles are selected per topic before being sent to the LLM.

This helps control:

* prompt size
* token usage
* processing time
* digest length
* context-window limitations

---

# 🔒 Reliability Considerations

Samachar was designed with several external failure points in mind.

```text
                 External Dependencies
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
     News API           LLM            Telegram
        │                │                │
        ▼                ▼                ▼
   Error Handling    Fallbacks       Bot Handling
```

The application therefore avoids assuming that external services will always be available.

---

# 📈 Future Improvements

Possible future improvements include:

* Per-user topic isolation
* More advanced article ranking
* Story-level clustering
* Source credibility scoring
* Redis caching
* Background task queues
* Structured logging
* Metrics and observability
* API authentication
* Horizontal scaling
* More granular notification preferences

---

# 🎓 What Samachar Demonstrates

Samachar demonstrates how to build a backend system that coordinates several independent technologies and external services.

### Backend Engineering

* FastAPI
* REST API design
* Dependency injection
* Service-layer architecture
* Async Telegram handlers

### Database Engineering

* PostgreSQL
* SQLAlchemy ORM
* relational modeling
* many-to-many association tables
* composite primary keys
* unique constraints
* persistent state management

### External Integrations

* News API
* Telegram Bot API
* Multiple LLM providers
* HTTP clients
* API authentication

### AI Engineering

* Prompt engineering
* Structured LLM input
* News summarization
* Multi-provider fallback
* Context-size control

### Reliability

* External API error handling
* LLM fallback
* Duplicate prevention
* Read/unread state
* Reusable processing pipelines

### Infrastructure

* APScheduler
* Docker
* Docker Compose
* Environment-based configuration

---

# 📊 System at a Glance

```text
                           SAMACHAR
                              │
                              ▼
                     ┌─────────────────┐
                     │  Telegram Bot   │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │     FastAPI     │
                     │   Orchestrator  │
                     └────────┬────────┘
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
        ┌─────────┐     ┌───────────┐    ┌───────────┐
        │ News API│     │ PostgreSQL│    │ LLM Layer │
        └────┬────┘     └─────┬─────┘    └─────┬─────┘
             │                │                │
             │                │          ┌─────┼─────┐
             │                │          ▼     ▼     ▼
             │                │        Groq OpenRouter Gemini
             │                │
             └────────────────┼────────────────┘
                              │
                              ▼
                       Digest Generation
                              │
                              ▼
                          Telegram
                              ▲
                              │
                         APScheduler
                           8:00 AM
```

---

# 🚀 Project Outcome

Samachar transforms a collection of independent services into a single automated product:

```text
News API
    +
PostgreSQL
    +
LLM Integration
    +
Telegram Bot
    +
Task Scheduling
    +
Docker
        ↓
Personalized AI News Digest
```

The result is a complete backend workflow that can **collect information, persist state, process it using AI, recover from external LLM failures, and automatically deliver the final result to users**.

---

# 👨‍💻 Author

**Pallav Sharma**

GitHub: [@pallav2712](https://github.com/pallav2712)

---

## 📄 License

This project is developed as a personal backend and portfolio project.
