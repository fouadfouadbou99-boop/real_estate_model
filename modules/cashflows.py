import pandas as pd


def build_cashflows(
        rent,
        growth,
        vacancy,
        charges,
        horizon,
        debt_service):

    rows = []

    current_rent = rent

    for y in range(1, horizon + 1):

        net_rent = current_rent * (1 - vacancy)

        noi = net_rent * (1 - charges)

        cf_equity = noi - debt_service

        rows.append([
            y,
            current_rent,
            net_rent,
            noi,
            cf_equity
        ])

        current_rent *= (1 + growth)

    return pd.DataFrame(
        rows,
        columns=[
            "Année",
            "Loyer",
            "Loyer Net",
            "NOI",
            "CF Equity"
        ]
    )
