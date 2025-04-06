import spacy
import PyPDF2

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Sample job requirements (You can make it dynamic from a form later)
required_skills = ["Python", "Machine Learning", "Data Analysis", "Communication", "SQL", "Leadership"]

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

def analyze_resume(text):
    doc = nlp(text)
    words = [token.text.lower() for token in doc if token.is_alpha]
    
    matched = [skill for skill in required_skills if skill.lower() in words]
    missing = [skill for skill in required_skills if skill.lower() not in words]
    
    score = int((len(matched) / len(required_skills)) * 100)

    # Feedback
    feedback = f"📝 Resume Analysis Complete!\n\n✅ Matched Skills: {', '.join(matched) if matched else 'None'}\n"
    feedback += f"❌ Missing Skills: {', '.join(missing) if missing else 'None'}\n"
    feedback += f"\n📊 Match Score: {score}%\n"
    
    if score < 50:
        feedback += "⚠️ Your resume needs improvement. Try adding more relevant skills.\n"
    elif score < 80:
        feedback += "👍 You're doing good! Add a few more skills to increase your chances.\n"
    else:
        feedback += "🔥 Great job! Your resume matches well with the job description.\n"

    return feedback

# === Run it on a sample PDF ===
if __name__ == "__main__":
    file_path = "resumes/Rajadurai_Resume_BE.pdf"  # <-- Change this to your actual file path
    resume_text = extract_text_from_pdf(file_path)
    result = analyze_resume(resume_text)
    print(result)

import PyPDF2

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
        return text

from groq import Groq

client = Groq(api_key="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")  # Replace with your actual key

def detailed_feedback(feedback):
    prompt = f"""
    Give me detailed feedback on this data in the following bullet point format:

    **1. Compatibility Score:**  
    - Score: [value]  
    - Brief analysis

    **2. Skills that Match:**  
    - Skill 1  
    - Skill 2  
    - Skill 3  

    **3. Skills that Didn't Match:**  
    - Missing Skill 1  
    - Missing Skill 2  
    - Missing Skill 3  

    **4. Overall Analysis:**  
    - Summary bullet points

    **5. Personalized Improvements:**  
    - Improvement 1  
    - Improvement 2  
    - Improvement 3  
    - Improvement 4  
    - Improvement 5

    Feedback:  
    {feedback}

    Return the above sections formatted with bullet points and bold titles.
    """

    try:
        print("Getting feedback")
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192"
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"AI feedback error: {str(e)}"
