import streamlit as st
import PyPDF2
import io
from openai import OpenAI

# ✅ Get API key from Streamlit secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# ✅ Set OpenRouter as base URL
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# 🖥️ Page config
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📃", layout="centered")
st.title("AI Resume Analyzer")
st.markdown("Upload your resume and get AI-powered feedback tailored to your needs!")

# 📤 File + job role input
upload_file = st.file_uploader("Upload your Resume (PDF or TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you're targeting (optional)")
analyze = st.button("Analyze Resume")

# 📄 PDF/Text extraction logic
def extract_txt_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(upload_file):
    if upload_file.type == "application/pdf":
        return extract_txt_from_pdf(io.BytesIO(upload_file.read()))
    return upload_file.read().decode("utf-8")

# 🔍 Analyze logic
if analyze and upload_file:
    try:
        file_content = extract_text_from_file(upload_file)
        if not file_content.strip():
            st.warning("Uploaded file is empty or unreadable.")
            st.stop()

        prompt = f"""Please analyze this resume and provide constructive feedback. 
Focus on the following aspects:
1. Content clarity and impact
2. Skills presentation
3. Experience descriptions
4. Specific improvements for {job_role if job_role else 'general job applications'}

Resume content:
{file_content}

Please provide your analysis in a clear, structured format with specific recommendations."""

        # ✅ Make request to OpenRouter with valid model
        response = client.chat.completions.create(
            model="openai/gpt-4o",  # ✅ Use correct OpenRouter-supported model name
            messages=[
                {"role": "system", "content": "You are an expert resume reviewer with years of experience in HR and recruitment."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        st.markdown("### 📊 Resume Analysis")
        st.markdown(response.choices[0].message.content)

    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
