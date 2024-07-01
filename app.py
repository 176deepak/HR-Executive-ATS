import pandas as pd
import gradio as gr
from utils import *


def shortlist(api_key, hr, jd, resumes, ats_score):
    shortlisted_candidates = pd.DataFrame(columns=["name", "contact", "email", "ats_score", "final_thoughts"])
    
    if hr == "Technical HR Executive":
        tech_hr = HR_Executive('gemini-1.5-flash', system_instructions["tech_hr_system_instruction"], api_key)
        prompt = f"Shortlist the candidate with minimum {ats_score} ats score."
        
        for resume in resumes:
            resume_imgs = pdf_2_images(resume)
            result = tech_hr.run([jd, *resume_imgs, prompt])
            if result.get("shortlist", False):
                shortlisted_candidates = shortlisted_candidates._append(result.get("details"), ignore_index=True)
                
        
    if hr == "Non-Technical HR Executive":
        nontech_hr = HR_Executive('gemini-1.5-flash', system_instructions["nontech_hr_system_instruction"], api_key)
        prompt = f"Shortlist the candidate with minimum {ats_score} ats score."
        
        for resume in resumes:
            resume_imgs = pdf_2_images(resume)
            result = nontech_hr.run([jd, *resume_imgs, prompt])
            if result.get("shortlist", False):
                shortlisted_candidates = shortlisted_candidates._append(result.get("details"), ignore_index=True)
                
    
    return shortlisted_candidates
    

css = """
#header {
    text-align: center;
    font-size: 48px !important;
    padding-bottom: 50px;
}

#shortlisted {
    text-align: center;
    font-size: 48px !important;
    padding-top: 50px;
}

#demo-video {
    text-align: center;
    font-size: 48px !important;
    padding-top: 50px;
}
"""


with gr.Blocks(css=css) as app:
    gr.Markdown(
        value="# Your Technical/Non-Technical HR Executive", 
        elem_id="header"
    )
    
    with gr.Row():
        api_key = gr.Textbox(label="API Key", placeholder="Enter your Gemini API key...", type="password")
    
    with gr.Row():
        hr = gr.Dropdown(
            choices=[
                "Technical HR Executive", 
                "Non-Technical HR Executive"
            ], 
            label="Select HR Executive", 
            interactive=True
        )
    
    with gr.Row(variant='panel'):
        with gr.Column(scale=3):
            jd = gr.Textbox(
                placeholder="Job Description here...", 
                label="Job Description", 
                elem_id="JD", 
                lines=20
            )
        with gr.Column():
            resumes = gr.File(
                label="Resume/CV", 
                file_types=["file"], 
                file_count='multiple', 
                elem_id="resume", 
                height=350
            )
            ats_score = gr.Slider(
                label="ATS Score", 
                elem_id="ats"
            )

    with gr.Row():
        shortlist_btn = gr.Button("Shortlist")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("## Shortlisted Candidates", elem_id="shortlisted")
            output = gr.Dataframe(
                wrap=True
            )

    with gr.Row():
        shortlist_btn.click(
            shortlist, 
            inputs=[api_key, hr, jd, resumes, ats_score], 
            outputs=output
        )
        
    with gr.Row():
        with gr.Column():
            gr.Markdown("## See Demo", elem_id="demo-video")
            video_input = gr.Video(value="demo.mp4", autoplay=True)
        

if __name__ == "__main__":
    app.launch()