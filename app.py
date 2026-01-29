import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="COVID-19 Data Dashboard",
    page_icon="📊",
    layout="wide"
)


st.title("📊 COVID-19 Data Visualization")
st.write("Dataset preview at top and graphs below")
st.divider()

@st.cache_data
def load_data():
    return pd.read_csv("covid_19.csv")

df = load_data()
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

# ---------------- DATA PREVIEW (TOP) ----------------
st.subheader("📄 Dataset Preview")
st.dataframe(df, width="stretch")


st.divider()


st.subheader("📊 Graph Controls")

col1, col2 = st.columns(2)

with col1:
    metric = st.selectbox("Select Metric", numeric_cols)

with col2:
    graph = st.selectbox(
        "Select Graph Type",
        ["Line Chart", "Bar Graph", "Histogram", "Pie Chart", "Dot Plot"]
    )


st.subheader(f"{graph} for {metric}")

fig, ax = plt.subplots(figsize=(10, 4))

if graph == "Line Chart":
    ax.plot(df[metric])
    ax.set_xlabel("Index")
    ax.set_ylabel(metric)

elif graph == "Bar Graph":
    ax.bar(range(len(df)), df[metric])
    ax.set_xlabel("Index")
    ax.set_ylabel(metric)

elif graph == "Histogram":
    ax.hist(df[metric], bins=25)
    ax.set_xlabel(metric)
    ax.set_ylabel("Frequency")

elif graph == "Pie Chart":
    top_values = df[metric].value_counts().head(5)
    ax.pie(
        top_values.values,
        labels=top_values.index,
        autopct="%1.1f%%",
        startangle=90
    )
    ax.set_title("Top 5 Value Distribution")

elif graph == "Dot Plot":
    ax.plot(df[metric], '.', markersize=6)
    ax.set_xlabel("Index")
    ax.set_ylabel(metric)

st.pyplot(fig)


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
