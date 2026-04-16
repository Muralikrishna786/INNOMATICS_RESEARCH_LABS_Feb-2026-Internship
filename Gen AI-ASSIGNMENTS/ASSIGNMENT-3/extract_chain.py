from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm import get_llm

llm = get_llm()

prompt = PromptTemplate(
    input_variables=["resume"],
    template="""
Extract structured data from resume.

STRICT RULES:
- Only extract from given text
- Do NOT assume anything
- Return VALID JSON only

FORMAT:
{{
  "skills": [],
  "experience": "",
  "tools": []
}}

Resume:
{resume}
"""
)

extract_chain = prompt | llm | StrOutputParser()