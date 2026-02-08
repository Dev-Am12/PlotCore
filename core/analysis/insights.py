def missing_values_insight(summary):
    missing = summary["missing_values"]
    cols_with_missing = [col for col, count in missing.items() if count > 0]
    if len(cols_with_missing) >= 2:
        return {
            "type": "missing",
            "message": f"{len(cols_with_missing)} columns contain missing values."
        }

    return None


def variability_insight(df, numeric_columns):
    if not numeric_columns:
        return None

    stds = df[numeric_columns].std()
    if stds.empty:
        return None

    max_col = stds.idxmax()
    max_std = stds[max_col]
    mean_std = stds.mean()

    if max_std > 1.5 * mean_std:
        return {
            "type": "variability",
            "message": f"Column '{max_col}' shows high variability compared to others."
        }

    return None


def outlier_insight(df, numeric_columns):
    if not numeric_columns:
        return None

    for col in numeric_columns:
        series = df[col].dropna()
        if series.empty:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:
            continue

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers = series[(series < lower) | (series > upper)]
        if len(outliers) >= 5:
            return {
                "type": "outlier",
                "message": f"Column '{col}' contains several extreme outliers."
            }

    return None


def generate_insights(df, summary, numeric_columns):
    insights = []

    mv = missing_values_insight(summary)
    if mv:
        insights.append(mv)

    var = variability_insight(df, numeric_columns)
    if var:
        insights.append(var)

    out = outlier_insight(df, numeric_columns)
    if out:
        insights.append(out)

    return insights