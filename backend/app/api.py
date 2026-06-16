from fastapi import APIRouter, HTTPException
from collections import Counter
from app.models import AnalysisResult, GithubProfile, RepoAnalysis, AIInsight, AICareerRecommendation, AILikelyQuestions, AIRepoInsights
from app.github_service import fetch_github_user, fetch_github_repos
from app.ai_service import generate_developer_insights

router = APIRouter()

@router.get("/analyze/{username}", response_model=AnalysisResult)
async def analyze_github_profile(username: str):
    try:
        user_data = fetch_github_user(username)
    except ValueError:
        raise HTTPException(status_code=404, detail="GitHub user not found")
        
    repos_data = fetch_github_repos(username)
    
    total_stars = sum(r.get("stargazers_count", 0) for r in repos_data)
    total_forks = sum(r.get("forks_count", 0) for r in repos_data)
    
    languages = [r["language"] for r in repos_data if r.get("language")]
    lang_counts = dict(Counter(languages))
    
    top_repos = sorted(repos_data, key=lambda x: x.get("stargazers_count", 0), reverse=True)[:5]
    top_repos_formatted = [
        RepoAnalysis(
            name=r["name"],
            description=r.get("description"),
            language=r.get("language"),
            stars=r.get("stargazers_count", 0),
            forks=r.get("forks_count", 0)
        ) for r in top_repos
    ]
    
    ai_data = generate_developer_insights(user_data, repos_data)
    
    # Calculate recruiter scores (mocked based on basic metrics for now, enhanced by AI theoretically)
    score_technical = min(100, len(lang_counts) * 10 + (total_stars * 2))
    score_quality = min(100, (total_stars / max(1, len(repos_data))) * 10)
    score_consistency = min(100, user_data.get("public_repos", 0) * 2)
    score_impact = min(100, total_forks * 5 + user_data.get("followers", 0) * 2)
    score_portfolio = min(100, (score_technical + score_quality + score_impact) // 3)
    overall_score = (score_technical + score_quality + score_consistency + score_impact + score_portfolio) // 5
    
    if overall_score > 85: level = "Open Source Veteran"
    elif overall_score > 70: level = "Senior Potential"
    elif overall_score > 50: level = "Strong Contributor"
    elif overall_score > 30: level = "Emerging Talent"
    else: level = "Beginner"
    
    profile = GithubProfile(
        username=user_data["login"],
        name=user_data.get("name"),
        avatar_url=user_data["avatar_url"],
        bio=user_data.get("bio"),
        location=user_data.get("location"),
        followers=user_data.get("followers", 0),
        following=user_data.get("following", 0),
        public_repos=user_data.get("public_repos", 0),
        created_at=user_data["created_at"],
        total_stars=total_stars,
        total_forks=total_forks
    )
    
    return AnalysisResult(
        profile=profile,
        languages=lang_counts,
        top_repos=top_repos_formatted,
        score_technical=int(score_technical),
        score_quality=int(score_quality),
        score_consistency=int(score_consistency),
        score_impact=int(score_impact),
        score_portfolio=int(score_portfolio),
        overall_score=int(overall_score),
        developer_level=level,
        ai_insights=AIInsight(**ai_data),
        career_recommendations=[AICareerRecommendation(**rec) for rec in ai_data.get("career_recommendations", [])],
        interview_prep=AILikelyQuestions(**ai_data.get("interview_prep", {})),
        repo_insights=AIRepoInsights(**ai_data.get("repo_insights", {}))
    )
