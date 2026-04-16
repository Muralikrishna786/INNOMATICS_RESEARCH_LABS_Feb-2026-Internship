from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm import get_llm

llm = get_llm()

prompt = PromptTemplate(
    input_variables=["resume_data", "job_description"],
    template="""
Compare resume with job description.

RULES:
- Only use given data
- No assumptions
- Return VALID JSON

FORMAT:
{{
  "matching_skills": [],
  "missing_skills": []
}}

Resume:
{resume_data}

Job:
{job_description}
"""
)

match_chain = prompt | llm | StrOutputParser()