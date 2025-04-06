from resumefeedback import detailed_feedback
from flask import Flask, render_template, request, jsonify
from utils import extract_text_from_pdf, extract_skills, calculate_match
import os
from groq import Groq
app = Flask(__name__)
UPLOAD_FOLDER = "resumes"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api_key = "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"
client = Groq(
            api_key=api_key,
        )

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    print('message',user_message)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"You are a helpful assistant.Provide a answer like you are texting to the user : {user_message}",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    response = chat_completion.choices[0].message.content
    return {"response": response}

@app.route("/match", methods=["POST"])
def match():
    resume = request.files["resume"]
    job_description = request.form["jobdesc"]
    
    resume_path = os.path.join("resumes", resume.filename)
    resume.save(resume_path)

    resume_text = extract_text_from_pdf(resume_path)
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    data = calculate_match(resume_skills, job_skills)
    
    result = detailed_feedback(data)
    print(result)
    
    return render_template("results.html", result = result)


    
    return render_template(
    "index.html",
    ai_feedback=ai_feedback
)


if __name__ == '__main__':
    app.run(debug=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

UPLOAD_FOLDER = "resumes"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

import spacy

# Load spaCy model once globally
nlp = spacy.load("en_core_web_sm")

@app.route('/match', methods=['POST'])
def match():
    # Get job description text from form
    job_description = request.form['job_description']

    # Process job description using spaCy
    doc = nlp(job_description)

    # Extract named entities
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Filter skills (you can create a custom filter or keyword list for better results)
    skills = [ent.text for ent in doc.ents if ent.label_ in ['SKILL', 'WORK_OF_ART', 'ORG', 'PRODUCT']]

    # Show it on page or return as debug
    return render_template('result.html', skills=skills, entities=entities)


if __name__ == "__main__":
    app.run(debug=True)
