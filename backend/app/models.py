from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class GithubProfile(BaseModel):
    username: str
    name: Optional[str]
    avatar_url: str
    bio: Optional[str]
    location: Optional[str]
    followers: int
    following: int
    public_repos: int
    created_at: str
    total_stars: int
    total_forks: int

class RepoAnalysis(BaseModel):
    name: str
    description: Optional[str]
    language: Optional[str]
    stars: int
    forks: int

class AICareerRecommendation(BaseModel):
    role: str
    confidence: int

class AIInsight(BaseModel):
    summary: str
    strengths: List[str]
    weaknesses: List[str]
    technical_focus: List[str]
    growth_opportunities: List[str]
    learning_recommendations: List[str]

class AILikelyQuestions(BaseModel):
    questions: List[str]
    topics: List[str]

class AIRepoInsights(BaseModel):
    best_project: str
    best_project_reason: str
    complex_project: str
    complex_project_reason: str

class AnalysisResult(BaseModel):
    profile: GithubProfile
    languages: Dict[str, int]
    top_repos: List[RepoAnalysis]
    score_technical: int
    score_quality: int
    score_consistency: int
    score_impact: int
    score_portfolio: int
    overall_score: int
    developer_level: str
    ai_insights: AIInsight
    career_recommendations: List[AICareerRecommendation]
    interview_prep: AILikelyQuestions
    repo_insights: AIRepoInsights
