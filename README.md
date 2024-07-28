# Python-fastapi
## 🌟 Introduction

This project implements a sophisticated FastAPI server with two powerful endpoints:

1. **Retrieval-Augmented Generation (RAG)**: Get tailored responses and relevant articles based on your mental health queries.
2. **Text Classification**: Classify texts to determine whether they might indicate suicidal thoughts.

## 🚀 Quick Start Guide

### Clone the Repository

Begin by cloning the repository to your local development environment:

```bash
git clone https://github.com/ChintanD2205/Python-fastapi.git
cd Python-fastap
```

### Setup the Environment

Create a virtual environment and activate it:

```bash
python -m venv infiheal_venv
infiheal_venv\Scripts\activate
```

Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

#### Locally

To run the FastAPI server locally, execute:

```bash
uvicorn main:app --reload
```

Access the running server at [http://localhost:8000](http://localhost:8000).

#### Docker Deployment

For containerized deployment with Docker:

1. Build the Docker image:

   ```bash
   docker build -t Python-fastapi .
   ```

2. Start the Docker container:

   ```bash
   docker run -p 8000:8000 Python-fastapi
   ```

The application will be available at [http://localhost:8000](http://localhost:8000).

## 🛠️ API Endpoints

### **/rag** - Retrieval-Augmented Generation

- **Method:** `POST`
- **Description:** Provides a helpful response and suggests relevant articles based on your mental health inquiry.
- **Request Payload:** 
  ```json
  {
    "query": "Your mental health question here"
  }
  ```
- **Response Format:**
  ```json
  {
    "response": "Generated response text",
    "relevant_articles": ["URL1", "URL2", ...]
  }
  ```

### **/classification** - Text Classification

- **Method:** `POST`
- **Description:** Analyzes the text and classifies it to indicate potential suicidal ideation.
- **Request Payload:** 
  ```json
  {
    "query": "Text to classify"
  }
  ```
- **Response Format:**
  ```json
  {
    "response": "Classification result (e.g., 'Suicidal', 'Not Suicidal')"
  }
  ```

## 🧪 Testing the API

You can use tools like `curl` or Postman to test the endpoints:

#### Test the RAG Endpoint

```bash
curl -X POST "http://localhost:8000/rag" -H "Content-Type: application/json" -d '{"query":"I'm feeling overwhelmed"}'
```

#### Test the Classification Endpoint

```bash
curl -X POST "http://localhost:8000/classification" -H "Content-Type: application/json" -d '{"query":"I'm feeling very low and hopeless"}'
```

## 📦 Additional Information

- **Python Version:** Requires Python 3.9 or higher.
- **Dependencies:** Managed through `requirements.txt`.
- **Docker Support:** For a containerized environment, ensure Docker is installed.

For any questions or issues, please raise them in the GitHub repository.
