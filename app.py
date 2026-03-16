import streamlit as st
import pandas as pd
import plotly.express as px
from github_api import get_user_profile, get_repositories
from analyzer import analyze_repos

st.set_page_config(page_title="GitHub Intelligence Analyzer", layout="wide")

st.title("🚀 GitHub Developer Intelligence Analyzer")

username = st.text_input("Enter GitHub Username")

if username:

    profile = get_user_profile(username)

    if not profile:
        st.error("User not found")
        st.stop()

    repos = get_repositories(username)

    stats = analyze_repos(repos, profile["followers"])

    # Profile section
    col1, col2 = st.columns([1,3])

    with col1:
        st.image(profile["avatar_url"], width=120)

    with col2:
        st.subheader(profile["name"])
        st.write(profile["bio"])
        st.write("Followers:", profile["followers"])
        st.write("Following:", profile["following"])

    # Developer metrics
    st.subheader("📊 Developer Statistics")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Repositories", stats["repos"])
    c2.metric("Stars", stats["stars"])
    c3.metric("Forks", stats["forks"])
    c4.metric("Developer Score", round(stats["score"]))

    st.success(f"Developer Level: {stats['level']}")

    # Skill Extraction
    st.subheader("🧠 Extracted Skills")

    if stats["skills"]:
        st.write(", ".join(stats["skills"]))
    else:
        st.write("No languages detected")

    # Language chart
    st.subheader("💻 Language Distribution")

    df_lang = pd.DataFrame(
        stats["languages"].items(),
        columns=["Language", "Count"]
    )

    fig = px.pie(
        df_lang,
        values="Count",
        names="Language",
        title="Programming Languages Used"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Top repositories
    st.subheader("🏆 Top Repositories")

    repo_table = []

    for repo in stats["top_repos"]:
        repo_table.append({
            "Repository": repo["name"],
            "Stars": repo["stargazers_count"],
            "Forks": repo["forks_count"],
            "Language": repo["language"]
        })

    st.dataframe(pd.DataFrame(repo_table))

    # Timeline
    st.subheader("📈 Repository Creation Timeline")

    df_dates = pd.DataFrame(stats["dates"], columns=["Date"])
    df_dates["Count"] = 1

    timeline = df_dates.groupby("Date").count().reset_index()

    fig2 = px.line(
        timeline,
        x="Date",
        y="Count",
        title="Repository Creation Over Time"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Profile summary
    st.subheader("📝 Profile Summary")

    summary = f"""
    {profile['name']} is a developer with experience in {", ".join(stats['skills'])}.
    The developer owns {stats['repos']} repositories with a total of {stats['stars']} stars.
    Based on repository activity and contributions, the developer is classified as {stats['level']} level.
    """

    st.info(summary)

# Developer Comparison
st.subheader("⚔️ Compare Two Developers")

user1 = st.text_input("Developer 1 Username")
user2 = st.text_input("Developer 2 Username")

if user1 and user2:

    p1 = get_user_profile(user1)
    p2 = get_user_profile(user2)

    r1 = get_repositories(user1)
    r2 = get_repositories(user2)

    s1 = analyze_repos(r1, p1["followers"])
    s2 = analyze_repos(r2, p2["followers"])

    df_compare = pd.DataFrame({
        "Metric": ["Repositories", "Stars", "Forks", "Score"],
        user1: [s1["repos"], s1["stars"], s1["forks"], round(s1["score"])],
        user2: [s2["repos"], s2["stars"], s2["forks"], round(s2["score"])]
    })

    st.dataframe(df_compare)