import os 
import json
import traceback
import pandas as pd

from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_data
from mcqgenerator.logger import logging

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain

load_dotenv()
key=os.getenv("OPENAI_API_KEY")

llm=ChatOpenAI( openai_api_key=key,model_name="",temperature=0.5)

TEMPLATE = """

TEXT : {text}

You are an expert MCQ creator.Given the above text,it is your job to create a quiz of {number} multiple choice question for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well. Make sure to format your response like RESPONSE_JSON below and use it as a guide. Ensure to make {number} MCQs
###RESPONE_JSON
{response_json}

"""

quiz_generating_prompt=PromptTemplate(input_variables=["text","number","subject","tone","response_json"],
                                      template=TEMPLATE
                                      )

quiz_chain=LLMChain(llm=llm,
                    prompt=quiz_generating_prompt,
                    output_key="quiz",
                    verbose=False )

TEMPLATE2 = """
You are an expert grammarian and educational reviewer.Given the following MCQ quiz for {subject} students.Ypu need to evaluate  the complexity of  the question and give a complete analysis of the quiz.Onlye use at max 50 words for complexity.
if the quiz is not at per with the cognative and analytical of the student,update the quiz question which needs to be changed the tone that us perfectly fits the student ability.
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""
quiz_evaluating_prompt=PromptTemplate(input_variables=["quiz","subject"],
                                      template=TEMPLATE2)

review_chain=LLMChain(llm=llm,
                      prompt=quiz_evaluating_prompt,
                      output_key="review",
                      verbose=False)

generate_evaluate_chain=SequentialChain(chains=[quiz_chain,review_chain],
                                        input_variables=["text","number","subject","tone","response_json"],
                                        output_variables=["quiz","review"],
                                        verbose=False)

