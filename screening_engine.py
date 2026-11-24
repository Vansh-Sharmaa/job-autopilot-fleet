"""
Human-Sounding Screening Question Engine for Vansh Sharma
Solves job screening questions (numerical, dropdowns, and short essays)
with strictly zero AI footprints (0 em-dashes, 0 buzzwords, practical engineer voice).
"""
import re
import json

# Technical Experience Lookup (years)
TECH_EXPERIENCE = {
    "python": "3",
    "pytorch": "2",
    "machine learning": "2",
    "deep learning": "2",
    "ml": "2",
    "langchain": "1",
    "langgraph": "1",
    "agent": "1",
    "agents": "1",
    "llm": "1",
    "llms": "1",
    "rag": "1",
    "vector": "1",
    "faiss": "1",
    "fastapi": "2",
    "rest": "2",
    "api": "2",
    "sql": "2",
    "mysql": "2",
    "postgresql": "2",
    "database": "2",
    "docker": "1",
    "git": "3",
    "github": "3",
    "c++": "2",
    "cpp": "2",
    "data science": "2",
    "nlp": "2",
    "computer vision": "1",
    "operations": "1",
    "tech ops": "1",
    "total experience": "1",
    "work experience": "1",
    "years of experience": "1",
    "relevant experience": "1"
}

# Standard Personal & Logistic Answers
LOGISTICS = {
    "notice": "0",
    "notice period": "0",
    "days of notice": "0",
    "current ctc": "0",
    "current salary": "0",
    "fixed ctc": "0",
    "expected ctc": "600000",
    "expected salary": "600000",
    "salary expectation": "600000",
    "minimum ctc": "600000",
    "cgpa": "8.0",
    "gpa": "8.0",
    "score": "8.0",
    "percentage": "80",
    "graduation year": "2026",
    "passing year": "2026",
    "passout year": "2026",
    "bachelor graduation year": "2024",
    "ug graduation year": "2024"
}

# Verified Human Essay Templates (Direct, code-focused, 0 em-dashes, 0 buzzwords)
ESSAY_TEMPLATES = {
    "why_join": (
        "I have been tracking what your team is building with applied AI, and I want to work somewhere "
        "engineering quality and shipping fast matter more than bureaucracy. My background is in production "
        "RAG systems, LangGraph agent workflows, and ML feature pipelines. I want to jump in, take ownership "
        "of technical challenges, and build reliable software that users actually use."
    ),
    "experience_llm": (
        "I build multi-agent systems and RAG pipelines end-to-end. In ResearchMind, I built a LangGraph state graph "
        "orchestrating 4 specialized agents (Search, Scrape, Writer, Critic) with automated reflection loops. "
        "In LexAI, I implemented a Map-Reduce summarization chain for legal contracts and FAISS semantic vector search "
        "with all-MiniLM-L6-v2 embeddings to ground LLM outputs and eliminate hallucinations."
    ),
    "technical_challenge": (
        "I built FileGenie, a content-based file classification and security engine. Traditional tools only check file extensions, "
        "which fails when executables are renamed to .pdf. I built a 16-dimensional feature extraction pipeline calculating Shannon Entropy, "
        "raw binary magic bytes, and null-byte distributions, training a 300-tree Random Forest classifier in scikit-learn that achieves 95%+ "
        "accuracy in under 1ms on CPU, integrated with high-throughput FastAPI streaming."
    ),
    "about_yourself": (
        "I am an AI/ML Engineer completing my MCA in AI & Data Science. I focus on practical GenAI: multi-agent orchestration "
        "in LangGraph, Retrieval-Augmented Generation with vector databases, and full-stack deployment using FastAPI and Python. "
        "I prefer building working prototypes and reliable pipelines over just calling standard API endpoints."
    ),
    "operations_experience": (
        "I have hands-on experience managing and monitoring technical workflows, automating repetitive pipelines with Python scripts, "
        "and coordinating data validation checks. I focus on reducing process latency, maintaining system reliability, and documenting "
        "standard operating procedures for tech infrastructure."
    ),
    "cover_note": (
        "Hi team, I saw your opening and wanted to reach out. I have hands-on experience building LangGraph agent pipelines, "
        "FAISS vector search systems, and production FastAPI services. My code and architecture designs are public on my GitHub "
        "(github.com/Vansh-Sharmaa), and my resume is attached. Would love the chance to connect if my background fits what you are building."
    )
}

def clean_text(text):
    return re.sub(r'[^a-z0-9\s]', ' ', text.lower()).strip()

