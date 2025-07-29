import os
import sys
import json
import traceback
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import ast  # ✅ Needed to safely parse Python-like dict

# ✅ Set up import path early
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# ✅ Import after fixing sys.path
from mcqgenerator.logger import logging
from mcqgenerator.utils import read_file, get_data
from mcqgenerator.MCQ_Generator import generate_evaluate_chain
from langchain.callbacks import get_openai_callback

# ✅ Load environment variables
load_dotenv()

# ✅ Load JSON config
with open(r'C:\Users\UPASHAK GAYEN\OneDrive\Desktop\mcqgen\Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

# ✅ Streamlit UI
st.title("MCQ Generator Application with LangChain")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or txt file", type=["txt", "pdf"])
    mcq_count = st.number_input("Number of MCQs to generate", min_value=1, max_value=5)
    mcq_subject = st.text_input("Subject of the MCQs", max_chars=20)
    mcq_tone = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])
    button = st.form_submit_button("Generate MCQs")

    if button and uploaded_file is not None and mcq_count and mcq_subject and mcq_tone:
        with st.spinner("Generating MCQs..."):
            try:
                text = read_file(uploaded_file)
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain({
                        "text": text,
                        "number": mcq_count,
                        "subject": mcq_subject,
                        "tone": mcq_tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    })

                # ✅ Show token usage
                st.text(f"Total tokens used: {cb.total_tokens}")
                st.text(f"Prompt tokens used: {cb.prompt_tokens}")
                st.text(f"Completion tokens used: {cb.completion_tokens}")
                st.text(f"Total cost: ${cb.total_cost:.4f}")

                # ✅ Handle response and quiz display
                if isinstance(response, dict):
                    quiz_raw = response.get("quiz")
                    st.write("🔍 Full response:", response)
                    if quiz_raw and "RESPONSE_JSON" in quiz_raw:
                        quiz_str = quiz_raw.replace("###RESPONE_JSON", "").strip()
                        try:
                            parsed_quiz = ast.literal_eval(quiz_str)  # ✅ Convert string to dict
                            table_data = get_data(parsed_quiz)
                            if table_data:
                                df = pd.DataFrame(table_data)
                                df.index = df.index + 1
                                st.table(df)
                                st.text_area(label="📌 Review", value=response.get("review", "No review found"), height=150)
                            else:
                                st.error("⚠️ Could not parse MCQs from response.")
                        except Exception as e:
                            st.error(f"⚠️ Failed to parse quiz: {e}")
                    else:
                        st.warning("⚠️ No quiz data found in response.")
                else:
                    st.write("⚠️ Response is not a dictionary:", response)

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error(f"An error occurred: {e}")
