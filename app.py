import os
import re
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader

# Load environment variables (.env) if present
load_dotenv()

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Resume Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide"
)

# ---------------------------------------------------------
# 1. Maintainable Python Skill Dictionary
# ---------------------------------------------------------
SKILL_DICTIONARY = {
    "Python": {
        "aliases": ["python", "python3", "python 3", "py3"],
        "category": "Programming Languages"
    },
    "Java": {
        "aliases": ["java", "core java", "j2se"],
        "category": "Programming Languages"
    },
    "C++": {
        "aliases": ["c++", "cpp"],
        "category": "Programming Languages"
    },
    "JavaScript": {
        "aliases": ["javascript", "js", "ecmascript", "es6"],
        "category": "Programming Languages"
    },
    "HTML / CSS": {
        "aliases": ["html", "html5", "css", "css3", "html/css"],
        "category": "Web Technologies"
    },
    "SQL": {
        "aliases": ["sql", "mysql", "postgresql", "sqlite", "pl/sql", "ms sql", "transact-sql"],
        "category": "Databases"
    },
    "Git": {
        "aliases": ["git", "github", "gitlab", "version control"],
        "category": "Developer Tools"
    },
    "REST APIs": {
        "aliases": ["rest api", "rest apis", "restful api", "restful apis", "restful web services", "restful service", "rest endpoints", "rest"],
        "category": "Backend Architecture"
    },
    "FastAPI": {
        "aliases": ["fastapi", "fast-api"],
        "category": "Backend Frameworks"
    },
    "Docker": {
        "aliases": ["docker", "dockerfile", "containerization", "docker containers"],
        "category": "DevOps & Deployment"
    },
    "Linux": {
        "aliases": ["linux", "ubuntu", "debian", "centos", "unix bash", "bash scripting"],
        "category": "Operating Systems & Tools"
    },
    "Object-Oriented Programming": {
        "aliases": ["object-oriented programming", "object oriented programming", "oop", "oops", "oop concepts"],
        "category": "Core CS Concepts"
    },
    "Data Structures": {
        "aliases": ["data structures", "algorithms", "dsa", "data structures and algorithms"],
        "category": "Core CS Concepts"
    },
    "Unit Testing": {
        "aliases": ["unit testing", "unit test", "pytest", "unittest", "tdd", "test driven development"],
        "category": "Software Quality"
    },
    "NumPy": {
        "aliases": ["numpy", "np"],
        "category": "Data Science Libraries"
    },
    "Pandas": {
        "aliases": ["pandas", "pd"],
        "category": "Data Science Libraries"
    },
    "Machine Learning": {
        "aliases": ["machine learning", "ml", "supervised learning", "unsupervised learning", "scikit-learn", "sklearn"],
        "category": "Artificial Intelligence"
    },
    "Deep Learning": {
        "aliases": ["deep learning", "neural networks", "tensorflow", "keras", "pytorch"],
        "category": "Artificial Intelligence"
    },
    "Data Analysis": {
        "aliases": ["data analysis", "data analytics", "exploratory data analysis", "eda", "data insights"],
        "category": "Data Science"
    },
    "Data Visualization": {
        "aliases": ["data visualization", "data visualisation", "matplotlib", "seaborn", "charts", "plotly"],
        "category": "Data Science"
    },
    "Excel": {
        "aliases": ["excel", "ms excel", "microsoft excel", "spreadsheets", "vlookup"],
        "category": "Business Tools"
    },
    "Power BI": {
        "aliases": ["power bi", "powerbi"],
        "category": "Business Intelligence"
    },
    "Tableau": {
        "aliases": ["tableau"],
        "category": "Business Intelligence"
    },
    "React": {
        "aliases": ["react", "reactjs", "react.js"],
        "category": "Frontend Frameworks"
    }
}

