import streamlit as st
import pandas as pd
import plotly.express as px
from github_api import get_user_profile, get_repositories
from analyzer import analyze_repos

# Page Config
st.set_page_config(page_title="GitHub Intelligence", page_icon="🚀", layout="wide")

# Custom CSS for a professional look
st.markdown("""
    <style>
    /* Metric Cards Fix */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05); /* Semi-transparent background */
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 15px;
        border-radius: 10px;
        color: inherit; /* Inherits text color from theme */
    }
    
    /* Repo Cards Fix */
    .repo-card {
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        background-color: rgba(255, 255, 255, 0.05);
        color: inherit;
    }

    /* Skill Pills Fix */
    .skill-pill {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 15px;
        background-color: #1e3a8a; /* Darker blue for visibility */
        color: #ffffff;
        font-size: 12px;
        margin: 2px;
        border: 1px solid #3b82f6;
    }
    
    /* Ensure metric labels are visible */
    [data-testid="stMetricLabel"] {
        color: inherit !important;
    }
    
    /* Ensure metric values are visible */
    [data-testid="stMetricValue"] {
        color: inherit !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 GitHub Developer Intelligence Analyzer")
st.markdown("---")

username = st.text_input("🔍 Enter GitHub Username", placeholder="e.g. bhagyasreegurrala")

if username:
    with st.spinner('⚡ Fetching developer insights...'):
        profile = get_user_profile(username)

        if not profile:
            st.error("User not found. Please check the username.")
            st.stop()

        repos = get_repositories(username)
        stats = analyze_repos(repos, profile["followers"])

    # Profile Header Section
    col_img, col_info = st.columns([1, 4])
    with col_img:
        st.image(profile["avatar_url"], width=150, use_container_width=False)
    with col_info:
        st.header(f"{profile.get('name') or username}")
        st.caption(f"📍 {profile.get('location', 'Global')}")
        st.write(profile.get("bio", "No bio provided."))
        
        # Display skills as Pills
        if stats["skills"]:
            pill_html = "".join([f'<span class="skill-pill">{s}</span>' for s in stats["skills"]])
            st.markdown(pill_html, unsafe_allow_html=True)

    st.markdown("### 📊 Performance Metrics")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Repositories", stats["repos"])
    c2.metric("Total Stars", stats["stars"])
    c3.metric("Total Forks", stats["forks"])
    c4.metric("Dev Score", f"{round(stats['score'])} pts")

    # Visualizations
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("💻 Language Stack")
        df_lang = pd.DataFrame(stats["languages"].items(), columns=["Language", "Count"])
        # Modern Donut Chart
        fig = px.pie(df_lang, values="Count", names="Language", hole=0.5,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(showlegend=True, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("📈 Growth Timeline")
        df_dates = pd.DataFrame(stats["dates"], columns=["Date"])
        df_dates["Count"] = 1
        timeline = df_dates.groupby("Date").count().reset_index()
        fig2 = px.area(timeline, x="Date", y="Count", markers=True,
                       color_discrete_sequence=['#00CC96'])
        st.plotly_chart(fig2, use_container_width=True)

    # 🏆 Featured Repositories 
    st.subheader("🏆 Featured Repositories")
    for repo in stats["top_repos"]:
        with st.container():
            st.markdown(f"""
            <div class="repo-card">
                <div style="display: flex; justify-content: space-between;">
                    <strong>{repo['name']}</strong>
                    <span>⭐ {repo['stargazers_count']} | 🍴 {repo['forks_count']}</span>
                </div>
                <small style="opacity: 0.8;">Main Language: {repo['language'] or 'N/A'}</small>
            </div>
            """, unsafe_allow_html=True)

    # 📝 Profile Summary 
    st.subheader("📝 Profile Summary")

    # Use username as a fallback if the GitHub 'name' field is None or empty
    display_name = profile.get('name') or username
    primary_skill = max(stats['languages'], key=stats['languages'].get) if stats['languages'] else 'various technologies'

    summary = f"""
    **{display_name}** is a **{stats['level']}** developer with a high focus on **{primary_skill}**. 
    The developer manages **{stats['repos']}** repositories with a total of **{stats['stars']}** stars and **{stats['forks']}** forks.
    """

    st.success(f"**Dev Level:** {stats['level']}")
    st.info(summary)

# Comparison Section (Collapsible)
with st.expander("⚔️ Developer Comparison"):
    u1, u2 = st.columns(2)
    user1 = u1.text_input("Username 1", key="comp_user1")
    user2 = u2.text_input("Username 2", key="comp_user2")

    if user1 and user2:
        with st.spinner('Calculating comparison...'):
            p1, p2 = get_user_profile(user1), get_user_profile(user2)
            
            if p1 and p2:
                r1 = get_repositories(user1)
                r2 = get_repositories(user2)
                s1 = analyze_repos(r1, p1["followers"])
                s2 = analyze_repos(r2, p2["followers"])
                
                # 1. Detailed Metric Table
                df_compare = pd.DataFrame({
                    "Metric": ["Level", "Primary Language", "Total Repos", "Total Stars", "Avg Stars/Repo", "Followers", "Dev Score"],
                    user1: [s1["level"], s1.get("primary_lang", "N/A"), s1["repos"], s1["stars"], s1.get("avg_stars", 0), s1.get("followers", p1["followers"]), round(s1["score"])],
                    user2: [s2["level"], s2.get("primary_lang", "N/A"), s2["repos"], s2["stars"], s2.get("avg_stars", 0), s2.get("followers", p2["followers"]), round(s2["score"])]
                }).set_index("Metric")
                
                st.table(df_compare)

                # 2. Visual Bar Chart Comparison
                chart_data = pd.DataFrame({
                    "Developer": [user1, user2],
                    "Score": [s1["score"], s2["score"]],
                    "Stars": [s1["stars"], s2["stars"]],
                    "Followers": [p1["followers"], p2["followers"]]
                })
                
                fig_comp = px.bar(chart_data, x="Developer", y="Score", 
                                 title="Score Comparison",
                                 color="Developer",
                                 text_auto=True)
                st.plotly_chart(fig_comp, use_container_width=True)
                
            else:
                st.error("Check usernames and try again.")