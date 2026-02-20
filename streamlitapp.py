import json
import traceback

import pandas as pd
import streamlit as st
from langchain_community.callbacks.manager import get_openai_callback

from src.mcqgenerator.MCQgenerator import RESPONSE_JSON, generate_evaluate_chain
from src.mcqgenerator.utils import get_table_data, read_file

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(page_title="MCQ Generator", page_icon="📝", layout="centered")
st.title("📝 MCQ Generator with LangChain")
st.markdown(
    "Upload a **PDF** or **TXT** file and generate multiple-choice questions automatically."
)

# ---------------------------------------------------------------------------
# Input form
# ---------------------------------------------------------------------------

with st.form("mcq_form"):
    uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

    col1, col2 = st.columns(2)

    with col1:
        mcq_count = st.number_input(
            "Number of MCQs",
            min_value=3,
            max_value=50,
            value=5,
            step=1,
        )

    with col2:
        tone = st.selectbox(
            "Complexity / Tone",
            options=["Simple", "Medium", "Hard"],
            index=1,
        )

    submitted = st.form_submit_button("Generate MCQs")

# ---------------------------------------------------------------------------
# Generation logic
# ---------------------------------------------------------------------------

if submitted:
    if uploaded_file is None:
        st.error("Please upload a PDF or TXT file before generating.")
    else:
        with st.spinner("Generating MCQs… this may take a moment."):
            try:
                text = read_file(uploaded_file)

                result = generate_evaluate_chain(
                    text=text,
                    number=int(mcq_count),
                    tone=tone,
                    response_json=RESPONSE_JSON,
                )

                quiz_str = result.get("quiz", "")

                # The LLM sometimes wraps the JSON inside a markdown code block –
                # strip it if present.
                if "```" in quiz_str:
                    quiz_str = quiz_str.split("```")[1]
                    if quiz_str.startswith("json"):
                        quiz_str = quiz_str[4:]

                # ---------------------------------------------------------------
                # Token / cost summary
                # ---------------------------------------------------------------
                st.subheader("Usage Summary")
                usage_cols = st.columns(4)
                usage_cols[0].metric("Total tokens", result["total_tokens"])
                usage_cols[1].metric("Prompt tokens", result["prompt_tokens"])
                usage_cols[2].metric("Completion tokens", result["completion_tokens"])
                usage_cols[3].metric("Estimated cost", f"${result['total_cost']:.5f}")

                # ---------------------------------------------------------------
                # Quiz table
                # ---------------------------------------------------------------
                table_data = get_table_data(quiz_str)

                if table_data and isinstance(table_data, list):
                    st.subheader("Generated Quiz")
                    df = pd.DataFrame(table_data)
                    st.table(df)
                else:
                    st.warning("Could not parse the quiz. Raw LLM output shown below.")
                    st.code(quiz_str, language="json")

            except Exception as e:
                traceback.print_exc()
                st.error(f"An error occurred: {e}")
