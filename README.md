# Discord Admin Dashboard

## Features

- Discord OAuth Login
- Dynamic Guild Fetching
- Config Management Dashboard
- Protected Admin Routes
- Dynamic Channel Dropdown Architecture
- Scraper Integration Ready
- Django ORM Persistence
- Message Storage System

## Current Architecture

Discord OAuth
↓
Django Dashboard
↓
ChannelConfig Database
↓
Integrated Scraper Layer
↓
FetchedMessage Database
↓
Dashboard/API Layer

## Tech Stack

- Django
- Discord OAuth2
- discord.py-self
- Playwright
- SQLite
- HTML/CSS/JavaScript

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


---

# PART 4 — UPDATE `.env.example`

Replace with:

```env id="r1k5wc"
SECRET_KEY=

DEBUG=

DISCORD_CLIENT_ID=

DISCORD_CLIENT_SECRET=

DISCORD_REDIRECT_URI=

DISCORD_USER_TOKEN=

EMAIL=

PASSWORD=