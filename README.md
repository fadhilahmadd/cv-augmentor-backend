# CV Augmentor: AI Multi-Agent System

CV Augmentor is an intelligent system designed to assist technical recruiters by providing a deep, data-driven analysis of a candidate's CV. It goes beyond simple keyword matching to identify a candidate's true potential, perform a skill-gap analysis against current market demands, and propose a personalized upskilling path.

This system leverages a multi-agent workflow orchestrated by LangGraph, with a robust FastAPI backend, to transform a raw CV into an actionable intelligence report.

-----

## 🏗️ Architectural Overview

The application is built on a clean, scalable architecture with a clear separation of concerns:

1.  **FastAPI Backend**: A high-performance web server that exposes a REST API. It handles incoming requests, manages validation and error handling, and serves as the entry point to the system.
2.  **LangGraph Core**: The engine of the application. It's a state machine that orchestrates a workflow of specialized AI agents, ensuring data flows logically from one step to the next.

### The Agent Workflow

The system processes a CV through a sequence of four specialized agents:

  * **1. CV Parsing & Normalization Agent**: Ingests the raw CV text and parses it into a structured JSON format.
  * **2. Specialized Skill Analyst Agent**: Analyzes the structured data to identify both explicit and implicit technical and soft skills.
  * **3. Market Intelligence Agent**: Uses a search tool to research current market demands and in-demand skills for the specified job role.
  * **4. Recommendation & Report Agent**: Synthesizes all the gathered information to generate the final, comprehensive report in Markdown format.

-----

## ✨ Key Features

  * **Deep CV Analysis**: Extracts and structures information from raw CV text.
  * **Implicit Skill Detection**: Infers skills from project descriptions and experience.
  * **Real-time Market Intelligence**: Queries the web for up-to-date skill requirements.
  * **Automated Skill-Gap Reporting**: Generates a detailed report comparing the candidate's skills to market demands.
  * **Personalized Upskilling Plans**: Provides actionable recommendations for candidate development.
  * **Robust API**: Built with FastAPI, including automated validation and professional error handling.
  * **Scalable Codebase**: Features a modular structure, centralized configuration, and global handlers for easy maintenance and expansion.

-----

## ⚙️ Setup and Installation

Follow these steps to set up and run the project locally.

### 1\. Prerequisites

  * Python 3.9+
  * An active Google API Key with the Gemini API enabled.
  * A Tavily API Key for the search tool.

### 2\. Clone the Repository

```bash
git clone https://github.com/fadhilahmadd/cv-augmentor-backend.git
cd cv-augmentor-backend
```

### 3\. Set Up a Virtual Environment

It's highly recommended to use a virtual environment.

```bash
# Create the virtual environment
python -m venv venv

# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

### 4\. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5\. Configure Environment Variables

Create a file named `.env` in the root of the project and add your API keys.

```ini
# Get from Google AI Studio
GOOGLE_API_KEY="AIza..."

# Get from Tavily AI
TAVILY_API_KEY="tvly-..."
```

**If you need a service account key file**

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/ee-email1-sa.json
```

-----

## 🚀 How to Run

With your virtual environment activated, start the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. The `--reload` flag will automatically restart the server when you make code changes.

-----

## 🔌 API Usage

You can interact with the API using the automatically generated documentation or by sending a request directly.

  * **Interactive Docs (Swagger UI)**: Navigate to `http://127.0.0.1:8000/docs` in your browser.

### Endpoint: `POST /api/v1/analysis`

This is the main endpoint for submitting a CV for analysis.

#### Request Body

The endpoint expects a JSON body with the following structure:

```json
{
  "cv_text": "The full text content of the candidate's CV...",
  "job_role": "The target job role, e.g., Senior AI Engineer"
}
```

#### Example `curl` Command

```bash
curl -X POST "http://127.0.0.1:8000/api/analysis" \
-H "Content-Type: application/json" \
-d '{
  "cv_text": "John Doe\nAI Engineer\njohn.doe@email.com...",
  "job_role": "Senior AI Engineer"
}'
```
