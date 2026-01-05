# Ticket Booking System

Designing a ticket booking system.

## Prerequisites

- Docker + Docker Compose
- Make
- Node.js + npm
- uv (for the backend)

## 1) Start Postgres + Redis locally

Bring up the local containers:

```bash
make docker-run
```

Create the database tables by copying and pasting the SQL scripts from `db/`:

- `db/sql_create_table.sql`
- `db/data_add_query.sql`

## 2) Prepare and run the backend

```bash
cd backend
make install
make dev
```

## 3) Run the UI

```bash
cd ui
npm install
npm run dev
```

