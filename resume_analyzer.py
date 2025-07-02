import streamlit as st
import PyPDF2
import spacy
from fuzzywuzzy import fuzz
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Resume Analyzer by Vaibhav",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="auto"
)

# -------------------- HEADER --------------------
st.markdown("## 👨‍💻 Built with ❤️ by **Vaibhav B N**")
st.markdown("### 🚀 Powered by Python, spaCy (NLP), and Streamlit")

# -------------------- LOAD NLP MODEL --------------------
nlp = spacy.load("en_core_web_sm")

# -------------------- FUNCTIONS --------------------
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_keywords(text):
    doc = nlp(text.lower())
    return list(set([token.text for token in doc if token.is_alpha and not token.is_stop]))

def calculate_job_fit(resume_keywords, jd_keywords):
    matched = set(resume_keywords) & set(jd_keywords)
    score = int(len(matched) / len(jd_keywords) * 100) if jd_keywords else 0
    return score, matched

def generate_wordcloud(keywords):
    text = " ".join(keywords)
    return WordCloud(width=800, height=400, background_color='white').generate(text)

# -------------------- SIDEBAR --------------------
st.sidebar.title("📂 Resume Analyzer")
st.sidebar.info("Upload your resume and paste a job description to get match results.")

# -------------------- UI TABS --------------------
tab1, tab2 = st.tabs(["📄 Analyze", "📊 Summary"])

with tab1:
    st.title("Upload & Analyze Resume")

    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    jd_text = st.text_area("Paste Job Description")

    if resume_file and jd_text:
        resume_text = extract_text_from_pdf(resume_file)
        resume_keywords = extract_keywords(resume_text)
        jd_keywords = extract_keywords(jd_text)

        score, matched = calculate_job_fit(resume_keywords, jd_keywords)
        missing_keywords = set(jd_keywords) - set(resume_keywords)

        st.success(f"✅ Job Fit Score: {score}%")
        st.markdown(f"**Matched Keywords ({len(matched)}):**")
        st.write(", ".join(matched))

        # Word Cloud
        st.subheader("☁️ Resume Keyword Word Cloud")
        fig_wc, ax_wc = plt.subplots()
        ax_wc.imshow(generate_wordcloud(resume_keywords), interpolation='bilinear')
        ax_wc.axis('off')
        st.pyplot(fig_wc)

        # Bar Chart
        st.subheader("📊 Keyword Match Chart")
        labels = ['Matched', 'Missing']
        values = [len(matched), len(missing_keywords)]
        fig_bar, ax_bar = plt.subplots()
        ax_bar.bar(labels, values, color=['green', 'red'])
        ax_bar.set_ylabel('Keyword Count')
        st.pyplot(fig_bar)

        # Downloadable Report
        report = f"""
Job Fit Score: {score}%

Matched Keywords:
{', '.join(matched)}

Missing Keywords:
{', '.join(missing_keywords)}
        """
        st.download_button(
            label="📥 Download Report as .txt",
            data=report,
            file_name="resume_analysis.txt",
            mime="text/plain"
        )

    else:
        st.info("⬆️ Upload a PDF resume and paste a job description to begin analysis.")

with tab2:
    st.header("📊 Summary")
    st.write("This app analyzes your resume and compares it with a job description.")
    st.write("- Extracts and compares keywords using spaCy")
    st.write("- Calculates job fit score")
    st.write("- Displays matched & missing keywords")
    st.write("- Visualizes results with Word Cloud & Charts")
    st.write("- Lets you download a summary report")
