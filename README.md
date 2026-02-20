# MCQ Generator with LangChain

A Streamlit web application that automatically generates multiple-choice questions (MCQs) from any PDF or TXT file using LangChain and an OpenAI-compatible LLM via OpenRouter.

## Features

- Upload a **PDF** or **TXT** file as the source text
- Choose the **number of MCQs** to generate (3–50)
- Select the **complexity/tone**: Simple, Medium, or Hard
- Displays a formatted question table with correct answers
- Shows token usage and estimated cost per generation

## Project Structure

```
MCQ/
├── src/
│   └── mcqgenerator/
│       ├── MCQgenerator.py   # LLM chain & generation logic
│       ├── utils.py          # File reading & table helpers
│       └── logger.py         # Logging configuration
├── experiment/
│   └── test.ipynb            # Exploratory notebook
├── streamlitapp.py           # Streamlit frontend
├── setup.py
├── requirements.txt
├── response.json             # Example response JSON structure
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/mcq-generator.git
cd mcq-generator
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```
OPENAI_API_KEY=your_openrouter_api_key_here
```

> Get a free OpenRouter API key at https://openrouter.ai

### 5. Run the app

```bash
streamlit run streamlitapp.py
```

## Requirements

See [requirements.txt](requirements.txt) for the full list. Key dependencies:

| Package | Purpose |
|---|---|
| `langchain` | LLM orchestration |
| `langchain-openai` | OpenAI-compatible LLM client |
| `langchain-community` | Community integrations & callbacks |
| `openai` | OpenAI SDK |
| `streamlit` | Web UI |
| `PyPDF2` | PDF text extraction |
| `python-dotenv` | `.env` file loading |

## License

MIT
