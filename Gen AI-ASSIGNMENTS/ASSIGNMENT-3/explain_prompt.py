from langchain_core.prompts import PromptTemplate

explain_prompt = PromptTemplate(
    input_variables=["score", "match_data"],
    template="""
Give short recruiter explanation (3-5 lines only).

Score: {score}
Match: {match_data}
"""
)