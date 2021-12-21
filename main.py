from fastapi import FastAPI
from Keywords_No_Filter import Resume

resumes_local_path = 'Downloaded_Resumes'
image_folder = "Pdf to image"
tech_key_path = r'Keywords\Technician.txt'
civil_key_path = r'Keywords\Civil.txt'
mech_key_path = r'Keywords\Mechanical.txt'
junk_files = 'Junk_Files'

app = FastAPI()

@app.get("/candidate-resume/{get_url}")
def root(get_url):

    resume_path = "https://shramintest.s3.ap-south-1.amazonaws.com/document/" + get_url
    
    res = Resume(resume_path, resumes_local_path, image_folder, tech_key_path, civil_key_path, mech_key_path, 
             junk_files)
    score,word = res.check_keyword()
    keyword = {'textResumeScore': score, 'keyword':word}
    res.delete_file()
    return keyword
