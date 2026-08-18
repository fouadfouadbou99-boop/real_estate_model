import io
import pandas as pd


def export_excel(
        investment_df,
        debt_df,
        cf_df,
        kpi_df):

    output = io.BytesIO()

    with pd.ExcelWriter(
            output,
            engine="xlsxwriter") as writer:

        investment_df.to_excel(
            writer,
            sheet_name="Investissement",
            index=False
        )

        debt_df.to_excel(
            writer,
            sheet_name="Dette",
            index=False
        )

        cf_df.to_excel(
            writer,
            sheet_name="Cashflows",
            index=False
        )

        kpi_df.to_excel(
            writer,
            sheet_name="KPI",
            index=False
        )

    output.seek(0)

    return output
