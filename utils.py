import fitz  # PyMuPDF
import re

from groq import Groq
api_key = "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"
client = Groq(
            api_key=api_key,
        )
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_skills(text):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"This is my resume\n {text}\n Just give me the skills as a python list",
        }
    ],
    model="llama-3.3-70b-versatile",
)
    print(text)
    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content

def calculate_match(resume_skills, job_skills):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"You should only respond, as this list, do not add any text to this only this list Give me a detailed explanation from this data on this format Compatibility Score: 0% \n ✅ Skills that match: \n ❌ Skills that didn't match: \n\nThis is user's skills\n {resume_skills}\n This is the job requirement's skills\n {job_skills} \n ",
        }
        
    ],
    model="llama-3.3-70b-versatile",
)
    print(chat_completion.choices[0].message.content)
   
    
    return chat_completion.choices[0].message.content
    
    

