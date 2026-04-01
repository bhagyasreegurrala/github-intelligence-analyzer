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
    .main { background-color: #f8f9fa; }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .repo-card {
        border: 1px solid #e6e9ef;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        background-color: white;
    }
    .skill-pill {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 15px;
        background-color: #e1f5fe;
        color: #01579b;
        font-size: 12px;
        margin: 2px;
        border: 1px solid #01579b;
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

    # Top Repositories as Cards
    st.subheader("🏆 Featured Repositories")
    for repo in stats["top_repos"]:
        with st.container():
            st.markdown(f"""
            <div class="repo-card">
                <strong>{repo['name']}</strong> | ⭐ {repo['stargazers_count']} | 🍴 {repo['forks_count']}<br>
                <small>Language: {repo['language'] or 'N/A'}</small>
            </div>
            """, unsafe_allow_html=True)

    # Automated Summary
    st.success(f"**Dev Level:** {stats['level']}")
    st.info(f"**Insights:** {profile.get('name', username)} is a {stats['level']} developer with a high focus on {max(stats['languages'], key=stats['languages'].get) if stats['languages'] else 'various technologies'}.")

# Comparison Section (Collapsible)
with st.expander("⚔️ Compare Developers"):
    u1, u2 = st.columns(2)
    user1 = u1.text_input("Username 1")
    user2 = u2.text_input("Username 2")

    if user1 and user2:
        # (Comparison logic remains the same but within this expander)
        p1, p2 = get_user_profile(user1), get_user_profile(user2)
        r1, r2 = get_repositories(user1), get_repositories(user2)
        s1, s2 = analyze_repos(r1, p1["followers"]), analyze_repos(r2, p2["followers"])
        
        df_compare = pd.DataFrame({
            "Metric": ["Repos", "Stars", "Forks", "Score"],
            user1: [s1["repos"], s1["stars"], s1["forks"], round(s1["score"])],
            user2: [s2["repos"], s2["stars"], s2["forks"], round(s2["score"])]
        }).set_index("Metric")
        st.table(df_compare)