# AI-Powered Pharma CRM Assistant

An AI-powered CRM assistant for pharmaceutical sales representatives that automates interaction logging using natural language. Users can describe a meeting in plain English, and the AI extracts structured information to automatically populate the CRM form before saving it to the database.

---

## Features

- 🤖 AI-powered interaction extraction using LangGraph + LLM
- 📝 Auto-fills CRM interaction form from natural language
- 👨‍⚕️ Automatic Healthcare Professional (HCP) matching
- 📅 Auto-extracts date, time, attendees, meeting type, discussion and summary
- 💾 Save interactions to PostgreSQL database
- 🔍 Search and manage HCP records
- ⚡ FastAPI backend with React frontend
- 🎯 Tool-calling architecture for reliable structured outputs

---

## Tech Stack

### Frontend

- React
- Redux Toolkit
- React Select
- Axios
- Tailwind CSS

### Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- LangGraph
- LangChain
- Groq LLM

---

## Project Architecture

```
User
   │
   ▼
React Frontend
   │
   ▼
FastAPI Backend
   │
   ▼
LangGraph Agent
   │
   ▼
Groq LLM
   │
   ▼
Tool Calls
   │
   ├── Extract Interaction
   ├── Search HCP
   └── Save Interaction
   │
   ▼
PostgreSQL Database
```

---

## Workflow

1. User describes an interaction in natural language.
2. AI extracts:
   - HCP Name
   - Meeting Type
   - Date
   - Time
   - Attendees
   - Discussion
   - Summary
3. Frontend automatically populates the interaction form.
4. User reviews the information.
5. Interaction is saved into PostgreSQL.

---

## Example

### User Input

```
Met Dr. Rahul Mehta today at 10:30 AM over Zoom with Jane Smith. Discussed the efficacy of Prodo-X and he requested a follow-up next month.
```

### AI Extracts

```
HCP: Dr. Rahul Mehta
Meeting Type: Virtual
Date: Today's Date
Time: 10:30 AM
Attendees: Dr. Rahul Mehta, Jane Smith
Discussion: Discussed the efficacy of Prodo-X
Summary: Positive response, requested follow-up next month
```

The interaction form is automatically populated for user review before saving.

---

## Folder Structure

```
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── api/
│   ├── features/
│   └── store/

backend/
├── api/
├── models/
├── schemas/
├── database/
├── langgraph/
├── tools/
└── main.py
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd ai-pharma-crm
```

---

### Backend

```bash
cd backend

python -m venv venv

source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload
```

---

### Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## Environment Variables

Backend `.env`

```
DATABASE_URL=your_database_url

GROQ_API_KEY=your_groq_api_key

MODEL_NAME=llama-3.1-8b-instant
```

---

## API Endpoints

### Chat

```
POST /api/chat
```

Uses the AI agent to extract interaction details.

---

### Healthcare Professionals

```
GET /api/hcps
```

Returns all HCP records.

---

### Interactions

```
POST /api/interactions
```

Stores an interaction in the database.

---

## Future Improvements

- Voice interaction logging
- Authentication & authorization
- Material/sample tracking
- Calendar integration
- AI-generated follow-up recommendations
- Dashboard analytics
- Advanced HCP search

---

## Author

**Vishmitha Poojary**

MCA Student | Full Stack & AI Developer
