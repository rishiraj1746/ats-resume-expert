from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PIL import Image
import fitz  # PyMuPDF
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyDnmUT1_OW26zhW79Oe4Hxr4iv8-qk9x-Y"))

# Function to send data to Gemini model
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Function to process uploaded PDF using PyMuPDF
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        
        # Get first page as image
        first_page = pdf_document[0]
        pix = first_page.get_pixmap()  # render as image

        # Convert Pixmap to PIL Image
        img_byte_arr = io.BytesIO()
        img = Image.open(io.BytesIO(pix.tobytes("png")))  # as PNG, safe format
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App Layout
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

# Input Job Description
input_text = st.text_area("Job Description:", key="input")

# Upload PDF
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("✅ PDF Uploaded Successfully!")

# Define prompts
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality.
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

# Buttons
submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage Match")

# Handling button click events
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.warning("⚠️ Please upload the resume.")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.warning("⚠️ Please upload the resume.")