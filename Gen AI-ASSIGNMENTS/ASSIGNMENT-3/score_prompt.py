from langchain_core.prompts import PromptTemplate

score_prompt = PromptTemplate(
    input_variables=["match_data"],
    template="""
Assign score 0-100.

Return ONLY JSON:
{{
  "score": 0
}}

Match:
{match_data}
"""
)