# ---------------------------------------------------------
# 2. Predefined Python Learning Roadmap Dictionary
# ---------------------------------------------------------
LEARNING_ROADMAP = {
    "REST APIs": {
        "why_it_matters": "Modern web applications communicate using RESTful web services. Python developers must understand how to create and consume API endpoints.",
        "topics_to_study": [
            "HTTP Methods (GET, POST, PUT, DELETE, PATCH)",
            "HTTP Status Codes (200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Internal Server Error)",
            "JSON data serialization and deserialization",
            "Request query parameters, headers, and request bodies",
            "API testing tools (Postman, Thunder Client, or cURL)"
        ],
        "practical_exercise": "Create a simple Python Flask or FastAPI script with 2 GET endpoints and 1 POST endpoint to return and add items in a dictionary.",
        "mini_project": "Student Notes API: Build a CRUD (Create, Read, Update, Delete) RESTful service with SQLite database storage.",
        "priority": "High"
    },
    "Unit Testing": {
        "why_it_matters": "Companies value code reliability and maintainability. Demonstrating automated unit tests sets entry-level candidates apart.",
        "topics_to_study": [
            "Basics of automated testing vs. manual testing",
            "Python's built-in `unittest` module",
            "Writing test assertions with `pytest`",
            "Testing edge cases (empty inputs, invalid data types, boundary values)",
            "Test coverage concepts and mocking basics"
        ],
        "practical_exercise": "Write 5 unit test functions using `pytest` to test a simple calculator module that handles division-by-zero exceptions.",
        "mini_project": "Test Suite for an E-Commerce Cart: Create automated tests checking item addition, discount calculation, and checkout validation.",
        "priority": "High"
    },
    "FastAPI": {
        "why_it_matters": "FastAPI is widely adopted by high-performance Python engineering teams because of automatic OpenAPI documentation and native async support.",
        "topics_to_study": [
            "Path and query parameters in FastAPI",
            "Data validation and schemas with Pydantic",
            "Automatic interactive documentation (Swagger UI at /docs)",
            "Dependency Injection system in FastAPI",
            "Connecting FastAPI with SQLite or PostgreSQL using SQLAlchemy"
        ],
        "practical_exercise": "Build a FastAPI endpoint that accepts a student profile JSON payload, validates the GPA and email format with Pydantic, and returns a greeting.",
        "mini_project": "Job Board API: A FastAPI backend that allows recruiters to post openings and students to query jobs by required skills.",
        "priority": "Medium"
    },
    "Docker": {
        "why_it_matters": "Docker standardizes software execution across development, testing, and production servers, eliminating 'it works on my machine' problems.",
        "topics_to_study": [
            "Containers vs Virtual Machines concepts",
            "Writing a clean `Dockerfile` (FROM, WORKDIR, COPY, RUN, CMD)",
            "Docker CLI commands: `docker build`, `docker run`, `docker ps`, `docker stop`",
            "Port forwarding and mapping between container and host",
            "Docker Compose basics for multi-service applications"
        ],
        "practical_exercise": "Write a `Dockerfile` for a simple Python script, build the image, and run it locally in an isolated container.",
        "mini_project": "Containerized Flask/FastAPI Web App: Package your Python application and run it with a single command.",
        "priority": "Medium"
    },
    "Git": {
        "why_it_matters": "Every engineering team collaborates using version control. Knowing Git commands and branching workflows is mandatory for any developer position.",
        "topics_to_study": [
            "Git repository lifecycle: untracked, staged, committed",
            "Core commands: `git init`, `git add`, `git commit`, `git status`, `git log`",
            "Branching and merging: `git branch`, `git checkout -b`, `git merge`",
            "Resolving merge conflicts calmly",
            "Pushing and pulling to remote repositories on GitHub"
        ],
        "practical_exercise": "Initialize a local Git repository, make three distinct commits, create a feature branch, make a change, and merge it back to main.",
        "mini_project": "Open Source Portfolio: Host all your college projects on GitHub with descriptive README.md files and clean commit histories.",
        "priority": "Critical"
    },
    "SQL": {
        "why_it_matters": "Relational databases store the vast majority of enterprise operational data. Writing queries is crucial for developers and analysts alike.",
        "topics_to_study": [
            "Relational database concepts (Tables, Primary Keys, Foreign Keys)",
            "Data definition & manipulation: CREATE, INSERT, UPDATE, DELETE",
            "Data querying: SELECT, WHERE, ORDER BY, LIMIT",
            "Aggregations: COUNT, SUM, AVG, GROUP BY, HAVING",
            "Relational JOINs: INNER JOIN, LEFT JOIN, RIGHT JOIN"
        ],
        "practical_exercise": "Write a SQL query that retrieves all students who scored above 80% and joins their records with course information.",
        "mini_project": "Library Management Database: Design a normalized schema in MySQL/SQLite with tables for Books, Members, and Loans.",
        "priority": "Critical"
    },
    "Object-Oriented Programming": {
        "why_it_matters": "OOP structures code into reusable, modular objects, making complex systems easier to understand, maintain, and scale.",
        "topics_to_study": [
            "Classes and Objects (`__init__`, self)",
            "Encapsulation (Private attributes, getters and setters)",
            "Inheritance (Base classes, subclasses, `super()`)",
            "Polymorphism (Method overriding and operator overloading)",
            "Composition vs Inheritance"
        ],
        "practical_exercise": "Create a `BankAccount` class with `deposit`, `withdraw`, and `get_balance` methods, handling insufficient funds gracefully.",
        "mini_project": "School Management System: Create classes for `Person`, `Student`, `Teacher`, and `Course` with realistic interactions.",
        "priority": "Critical"
    },
    "Data Structures": {
        "why_it_matters": "Data structures and algorithms form the backbone of efficient problem solving and technical interview assessments.",
        "topics_to_study": [
            "Arrays, Lists, and Dictionaries time complexities",
            "Linked Lists (Singly and Doubly linked)",
            "Stacks and Queues implementation",
            "Binary Trees and Binary Search Trees (BST)",
            "Basic sorting & searching (Binary search, Merge sort)"
        ],
        "practical_exercise": "Implement a Stack data structure in Python with `push`, `pop`, `peek`, and `is_empty` methods.",
        "mini_project": "Expression Evaluator: Write a script that checks for balanced parentheses in mathematical expressions using a stack.",
        "priority": "Critical"
    },
    "NumPy": {
        "why_it_matters": "NumPy powers numerical computing in Python, providing multidimensional arrays and optimized vectorized operations essential for ML and data science.",
        "topics_to_study": [
            "N-dimensional arrays (`ndarray`) vs Python lists",
            "Array creation, indexing, slicing, and reshaping",
            "Vectorized arithmetic operations and broadcasting rules",
            "Statistical methods: mean, median, std, min, max",
            "Linear algebra operations (dot product, matrix multiplication)"
        ],
        "practical_exercise": "Generate a 10x10 matrix of random numbers, compute the column averages, and normalize all values between 0 and 1.",
        "mini_project": "Image Filter using NumPy: Load a grayscale image as a 2D array and apply custom thresholding and blurring filters.",
        "priority": "High"
    },
    "Pandas": {
        "why_it_matters": "Pandas is the industry standard for tabular data manipulation, data cleaning, and feature engineering.",
        "topics_to_study": [
            "Series and DataFrame data structures",
            "Loading CSV, Excel, and JSON data (`read_csv`, `read_excel`)",
            "Filtering, selecting columns, and indexing (`loc`, `iloc`)",
            "Handling missing values (`isna`, `fillna`, `dropna`)",
            "Grouping and aggregation (`groupby`, `pivot_table`)"
        ],
        "practical_exercise": "Load a sample CSV file, calculate summary statistics, replace missing values with the median, and filter rows by condition.",
        "mini_project": "Student Performance Data Analyzer: Analyze grade distribution and identify passing rates across different subjects.",
        "priority": "Critical"
    },
    "Machine Learning": {
        "why_it_matters": "Understanding ML fundamentals enables candidates to build predictive models, automate decision-making, and extract patterns from historical data.",
        "topics_to_study": [
            "Supervised vs Unsupervised learning paradigms",
            "Data preprocessing: scaling, encoding categorical variables",
            "Train-test splitting and cross-validation",
            "Core algorithms: Linear Regression, Logistic Regression, Decision Trees",
            "Evaluation metrics: Accuracy, Precision, Recall, F1-Score, RMSE"
        ],
        "practical_exercise": "Train a Decision Tree Classifier using Scikit-Learn on the Iris dataset and print the classification report.",
        "mini_project": "House Price Predictor: Build a linear regression model predicting housing prices based on features like area and bedrooms.",
        "priority": "High"
    },
    "Data Visualization": {
        "why_it_matters": "Data findings are only valuable if stakeholders can understand them. Charts and visual dashboards communicate complex patterns clearly.",
        "topics_to_study": [
            "Choosing the right chart: bar, line, scatter, histogram, heatmap",
            "Matplotlib basics (figures, axes, labels, titles, legends)",
            "Seaborn statistical graphics (pairplots, boxplots, countplots)",
            "Interactive dashboards with Streamlit or Plotly",
            "Color theory and accessibility in chart design"
        ],
        "practical_exercise": "Plot a histogram and boxplot comparing exam marks across two student batches with proper titles and labels.",
        "mini_project": "COVID-19 / Sales Interactive Dashboard: Create a multi-chart interactive Streamlit dashboard.",
        "priority": "Medium"
    },
    "Data Analysis": {
        "why_it_matters": "Companies collect massive amounts of operational data. Analysts turn raw logs into actionable business insights.",
        "topics_to_study": [
            "Exploratory Data Analysis (EDA) process and mindset",
            "Identifying trends, outliers, and data anomalies",
            "Formulating business hypotheses and validating with data",
            "Correlation analysis vs Causation",
            "Presenting analytical conclusions to non-technical audiences"
        ],
        "practical_exercise": "Perform EDA on a retail sales dataset and write a 1-page bulleted summary of the top-performing products and peak hours.",
        "mini_project": "E-Commerce Customer Churn Analysis: Analyze customer purchase histories to discover factors driving cancellation.",
        "priority": "High"
    },
    "Linux": {
        "why_it_matters": "Most cloud servers, containers, and deployment systems run on Linux. Basic command-line proficiency is expected of every technical recruit.",
        "topics_to_study": [
            "File system navigation (`ls`, `cd`, `pwd`, `mkdir`, `rm`)",
            "File viewing and text search (`cat`, `less`, `grep`, `head`, `tail`)",
            "File permissions (`chmod`, `chown`)",
            "Process management (`ps`, `top`, `kill`)",
            "Basic bash automation scripts"
        ],
        "practical_exercise": "Write a 5-line bash script that backs up a directory to a zip file and logs the current date and time.",
        "mini_project": "Server Log Monitor Script: A script that parses access logs and flags IP addresses with excessive 404 errors.",
        "priority": "Medium"
    },
    "HTML / CSS": {
        "why_it_matters": "HTML and CSS form the foundational visual presentation layer of every website and web-based application.",
        "topics_to_study": [
            "Semantic HTML5 elements (header, nav, section, article, footer)",
            "CSS Box Model (margin, border, padding, content)",
            "Flexbox and CSS Grid layout systems",
            "Responsive design and media queries for mobile devices",
            "CSS custom properties (variables) and modern transitions"
        ],
        "practical_exercise": "Build a responsive two-column product card that adapts gracefully to mobile screen widths.",
        "mini_project": "Responsive Portfolio Landing Page: Showcase your resume and academic projects.",
        "priority": "Medium"
    },
    "JavaScript": {
        "why_it_matters": "JavaScript is the primary programming language of the interactive web, running in all modern browsers and on server environments (Node.js).",
        "topics_to_study": [
            "ES6+ syntax: `let`/`const`, arrow functions, template literals, destructuring",
            "DOM selection and manipulation (`querySelector`, event listeners)",
            "Asynchronous JavaScript: Promises, `async`/`await`, `fetch` API",
            "Array methods: `map()`, `filter()`, `reduce()`, `forEach()`",
            "JSON handling and error handling with `try...catch`"
        ],
        "practical_exercise": "Build an interactive Todo application with add, toggle, and delete functionality in vanilla JavaScript.",
        "mini_project": "Interactive Weather Widget: Fetch current weather data from OpenWeather API and update the UI asynchronously.",
        "priority": "High"
    }
}

