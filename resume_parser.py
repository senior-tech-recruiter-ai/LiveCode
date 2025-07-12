# © 2025 Shakeel Qureshi.  
# Proprietary - See [PROPRIETARY_LICENSE](PROPRIETARY_LICENSE) in repo root.  

"""
DISCLAIMER:
This is a simplified public demo of a resume parsing tool using open-source NLP libraries.
It does not reflect the proprietary scoring or matching logic used in production systems
like TalentSync™, FitScore™, or EngageIQ™.
"""


import os
import spacy
import json
import docx
import re
from PyPDF2 import PdfReader

# Load spaCy model (install with: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip())

def parse_resume(text):
    doc = nlp(text)
    name = None
    email = None
    phone = None
    skills = []

    for ent in doc.ents:
        if ent.label_ == "PERSON" and not name:
            name = ent.text
        elif ent.label_ == "EMAIL":
            email = ent.text
        elif ent.label_ == "PHONE":
            phone = ent.text

    # Simple keyword match for skill extraction
    keywords = ['Python', 'JavaScript', 'SQL', 'React', 'AWS', 'Django', 'NLP', 'LLM', 'GPT', 'Kubernetes']
    for kw in keywords:
        if kw.lower() in text.lower():
            skills.append(kw)

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": list(set(skills))
    }

def parse_file(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")

    text = clean_text(text)
    return parse_resume(text)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Resume Parser (LLM + NLP)")
    parser.add_argument("filepath", help="Path to resume file (.pdf or .docx)")
    parser.add_argument("--json", help="Output as JSON file", action="store_true")
    args = parser.parse_args()

    result = parse_file(args.filepath)

    if args.json:
        out_path = os.path.splitext(args.filepath)[0] + "_parsed.json"
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2)
        print(f"[✓] Parsed resume saved to {out_path}")
    else:
        print(json.dumps(result, indent=2))
