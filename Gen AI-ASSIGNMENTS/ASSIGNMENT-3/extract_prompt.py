from langchain_core.prompts import PromptTemplate

extract_prompt = PromptTemplate(
    input_variables=["resume"],
    template="""
Extract resume data.

Return ONLY JSON:
{{
  "skills": [],
  "experience": "",
  "tools": []
}}

Resume:
{resume}
"""
)