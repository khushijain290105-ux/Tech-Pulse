import streamlit as st
import pandas as pd

# PAGE CONFIGURATION

st.set_page_config(
    page_title="Tech Pulse",
    page_icon="🚀",
    layout="wide"
)

# CUSTOM DASHBOARD STYLE

st.markdown("""
<style>

.main {
    padding-top: 2rem;
}

h1 {
    font-size: 42px;
}

h2 {
    font-size: 30px;
}

h3 {
    font-size: 22px;
}

div[data-testid="stMetric"] {
    background-color: #f5f7fa;
    border: 1px solid #e0e0e0;
    padding: 15px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# TITLE

st.title("🚀 Tech Pulse")
st.subheader("Skills Demand & Workforce Intelligence Dashboard")

# LOAD DATASET
df = pd.read_csv("jobs.csv")

# DATA CLEANING

# Convert Salary to numeric
df["Salary"] = pd.to_numeric(
    df["Salary"],
    errors="coerce"
)

# Convert Experience to numeric
df["Experience"] = pd.to_numeric(
    df["Experience"],
    errors="coerce"
)

# INTERACTIVE FILTERS
st.header("🎯 Interactive Filters")

col1, col2, col3, col4 = st.columns(4)

# CITY FILTER

with col1:

    selected_city = st.selectbox(
        "📍 Select City",
        ["All"] +
        sorted(
            df["Location"]
            .dropna()
            .unique()
            .tolist()
        )
    )

# JOB ROLE FILTER

with col2:

    selected_role = st.selectbox(
        "💼 Select Job Role",
        ["All"] +
        sorted(
            df["Job Title"]
            .dropna()
            .unique()
            .tolist()
        )
    )

# COMPANY FILTER

with col3:

    selected_company = st.selectbox(
        "🏢 Select Company",
        ["All"] +
        sorted(
            df["Company"]
            .dropna()
            .unique()
            .tolist()
        )
    )

# EXPERIENCE FILTER

with col4:

    experience_values = sorted(
        df["Experience"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_experience = st.selectbox(
        "🎓 Select Experience",
        ["All"] + experience_values
    )

# APPLY FILTERS

filtered_df = df.copy()

# City filter
if selected_city != "All":

    filtered_df = filtered_df[
        filtered_df["Location"] == selected_city
    ]

# Job Role filter
if selected_role != "All":

    filtered_df = filtered_df[
        filtered_df["Job Title"] == selected_role
    ]

# Company filter
if selected_company != "All":

    filtered_df = filtered_df[
        filtered_df["Company"] == selected_company
    ]

# Experience filter
if selected_experience != "All":

    filtered_df = filtered_df[
        filtered_df["Experience"] == selected_experience
    ]

# FILTERED JOB DATA

st.markdown("---")

st.header("📊 Filtered Job Data")

if filtered_df.empty:

    st.warning(
        "⚠️ No jobs found for the selected filters."
    )

    st.stop()

else:

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# DOWNLOAD FILTERED DATA

st.subheader("📥 Download Filtered Data")

csv_data = filtered_df.to_csv(
    index=False
)

st.download_button(
    label="📥 Download CSV",
    data=csv_data,
    file_name="tech_pulse_filtered_data.csv",
    mime="text/csv"
)

# JOB MARKET OVERVIEW

st.markdown("---")

st.header("📌 Job Market Overview")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Total Jobs",
        len(filtered_df)
    )

with col2:

    st.metric(
        "Total Cities",
        filtered_df["Location"].nunique()
    )

with col3:

    st.metric(
        "Total Companies",
        filtered_df["Company"].nunique()
    )

# CITY-WISE JOB DEMAND

st.markdown("---")

st.header("🌆 City-wise Job Demand")

city_counts = (
    filtered_df["Location"]
    .value_counts()
)

st.bar_chart(
    city_counts
)

st.subheader("📋 City Job Count")

st.dataframe(
    city_counts
    .rename("Number of Jobs")
    .reset_index(),
    use_container_width=True
)

# JOB ROLE DISTRIBUTION

st.markdown("---")

st.header("💼 Job Role Distribution")

role_counts = (
    filtered_df["Job Title"]
    .value_counts()
)

st.bar_chart(
    role_counts
)

st.subheader("📋 Job Role Count")

st.dataframe(
    role_counts
    .rename("Number of Jobs")
    .reset_index(),
    use_container_width=True
)

# TOP SKILLS IN DEMAND
st.markdown("---")

st.header("🔥 Top Skills in Demand")

skills = (
    filtered_df["Skills"]
    .dropna()
    .astype(str)
    .str.split(",")
    .explode()
    .str.strip()
)

skill_counts = skills.value_counts()

st.bar_chart(
    skill_counts
)

st.subheader("📋 Skill Demand")

st.dataframe(
    skill_counts
    .rename("Demand")
    .reset_index(),
    use_container_width=True
)

# SALARY ANALYSIS

st.markdown("---")

st.header("💰 Salary Analysis")

salary_df = filtered_df.dropna(
    subset=["Salary"]
)

if salary_df.empty:

    st.warning(
        "⚠️ Salary data is not available for the selected filters."
    )

else:

    # SALARY METRICS

    avg_salary = salary_df["Salary"].mean()

    highest_salary = salary_df["Salary"].max()

    lowest_salary = salary_df["Salary"].min()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Average Salary",
            f"₹{avg_salary:,.0f}"
        )

    with col2:

        st.metric(
            "Highest Salary",
            f"₹{highest_salary:,.0f}"
        )

    with col3:

        st.metric(
            "Lowest Salary",
            f"₹{lowest_salary:,.0f}"
        )

    # SALARY BY JOB ROLE
   
    st.subheader("📊 Salary by Job Role")

    salary_by_role = (
        salary_df
        .groupby("Job Title")["Salary"]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    st.bar_chart(
        salary_by_role
    )

    # EXPERIENCE VS SALARY

    st.subheader("📈 Experience vs Salary")

    experience_salary = (
        salary_df
        .groupby("Experience")["Salary"]
        .mean()
        .sort_index()
    )

    st.line_chart(
        experience_salary
    )

    # COMPANY-WISE SALARY ANALYSIS

    st.subheader("🏢 Company-wise Salary Analysis")

    salary_by_company = (
        salary_df
        .groupby("Company")["Salary"]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    st.bar_chart(
        salary_by_company
    )

    # SALARY DETAILS
   
    st.subheader("📋 Salary Details")

    salary_table = salary_df[
        [
            "Job Title",
            "Company",
            "Experience",
            "Salary"
        ]
    ]

    st.dataframe(
        salary_table,
        use_container_width=True
    )

# KEY INSIGHTS

st.markdown("---")

st.header("🔑 Key Insights")

# Most demanded city

if not city_counts.empty:

    top_city = city_counts.idxmax()
    top_city_jobs = city_counts.max()

    st.success(
        f"📍 **Top Job Location:** {top_city} "
        f"has the highest number of jobs ({top_city_jobs})."
    )

# Most demanded job role

if not role_counts.empty:

    top_role = role_counts.idxmax()
    top_role_jobs = role_counts.max()

    st.info(
        f"💼 **Most Demanded Job Role:** {top_role} "
        f"with {top_role_jobs} job opportunities."
    )

# Most demanded skill

if not skill_counts.empty:

    top_skill = skill_counts.idxmax()
    top_skill_demand = skill_counts.max()

    st.warning(
        f"🔥 **Most Demanded Skill:** {top_skill} "
        f"with demand in {top_skill_demand} job listings."
    )

# Highest paying company

if not salary_df.empty and not salary_by_company.empty:

    highest_company = salary_by_company.idxmax()
    highest_company_salary = salary_by_company.max()

    st.success(
        f"🏢 **Highest Paying Company:** {highest_company} "
        f"with an average salary of "
        f"₹{highest_company_salary:,.0f}."
    )

# Average salary insight

if not salary_df.empty:

    st.info(
        f"💰 **Average Salary:** "
        f"₹{avg_salary:,.0f} across the filtered job listings."
    )

# DASHBOARD FOOTER

st.markdown("---")

st.caption(
    "🚀 Tech Pulse | Skills Demand & Workforce Intelligence Dashboard"
)