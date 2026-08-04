import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Load environment variables (your OPENAI_API_KEY)
load_dotenv()

# We use ChatOpenAI which is the modern standard for models like gpt-4 or gpt-3.5-turbo
llm = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo")

# Create a prompt template for root cause analysis
# PromptTemplate automatically reads the variable names from the curly braces
analysis_template = """
You are a senior SAP CPI integration developer.
A message failed in the iFlow: {iflow_name}.
The error message received was: {error_msg}

Analyze the following payload and correct the issue based on the error message.
Return only the corrected payload, no markdown formatting or conversational text.

Raw Payload:
{payload}
"""

prompt = PromptTemplate.from_template(analysis_template)

# Create the LangChain pipeline using the pipe operator
# The prompt template is applied first, then the resulting prompt is sent to the LLM
analysis_chain = prompt | llm

def analyze_and_correct_payload(iflow_name: str, error_msg: str, payload: str):
    """
    Invokes the LangChain pipeline to analyze the SAP error and correct the payload.
    """
    response = analysis_chain.invoke({
        "iflow_name": iflow_name,
        "error_msg": error_msg,
        "payload": payload
    })
    
    # The response is an AIMessage object, we want its content
    return response.content