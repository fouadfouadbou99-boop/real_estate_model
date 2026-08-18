import numpy as np
import numpy_financial as npf


def calculate_kpis(
        investment,
        equity,
        debt,
        noi1,
        debt_service,
        interest,
        discount_rate,
        project_cf,
        equity_cf):

    tri_project = npf.irr(project_cf)

    tri_equity = npf.irr(equity_cf)

    npv = npf.npv(
        discount_rate,
        project_cf
    )

    dscr = noi1 / debt_service

    icr = noi1 / interest

    debt_yield = noi1 / debt

    moic = sum(equity_cf[1:]) / equity

    return {
        "TRI Projet": tri_project,
        "TRI Equity": tri_equity,
        "VAN": npv,
        "DSCR": dscr,
        "ICR": icr,
        "Debt Yield": debt_yield,
        "MOIC": moic
    }
