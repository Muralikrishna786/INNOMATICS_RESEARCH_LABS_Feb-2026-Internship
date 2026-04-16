from langchain_core.prompts import PromptTemplate
from llm import get_llm

llm = get_llm()

prompt = PromptTemplate.from_template("""
You are a recruiter.

Give a SHORT explanation (2-3 lines only).

Score: {score}
Matching Skills: {matching_skills}
Missing Skills: {missing_skills}

Answer:
""")

explain_chain = prompt | llm