# ---------------------------------------------------------
# 3. Excel Spreadsheet Loader & Parser
# ---------------------------------------------------------
def load_requirements_from_excel(filepath: str = "company_requirements.xlsx") -> tuple[pd.DataFrame, str]:
    """Reads company job requirements from the Excel spreadsheet.
    Returns (DataFrame, error_message).
    """
    if not os.path.exists(filepath):
        return pd.DataFrame(), f"Requirements spreadsheet `{filepath}` not found in project directory."
    try:
        df = pd.read_excel(filepath)
        required_columns = [
            "Company Name", "Job Role", "Job Description",
            "Required Skills", "Preferred Skills", "Qualification", "Experience Level"
        ]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return pd.DataFrame(), f"The Excel file is missing required columns: {missing_columns}"
        return df, ""
    except Exception as e:
        return pd.DataFrame(), f"Error reading Excel file: {str(e)}"


def parse_comma_separated_skills(cell_value) -> list[str]:
    """Safely parses comma-separated skills from an Excel cell into a clean list."""
    if pd.isna(cell_value) or not str(cell_value).strip():
        return []
    return [skill.strip() for skill in str(cell_value).split(",") if skill.strip()]


# ---------------------------------------------------------
# 4. PDF Resume Text Extraction Helper
# ---------------------------------------------------------
def extract_text_from_pdf(pdf_file) -> tuple[str, str]:
    """Extracts text from an uploaded PDF resume using PyPDF.
    Returns (extracted_text, error_message).
    """
    try:
        reader = PdfReader(pdf_file)
        if len(reader.pages) == 0:
            return "", "The uploaded PDF has 0 pages."

        extracted_text = []
        for idx, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            if page_text.strip():
                extracted_text.append(f"--- Page {idx + 1} ---\n{page_text}")

        full_text = "\n\n".join(extracted_text).strip()
        if not full_text:
            return "", (
                "No readable text could be extracted. The file may be an image-only/scanned PDF, "
                "or encrypted. Note: Scanned image resumes are not supported in this version."
            )
        return full_text, ""
    except Exception as e:
        return "", f"Error reading PDF: {str(e)}"


