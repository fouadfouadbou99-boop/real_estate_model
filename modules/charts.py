import plotly.express as px


def noi_chart(df):

    return px.line(
        df,
        x="Année",
        y="NOI",
        title="Evolution du NOI"
    )


def equity_cf_chart(df):

    return px.bar(
        df,
        x="Année",
        y="CF Equity",
        title="Cash Flow Equity"
    )


def debt_equity_chart(debt, equity):

    return px.pie(
        names=["Dette", "Equity"],
        values=[debt, equity],
        title="Structure Financière"
    )
