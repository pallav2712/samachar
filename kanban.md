## Backlog / To Do

### M-11: Provider Selection & Setup

  - tags: [Phase-1]
  - defaultExpanded: false
  - steps:
      - [x] Research and select a free News API provider (e.g., NewsAPI, GNews, MediaStack). Generate API keys.
      - [x] Research and select a free/freemium LLM provider (e.g., Google Gemini API, Groq, or OpenAI free tier). Generate API keys.
      - [x] Use Telegram's "BotFather" to create a new bot and obtain your Bot Token.

### M-12: Environment Setup

  - tags: [Phase-1]
  - defaultExpanded: false
  - steps:
      - [ ] Install Python and set up a virtual environment.
      - [ ] Initialize a Git repository and create a .gitignore file to hide API keys and environment variables.
      - [ ] Create an environment variable file to securely store your API keys, database credentials, and bot token.

### M-13: Hello World Backend

  - tags: [Phase-1]
  - defaultExpanded: false
  - steps:
      - [ ] Install FastAPI and an ASGI server (like Uvicorn).
      - [ ] Structure your project folders (e.g., separate directories for routes, database, services).
      - [ ] Create a basic health-check endpoint that returns a simple success message.
      - [ ] Run the server and verify it works.

### M-21: PostgreSQL Setup & Schema

  - tags: [Phase-2]
  - defaultExpanded: false
  - steps:
      - [ ] Install PostgreSQL on your local machine and create a new database for Samachar.
      - [ ] Design two tables: topics (to store user-subscribed topics) and articles (to store headlines, URLs, content, and fetch dates).
      - [ ] Install an ORM (like SQLAlchemy) or a database driver.
      - [ ] Write the database connection logic and create the tables.

### M-22: News API Integration

  - tags: [Phase-2]
  - defaultExpanded: false
  - steps:
      - [ ] Write a service module to communicate with your chosen News API.
      - [ ] Create functions to fetch "General News" and "Topic-Specific News".
      - [ ] Implement error handling for failed API requests or empty results.

### M-23: Data Pipeline

  - tags: [Phase-2]
  - defaultExpanded: false
  - steps:
      - [ ] Combine the Database and News modules.
      - [ ] Write logic that checks the DB for user topics, fetches the relevant news, and saves the fetched articles into the articles table, avoiding duplicates.
      - [ ] Create a temporary FastAPI endpoint to manually trigger and test this pipeline.

### M-31: LLM Integration

  - tags: [Phase-3]
  - defaultExpanded: false
  - steps:
      - [ ] Write a service module to communicate with your chosen LLM API.
      - [ ] Design a prompt that takes raw article data and asks the AI to output a concise, bulleted, and readable morning digest.
      - [ ] Create a function that retrieves today's unread articles from the DB, passes them to the LLM, and returns the formatted summary.

### M-32: Telegram Bot Basics

  - tags: [Phase-3]
  - defaultExpanded: false
  - steps:
      - [ ] Install a Telegram Bot wrapper library.
      - [ ] Set up a polling mechanism (easier for beginners than webhooks) to listen for messages.
      - [ ] Implement basic commands: /start (welcome message) and /help (list of available commands).

### M-33: Interactive Commands & Wiring

  - tags: [Phase-3]
  - defaultExpanded: false
  - steps:
      - [ ] Implement /subscribe [topic] and /unsubscribe [topic]. Wire these commands to update your PostgreSQL database.
      - [ ] Implement the /digest command. Wire this so that when the user types it, the bot triggers the News Fetcher -> triggers the LLM Summarizer -> sends the final text back as a Telegram message.

### M-41: Task Scheduling

  - tags: [Phase-4]
  - defaultExpanded: false
  - steps:
      - [ ] Install a lightweight scheduling library (like APScheduler).
      - [ ] Configure a job that runs every day at 8:00 AM your local time.
      - [ ] Point this job to the exact same pipeline used by the /digest command (Fetch -> Summarize -> Send to Telegram).

### M-42: Dockerization

  - tags: [Phase-4]
  - defaultExpanded: false
  - steps:
      - [ ] Write a Dockerfile that dictates how to build your FastAPI application.
      - [ ] Write a docker-compose.yml file that defines two services: your backend app and the PostgreSQL database. Include volume mapping for the database so data isn't lost when the container restarts.
      - [ ] Write a comprehensive README documenting the project, how to add API keys, and how to start the application.

## In Progress

## Review & Test

## Done



