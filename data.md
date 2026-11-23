# Candidate Profile & Form-Filling Knowledge Base

Use this file to populate all application form fields, file uploads, and screening questions.
Every agent (Claude, Codex, OpenCode) must read from this file.

---

## 1. Basic Personal Information

| Field | Value |
| :--- | :--- |
| **First Name** | Vansh |
| **Last Name** | Sharma |
| **Full Name** | Vansh Sharma |
| **Email** | engagevansh@gmail.com |
| **Phone (Full with Country Code)** | `+919368478556` (Use when single input field) |
| **Phone (Clean 10-Digits)** | `9368478556` (Use when Country Code dropdown exists) |
| **Country Code** | +91 (India) |
| **Current City / State** | Dehradun / Delhi NCR, India |
| **Country** | India |
| **Postal / ZIP Code** | 248001 |
| **LinkedIn URL** | https://linkedin.com/in/vnxsh |
| **GitHub URL** | https://github.com/Vansh-Sharmaa |
| **Portfolio / Website** | https://github.com/Vansh-Sharmaa |
| **Resume PDF File Path** | `D:\improved resume\Vansh_Sharma_Resume.pdf` (Base) |
| **Dynamic Tailored Resumes** | `D:\improved resume\tailored\` (Generated via `tailor_resume.py`) |

---

## 1.5. Strict Resume Relevance & Matching Filter (MANDATORY FOR ALL AGENTS)

Every agent must evaluate each job description against `D:\improved resume\Vansh_Sharma_Resume.pdf` before applying:

### ✅ APPLY ONLY IF MATCHES:
1. **Target Roles:** AI Engineer, GenAI Engineer, Machine Learning Engineer, Python AI Developer, LLM Engineer, RAG Engineer, Data Scientist (Junior/Associate).
2. **Core Tech Stack Match (Must match at least 2):**
   - Python
   - LLMs / Generative AI / RAG / LangChain / LangGraph
   - Vector Databases / FAISS / Semantic Search
   - PyTorch / scikit-learn / Machine Learning
   - FastAPI / Backend APIs
3. **Experience Requirement:** 0–2 years, Entry-Level, Associate, Graduate, or Not Specified.

### ❌ REJECT / SKIP IMMEDIATELY IF:
1. Demands **3+ or 5+ years** of professional experience (senior / staff / lead roles).
2. Non-technical roles (Sales, BPO, HR, Digital Marketing, Support).
3. Unrelated stacks (Java/Spring Boot only, Frontend React-only, C#/.NET only, PHP only).
4. Unpaid internships or shady consultancies asking for registration fees.
5. **Tier-1 Cool-Off Protection:** Google, Microsoft, Amazon, Meta, Apple, Uber, Razorpay, Swiggy, Zomato (Strict 6-month cool-off period; apply to them via manual referral only).

---

## 2. Education Details

| Field | Value |
| :--- | :--- |
| **Master's Degree** | Master of Computer Applications (MCA) |
| **Specialization** | Artificial Intelligence & Data Science |
| **University / Institute** | Graphic Era Hill University |
| **Graduation Year** | 2024 – 2026 (Final Year / Passing 2026) |
| **CGPA / Score** | 8.0 / 10 |
| **Bachelor's Degree** | Bachelor of Computer Applications (BCA) |
| **University / Institute** | DIT University |
| **Graduation Year** | 2021 – 2024 |
| **CGPA / Score** | 7.7 / 10 |

---

## 3. Standard Dropdown & Radio Button Answers

* **Are you legally authorized to work in India?** $\rightarrow$ **Yes**
* **Will you now or in the future require visa sponsorship?** $\rightarrow$ **No**
* **Notice Period / Availability:** $\rightarrow$ **Immediate (0 days / Can join immediately)**
* **Willing to relocate?** $\rightarrow$ **Yes**
* **Preferred Locations:** $\rightarrow$ **Remote, Bengaluru, Noida, Gurgaon, Delhi NCR, Hyderabad, Pune**
* **Work Mode:** $\rightarrow$ **Open to Remote, Hybrid, or On-site**
* **Employment Type:** $\rightarrow$ **Full-Time, Internship, or Contract**
* **Gender:** $\rightarrow$ **Male** *(or "Prefer not to say" if optional)*
* **Veteran / Disability status:** $\rightarrow$ **No / None**

---

## 4. Technical Skill Experience Numbers

When forms ask "How many years of experience do you have with [Skill]?":

| Technology | Numeric Value to Enter |
| :--- | :--- |
| **Python** | 3 years |
| **PyTorch / Machine Learning** | 2 years |
| **LangChain / LangGraph / Agents** | 1 year |
| **RAG / Vector Databases (FAISS)** | 1 year |
| **FastAPI / REST APIs** | 2 years |
| **SQL / Databases (PostgreSQL, MySQL)** | 2 years |
| **Git / GitHub** | 3 years |
| **Docker** | 1 year |
| **Total Professional Experience** | 0 to 1 year *(Fresher / Entry Level)* |

---

## 5. Compensation & Salary Expectations

* **Expected CTC (INR):** ₹6,00,000 - ₹9,00,000 per annum *(or enter `700000` / `Negotiable`)*
* **Expected Salary (USD / Global):** $25,000 - $40,000 / year *(or `Flexible based on role`)*
* **Current CTC:** `0` or `Fresher / Student`

---

## 6. Human-Sounding Screening Questions (ZERO-AI FOOTPRINT RULEBOOK)

> 🚫 **HARD NEGATIVE CONSTRAINTS (INSTANT FAIL IF VIOLATED):**
> 1. **Punctuation Tells:** NEVER use em-dashes (` - `) or en-dashes (`–`). Human engineers use commas, hyphens (`-`), colons, or parentheses.
> 2. **Banned AI Vocabulary:** NEVER use words like *delve, testament, tapestry, spearhead, robust, seamless, seamlessly, leverage, leveraging, foster, beacon, pivotal, crucial, revolutionize, thrilled, esteemed, elevate, multifaceted, paramount, furthermore, moreover, synergy*.
> 3. **Banned Greetings:** NEVER start with *"I hope this message finds you well"*, *"As an ambitious AI enthusiast"*, or *"It is with great enthusiasm that I write to apply"*.
> 4. **Banned Formatting:** Never use excessive bullet points or numbered lists inside small text boxes. Write in 2-3 short, clean sentences.
> 5. **Engineer Voice:** Write like a real developer talking in a Slack channel: direct, technical, humble, confident, focused on code, latency, and features.

### Q: "Why do you want to join our company?"
> *"I've been tracking what your team is building with applied AI, and I want to work somewhere engineering quality and shipping fast matter more than corporate bureaucracy. My background is in production RAG systems, LangGraph agent workflows, and ML feature pipelines. I want to jump in, take ownership of messy problems, and build features that users actually use."*

### Q: "Describe your experience with LLMs / GenAI / RAG."
> *"I build multi-agent systems and RAG pipelines end-to-end. In ResearchMind, I built a LangGraph state graph orchestrating 4 specialized agents (Search, Scrape, Writer, Critic) with automated reflection loops. In LexAI, I implemented a Map-Reduce summarization chain for 10k+ word legal contracts and FAISS semantic vector search with all-MiniLM-L6-v2 embeddings to ground LLM outputs and eliminate hallucinations."*

### Q: "Tell me about a challenging technical project you built."
> *"I built FileGenie, a content-based file classification and security engine. Traditional tools only check file extensions, which fails when executables are renamed to .pdf. I built a 16-dimensional feature extraction pipeline calculating Shannon Entropy, raw binary magic bytes, and null-byte distributions, training a 300-tree Random Forest classifier in scikit-learn that achieves 95%+ accuracy in under 1ms on a CPU. It taught me how to combine ML theory with high-throughput FastAPI streaming."*

### Q: "Tell us about yourself / Short Bio."
> *"I am an AI/ML Engineer completing my MCA in AI & Data Science. I focus on practical GenAI: multi-agent orchestration in LangGraph, Retrieval-Augmented Generation with vector databases, and full-stack deployment using FastAPI and Python. I prefer building working prototypes and reliable pipelines over just calling standard API endpoints."*

### Q: Short Cover Note / Quick Message to Recruiter
> *"Hi team, I saw your opening for an AI Engineer and wanted to reach out. I have hands-on experience building LangGraph agent pipelines, FAISS vector search systems, and production FastAPI services. My code and architecture designs are public on my GitHub (github.com/Vansh-Sharmaa), and my resume is attached. Would love the chance to connect if my background fits what you're building."*
