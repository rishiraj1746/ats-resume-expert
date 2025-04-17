from dotenv import load_dotenv
import streamlit as st
import os
import fitz  # PyMuPDF
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Make sure your .env file has the correct key

# Function to extract plain text from uploaded PDF using PyMuPDF
def extract_pdf_text(uploaded_file):
    if uploaded_file is not None:
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        all_text = ""
        for page in pdf_document:
            text = page.get_text()
            all_text += text + "\n"
        return all_text
    else:
        raise FileNotFoundError("No file uploaded")

# Function to send data to Gemini model
def get_gemini_response(prompt, resume_text, job_description):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt, resume_text, job_description])
    return response.text

# Streamlit App Layout
st.set_page_config(page_title="ATS Resume Expert")
st.header("📄 ATS Resume Expert")
st.markdown("Easily compare your resume with a job description using Google Gemini.")

# Input Job Description
input_text = st.text_area("🧾 Paste Job Description:", key="input")

# Upload PDF
uploaded_file = st.file_uploader("📤 Upload your Resume (PDF Only)", type=["pdf"])

if uploaded_file is not None:
    st.success("✅ Resume Uploaded Successfully!")

# Define Prompts
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
submit1 = st.button("🔍 HR Review")
submit3 = st.button("📊 ATS Match Score")

# Handling button click events
if submit1:
    if uploaded_file and input_text.strip():
        with st.spinner("Analyzing Resume..."):
            resume_text = extract_pdf_text(uploaded_file)
            response = get_gemini_response(input_prompt1, resume_text, input_text)
            st.subheader("📌 HR Review:")
            st.write(response)
    else:
        st.warning("⚠️ Please upload a resume and enter job description.")

elif submit3:
    if uploaded_file and input_text.strip():
        with st.spinner("Calculating ATS Match..."):
            resume_text = extract_pdf_text(uploaded_file)
            response = get_gemini_response(input_prompt3, resume_text, input_text)
            st.subheader("📈 ATS Match Result:")
            st.write(response)
    else:
        st.warning("⚠️ Please upload a resume and enter job description.")