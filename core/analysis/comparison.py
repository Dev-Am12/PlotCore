def compare_structure(summary_a, summary_b):
    cols_a = set(summary_a["columns"])
    cols_b = set(summary_b["columns"])

    common_columns = sorted(cols_a & cols_b)
    only_in_a = sorted(cols_a - cols_b)
    only_in_b = sorted(cols_b - cols_a)

    return {
        "rows": (summary_a["num_rows"], summary_b["num_rows"]),
        "columns": (summary_a["num_cols"], summary_b["num_cols"]),
        "common_columns": common_columns,
        "only_in_a": only_in_a,
        "only_in_b": only_in_b,
    }

def compare_dtypes(summary_a, summary_b):
    mismatches = {}
    for col in summary_a["columns"]:
        if col in summary_b["columns"]:
            dtype_a = summary_a["dtypes"].get(col)
            dtype_b = summary_b["dtypes"].get(col)

            if dtype_a != dtype_b:
                mismatches[col] = (dtype_a, dtype_b)

    return mismatches

def compare_missing_values(summary_a, summary_b):
    comparison = {}
    for col in summary_a["missing_values"]:
        if col in summary_b["missing_values"]:
            comparison[col] = {
                "dataset_a": summary_a["missing_values"][col],
                "dataset_b": summary_b["missing_values"][col],
            }

    return comparison