# ---------------------------------------------------------
# 5. Normalized Skill Extraction Engine (Regex Word-Boundaries)
# ---------------------------------------------------------
def extract_skills_from_text(text: str, skill_dict: dict) -> dict:
    """Scans resume text using word boundaries and aliases from SKILL_DICTIONARY.
    Prevents false positives (e.g., 'c' in 'cloud', 'git' in 'digital', 'rest' in 'restaurant').
    Returns {skill_name: [matched_aliases]}.
    """
    if not text:
        return {}

    detected_skills = {}
    for skill_name, data in skill_dict.items():
        aliases = data.get("aliases", [skill_name])
        matched_instances = []
        for alias in aliases:
            # Word boundary matching: (?<!\w) at start and (?!\w) at end
            pattern = r"(?<!\w)" + re.escape(alias.strip()) + r"(?!\w)"
            if re.search(pattern, text, re.IGNORECASE):
                matched_instances.append(alias)

        if matched_instances:
            detected_skills[skill_name] = matched_instances

    return detected_skills


# ---------------------------------------------------------
# 6. Optional AI Mentor (Google Gemini)
# ---------------------------------------------------------
def generate_gemini_study_plan(role_name: str, company_name: str, missing_skills: list, resume_text: str, api_key: str) -> str:
    """Calls Google Gemini to generate a personalized study plan for missing skills."""
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an encouraging academic career mentor. Evaluate a student's resume against "
            "the requirements of '{company_name}' for the position of '{role_name}'.\n"
            "Missing Skills to Bridge: {missing_skills}\n\n"
            "Format your advice clearly with:\n"
            "1. Realistic Assessment of the Student's Starting Point\n"
            "2. Tailored 4-Week Action Plan targeting the missing skills\n"
            "3. Suggested Portfolio Mini-Project showcasing the missing skills\n"
            "Keep the tone supportive, academic, and realistic for a college student."
        ),
        ("human", "Here is my extracted resume text:\n{resume_text}")
    ])

    candidate_models = ["gemini-flash-lite-latest", "gemini-3-flash-preview", "gemini-flash-latest"]
    last_error = None
    for model_name in candidate_models:
        try:
            llm = ChatGoogleGenerativeAI(google_api_key=api_key, model=model_name, temperature=0.2)
            chain = prompt | llm | StrOutputParser()
            res = chain.invoke({
                "company_name": company_name,
                "role_name": role_name,
                "missing_skills": ", ".join(missing_skills),
                "resume_text": resume_text[:3000]
            })
            return str(res)
        except Exception as e:
            last_error = e
            continue

    raise last_error if last_error else RuntimeError("Could not connect to Gemini models.")


