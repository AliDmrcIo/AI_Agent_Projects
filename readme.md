# Step-by-Step AI Agent Development with LangChain

This repository contains a series of Python projects that guide you from the basics to advanced levels of creating AI agents using the LangChain library. The projects start with a simple LLM call and progressively introduce modern AI concepts such as tool usage, memory management, structured outputs, Retrieval-Augmented Generation (RAG), and using local (on-premise) models.

## Core Concepts Covered

- **Basic LLM Integration**: Using the Google Gemini model with LangChain.
- **Prompt Templating**: Creating dynamic and reusable prompts.
- **Agents and Tool Usage**: Giving LLMs external capabilities, like a calculator.
- **Memory**: Adding the ability for agents to remember conversation history.
- **Output Parsers**: Converting responses from LLMs into structured formats like JSON.
- **API Integration**: Connecting agents to external world APIs (e.g., for currency exchange rates).
- **Retrieval-Augmented Generation (RAG)**:
    - Generating responses by retrieving information from a text (`.txt`) file.
    - Generating responses by retrieving information from a database (`SQLite`).
- **Local LLM Usage**: Using local models like LLaMA (via Ollama) on your own machine instead of cloud-based models like Gemini.
- **Real-World Project**: Developing a system that classifies customer complaints, routes them to the appropriate department, generates responses using a RAG-powered knowledge base, and reports the results to an Excel file.

## ⚙️ Setup and Getting Started

Follow these steps to run the projects:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/AliDmrcIo/AI_Agent_Projects.git
    cd AI_Agent_Projects
    ```

2.  **Activate the Virtual Environment:**
    This project includes a `venv` virtual environment. First, activate this environment.
    ```bash
    # For Windows
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies (or Create `requirements.txt`):**
    Before sharing your project, it is recommended to create a `requirements.txt` file so others can easily install the dependencies. You can create this file by running the following command while your virtual environment is active:
    ```bash
    pip freeze > requirements.txt
    ```
    After that, anyone who clones the project can install all the libraries with the following command:
    ```bash
    pip install -r requirements.txt
    ```
    
4.  **Create Your `.env` File:**
    Create a file named `.env` in the project's root directory. Add your Gemini API key in the following format:
    ```
    GEMINI_API_KEY="AIzaSy...YOUR_API_KEY"
    ```

5.  **Create the Database:**
    To create the SQLite database for projects 12 and 13, run the following script:
    ```bash
    python 12_db.py
    ```

6.  **Install Ollama for Local LLM:**
    To run the `13_sikayet_siniflandirma_ve_rag_db_LLaMA.py` project, you need to have [Ollama](https://ollama.com/) installed on your system and the `llama3.2:3b` model downloaded.
    ```bash
    ollama pull llama3.2:3b
    ```

## 📁 Project Files and Descriptions

---

### Part 1: LangChain Fundamentals

-   **`1_langchain_openai_giris.py`**: The most basic "Hello World" application with LangChain and Gemini. It shows how to ask a question to an LLM and get a response.
-   **`2_prompt_template.py`**: Teaches how to dynamically insert user input into a template using `PromptTemplate`.
-   **`5_output_parser.py`**: Shows how to convert a text-based response from an LLM into a structured JSON object (e.g., product name, price, category) using `Pydantic`.

### Part 2: Agents and Tools

-   **`3_agent_tool_kullanimi.py`**: An introduction to the concept of agents. The LLM is given `addition`, `multiplication`, and `division` tools to perform mathematical operations. The agent selects and uses the correct tool based on the user's question.
-   **`4_agent_memory.py`**: Adds **memory** to the previous project. The agent can now understand commands like "multiply the result of the previous operation by 5" because it remembers the conversation history.
-   **`6_langchain_agent_comparison.py`**: Compares how different Agent behaviors (ReAct vs. Structured) can be simulated by changing the model and `temperature` settings.
-   **`7_agent_with_api.py`**: Gives the agent the ability to communicate with the outside world. A tool is created that fetches real-time currency exchange rates from an API to provide an answer.
-   **`8_multi_step_agents.py`**: **(Legacy Version Incompatibility)** Introduces the "Plan and Execute" agent structure for multi-step tasks. Note: This script may not work due to incompatibilities with recent LangChain versions but is included to demonstrate the concept.

### Part 3: Customer Complaint Management Project (Step-by-Step Development)

This section demonstrates how a single project idea is progressively enhanced with more capabilities.

-   **`9_sikayet_siniflandirma_projesi.py`**: The first step of the project. It takes a user complaint and uses an LLM to classify it into a `category`, the `unit to be routed to`, and a `response to the customer`.
-   **`10_sikayet_siniflandirma_2.py`**: Adds **Excel reporting** functionality to project 9. Each complaint is saved to an `sikayet_raporu.xlsx` file with a timestamp.
-   **`11_sikayet_siniflandirma_ve_rag.py`**: Adds **RAG (Retrieval-Augmented Generation)** to the project. The agent now utilizes a knowledge base from the `11_icin_rag_veriler.txt` file when responding to the customer, resulting in more accurate and context-aware answers.
-   **`12_sikayet_siniflandirma_ve_rag_db.py`**: The RAG's data source is moved from a `.txt` file to an **SQLite database**. This provides a more scalable and manageable knowledge base. The `12_db.py` script creates this database.
-   **`13_sikayet_siniflandirma_ve_rag_db_LLaMA.py`**: The final version of the project. The entire system is updated to run with a **local (on-premise) LLaMA model** instead of the cloud-based Gemini, ensuring data privacy and eliminating API costs.
