from dotenv import load_dotenv
load_dotenv()

from chains.extract_chain import extract_chain
from chains.match_chain import match_chain
from chains.score_chain import score_chain
from chains.explain_chain import explain_chain

import json
import re


def safe_json_parse(text):
    text = str(text)

    match = re.search(r'\{[\s\S]*?\}', text)

    if match:
        try:
            return json.loads(match.group())
        except:
            return {}

    return {}


def clean_output(text):
    return text.strip().split("\n")[0:3]

def run_pipeline(resume, job_description):

    # ---------- STEP 1: MANUAL EXTRACTION ----------
    resume_lower = resume.lower()

    skills_list = ["python", "machine learning", "sql", "nlp", "pandas"]

    extracted_skills = [skill for skill in skills_list if skill in resume_lower]

    if "year" in resume_lower:
        experience = resume.split("Experience:")[-1].strip()
    else:
        experience = "0 years"

    extracted = {
        "skills": extracted_skills,
        "experience": experience,
        "tools": []
    }

    print("Extracted:", extracted)

    # ---------- STEP 2: MATCHING ----------
    job_lower = job_description.lower()
    required_skills = [skill for skill in skills_list if skill in job_lower]

    matching_skills = [s for s in extracted_skills if s in required_skills]
    missing_skills = [s for s in required_skills if s not in extracted_skills]

    matched = {
        "matching_skills": matching_skills,
        "missing_skills": missing_skills
    }

    print("Match:", matched)

    # ---------- STEP 3: SCORING ----------
    score_value = int((len(matching_skills) / len(required_skills)) * 100) if required_skills else 0

    score = {"score": score_value}
    print("Score:", score)

    # ---------- STEP 4: EXPLANATION (LLM OK HERE) ----------
    explanation = explain_chain.invoke({
    "score": score,
    "matching_skills": matched["matching_skills"],
    "missing_skills": matched["missing_skills"]
})
    explanation_text = explanation.strip().split("### Output:")[-1].strip()

    # limit to 3 lines
    explanation_text = "\n".join(explanation_text.split("\n")[:3])
    print("Explanation:", explanation)

    return explanation

if __name__ == "__main__":

    # Load files
    with open(r"C:\Users\mural\resume-screening-ai\data\resume_strong.txt") as f:
        strong_resume = f.read()

    with open(r"C:\Users\mural\resume-screening-ai\data\resume_avg.txt") as f:
        avg_resume = f.read()

    with open(r"C:\Users\mural\resume-screening-ai\data\resume_weak.txt") as f:
        weak_resume = f.read()

    with open(r"C:\Users\mural\resume-screening-ai\data\job_description.txt") as f:
        job_description = f.read()

    print("\n===== STRONG CANDIDATE =====")
    run_pipeline(strong_resume, job_description)

    print("\n===== AVERAGE CANDIDATE =====")
    run_pipeline(avg_resume, job_description)

    print("\n===== WEAK CANDIDATE =====")
    run_pipeline(weak_resume, job_description)