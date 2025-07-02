import streamlit as st
import PyPDF2
import spacy
from fuzzywuzzy import fuzz
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="centered")

# App Header
st.markdown("👨‍💻 Built with ❤️ by **Vaibhav B N**")
st.markdown("🚀 Powered by Python, spaCy (NLP), and Streamlit")

# Load spaCy model with fallback
try:
    nlp = spacy.load("en_core_web_sm")
except:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Extract text from PDF
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return "".join(page.extract_text() or "" for page in reader.pages)

# Extract keywords using spaCy
def extract_keywords(text):
    doc = nlp(text.lower())
    return list(set([token.text for token in doc if token.is_alpha and not token.is_stop]))

# Calculate job fit score
def calculate_job_fit(resume_keywords, jd_keywords):
    matched = set(resume_keywords) & set(jd_keywords)
    score = int(len(matched) / len(jd_keywords) * 100) if jd_keywords else 0
    return score, matched

# Generate word cloud
def generate_wordcloud(keywords):
    text = " ".join(keywords)
    return WordCloud(width=800, height=400, background_color='white').generate(text)

# Sidebar
st.sidebar.title("📂 Resume Analyzer")
st.sidebar.info("Upload your resume and paste a job description to get results.")

# Tabs
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
        missing = set(jd_keywords) - set(resume_keywords)

        st.success(f"✅ Job Fit Score: {score}%")
        st.markdown(f"**Matched Keywords ({len(matched)}):**")
        st.write(", ".join(matched))

        # Word Cloud
        st.subheader("☁️ Resume Keyword Word Cloud")
        fig_wc, ax_wc = plt.subplots()
        ax_wc.imshow(generate_wordcloud(resume_keywords), interpolation='bilinear')
        ax_wc.axis('off')
        st.pyplot(fig_wc)

        # Keyword Bar Chart
        st.subheader("📊 Keyword Match Chart")
        fig_bar, ax_bar = plt.subplots()
        ax_bar.bar(["Matched", "Missing"], [len(matched), len(missing)], color=["green", "red"])
        st.pyplot(fig_bar)

        # Report Download
        report = f"""
Job Fit Score: {score}%

Matched:
{', '.join(matched)}

Missing:
{', '.join(missing)}
"""
        st.download_button("📥 Download Report", data=report, file_name="resume_analysis.txt", mime="text/plain")

    else:
        st.info("⬆️ Upload a resume and paste a job description to begin.")

with tab2:
    st.header("📊 Summary")
    st.write("- Extracts and compares keywords using spaCy")
    st.write("- Calculates job fit score")
    st.write("- Shows matched & missing keywords")
    st.write("- Visualizes results using word cloud & charts")
    st.write("- Lets you download a summary report")
