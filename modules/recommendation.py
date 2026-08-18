def get_recommendation(
        tri_equity,
        dscr,
        ltv,
        van):

    if van < 0:
        return "❌ Rejeter"

    if (
        tri_equity > 0.15
        and dscr > 1.5
        and ltv < 0.50
    ):
        return "✅ Investir"

    if (
        tri_equity > 0.10
        and dscr > 1.20
    ):
        return "⚠ Investir sous conditions"

    return "❌ Rejeter"
