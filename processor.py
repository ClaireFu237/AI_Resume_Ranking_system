from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

# Initialize Ollama with local model
llm = Ollama(model="deepseek-r1:1.5b", temperature=0) 

def extract_text_from_pdf(pdf_path):
    """
    Extracts all text from a given PDF file path.
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            # Iterate through each page and extract text
            for page in pdf_reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text: {e}")
    return text

def analyze_resume(resume_text, job_description):
    """
    Sends resume and JD to local Ollama model and returns the score/summary.
    """
    template = """
    You are a professional HR manager. Analyze the resume based on the job description.
    
    Job Description: {job_desc}
    Resume Content: {resume_content}
    
    Output exactly in this format:
    Score: [0-100]
    Summary: [Brief analysis]
    """
    
    prompt = PromptTemplate.from_template(template)
    # Combine prompt with data
    formatted_prompt = prompt.format(
        job_desc=job_description, 
        resume_content=resume_text
    )
    
    # Call local LLM
    response = llm.invoke(formatted_prompt)
    return response