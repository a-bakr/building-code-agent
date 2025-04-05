---
title: "Building Code Agent"
publishedAt: "2025-04-05" # Updated date
summary: "Development of an intelligent agent to assist with building code inquiries, leveraging Retrieval-Augmented Generation (RAG) on specific legal documents like the Egyptian building code."
# website: "" # Add website URL if applicable
images:
    - "/samples/01.png" # Using sample images from the project
    - "/samples/02.png"
team:
    - name: "Abdallah Bakr" # Assuming the same team member
      role: "AI/ML Engineer"
      avatar: "/images/avatar.jpg" # Assuming same avatar path, adjust if needed
      linkedIn: "https://www.linkedin.com/in/abdallah-bakr/" # Assuming same LinkedIn
---

## Overview

Development of an intelligent agent designed to provide answers and guidance related to building codes. This system utilizes Retrieval-Augmented Generation (RAG) techniques, querying specific documents like the Egyptian building law (`docs/egypt_building_law.pdf`) to provide contextually relevant information. It likely features a core agent logic (`agent.py`), a dedicated retriever (`retriever.py`), extensible tools (`tools.py`), and potentially a user interface (`app.py`).

## Key Features (Inferred)

-   **Building Code Querying**: Allows users to ask questions about building regulations and standards.
-   **Retrieval-Augmented Generation (RAG)**: Uses documents in the `docs` folder (e.g., `egypt_building_law.pdf`, `code_ar.txt`, `code_en.txt`) to ground responses in factual information from the provided legal texts.
-   **Extensible Agent Tools**: The `tools.py` file suggests the agent can perform specific actions or use external capabilities beyond simple Q&A.
-   **Potential Web Interface**: `app.py` likely provides a user-friendly interface (e.g., Streamlit, Flask) for interacting with the agent.
-   **Multi-lingual Support (Potential)**: Presence of `code_ar.txt` and `code_en.txt` suggests potential support for Arabic and English queries or documents.

## Technologies Used (Inferred)

-   **Python**: Core programming language.
-   **LangChain (Likely)**: Often used for building RAG agents and orchestrating AI workflows. (Confirm based on `requirements.txt` if possible)
-   **Vector Database (Likely)**: For efficient document retrieval in the RAG process (e.g., FAISS, ChromaDB). (Confirm based on `requirements.txt` or `retriever.py`)
-   **LLM (Likely)**: A Large Language Model (e.g., OpenAI GPT, Google Gemini, local models) to power the agent's understanding and generation. (Configured via `.env`)
-   **Streamlit/Flask (Potential)**: For the web application interface (`app.py`).
-   **Jupyter Notebook (`play.ipynb`)**: For development, testing, and experimentation.

## Challenges and Learnings (Potential)

-   Ensuring accurate retrieval from dense legal documents like building codes.
-   Handling ambiguity in user queries related to complex regulations.
-   Integrating the retriever effectively with the LLM for accurate and relevant answers.
-   Optimizing the RAG pipeline for performance and cost.
-   Developing an intuitive interface (`app.py`) for complex queries.

## Outcome (Goal)

The Building Code Agent aims to be a reliable tool for architects, engineers, contractors, and homeowners to quickly find accurate information about building regulations based on specific legal documents. It simplifies the process of navigating complex codes by providing direct answers grounded in the source material.
