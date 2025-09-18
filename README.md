# CV Augmentor: AI Multi-Agent System

CV Augmentor is an intelligent system designed to assist technical recruiters by providing a deep, data-driven analysis of a candidate's CV. It goes beyond simple keyword matching to identify a candidate's true potential, perform a skill-gap analysis against current market demands, and propose a personalized upskilling path.

This system leverages a multi-agent workflow orchestrated by LangGraph, with a robust FastAPI backend and a persistent PostgreSQL database, to transform raw CVs into actionable intelligence reports.

-----

## 🏗️ Architectural Overview

The application is built on a clean, scalable architecture with a clear separation of concerns:

1.  **FastAPI Backend**: A high-performance web server that exposes a REST API. It handles incoming requests, manages validation and error handling, and serves as the entry point to the system.
2.  **PostgreSQL Database**: Provides a persistent and robust storage solution for all analysis jobs and their results, managed via SQLAlchemy.
3.  **LangGraph Core**: The engine of the application. It's a state machine that orchestrates a workflow of specialized AI agents, ensuring data flows logically from one step to the next.

### The Agent Workflow

The system processes a CV through a sequence of four specialized agents:

  * **1. CV Parsing & Normalization Agent**: Ingests the raw CV text and parses it into a structured JSON format.
  * **2. Specialized Skill Analyst Agent**: Analyzes the structured data to identify both explicit and implicit technical skills.
  * **3. Market Intelligence Agent**: Uses a search tool to research current market demands and in-demand skills for the specified job role.
  * **4. Recommendation & Report Agent**: Synthesizes all the gathered information to generate the final, comprehensive report in Markdown format.

-----

## ✨ Key Features

  * **Deep CV Analysis**: Extracts and structures information from raw CV text.
  * **Implicit Skill Detection**: Infers skills from project descriptions and experience.
  * **Real-time Market Intelligence**: Queries the web for up-to-date skill requirements.
  * **Asynchronous Job Processing**: Handles multiple requests concurrently without blocking, ideal for long-running analyses.
  * **Batch & Single File Uploads**: Supports both single CV text input and batch uploads of multiple `.txt` files.
  * **Persistent Job Storage**: All jobs and results are stored securely in a PostgreSQL database.
  * **Downloadable Results**: Provides endpoints to download individual reports or a ZIP archive of an entire batch.
  * **Production-Ready**: Includes a full Docker and Docker Compose setup for easy and reliable deployment.

-----

## 🚀 How to Run

You can run the application using Docker (recommended for ease of use) or set it up locally.

### Option 1: Docker Setup (Recommended)

This is the simplest and most reliable way to get started.

1.  **Prerequisites**: Docker and Docker Compose must be installed.
2.  **Configure Environment**: Copy the `example.env` file to a new file named `.env` and fill in your `GOOGLE_API_KEY` and `TAVILY_API_KEY`. The database credentials in this file are pre-configured to work with Docker Compose.
3.  **Build and Run**: From the project's root directory, run the following command:
    ```bash
    docker-compose up --build
    ```
    This command will build the API image, start the PostgreSQL database container, and run your application. The API will be available at `http://localhost:8000`.

### Option 2: Local Setup

1.  **Prerequisites**:
      * Python 3.9+
      * A running PostgreSQL server.
2.  **Set Up Virtual Environment & Install Dependencies**:
    ```bash
    # Create the virtual environment
    python -m venv venv

    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    .\venv\Scripts\activate

    pip install -r requirements.txt
    ```

    **If you need a service account key file**

    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS=/path/to/ee-email1-sa.json
    ```

3.  **Configure Environment Variables**: Create a `.env` file and fill in your API keys and the connection details for your local PostgreSQL server.
4.  **Run the Application**:
    ```bash
    uvicorn app.main:app --reload
    ```
5. **Configure Authentication**

    This application supports two methods for authenticating with Google Cloud APIs.

    **Method 1: API Key (Recommended for Local Development)**

    Add your `GOOGLE_API_KEY` to the `.env` file.

    ```ini
    GOOGLE_API_KEY="AIza..."
    ````

    **Method 2: Service Account (Recommended for Production/Docker)**

    1.  Place your service account JSON key file in the root of the project (e.g., `ee-email1-sa.json`).
    2.  The `docker-compose.yml` file is pre-configured to mount this file and use it for authentication when you run `docker-compose up`.
    3.  **Important**: Ensure your service account key file (`*.json`) is listed in your `.gitignore` file.

-----

## 🔌 API Usage

The API is asynchronous. You first submit a job and then use the returned `job_id` to check the status and retrieve the result.

  * **Interactive Docs (Swagger UI)**: Navigate to `http://127.0.0.1:8000/docs` in your browser.

### Step 1: Submit a Job

You can submit a single CV as text or upload a batch of `.txt` files.

  * **Endpoint for Text Input**: `POST /api/analyze/text`
  * **Endpoint for File Uploads**: `POST /api/analyze/batch`

### Step 2: Check Job Status

Use the `job_id` from the previous step to poll this endpoint until the status is `completed`.

  * **Endpoint**: `GET /api/analyze/status/{job_id}`

### Step 3: Download Results

Once a job is complete, you can download the report(s).

  * **Download a single report**: `GET /api/analyze/result/{job_id}`
  * **Download all reports from a batch**: `GET /api/analyze/results/all/{batch_id}`