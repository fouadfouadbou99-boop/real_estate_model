import pandas as pd
import numpy as np
import numpy_financial as npf


def calculate_investment(price, fees_pct, works, ltv):

    investment = price + price * fees_pct + works
    debt = investment * ltv
    equity = investment - debt

    return investment, debt, equity


def amortizing_debt_schedule(debt, rate, years):

    annuity = npf.pmt(rate, years, -debt)

    balance = debt

    rows = []

    for y in range(1, years + 1):

        interest = balance * rate
        principal = annuity - interest
        end_balance = max(balance - principal, 0)

        rows.append([
            y,
            balance,
            annuity,
            interest,
            principal,
            end_balance
        ])

        balance = end_balance

    return pd.DataFrame(
        rows,
        columns=[
            "Année",
            "Solde Début",
            "Annuité",
            "Intérêts",
            "Principal",
            "Solde Fin"
        ]
    )


def bullet_debt_schedule(debt, rate, years):

    rows = []

    for y in range(1, years + 1):

        interest = debt * rate

        principal = debt if y == years else 0

        rows.append([
            y,
            debt,
            interest,
            principal
        ])

    return pd.DataFrame(
        rows,
        columns=[
            "Année",
            "Dette",
            "Intérêts",
            "Principal"
        ]
    )
