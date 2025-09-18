from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder

cv_parser_prompt = PromptTemplate.from_template(
    """You are an expert data extraction agent. Your task is to parse the provided CV text into a structured JSON object.
    
    Extract the following sections precisely: contact_info, summary, experience, education, skills, and projects.
    The 'skills' section should be a list of strings. The 'experience' and 'projects' sections should be a list of objects, each with a 'title' and 'description'.
    
    CV Text:
    ---
    {cv_text}
    ---
    
    JSON Output:
    """
)

skill_analyst_prompt = PromptTemplate.from_template(
    """You are a senior technical recruiter and subject matter expert in AI engineering.
    Analyze the structured CV data below to identify the candidate's skills.
    
    Your task is to:
    1.  List all **explicitly mentioned** technical skills.
    2.  Infer **implicit skills** based on project descriptions and job experiences. For example, a project using FastAPI and PostgreSQL implies skills in "REST APIs" and "Database Management".
    3.  Categorize all skills into logical groups (e.g., 'Programming Languages', 'Frameworks & Libraries', 'Cloud/DevOps', 'Databases').
    
    Structured CV Data:
    ---
    {structured_cv}
    ---
    
    Return a JSON object with keys for explicit, implicit, and categorized skills.
    """
)

market_researcher_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a market intelligence analyst. Your goal is to identify the most in-demand skills for a specific job role by searching online."),
        ("user", "{input}"), 
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

report_generator_prompt = PromptTemplate.from_template(
    """You are an expert career strategist and AI talent advisor.
    Your task is to generate a comprehensive, well-structured report for a technical recruiter.
    
    Synthesize the candidate's skill analysis with the current market demands to create the report.
    The report must be in **Markdown format** and include the following sections:
    
    1.  **## Overall Summary**: A brief, 2-3 sentence executive summary of the candidate's profile and fit for the '{job_role}' role.
    2.  **## Key Strengths**: An analysis of where the candidate's skills strongly align with market demands. Use bullet points.
    3.  **## Skill-Gap Analysis**: A clear identification of which in-demand skills are missing or underdeveloped in the candidate's profile. Use bullet points.
    4.  **## Personalized Upskilling Path**: A practical, actionable plan for the candidate to bridge the identified skill gaps. Suggest specific technologies to learn, potential projects to build, or relevant certifications.
    
    Candidate's Skill Analysis:
    ---
    {skill_analysis}
    ---
    
    Current Market Demands for {job_role}:
    ---
    {market_analysis}
    ---

    **Begin the report directly with the first Markdown heading. Do not include any introductory sentences or conversational phrases.**
    """
)