# ---------------------------------------------------------
# 7. Main Application Logic
# ---------------------------------------------------------
def main():
    # Sidebar Controls
    st.sidebar.title("⚙️ Project Controls")
    st.sidebar.markdown("**Resume Skill Gap Analyzer**")
    st.sidebar.caption("NTCC BCA Project | Excel + Rule-Based + Optional Gemini")

    # Optional Google Gemini Key
    env_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or ""
    user_gemini_key = st.sidebar.text_input(
        "Google API Key (Optional for AI Advice)",
        value=env_key,
        type="password",
        help="Core skill gap analysis works 100% offline. Adding a key enables the AI study plan generator."
    )
    active_gemini_key = user_gemini_key.strip() if user_gemini_key else ""

    st.sidebar.markdown("---")
    st.sidebar.info(
        "📊 **Excel Requirements Source:**\n\n"
        "Job specifications are loaded directly from `company_requirements.xlsx`. "
        "You can add or modify roles in Excel without editing code."
    )

    if st.sidebar.button("🔄 Reset Project"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    # Header
    st.title("🎯 AI-Powered Company Requirement-Based Resume Skill Gap Analyzer")
    st.markdown(
        "An educational career-readiness tool that benchmarks a student's PDF resume against "
        "predefined company job requirements maintained in an **Excel spreadsheet** (`company_requirements.xlsx`)."
    )

    # Mandatory Educational Disclaimer
    st.warning(
        "⚠️ **Educational Assessment Notice:** This system is an educational readiness comparator designed to help "
        "students discover topics to study. The match percentage is a skill-coverage indicator, **not** an official "
        "company hiring score or automated ATS rejection algorithm."
    )

    st.markdown("---")

    # Step 1: Load Company Requirements from Excel
    st.subheader("1️⃣ Select Company & Job Role Requirements (From Excel)")

    df_companies, excel_err = load_requirements_from_excel("company_requirements.xlsx")
    if excel_err:
        st.error(f"❌ {excel_err}")
        st.stop()

    if df_companies.empty:
        st.error("❌ The `company_requirements.xlsx` file is empty. Please add job roles to the spreadsheet.")
        st.stop()

    # Company selection
    unique_companies = sorted(df_companies["Company Name"].dropna().unique().tolist())
    col_comp, col_role = st.columns(2)

    with col_comp:
        selected_company = st.selectbox("Select Target Company:", unique_companies, index=0)

    # Filter roles by selected company
    company_roles_df = df_companies[df_companies["Company Name"] == selected_company]
    available_roles = sorted(company_roles_df["Job Role"].dropna().unique().tolist())

    with col_role:
        selected_role = st.selectbox("Select Offered Job Role:", available_roles, index=0)

    # Extract target role row
    role_row = company_roles_df[company_roles_df["Job Role"] == selected_role].iloc[0]

    # Parse comma-separated skills
    req_skills = parse_comma_separated_skills(role_row.get("Required Skills", ""))
    pref_skills = parse_comma_separated_skills(role_row.get("Preferred Skills", ""))
    job_desc = str(role_row.get("Job Description", "No description provided."))
    qualification = str(role_row.get("Qualification", "Not Specified"))
    experience = str(role_row.get("Experience Level", "Not Specified"))

    # Display Target Role Card
    with st.container():
        st.markdown(f"#### 🏢 **{selected_company}** — *{selected_role}*")
        st.caption(job_desc)

        c_meta1, c_meta2 = st.columns(2)
        c_meta1.markdown(f"🎓 **Expected Qualification:** `{qualification}`")
        c_meta2.markdown(f"⏳ **Expected Experience:** `{experience}`")

        st.markdown("**📌 Mandatory Required Skills:** " + (" ".join([f"`{s}`" for s in req_skills]) if req_skills else "*None specified*"))
        if pref_skills:
            st.markdown("**⭐ Preferred / Bonus Skills:** " + " ".join([f"`{s}`" for s in pref_skills]))

    st.markdown("---")

    # Step 2: Student Resume Upload
    st.subheader("2️⃣ Student Resume Input")

    tab_upload, tab_demos = st.tabs(["📤 Upload Your Resume (PDF)", "🧪 Load Test Resumes (For College Viva Demo)"])

    uploaded_pdf = None
    demo_choice = None

    with tab_upload:
        user_file = st.file_uploader(
            "Upload your resume in PDF format:",
            type=["pdf"],
            help="Please upload a digital text-based PDF resume."
        )
        if user_file:
            uploaded_pdf = user_file

    with tab_demos:
        st.caption("Click any sample resume to test diverse evaluation scenarios live during evaluation:")
        demo_cols = st.columns(4)
        if demo_cols[0].button("📄 High Match Resume\n(Rohan Sharma)", use_container_width=True):
            demo_choice = "sample_resume_match.pdf"
        if demo_cols[1].button("📄 Partial Match Resume\n(Priya Patel)", use_container_width=True):
            demo_choice = "sample_resume_partial.pdf"
        if demo_cols[2].button("📄 Non-Match Resume\n(Amit Verma)", use_container_width=True):
            demo_choice = "sample_resume_nonmatch.pdf"
        if demo_cols[3].button("📄 Blank/Empty PDF\n(Error Test)", use_container_width=True):
            demo_choice = "sample_resume_blank.pdf"

    if demo_choice:
        st.session_state["active_demo_file"] = demo_choice

    active_pdf_source = uploaded_pdf or st.session_state.get("active_demo_file", None)

    if active_pdf_source is None:
        st.info("👈 Please upload a PDF resume or click one of the sample test resumes above to begin.")
        st.stop()

    if isinstance(active_pdf_source, str):
        file_display_name = active_pdf_source
        with open(active_pdf_source, "rb") as f:
            resume_text, extract_err = extract_text_from_pdf(f)
    else:
        file_display_name = active_pdf_source.name
        resume_text, extract_err = extract_text_from_pdf(active_pdf_source)

    if extract_err:
        st.error(f"❌ {extract_err}")
        st.stop()

    st.success(f"✅ Successfully loaded and extracted text from: `{file_display_name}` ({len(resume_text)} characters)")

    with st.expander("🔍 View Extracted Resume Plain Text"):
        st.text_area("Extracted Text", resume_text, height=180, disabled=True)

    st.markdown("---")

    # Step 3: Skill Extraction Engine
    st.subheader("3️⃣ Normalized Skill Extraction Engine")

    all_detected_skills = extract_skills_from_text(resume_text, SKILL_DICTIONARY)

    st.markdown(f"**Identified Skills Across Resume ({len(all_detected_skills)} total):**")
    if all_detected_skills:
        skill_chips = [f"`{s}`" for s in all_detected_skills.keys()]
        st.markdown(" ".join(skill_chips))
    else:
        st.warning("No technical skills from the standard dictionary were identified in this resume.")

    st.markdown("---")

    # Step 4: Skill Gap Comparison & Match Calculation
    st.subheader("4️⃣ Company Requirement Skill Gap Analysis")

    matched_required = [s for s in req_skills if s in all_detected_skills]
    missing_required = [s for s in req_skills if s not in all_detected_skills]

    matched_preferred = [s for s in pref_skills if s in all_detected_skills]
    missing_preferred = [s for s in pref_skills if s not in all_detected_skills]

    total_req = len(req_skills)
    matched_req_count = len(matched_required)
    match_percentage = round((matched_req_count / total_req) * 100, 1) if total_req > 0 else 0.0

    # Metrics
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Target Company", selected_company)
    m_col2.metric("Target Role", selected_role)
    m_col3.metric("Required Skills Matched", f"{matched_req_count} / {total_req}")
    m_col4.metric("Required Match Score", f"{match_percentage}%")

    st.progress(match_percentage / 100.0)

    # Build Comparison Table with Pandas
    table_rows = []
    for skill in req_skills:
        status = "✅ Demonstrated" if skill in matched_required else "❌ Missing / Not Found"
        action = "None (Skill Verified)" if skill in matched_required else "Study & Build Project"
        cat = SKILL_DICTIONARY.get(skill, {}).get("category", "General")
        table_rows.append({
            "Skill Name": skill,
            "Category": cat,
            "Requirement Type": "Mandatory Required",
            "Demonstrated in Resume": status,
            "Action Recommended": action
        })

    for skill in pref_skills:
        status = "⭐ Demonstrated (Bonus)" if skill in matched_preferred else "⭕ Optional Gap"
        action = "None (Bonus Strength)" if skill in matched_preferred else "Recommended Optional Study"
        cat = SKILL_DICTIONARY.get(skill, {}).get("category", "General")
        table_rows.append({
            "Skill Name": skill,
            "Category": cat,
            "Requirement Type": "Preferred (Bonus)",
            "Demonstrated in Resume": status,
            "Action Recommended": action
        })

    df_comparison = pd.DataFrame(table_rows)
    st.dataframe(df_comparison, use_container_width=True, hide_index=True)

    # Breakdown in Columns
    col_req_pass, col_req_miss = st.columns(2)

    with col_req_pass:
        st.success(f"**✅ Demonstrated Required Skills ({len(matched_required)}):**")
        if matched_required:
            for s in matched_required:
                aliases_used = ", ".join(all_detected_skills[s])
                st.write(f"- **{s}** *(matched keywords: `{aliases_used}`)*")
        else:
            st.write("None of the mandatory required skills were identified.")

    with col_req_miss:
        st.error(f"**❌ Missing Required Skills ({len(missing_required)}):**")
        if missing_required:
            for s in missing_required:
                st.write(f"- **{s}** *(Action: Must bridge this gap)*")
        else:
            st.write("🎉 Excellent! All mandatory required skills are demonstrated in the resume.")

    if pref_skills:
        st.caption("ℹ️ *Note: Preferred skills indicate additional strengths but do not compensate for missing mandatory required skills.*")

    st.markdown("---")

    # Step 5: Personalized Learning Roadmaps (Offline + AI)
    st.subheader("5️⃣ Personalized Learning Roadmaps & Study Checklist")

    if not missing_required:
        st.balloons()
        st.success("🌟 Outstanding! Your resume satisfies all mandatory required skills for this role. Consider exploring preferred skills to further stand out.")
    else:
        st.markdown(
            f"To improve your profile for **{selected_company} — {selected_role}**, "
            f"focus on bridging these **{len(missing_required)} missing required skills**:"
        )

        for skill in missing_required:
            roadmap = LEARNING_ROADMAP.get(skill, None)
            priority = roadmap.get("priority", "High") if roadmap else "High"
            priority_color = "red" if priority == "Critical" else ("orange" if priority == "High" else "blue")

            with st.expander(f"📘 Learn **{skill}** — Priority: :{priority_color}[{priority}]", expanded=True):
                if roadmap:
                    st.markdown(f"**Why this skill matters for {selected_role}:**")
                    st.info(roadmap.get("why_it_matters", "Essential requirement for this role."))

                    col_top, col_prac = st.columns(2)
                    with col_top:
                        st.markdown("**📚 Core Topics to Study:**")
                        for t in roadmap.get("topics_to_study", []):
                            st.write(f"- {t}")

                    with col_prac:
                        st.markdown("**🛠️ Practical Exercise:**")
                        st.write(roadmap.get("practical_exercise", "Implement small scripts."))

                        st.markdown("**🚀 Mini-Project Idea:**")
                        st.write(roadmap.get("mini_project", "Build an end-to-end project."))
                else:
                    st.write(f"Study core documentation, tutorials, and practical projects for **{skill}**.")

                st.checkbox(f"Mark as Completed: I have learned & built a project in **{skill}**", key=f"check_{skill}")

    # Optional AI Mentor Feature
    st.markdown("---")
    st.subheader("🤖 AI Career Mentor Advice (Optional)")

    if active_gemini_key:
        if st.button("✨ Generate AI Career Mentor Study Plan (Google Gemini)", type="primary"):
            with st.spinner("Analyzing resume against company specifications with Google Gemini..."):
                try:
                    ai_advice = generate_gemini_study_plan(
                        role_name=selected_role,
                        company_name=selected_company,
                        missing_skills=missing_required if missing_required else ["Advanced optimization"],
                        resume_text=resume_text,
                        api_key=active_gemini_key
                    )
                    st.markdown("### 📋 Mentor Evaluation Report")
                    st.markdown(ai_advice)
                except Exception as e:
                    st.error(f"Error calling Gemini: {str(e)}")
    else:
        st.caption("💡 Enter your Google API Key in the left sidebar to unlock personalized AI mentor study advice.")

    # Footer
    st.markdown("---")
    st.caption(
        "AI-Powered Company Requirement-Based Resume Skill Gap Analyzer | NTCC BCA Project | "
        "Excel Spreadsheet Driven & Rule-Based Matching"
    )


if __name__ == "__main__":
    main()
