import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

# Bestandsnamen
robot_file = "robot_restaurant_log_week_cleaned.json"
excel_file = "besteldata.xlsx"

# Inlezen robotlog
try:
    df_robot = pd.read_json(robot_file)
    st.success("Robotlog geladen")
except Exception as e:
    st.error(f"Fout bij inlezen robotlog: {e}")
    df_robot = pd.DataFrame()

# Inlezen Excel-besteldata
try:
    df_excel = pd.read_excel(excel_file)
    st.success("Excelbestand geladen")
except Exception as e:
    st.error(f"Fout bij inlezen Excelbestand: {e}")
    df_excel = pd.DataFrame()

# KPI 1: Klanttevredenheid jonge klanten (≤ 45 jaar)
def kpi1():
    try:
        df_robot["Birth_Date"] = pd.to_datetime(df_robot["Birth_Date"], format="%d-%m-%Y", errors="coerce")
        df_robot["Date"] = pd.to_datetime(df_robot["Date"], format="%d-%m-%Y", errors="coerce")
        df_robot["Age"] = (df_robot["Date"] - df_robot["Birth_Date"]).dt.days // 365

        df_excel["Birth_Date"] = pd.to_datetime(df_excel["Birth_Date"], dayfirst=True, errors="coerce")
        df_excel["Date"] = pd.to_datetime(df_excel["Date"], dayfirst=True, errors="coerce")
        df_excel["Age"] = (df_excel["Date"] - df_excel["Birth_Date"]).dt.days // 365

        young_robot = df_robot[df_robot["Age"] <= 45]
        young_excel = df_excel[df_excel["Age"] <= 45]

        avg_robot = young_robot["Rating"].mean()
        avg_excel = young_excel["Rating"].mean()

        st.subheader("KPI 1 - Klanttevredenheid jonge klanten (≤ 45 jaar)")
        st.metric("Gemiddelde beoordeling robot", f"{avg_robot:.2f}")
        st.metric("Gemiddelde beoordeling bediening", f"{avg_excel:.2f}")
    except Exception as e:
        st.error(f"Fout in KPI 1: {e}")

# KPI 3: Orders per uur (robot)
def kpi3():
    try:
        df_robot["Time_Picked"] = pd.to_datetime(df_robot["Time_Picked"], format="%H:%M:%S", errors="coerce")
        df_robot["Uur"] = df_robot["Time_Picked"].dt.hour
        orders_per_uur = df_robot.groupby("Uur")["Order_ID"].count()

        st.subheader("KPI 3 - Aantal robotorders per uur")
        fig, ax = plt.subplots()
        orders_per_uur.plot(kind="bar", ax=ax, color="steelblue")
        ax.set_ylabel("Aantal orders")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Fout in KPI 3: {e}")

# KPI 4: Bezorgsnelheid (bediening)
def kpi4():
    try:
        df_excel["Time_Order"] = pd.to_datetime(df_excel["Time_Ord"], format="%H:%M:%S", errors="coerce")
        df_excel["Time_Delivery"] = pd.to_datetime(df_excel["Time_Deli"], format="%H:%M:%S", errors="coerce")
        df_excel["Seconds"] = (df_excel["Time_Delivery"] - df_excel["Time_Order"]).dt.total_seconds()
        avg_time = df_excel["Seconds"].mean()

        st.subheader("KPI 4 - Gemiddelde bezorgtijd bediening (seconden)")
        st.metric(label="Gemiddelde bezorgtijd", value=f"{avg_time:.1f}")
    except Exception as e:
        st.error(f"Fout in KPI 4: {e}")

# KPI 5: Totale kosten per dag (bediening)
def kpi5():
    try:
        df_excel["Date"] = pd.to_datetime(df_excel["Date"], dayfirst=True, errors="coerce")
        kosten_per_dag = df_excel.groupby(df_excel["Date"].dt.date)["Total_Am"].sum()

        st.subheader("KPI 5 - Totale kosten per dag (bediening)")
        fig, ax = plt.subplots()
        kosten_per_dag.plot(kind="bar", ax=ax, color="darkred")
        ax.set_ylabel("Totale kosten (€)")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Fout in KPI 5: {e}")

# Navigatie
st.title("KPI Dashboard - Restaurant")

tabs = st.tabs([
    "KPI 1 - Tevredenheid",
    "KPI 3 - Orders per uur",
    "KPI 4 - Bezorgsnelheid",
    "KPI 5 - Kosten per dag"
])

with tabs[0]: kpi1()
with tabs[1]: kpi3()
with tabs[2]: kpi4()
with tabs[3]: kpi5()
