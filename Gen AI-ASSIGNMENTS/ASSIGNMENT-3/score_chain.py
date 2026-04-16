from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm import get_llm

llm = get_llm()

prompt = PromptTemplate(
    input_variables=["match_data"],
    template="""
Assign score (0-100).

RULES:
- More matching skills = higher score
- Missing skills reduce score
- Return ONLY JSON

FORMAT:
{{
  "score": 0
}}

Match:
{match_data}
"""
)

score_chain = prompt | llm | StrOutputParser()