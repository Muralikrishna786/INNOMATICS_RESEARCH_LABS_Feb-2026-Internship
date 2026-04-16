from langchain_core.prompts import PromptTemplate

match_prompt = PromptTemplate(
    input_variables=["resume_data", "job_description"],
    template="""
Compare resume and job.

Return ONLY JSON:
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