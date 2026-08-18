import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from numpy_financial import irr, npv, pmt

st.set_page_config(
    page_title="Real Estate Investment Analyzer",
    layout="wide"
)

st.title("🏢 Real Estate Investment Analyzer")

# ========================
# SIDEBAR
# ========================

st.sidebar.header("Hypothèses")

purchase_price = st.sidebar.number_input(
    "Prix acquisition",
    value=1000000.0
)

acquisition_fee_pct = st.sidebar.number_input(
    "Frais acquisition %",
    value=0.08
)

works = st.sidebar.number_input(
    "Travaux",
    value=100000.0
)

rent_year1 = st.sidebar.number_input(
    "Loyer brut année 1",
    value=120000.0
)

rent_growth = st.sidebar.number_input(
    "Croissance loyers %",
    value=0.02
)

vacancy = st.sidebar.number_input(
    "Vacance %",
    value=0.05
)

charges = st.sidebar.number_input(
    "Charges %",
    value=0.20
)

ltv = st.sidebar.number_input(
    "LTV cible",
    value=0.60
)

debt_rate = st.sidebar.number_input(
    "Taux dette",
    value=0.05
)

debt_term = st.sidebar.number_input(
    "Durée dette",
    value=20
)

holding_period = st.sidebar.number_input(
    "Horizon",
    value=20
)

exit_cap_rate = st.sidebar.number_input(
    "Exit Cap Rate",
    value=0.07
)

selling_cost = st.sidebar.number_input(
    "Frais cession",
    value=0.03
)

discount_rate = st.sidebar.number_input(
    "Taux actualisation",
    value=0.08
)

# ========================
# INVESTMENT
# ========================

investment_total = (
    purchase_price
    + purchase_price * acquisition_fee_pct
    + works
)

debt = investment_total * ltv
equity = investment_total - debt

# ========================
# DEBT SCHEDULE
# ========================

annuity = abs(
    pmt(
        debt_rate,
        debt_term,
        debt
    )
)

schedule = []

balance = debt

for year in range(1, debt_term + 1):

    interest = balance * debt_rate

    principal = annuity - interest

    ending_balance = max(
        balance - principal,
        0
    )

    schedule.append(
        [
            year,
            balance,
            annuity,
            interest,
            principal,
            ending_balance
        ]
    )

    balance = ending_balance

debt_df = pd.DataFrame(
    schedule,
    columns=[
        "Année",
        "Solde début",
        "Annuité",
        "Intérêts",
        "Principal",
        "Solde fin"
    ]
)

# ========================
# CASH FLOWS
# ========================

cashflows = []

for year in range(1, holding_period + 1):

    rent = rent_year1 * ((1 + rent_growth) ** (year - 1))

    rent_net = rent * (1 - vacancy)

    noi = rent_net * (1 - charges)

    debt_service = annuity

    cf_equity = noi - debt_service

    terminal_value = 0

    if year == holding_period:

        noi_next = noi * (1 + rent_growth)

        terminal_value = (
            noi_next / exit_cap_rate
        ) * (1 - selling_cost)

    cashflows.append(
        [
            year,
            rent,
            rent_net,
            noi,
            debt_service,
            cf_equity,
            terminal_value
        ]
    )

cf_df = pd.DataFrame(
    cashflows,
    columns=[
        "Année",
        "Loyer",
        "Loyer Net",
        "NOI",
        "Service Dette",
        "CF Equity",
        "Valeur Terminale"
    ]
)

# ========================
# KPI
# ========================

project_flows = [-investment_total]

project_flows.extend(
    list(cf_df["NOI"])
)

project_flows[-1] += cf_df.iloc[-1]["Valeur Terminale"]

equity_flows = [-equity]

equity_flows.extend(
    list(cf_df["CF Equity"])
)

equity_flows[-1] += cf_df.iloc[-1]["Valeur Terminale"]

tri_projet = irr(project_flows)

tri_equity = irr(equity_flows)

van = npv(
    discount_rate,
    equity_flows
)

moic = sum(equity_flows[1:]) / equity
   

cap_rate = (
    cf_df.iloc[0]["NOI"]
    / purchase_price
)

dscr = (
    cf_df.iloc[0]["NOI"]
    / annuity
)

ltv_calc = debt / investment_total

debt_yield = (
    cf_df.iloc[0]["NOI"]
    / debt
)

# ========================
# DASHBOARD
# ========================

st.header("📊 Dashboard")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "TRI Equity",
    f"{tri_equity:.2%}"
)

c2.metric(
    "TRI Projet",
    f"{tri_projet:.2%}"
)

c3.metric(
    "DSCR",
    f"{dscr:.2f}x"
)

c4.metric(
    "MOIC",
    f"{moic:.2f}x"
)

c5, c6, c7 = st.columns(3)

c5.metric(
    "LTV",
    f"{ltv_calc:.2%}"
)

c6.metric(
    "Debt Yield",
    f"{debt_yield:.2%}"
)

c7.metric(
    "VAN",
    f"{van:,.0f}"
)

# ========================
# TABLES
# ========================

st.subheader("Cash Flows")

st.dataframe(
    cf_df,
    use_container_width=True
)

st.subheader("Dette")

st.dataframe(
    debt_df,
    use_container_width=True
)

# ========================
# CHARTS
# ========================

st.subheader("NOI")

fig_noi = px.line(
    cf_df,
    x="Année",
    y="NOI",
    markers=True
)

st.plotly_chart(
    fig_noi,
    use_container_width=True
)

st.subheader("Cash Flow Equity")

fig_cf = px.bar(
    cf_df,
    x="Année",
    y="CF Equity"
)

st.plotly_chart(
    fig_cf,
    use_container_width=True
)

# ========================
# INVESTMENT DECISION
# ========================

st.subheader("Comité d'investissement")

if tri_equity > 0.15 and dscr > 1.5 and ltv_calc < 0.50:
    recommendation = "✅ INVESTIR"

elif tri_equity > 0.10 and dscr > 1.20:
    recommendation = "⚠️ INVESTIR SOUS CONDITIONS"

else:
    recommendation = "❌ REJETER"

st.success(recommendation)

st.markdown(
    f"""
### Synthèse

- TRI Equity : {tri_equity:.2%}
- TRI Projet : {tri_projet:.2%}
- DSCR : {dscr:.2f}x
- LTV : {ltv_calc:.2%}
- MOIC : {moic:.2f}x
- VAN : {van:,.0f}
"""
)
