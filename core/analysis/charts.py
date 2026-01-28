import os
import matplotlib
matplotlib.use("Agg") # IMPORTANT: non-GUI backend
import matplotlib.pyplot as plt

def ensure_charts_dir(media_root):
    charts_dir = os.path.join(media_root, "charts")
    os.makedirs(charts_dir, exist_ok=True)
    return charts_dir

def generate_missing_values_chart(dataset_id, missing_values, media_root):
    charts_dir = ensure_charts_dir(media_root)
    filename = f"missing_{dataset_id}.png"
    file_path = os.path.join(charts_dir, filename)

    if not os.path.exists(file_path):
        plt.figure(figsize=(12, 5))
        plt.bar(
            missing_values.keys(),
            missing_values.values(),
        )
        plt.xticks(rotation=45, ha="right")
        plt.xlabel("Columns")
        plt.ylabel("Number of Missing Values")
        plt.title("Missing Values per Column")
        plt.grid(axis="y", linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.savefig(file_path)
        plt.close()

    return f"charts/{filename}"

def generate_histogram(dataset_id, df, column, media_root):
    if column not in df.columns:
        return None

    charts_dir = ensure_charts_dir(media_root)
    filename = f"hist_{dataset_id}_{column}.png"
    file_path = os.path.join(charts_dir, filename)

    if not os.path.exists(file_path):
        plt.figure(figsize=(8, 5))
        plt.hist(df[column].dropna(), bins=30, edgecolor="black")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.title(f"Distribution of {column}")
        plt.grid(axis="y", linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.savefig(file_path)
        plt.close()

    return f"charts/{filename}"

def generate_boxplot(dataset_id, df, column, media_root):
    if column not in df.columns:
        return None

    charts_dir = ensure_charts_dir(media_root)
    filename = f"box_{dataset_id}_{column}.png"
    file_path = os.path.join(charts_dir, filename)

    if not os.path.exists(file_path):
        plt.figure(figsize=(6, 6))
        plt.boxplot(
            df[column].dropna(),
            vert=True,
            patch_artist=True
        )
        plt.ylabel(column)
        plt.title(f"Box Plot of {column}")
        plt.grid(axis="y", linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.savefig(file_path)
        plt.close()

    return f"charts/{filename}"

def generate_multi_boxplot(dataset_id, df, columns, media_root):
    if not columns:
        return None

    charts_dir = ensure_charts_dir(media_root)
    filename = f"box_multi_{dataset_id}.png"
    file_path = os.path.join(charts_dir, filename)

    if not os.path.exists(file_path):
        data = [df[col].dropna() for col in columns if col in df.columns]

        if not data:
            return None

        plt.figure(figsize=(max(6, len(columns) * 1.5), 6))
        plt.boxplot(
            data,
            labels=columns,
            patch_artist=True
        )
        plt.xticks(rotation=45, ha="right")
        plt.title("Box Plot Comparison of Numeric Columns")
        plt.ylabel("Values")
        plt.grid(axis="y", linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.savefig(file_path)
        plt.close()

    return f"charts/{filename}"