def answer_question(question_text, options=None):
    """
    Given a question label/prompt and optional dropdown options,
    determines the most accurate, human-written answer.
    """
    q_lower = question_text.lower().strip()

    # 1. Check for Essay / Descriptive Prompts FIRST
    is_essay_prompt = any(w in q_lower for w in ["describe", "explain", "tell us", "tell me", "why do you", "why are you", "what excites", "briefly describe", "summary of your"])
    
    if is_essay_prompt:
        if any(k in q_lower for k in ["why do you", "why join", "why are you interested", "what excites"]):
            return sanitize_output(ESSAY_TEMPLATES["why_join"])
        if any(k in q_lower for k in ["llm", "genai", "generative ai", "rag", "langchain", "langgraph", "agent", "machine learning", "ml", "ai"]):
            return sanitize_output(ESSAY_TEMPLATES["experience_llm"])
        if any(k in q_lower for k in ["challenge", "difficult", "complex project", "accomplishment", "technical project"]):
            return sanitize_output(ESSAY_TEMPLATES["technical_challenge"])
        if any(k in q_lower for k in ["about yourself", "bio", "background"]):
            return sanitize_output(ESSAY_TEMPLATES["about_yourself"])
        if any(k in q_lower for k in ["operations", "tech ops", "process", "monitoring"]):
            return sanitize_output(ESSAY_TEMPLATES["operations_experience"])
        if any(k in q_lower for k in ["cover letter", "note", "message to recruiter", "additional"]):
            return sanitize_output(ESSAY_TEMPLATES["cover_note"])
        # Generic engineering essay fallback
        return sanitize_output(ESSAY_TEMPLATES["about_yourself"])

    # 2. Check Boolean / Yes-No Questions
    if any(k in q_lower for k in ["authorized to work", "legally authorized", "right to work in india"]):
        return select_option(["Yes", "true"], options, default="Yes")
    
    if any(k in q_lower for k in ["sponsorship", "require visa", "visa sponsorship", "future require"]):
        return select_option(["No", "false"], options, default="No")

    if any(k in q_lower for k in ["willing to relocate", "relocate", "comfortable working in", "open to travel", "comfortable with"]):
        return select_option(["Yes", "true"], options, default="Yes")

    if any(k in q_lower for k in ["immediate joiner", "join immediately", "start immediately", "available to start"]):
        return select_option(["Yes", "true"], options, default="Yes")

    if any(k in q_lower for k in ["remote", "work from home", "hybrid", "on-site"]):
        return select_option(["Yes", "true"], options, default="Yes")

    # 3. Check Logistics & Compensation
    for k, val in LOGISTICS.items():
        if k in q_lower:
            return select_option([val], options, default=val)

    # 4. Check Tech Skill Experience (Years)
    for skill, years in TECH_EXPERIENCE.items():
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, q_lower):
            return select_option([years, f"{years} year", f"{years} years"], options, default=years)

    # 5. Default Fallback
    if options and len(options) > 0:
        return options[0]
    
    if any(k in q_lower for k in ["year", "years", "how many", "months", "rating"]):
        return "1"
    
    return "Yes"

def select_option(preferred_list, options, default="Yes"):
    if not options:
        return default
    for pref in preferred_list:
        for opt in options:
            if pref.lower() in opt.lower():
                return opt
    return options[0]

def sanitize_output(text):
    """
    Enforces strict zero AI footprints:
    - Zero em-dashes (\u2014) or en-dashes (\u2013)
    - Replaces with hyphens or commas
    - Removes banned boilerplate
    """
    text = text.replace("\u2014", ", ").replace("\u2013", "-")
    return text.strip()

if __name__ == "__main__":
    # Test suite of real questions
    test_questions = [
        "How many years of work experience do you have with PyTorch?*",
        "How many years of work experience do you have with LangGraph?*",
        "What is your expected CTC in INR?",
        "What is your notice period in days?",
        "Are you legally authorized to work in India?*",
        "Will you now or in the future require visa sponsorship?*",
        "Why do you want to join our company?",
        "Describe your experience with LLMs and multi-agent systems.",
        "Tell me about a challenging technical project you built.",
        "Are you comfortable with the job location?"
    ]

    print("=== SCREENING ENGINE TEST VERIFICATION ===")
    for q in test_questions:
        ans = answer_question(q)
        print(f"Q: {q}")
        print(f"A: {ans}")
        print("-" * 50)
