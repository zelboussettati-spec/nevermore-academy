import streamlit as st
from startscript import (
    laad_data,
    bereken_kpi1,
    figuur_kpi3,
    bereken_kpi4,
    figuur_kpi5
)

# Titel
st.set_page_config(layout="wide")
st.title("KPI Dashboard")

df_robot, df_mens = laad_data()

# KPI 1 - Klanttevredenheid jonge klanten
try:
    avg_robot, avg_mens = bereken_kpi1(df_robot, df_mens)
    st.subheader("KPI 1: Klanttevredenheid jonge klanten (≤ 45 jaar)")
    col1, col2 = st.columns(2)
    col1.metric("Gemiddelde beoordeling Robot", f"{avg_robot:.2f}")
    col2.metric("Gemiddelde beoordeling Mens", f"{avg_mens:.2f}")
except Exception as e:
    st.error(f"Fout in KPI 1: {e}")

# KPI 3 - Orders per uur
try:
    st.subheader("KPI 3: Orders per uur")
    fig = figuur_kpi3(df_robot, df_mens)
    st.pyplot(fig)
except Exception as e:
    st.error(f"Fout in KPI 3: {e}")

# KPI 4 - Bezorgsnelheid
try:
    st.subheader("KPI 4: Gemiddelde bezorgtijd")
    tijd_robot, tijd_mens = bereken_kpi4(df_robot, df_mens)
    col1, col2 = st.columns(2)
    col1.metric("Gem. bezorgtijd Robot", f"{tijd_robot:.1f} sec")
    col2.metric("Gem. bezorgtijd Mens", f"{tijd_mens:.1f} sec")
except Exception as e:
    st.error(f"Fout in KPI 4: {e}")

# KPI 5 - Totale kosten per dag
try:
    st.subheader("KPI 5: Kosten per dag")
    fig = figuur_kpi5(df_robot, df_mens)
    st.pyplot(fig)
except Exception as e:
    st.error(f"Fout in KPI 5: {e}")
