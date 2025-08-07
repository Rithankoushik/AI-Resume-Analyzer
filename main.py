import streamlit as st
import PyPDF2
import io
import httpx

OPENROUTER_API_KEY = st.secrets["OPENAI_API_KEY"]  # Your OpenRouter key
REFERER = "https://your-username-your-app-name.streamlit.app"  # 👈 UPDATE THIS

# Streamlit UI setup
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📃", layout="centered")
st.title("AI Resume Analyzer")
st.markdown("Upload your resume and get AI-powered feedback using DeepSeek-R1!")

upload_file = st.file_uploader("Upload your Resume (PDF or TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you're targeting (optional)")
analyze = st.button("Analyze Resume")

# Text extraction
def extract_txt_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    return "\n".join(page.extract_text() for page in pdf_reader.pages)

def extract_text_from_file(upload_file):
    if upload_file.type == "application/pdf":
        return extract_txt_from_pdf(io.BytesIO(upload_file.read()))
    return upload_file.read().decode("utf-8")

# Resume analysis logic
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

        # OpenRouter API call using DeepSeek-R1
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": REFERER,
            "X-Title": "AI Resume Analyzer"
        }

        json_payload = {
            "model": "deepseek/deepseek-r1-0528:free",
            "messages": [
                {"role": "system", "content": "You are an expert resume reviewer with years of experience in HR and recruitment."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }

        response = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=json_payload,
            timeout=30
        )

        result = response.json()

        if response.status_code == 200:
            st.markdown("### 📊 Resume Analysis")
            st.markdown(result["choices"][0]["message"]["content"])
        else:
            st.error(f"❌ API Error: {result}")

    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
