import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_developer_insights(profile_data: dict, repos_data: list) -> dict:
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        return get_fallback_insights(profile_data)
        
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    Act as a Senior Technical Recruiter and AI Engineering Manager.
    Analyze this GitHub developer profile and their top repositories.
    
    Profile: {json.dumps(profile_data)}
    Top Repositories (summary): {json.dumps([{'name': r['name'], 'desc': r['description'], 'lang': r['language'], 'stars': r['stargazers_count']} for r in repos_data[:10]])}
    
    Provide a detailed JSON response matching EXACTLY this structure:
    {{
      "summary": "2-3 sentences summarizing the developer's expertise and value.",
      "strengths": ["str1", "str2", "str3", "str4"],
      "weaknesses": ["str1", "str2"],
      "technical_focus": ["str1", "str2", "str3"],
      "growth_opportunities": ["str1", "str2"],
      "learning_recommendations": ["str1", "str2"],
      "career_recommendations": [
         {{"role": "Role Name", "confidence": 85}},
         {{"role": "Role Name", "confidence": 75}},
         {{"role": "Role Name", "confidence": 65}},
         {{"role": "Role Name", "confidence": 55}}
      ],
      "interview_prep": {{
         "questions": ["Specific technical question 1 based on their repos", "Specific architectural question 2", "Specific problem-solving question 3"],
         "topics": ["topic1", "topic2", "topic3", "topic4"]
      }},
      "repo_insights": {{
         "best_project": "exact_repo_name",
         "best_project_reason": "detailed reason why this stands out",
         "complex_project": "exact_repo_name",
         "complex_project_reason": "detailed reason why this is complex"
      }}
    }}
    
    Make sure to provide at least 4-5 different career_recommendations with varied percentages.
    The interview_prep should contain highly specific technical questions tailored to the exact languages and frameworks they use in their repositories. This is meant to help the developer prepare for an actual technical interview.
    """
    
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return get_fallback_insights(profile_data)

def get_fallback_insights(profile_data):
    return {
        "summary": "A developer active on GitHub with a variety of projects.",
        "strengths": ["Version Control", "Open Source Activity"],
        "weaknesses": ["Needs more data to analyze"],
        "technical_focus": ["Full Stack Development"],
        "growth_opportunities": ["Contribute to larger open source projects"],
        "learning_recommendations": ["Advanced System Design"],
        "career_recommendations": [
            {"role": "Software Engineer", "confidence": 80},
            {"role": "Backend Developer", "confidence": 70},
            {"role": "Frontend Developer", "confidence": 65},
            {"role": "Data Analyst", "confidence": 50}
        ],
        "interview_prep": {
            "questions": ["Explain your most complex GitHub project.", "How do you manage state in your applications?", "Describe a time you optimized code performance."],
            "topics": ["Data Structures", "Algorithms", "System Design"]
        },
        "repo_insights": {
            "best_project": "N/A",
            "best_project_reason": "Not enough AI data",
            "complex_project": "N/A",
            "complex_project_reason": "Not enough AI data"
        }
    }
