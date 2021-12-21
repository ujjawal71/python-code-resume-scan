'''
poppler - add to environmental variable
tessseract-ocr = add to environmental variable
'''


import requests
import urllib.request
from pdf2image import convert_from_path
import cv2
import pytesseract
import docx
from textblob import TextBlob
import os
import shutil

class Resume:
    
    file_ext_type = ''
    resume_found = ''
    local_path = ''
    file_found  = False

    def __init__(self, resume_path, resumes_local_path, image_folder, tech_key_path, civil_key_path, mech_key_path, 
             junk_files):
        self.resume_path = resume_path
        self.resumes_local_path = resumes_local_path
        self.image_folder = image_folder
        self.tech_key_path = tech_key_path
        self.civil_key_path = civil_key_path
        self.mech_key_path = mech_key_path
        self.junk_files = junk_files
    
    #resume_type = .pdf / .jpg/ .doc / .docx
    '''
    0 = pdf 
    1 = image
    2 = doc
    3 = docx 
    '''
    def get_resume_type(self):
        split_resume_path = self.resume_path.split(u'/')
        resume_name = split_resume_path[-1]
        
        if resume_name.endswith('.pdf'):
            self.file_ext_type = 'pdf'
            return  0, resume_name
        elif resume_name.endswith('.jpg') or resume_name.endswith('.jpeg') or resume_name.endswith('.png'):
            self.file_ext_type = 'img'
            return 1, resume_name
        elif resume_name.endswith('.doc'):
            self.file_ext_type = 'doc'
            return 2, resume_name
        elif resume_name.endswith('.docx'):
            self.file_ext_type = 'docx'
            return 3, resume_name
        else:
            self.file_ext_type = 'invalid'
            return 4, resume_name
        
    def download_resume(self):
        resume_type, res_name = self.get_resume_type()
        local_filename = self.resumes_local_path +"\\" + res_name
        
        if resume_type == 0:
            path_response = requests.get(self.resume_path)
        
            with open(local_filename , 'wb') as f:
                f.write(path_response.content)
            self.local_path = local_filename
            return 0 
            
        elif resume_type == 1:
            file_ext_sep = local_filename.split('.')
            image_filename = file_ext_sep[0] + '.jpeg'
            urllib.request.urlretrieve(self.resume_path, image_filename)
            self.local_path = image_filename
            return 1
        elif resume_type == 2:
            return 'doc'
        elif resume_type == 3:
            return 'docx'

       
    def pdf_text_extract(self):
        type  = self.download_resume()
        
        _img = self.local_path.split('\\')
        _img1 = _img[-1]
        image_file_name = _img1.split('.')

        if type == 0:
            pdf_img = convert_from_path(self.local_path, poppler_path= r'C:\Program Files\poppler-21.11.0\Library\bin')
            img_list = []
            for image in range(len(pdf_img)):
                img_name = f"{self.image_folder}\{image_file_name[0]}" + "_img" + str(image) + '.jpg'
                pdf_img[image].save(img_name, 'JPEG')
                img_list.append(img_name)
                img = cv2.imread(img_name, 1)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                return img_name
            data = ''
            for img in img_list:
                text = pytesseract.image_to_string(img)
                #data = TextBlob(text)
                #txt = str(data.correct())
                data += text
            return data

    def img_text_extract(self):
        type= self.download_resume()
        if type == 1:
            image = cv2.imread(self.local_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            text = pytesseract.image_to_string(image)
            #data = TextBlob(text)
            #txt = str(data.correct())
            return text

    def docx_text_extract(self):
        type = self.download_resume()
        if type == 3:
            _docx = docx.Document(self.local_path)
            data = ''
            full_text = []
            for para in _docx.paragraphs:
                full_text.append(para.text)
                data = '\n'.join(full_text)
                #text = TextBlob(data)
                #txt = str(text.correct())
                return data

    def find(self):
        pdf_txt = self.pdf_text_extract()
        img_txt = self.img_text_extract()
        docx_txt = self.docx_text_extract()
        tech_det = open(self.tech_key_path, 'r')
        tech_read =[line for line in tech_det.readlines()]
        civil_det = open(self.civil_key_path, 'r')
        civil_read = [line for line in civil_det.readlines()]
        #civil_read = civil_det.readlines()
        mech_det = open(self.mech_key_path, 'r')
        mech_read = [line for line in mech_det.readlines()]
        #mech_read = mech_det.readlines()
        
        keyword = []

        if self.file_ext_type == 'pdf':
            
            for tline in tech_read:
                tline = tline.split("\n")
                if tline[0] != "\n":
                    if tline[0] in pdf_txt.lower():
                        
                        self.file_found = True
                        keyword.append(tline)

                    else:
                        self.file_found = False
                else:
                    break
                    
            for cline in civil_read:
                
                cline = cline.split("\n")
                if tline[0] != "\n":
                    if cline[0] in pdf_txt.lower():
                        self.file_found = True
                        keyword.append(cline)
                    else:
                        self.file_found = False
                else:
                    break
                    
            for mline in mech_read:
                mline = mline.split("\n")
                if tline[0] != "\n":
                    if mline[0] in pdf_txt.lower():
                        self.file_found = True
                        keyword.append(mline)
                    else:
                        self.file_found = False
                else:
                    break
                   
        elif self.file_ext_type == 'img':
            for tline in tech_read:

                tline = tline.split("\n")
                if tline[0] != "\n":
                
                    if tline[0] in img_txt.lower():
                        self.file_found = True
                        keyword.append(tline)
                    else:
                        self.file_found = False
                else:
                    break
                
            for cline in civil_read:
                cline = cline.split("\n")
                
                if tline[0] != "\n":
                    if cline[0] in img_txt.lower():
                        self.file_found = True
                        keyword.append(cline)
                    else:
                        self.file_found = False
                else:
                    break  
            
            for mline in mech_read:
                if tline[0] != "\n":
                    if mline.strip() in img_txt.lower():
                        self.file_found = True
                        keyword.append(mline)
                    else:
                        self.file_found = False
                else:
                    break
                    
        elif self.file_ext_type == 'docx':
            for tline in tech_read:
               
                tline = tline.split("\n")
                if tline[0] != "\n":                
                    if tline[0] in docx_txt.lower():
                        self.file_found = True
                        keyword.append(tline)
                    else:
                        self.file_found = False
                else:
                    break
                
            for cline in civil_read:
                cline = cline.split("\n")
                if tline[0] != "\n":
                    if cline[0] in docx_txt.lower():
                        self.file_found = True
                        keyword.append(cline)
                    else:
                        self.file_found = False   
                else:
                    break   

            for mline in mech_read:
                mline = mline.split("\n")
                if tline[0] != "\n":
                    if mline[0] in docx_txt.lower():
                        self.file_found = True
                        keyword.append(mline)
                    else:
                        self.file_found = False
                else:break           
        return keyword

    def get_keyword(self):
        keywords = self.find()
        keyword_list = []
        for keyword in keywords:
            for k in keyword:
                if k =='':
                    pass
                else:
                    keyword_list.append(k)
        return keyword_list
    
    def check_keyword(self):
        keyword = self.get_keyword()
        if self.file_ext_type == 'invalid':
            return 0, 'Invalid file extension'
        elif keyword == []:
            file_split = self.local_path.split('\\')
            junk_path = self.junk_files
            junk_file = os.path.join(junk_path, file_split[-1])
            shutil.move(self.local_path, junk_file)
            os.remove(junk_file)
            return 0,'Keyword Not Found'
            
        else:
            return 1,keyword

    def delete_file(self):
        img_path = self.pdf_text_extract()
        os.remove(self.local_path)
        os.remove(img_path)
