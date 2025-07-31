---
title: building-code-agent
app_file: app.py
sdk: flask
sdk_version: 3.0.0
---
# Building Code Agent

## Description

This project implements an agent designed to assist with building codes, leveraging retrieval-augmented generation (RAG) based on provided documents (like the Egyptian building law found in the `docs` folder). The application features a Flask web interface for easy interaction with the building code assistant.

## Features

*   Web-based interface using Flask for building code queries
*   Agent-based interaction for answering building code questions
*   Image analysis of architectural plans
*   Retrieval-Augmented Generation (RAG) using documents in the `docs` directory
*   Support for English and Arabic queries

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd building-code-agent
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up environment variables:**
    Copy `.env.example` to `.env` and fill in the required values.
    ```bash
    cp .env.example .env
    # Edit .env with your specific configurations
    ```

## Usage

Run the Flask application:

```bash
python app.py
```

Then open your web browser and navigate to:
```
http://localhost:5000
```

The application will allow you to:
1. Upload an architectural plan image
2. Ask questions about building codes related to the plan
3. View the analysis results, extracted text, and relevant building codes

## Project Structure

```
.
├── .env.example        # Example environment variables
├── .env                # Environment variables (create from .env.example)
├── .gitignore          # Git ignore file
├── app.py              # Main Flask application
├── building-code-agent.md # Project notes/documentation
├── README.md           # This file
├── requirements.txt    # Python dependencies
├── uploads/            # Temporary folder for uploaded images
├── core/               # Core components
│   ├── __init__.py     # Module exports
│   ├── agent.py        # Core agent logic
│   ├── text_extraction.py # Text extraction from images
│   └── retriever.py    # Building code retriever component
├── docs/               # Documentation/data for RAG
│   ├── code_ar.json
│   ├── code_ar.txt
│   ├── code_en.txt
│   ├── code_genral.txt
│   └── egypt_building_law.pdf
├── static/             # Static files for web interface
│   ├── css/            # CSS stylesheets
│   ├── js/             # JavaScript files
│   └── samples/        # Sample images
└── templates/          # HTML templates
    └── index.html      # Main application template
```

## Dependencies

Key dependencies are listed in `requirements.txt`:
- Flask - Web framework
- LangChain - For agent construction and RAG
- OpenAI/Google Generative AI - For LLM capabilities
- Pillow - For image processing
- python-dotenv - For environment variables
- Chromadb - For vector storage

## API Endpoints

- `GET /` - Main web interface
- `POST /api/process` - Processes uploaded images and queries about building codes
- `GET /samples/<sample>` - Serves sample images for examples

---

*Note: Please ensure you have appropriate API keys configured in your .env file for the LLM services used in this application.*
