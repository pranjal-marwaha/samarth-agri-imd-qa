import streamlit as st
import pandas as pd
import os
import plotly.express as px

# -------------------------------
# APP CONFIG
# -------------------------------
st.set_page_config(page_title="Project Samarth - Govt Data Q&A", layout="wide")
st.title("🌾 Project Samarth — Intelligent Government Data Q&A System")

st.write("""
This prototype connects and analyzes government open datasets from **data.gov.in** — 
focusing on agriculture production and rainfall patterns to generate insights.
""")

# -------------------------------
# STEP 1 — LOAD & CLEAN DATA
# -------------------------------
os.makedirs("data", exist_ok=True)

# --- PRODUCTION DATA ---
try:
    prod = pd.read_csv("classification-wise_production_during_the_year_2017-18.csv")

    # Fix column names properly
    prod.columns = ["S.No", "Name of the Minerals", "Production"]
    prod.columns = prod.columns.str.strip()

    prod.to_csv("data/production_clean.csv", index=False)
    st.success("✅ Production data loaded successfully!")
except Exception as e:
    st.error(f"⚠️ Error loading Production data: {e}")

# --- RAINFALL DATA ---
# --- RAINFALL DATA ---
# --- RAINFALL DATA ---
try:
    rain = pd.read_csv("RS_Session_257_AU_2106_A.ii_.csv")
    rain.columns = rain.columns.str.strip()  # remove spaces around names
    st.write("Columns in Rainfall CSV before rename:", list(rain.columns))  # debug

    # Rename correctly based on your screenshot
    rain = rain.rename(columns={
        "Region": "region",
        "Rainfall - Actual": "rainfall_actual",
        "Rainfall - Normal": "rainfall_normal",
        "Rainfall - % Departure": "rainfall_departure"
    })

    rain.to_csv("data/rainfall_clean.csv", index=False)
    st.success(f"✅ Rainfall data loaded successfully! Renamed columns: {list(rain.columns)}")

except Exception as e:
    st.error(f"⚠️ Error loading Rainfall data: {e}")



   

# -------------------------------
# STEP 2 — SHOW CLEAN DATA
# -------------------------------
st.header("📊 Cleaned Data Preview")

tab1, tab2 = st.tabs(["🏭 Production Data", "🌧 Rainfall Data"])

with tab1:
    st.dataframe(prod)
    if "Production" in prod.columns:
        fig_prod = px.bar(
            prod,
            x="Name of the Minerals",
            y="Production",
            title="Production by Mineral Type",
            color="Name of the Minerals"
        )
        st.plotly_chart(fig_prod, use_container_width=True)

with tab2:
    st.dataframe(rain)
    if "rainfall_actual" in rain.columns:
        fig_rain = px.bar(
            rain,
            x="region",
            y=["rainfall_actual", "rainfall_normal"],
            barmode="group",
            title="Actual vs Normal Rainfall by Region"
        )
        st.plotly_chart(fig_rain, use_container_width=True)

# -------------------------------
# STEP 3 — INTELLIGENT Q&A
# -------------------------------
st.header("🧠 Ask Questions about the Data")

question = st.text_input("Ask a question (e.g. 'Which region had highest rainfall?')")

if st.button("Get Answer"):
    if question:
        answer = ""
        source = ""
        q = question.lower()

        # Example: Highest rainfall
        if "highest rainfall" in q:
            row = rain.loc[rain["rainfall_actual"].idxmax()]
            answer = f"The region with the highest rainfall is **{row['region']}** with {row['rainfall_actual']} mm."
            source = "RS_Session_257_AU_2106_A.ii_.csv"

        elif "lowest rainfall" in q:
            row = rain.loc[rain["rainfall_actual"].idxmin()]
            answer = f"The region with the lowest rainfall is **{row['region']}** with {row['rainfall_actual']} mm."
            source = "RS_Session_257_AU_2106_A.ii_.csv"

        elif "highest production" in q:
            row = prod.loc[prod["Production"].idxmax()]
            answer = f"The mineral with the highest production is **{row['Name of the Minerals']}** with {row['Production']} units."
            source = "classification-wise_production_during_the_year_2017-18.csv"

        elif "lowest production" in q:
            row = prod.loc[prod["Production"].idxmin()]
            answer = f"The mineral with the lowest production is **{row['Name of the Minerals']}** with {row['Production']} units."
            source = "classification-wise_production_during_the_year_2017-18.csv"

        elif "compare" in q and "rainfall" in q:
            answer = "📘 Comparing rainfall across regions — please refer to the rainfall chart above."
            source = "RS_Session_257_AU_2106_A.ii_.csv"

        else:
            answer = "⚙️ Sorry, I couldn’t understand that query yet. Try asking about rainfall or production."

        st.markdown(f"### 💬 Answer:\n{answer}")
        st.caption(f"📚 Source: {source}")
    else:
        st.warning("Please enter a question first.")

# -------------------------------
# STEP 4 — INSIGHTS
# -------------------------------
st.header("📈 Quick Insights")

col1, col2 = st.columns(2)

with col1:
    if not prod.empty:
        top_prod = prod.loc[prod["Production"].idxmax()]
        st.metric("Top Production Mineral", top_prod["Name of the Minerals"], delta=top_prod["Production"])

with col2:
    if not rain.empty:
        top_rain = rain.loc[rain["rainfall_departure"].idxmax()]
        st.metric("Highest Rainfall Departure", top_rain["region"], delta=f"{top_rain['rainfall_departure']}%")

st.info("✅ Prototype ready — integrates datasets, allows Q&A, and provides traceable results.")
#python -m streamlit run main.py