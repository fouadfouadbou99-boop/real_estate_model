import streamlit as st
import pandas as pd

from modules.finance import (
    calculate_investment,
    amortizing_debt_schedule
)

from modules.cashflows import (
    build_cashflows
)

from modules.kpi import (
    calculate_kpis
)

from modules.charts import (
    noi_chart,
    equity_cf_chart,
    debt_equity_chart
)

from modules.exports import (
    export_excel
)

from modules.recommendation import (
    get_recommendation
)

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Real Estate Analyzer",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Real Estate Investment Analyzer")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header("Hypothèses")

price = st.sidebar.number_input(
    "Prix Acquisition",
    value=1000000.0,
    step=10000.0
)

fees_pct = st.sidebar.number_input(
    "Frais Acquisition %",
    value=0.08
)

works = st.sidebar.number_input(
    "Travaux",
    value=100000.0,
    step=10000.0
)

rent = st.sidebar.number_input(
    "Loyer Brut Année 1",
    value=120000.0,
    step=5000.0
)

growth = st.sidebar.slider(
    "Croissance Loyers %",
    0.0,
    10.0,
    2.0
) / 100

vacancy = st.sidebar.slider(
    "Vacance %",
    0.0,
    20.0,
    5.0
) / 100

charges = st.sidebar.slider(
    "Charges %",
    0.0,
    50.0,
    20.0
) / 100

ltv = st.sidebar.slider(
    "LTV %",
    0.0,
    80.0,
    60.0
) / 100

debt_rate = st.sidebar.slider(
    "Taux Dette %",
    0.0,
    15.0,
    5.0
) / 100

debt_years = st.sidebar.number_input(
    "Durée Dette",
    value=20
)

horizon = st.sidebar.number_input(
    "Horizon",
    value=20
)

discount_rate = st.sidebar.slider(
    "Taux Actualisation %",
    0.0,
    15.0,
    8.0
) / 100

# ---------------------------------------------------
# INVESTISSEMENT
# ---------------------------------------------------

investment, debt, equity = calculate_investment(
    price,
    fees_pct,
    works,
    ltv
)

investment_df = pd.DataFrame({
    "Variable": [
        "Investissement",
        "Dette",
        "Equity"
    ],
    "Valeur": [
        investment,
        debt,
        equity
    ]
})

# ---------------------------------------------------
# DETTE
# ---------------------------------------------------

debt_df = amortizing_debt_schedule(
    debt,
    debt_rate,
    debt_years
)

debt_service = debt_df.iloc[0]["Annuité"]
interest_year1["Annuité" = debt_df.iloc[0]"]

# ---------------------------------------------------
# CASH FLOWS
# ---------------------------------------------------

cf_df = build_cashflows(
    rent,
    growth,
    vacancy,
    charges,
    horizon,
    debt_service
)

noi_year1["Intérêts = cf_df.iloc[0] ---------------------------------------------------
# TERMINAL VALUE
# ---------------------------------------------------

exit_cap = 0.07

terminal_value = (
    cf_df.iloc[-1]["NOI"] * (1 + growth)
) / exit_cap

# ---------------------------------------------------
# FLUX KPI
# ---------------------------------------------------

project_cf = [-investment]

for _, row in cf_df.iterrows():
    project_cf.append(row["NOI"])

project_cf[-1] += terminal_value

equity_cf = [-equity]

for _, row in cf_df.iterrows():
    equity_cf.append(row["CF Equity"])

equity_cf[-1] += terminal_value

# ---------------------------------------------------
# KPI
# ---------------------------------------------------

kpis = calculate_kpis(
    investment,
    equity,
    debt,
    noi_year1,
    debt_service,
    interest_year1,
    discount_rate,
    project_cf,
    equity_cf
)

# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------

st.subheader("📊 Dashboard")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "TRI Equity",
    f"{kpis['TRI Equity']:.2%}"
)

col2.metric(
    "TRI Projet",
    f"{kpis['TRI Projet']:.2%}"
)

col3.metric(
    "DSCR",
    f"{kpis['DSCR']:.2f}x"
)

col4.metric(
    "MOIC",
    f"{kpis['MOIC']:.2f}x"
)

col5.metric(
    "VAN",
    f"{kpis['VAN']:,.0f}"
)

# ---------------------------------------------------
# RECOMMANDATION
# ---------------------------------------------------

decision = get_recommendation(
    kpis["TRI Equity"],
    kpis["DSCR"],
    ltv,
    kpis["VAN"]
)

st.subheader("✅ Recommandation")

st.success(decision)

# ---------------------------------------------------
# GRAPHIQUES
# ---------------------------------------------------

st.subheader("📈 Analyse Graphique")

fig1 = noi_chart(cf_df)
st.plotly_chart(
    fig1,
    use_container_width=True
)

fig2 = equity_cf_chart(cf_df)
st.plotly_chart(
    fig2,
    use_container_width=True
)

fig3 = debt_equity_chart(
    debt,
    equity
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ---------------------------------------------------
# TABLEAUX
# ---------------------------------------------------

tab1, tab2, tab3 = st.tabs(
    [
        "Investissement",
        "Dette",
        "Cash-Flows"
    ]
)

with tab1:
    st.dataframe(
        investment_df,
        use_container_width=True
    )

with tab2:
    st.dataframe(
        debt_df,
        use_container_width=True
    )

with tab3:
    st.dataframe(
        cf_df,
        use_container_width=True
    )

# ---------------------------------------------------
# KPI TABLE
# ---------------------------------------------------

kpi_df = pd.DataFrame(
    {
        "KPI": list(kpis.keys()),
        "Valeur": list(kpis.values())
    }
)

# ---------------------------------------------------
# EXPORT EXCEL
# ---------------------------------------------------

excel_file = export_excel(
    investment_df,
    debt_df,
    cf_df,
    kpi_df
)

st.download_button(
    label="📊 Télécharger Excel",
    data=excel_file,
    file_name="Investment_Analysis.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# ---------------------------------------------------
# STRESS TEST SIMPLE
# ---------------------------------------------------

st.subheader("⚠ Stress Test")

stress_rent = rent * 0.9

stress_cf = build_cashflows(
    stress_rent,
    growth,
    vacancy,
    charges,
    horizon,
    debt_service
)

stress_noi = stress_cf.iloc[0]["NOI"]

stress_dscr = stress_noi / debt_service

stress_df = pd.DataFrame(
    {
        "Scénario": [
            "Base",
            "-10% Loyers"
        ],
        "DSCR": [
            kpis["DSCR"],
            stress_dscr
        ]
    }
)

st.dataframe(
    stress_df,
    use_container_width=True
)

st.caption(
    "Version 1 - Real Estate Analyzer"
)
