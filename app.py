import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="COVID-19 Data Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("📊 COVID-19 Data Visualization")
st.write("Hover on any point to see live popup data")
st.divider()

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("covid_19.csv")

df = load_data()

# Add index column for hover display
df["Index"] = df.index

numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

# ---------------- DATA PREVIEW ----------------
st.subheader("📄 Dataset Preview")
st.dataframe(df, width="stretch")

st.divider()

# ---------------- GRAPH CONTROLS ----------------
st.subheader("📊 Graph Controls")

col1, col2 = st.columns(2)

with col1:
    metric = st.selectbox("Select Metric", numeric_cols)

with col2:
    graph = st.selectbox(
        "Select Graph Type",
        ["Line Chart", "Bar Graph", "Histogram", "Pie Chart", "Dot Plot"]
    )

# ---------------- GRAPH DISPLAY ----------------
st.subheader(f"{graph} for {metric}")

if graph == "Line Chart":
    fig = px.line(
        df,
        x="Index",
        y=metric,
        title=f"{metric} over Index",
        hover_data={
            "Index": True,
            metric: ":,.2f"
        }
    )

elif graph == "Bar Graph":
    fig = px.bar(
        df,
        x="Index",
        y=metric,
        title=f"{metric} Bar Graph",
        hover_data={
            "Index": True,
            metric: ":,.2f"
        }
    )

elif graph == "Histogram":
    fig = px.histogram(
        df,
        x=metric,
        nbins=25,
        title=f"{metric} Distribution",
        hover_data={metric: ":,.2f"}
    )

elif graph == "Pie Chart":
    top_values = df[metric].value_counts().head(5).reset_index()
    top_values.columns = ["Value", "Count"]

    fig = px.pie(
        top_values,
        values="Count",
        names="Value",
        title="Top 5 Value Distribution",
        hover_data={"Count": True}
    )

elif graph == "Dot Plot":
    fig = px.scatter(
        df,
        x="Index",
        y=metric,
        title=f"{metric} Dot Plot",
        hover_data={
            "Index": True,
            metric: ":,.2f"
        }
    )

# Show chart
st.plotly_chart(fig, use_container_width=True)

# ---------------- STATISTICS ----------------
st.divider()
st.subheader("📌 Statistical Summary")

colA, colB, colC = st.columns(3)

with colA:
    st.metric("Minimum", round(df[metric].min(), 2))

with colB:
    st.metric("Maximum", round(df[metric].max(), 2))

with colC:
    st.metric("Average", round(df[metric].mean(), 2))

# ---------------- FOOTER ----------------
st.caption("Streamlit Data Visualization Project | Swarna Kanda")
