# © 2025 Shakeel Qureshi.  
# Proprietary - See [PROPRIETARY_LICENSE](PROPRIETARY_LICENSE) in repo root.  

"""
DISCLAIMER:
This is a simplified public demo of a resume parsing tool using open-source NLP libraries.
It does not reflect the proprietary scoring or matching logic used in production systems
like TalentSync™, FitScore™, or EngageIQ™.
"""

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_resume_with_gpt(resume_text):
    system_prompt = """You are an AI resume parser. Your job is to extract structured data from resumes.
Return only a JSON object with the following fields:
- Full Name
- Email
- Phone
- LinkedIn
- GitHub
- Skills (list)
- Education (list of {degree, field, institution, year})
- Experience (list of {job_title, company, duration, summary})
- Certifications (list)
- Location (city, country)
If a field is missing, leave it as null or an empty list.
"""

    user_prompt = f"Resume:\n{resume_text}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0
    )

    parsed_json = response['choices'][0]['message']['content']
    return parsed_json
