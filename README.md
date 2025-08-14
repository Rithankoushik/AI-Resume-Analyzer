# 📄 AI Resume Analyzer

An AI-powered Streamlit web application that analyzes resumes using Deepseek R1 and provides tailored feedback based on job roles.

---

## 🚀 Features

- 📤 Upload resumes in `.pdf` or `.txt` format
- 🧠 Uses **OpenRouter API** for intelligent feedback generation
- 📌 Job role-specific analysis with custom prompt engineering
- 💡 Suggestions on skills, clarity, and experience presentation
- 🧪 Built with **Streamlit** for interactive UI
- 📚 Modular design with support for future LLM chaining via **LangChain**

---

## 🛠 Tech Stack

- **Python 3.10+**
- **Streamlit**
- **Openrouter API**
- **LangChain (for prompt management & modular LLM design)**
- **PyPDF2** (PDF text extraction)
- **dotenv** (for environment variable management)

---

## ⚙️ Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/Rithankoushik/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Or 'venv\Scripts\activate' on Windows

# 3. Install dependencies
pip install -r requirements.txt  # or use uv pip install if using uv

# 4. Add your OpenAI API key
touch .env
echo "OPENAI_API_KEY=your_api_key_here" > .env

# 5. Run the app
streamlit run main.py


