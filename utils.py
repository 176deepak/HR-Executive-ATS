# import os
import json
import pypdfium2 as pdfium
import google.generativeai as genai


class HR_Executive:
    def __init__(self, model_n, instruction, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_n,
            generation_config={"response_mime_type": "application/json"},
            system_instruction=instruction, 
        )
        
    
    def run(self, inputs:list):
        response = self.model.generate_content(inputs)
        response = json.loads(response.text)
        return response
    

system_instructions = {
    "tech_hr_system_instruction": """
    You are an experienced Technical Human Resource Manager. Your task is to review the provided resume/CV against the technical job description. 
    
    Evaluate the candidate for the job based on the provided resume/CV. And extract the candidate contact details from resume/CV also, so that further HR executive can contact to candidate. Shortlist the candidate based on provided ats score.
    
    Your evaluation should include:
    1. A percentage match between the resume and the job description.
    2. Candidate details, like Name, contact, email.
    3. Final thoughts on the candidate's suitability for the position.
    4. Shortlisted status[True or False]. True, if ats score satisfy the given ats score else False.

    Give output in below JSON schema only:
    candidate_evaluation = {
        "details": {
            "name": str,
            "contact": str,
            "email": str,
            "ats_score": int,
            "final_thoughts":str
        },
        "shortlist": boolean
    }
    """,
    "nontech_hr_system_instruction": """
    You are an experienced Non-Technical Human Resource Manager. Your task is to review the provided resume/CV against the Non-Technical job description. 

    Evaluate the candidate for the job based on the provided resume/CV. And extract the candidate contact details from resume/CV also, so that further HR executive can contact to candidate. Shortlist the candidate based on provided ats score.

    Your evaluation should include:
    1. A percentage match between the resume and the job description.
    2. Candidate details, like Name, contact, email.
    3. Final thoughts on the candidate's suitability for the position.
    4. Shortlisted status[True or False]. True, if ats score satisfy the given ats score else False.

    Give output in below JSON schema only:
    candidate_evaluation = {
        "details": {
            "name": str,
            "contact": str,
            "email": str,
            "ats_score": int,
            "final_thoughts":str
        },
        "shortlist": boolean
    }
    """
}


def pdf_2_images(pdf_path): 
    pages = pdfium.PdfDocument(pdf_path)

    images = []
    for page in enumerate(pages):
        image = page[1].render(scale=4).to_pil()
        images.append(image)
    return images