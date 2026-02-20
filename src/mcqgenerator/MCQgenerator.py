import os
import json
import traceback
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.callbacks.manager import get_openai_callback

# ---------------------------------------------------------------------------
# Environment setup
# ---------------------------------------------------------------------------

load_dotenv()

# ---------------------------------------------------------------------------
# Response template – defines the expected JSON structure for the LLM output
# ---------------------------------------------------------------------------

RESPONSE_JSON = {
    "1": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "2": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "3": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
}

# ---------------------------------------------------------------------------
# Prompt template
# ---------------------------------------------------------------------------

TEMPLATE = """
Text: {text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide.
### RESPONSE_JSON
{response_json}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "tone", "response_json"],
    template=TEMPLATE,
)

# ---------------------------------------------------------------------------
# LLM – routed through OpenRouter so any compatible model can be used
# ---------------------------------------------------------------------------

llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    model="openai/gpt-oss-120b",
)

# ---------------------------------------------------------------------------
# Chain  (LangChain Expression Language)
# ---------------------------------------------------------------------------

quiz_chain = quiz_generation_prompt | llm

# ---------------------------------------------------------------------------
# Public helper
# ---------------------------------------------------------------------------


def generate_evaluate_chain(text: str, number: int, tone: str, response_json: dict):
    """
    Generates MCQs from the supplied *text* using the LLM chain.

    Parameters
    ----------
    text : str
        The source text from which questions should be generated.
    number : int
        How many MCQs to generate.
    tone : str
        Difficulty / tone for the questions, e.g. 'simple', 'medium', 'hard'.
    response_json : dict
        The response-format template passed to the LLM as guidance.

    Returns
    -------
    dict with keys:
        "quiz"              - raw string returned by the LLM
        "total_tokens"      - total tokens consumed
        "prompt_tokens"     - tokens used in the prompt
        "completion_tokens" - tokens used in the completion
        "total_cost"        - estimated USD cost
    """
    try:
        with get_openai_callback() as cb:
            response = quiz_chain.invoke(
                {
                    "text": text,
                    "number": number,
                    "tone": tone,
                    "response_json": json.dumps(response_json),
                }
            )

        # ChatOpenAI returns an AIMessage; extract the string content
        quiz_content = (
            response.content if hasattr(response, "content") else str(response)
        )

        return {
            "quiz": quiz_content,
            "total_tokens": cb.total_tokens,
            "prompt_tokens": cb.prompt_tokens,
            "completion_tokens": cb.completion_tokens,
            "total_cost": cb.total_cost,
        }

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        raise e
