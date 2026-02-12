import os
from flask import Flask, render_template, request
from processor import extract_text_from_pdf

app = Flask(__name__)
# Define the directory where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['resume']
        job_desc = request.form.get('job_description') # Get JD from form
        
        if file and job_desc:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            # 1. Extract text
            text = extract_text_from_pdf(file_path)
            
            # 2. AI Analysis via Ollama
            from processor import analyze_resume
            result = analyze_resume(text, job_desc)
            
            return f"<h1>Analysis Result:</h1><pre>{result}</pre>"
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)