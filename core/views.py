from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Dataset
import os
from .analysis.dataframe_summary import (
    load_dataframe,
    get_basic_summary,
    get_numeric_columns
)
from .analysis.charts import (
    generate_missing_values_chart,
    generate_histogram,
    generate_boxplot,
    generate_multi_boxplot
)
from .analysis.comparison import (
    compare_structure,
    compare_dtypes,
    compare_missing_values,
)
from .analysis.insights import generate_insights

def home(request):
    return render(request, 'core/home.html')

@login_required
def dataset_list(request):
    datasets = Dataset.objects.filter(owner=request.user)
    return render(request, 'core/dataset_list.html', {
        'datasets': datasets
    })

@login_required
def upload_dataset(request):
    error = None

    if request.method == 'POST':
        name = request.POST.get('name')
        file = request.FILES.get('file')

        # ---- BASIC VALIDATION ----
        if not file.name.endswith('.csv'):
            error = "Only CSV files are allowed."
        elif file.size == 0:
            error = "Uploaded file is empty / No data."

        if error:
            return render(request, 'core/upload_dataset.html', {
                'error': error
            })

        Dataset.objects.create(
            name=name,
            file=file,
            owner=request.user
        )

        return redirect('/datasets/')

    return render(request, 'core/upload_dataset.html')

# Dataset details view
@login_required
def dataset_detail(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id, owner=request.user)

    file_path = dataset.file.path
    
    # ---- Loading Dataframe & Summary (Error Catching) ----
    df = load_dataframe(file_path)
    if df is None:
        return render(request, 'core/dataset_detail.html', {
            'dataset': dataset,
            'error': 'Unable to read CSV file. The file may be corrupted or invalid.'
        })

    # ---- BASIC INSIGHTS ----
    summary = get_basic_summary(df)
    num_rows = summary["num_rows"]
    num_cols = summary["num_cols"]
    columns = summary["columns"]
    dtypes = summary["dtypes"]
    missing_values = summary["missing_values"] 

    # ---- CHART 1: Missing Values Bar Chart ----
    missing_chart_path = generate_missing_values_chart(
        dataset.id,
        missing_values,
        settings.MEDIA_ROOT
    )

    # ---- CHART 2: Histogram for Selected Numeric Column ----
    numeric_cols = get_numeric_columns(df)

    selected_col = request.GET.get('column')
    histogram_path = None

    if numeric_cols:
        if selected_col not in numeric_cols:
            selected_col = numeric_cols[0]

        histogram_path = generate_histogram(
            dataset.id,
            df,
            selected_col,
            settings.MEDIA_ROOT
        )

    # ---- Chart 3: Boxplot for Numeric Columns (Single Column) ----
    boxplot_path = None

    if numeric_cols and selected_col:
        boxplot_path = generate_boxplot(
            dataset.id,
            df,
            selected_col,
            settings.MEDIA_ROOT
        )

    # ---- Chart 4: Boxplot for Numeric Columns (Multi Columns) ----
    multi_boxplot_path = None

    if numeric_cols:
        multi_boxplot_path = generate_multi_boxplot(
            dataset.id,
            df,
            numeric_cols,
            settings.MEDIA_ROOT
        )

    # ---- Insights (basic) ----
    insights = generate_insights(df, summary, numeric_cols)

    context = {
        'dataset': dataset,
        'num_rows': num_rows,
        'num_cols': num_cols,
        'columns': columns,
        'dtypes': dtypes,
        'missing_values': missing_values,
        'missing_chart_url': settings.MEDIA_URL + missing_chart_path,
        'numeric_columns': numeric_cols,
        'selected_column': selected_col,
        'histogram_url': (
            settings.MEDIA_URL + histogram_path
            if histogram_path else None
        ),
        'boxplot_url': (
            settings.MEDIA_URL + boxplot_path
            if boxplot_path else None
        ),
        'multi_boxplot_url': (
        settings.MEDIA_URL + multi_boxplot_path
        if multi_boxplot_path else None
        ),
        "insights": insights,
    }

    return render(request, 'core/dataset_detail.html', context)

@login_required
def delete_dataset(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id, owner=request.user)

    if request.method == 'POST':
        # Delete CSV file
        if dataset.file and os.path.exists(dataset.file.path):
            os.remove(dataset.file.path)

        # Delete related charts
        charts_dir = os.path.join(settings.MEDIA_ROOT, 'charts')
        if os.path.exists(charts_dir):
            for file in os.listdir(charts_dir):
                if file.startswith(f'hist_{dataset.id}_') or file.startswith(f'missing_{dataset.id}'):
                    os.remove(os.path.join(charts_dir, file))

        dataset.delete()
        return redirect('/datasets/')

    return render(request, 'core/confirm_delete.html', {'dataset': dataset})

@login_required
def compare_selector(request):
    datasets = Dataset.objects.filter(owner=request.user)
    error = None
    if request.method == "POST":
        dataset_a_id = request.POST.get("dataset_a")
        dataset_b_id = request.POST.get("dataset_b")
        if not dataset_a_id or not dataset_b_id:
            error = "Please select two datasets."
        elif dataset_a_id == dataset_b_id:
            error = "Please select two different datasets."
        else:
            return redirect(
                "compare_detail",
                dataset_a_id=dataset_a_id,
                dataset_b_id=dataset_b_id,
            )

    return render(request, "core/compare_selector.html", {"datasets": datasets, "error": error,})

@login_required
def compare_detail(request, dataset_a_id, dataset_b_id):
    dataset_a = get_object_or_404(
        Dataset, id=dataset_a_id, owner=request.user
    )
    dataset_b = get_object_or_404(
        Dataset, id=dataset_b_id, owner=request.user
    )
        
    df_a = load_dataframe(dataset_a.file.path)
    df_b = load_dataframe(dataset_b.file.path)

    if df_a is None or df_b is None:
        return render(
            request,
            "core/compare_detail.html",
            {
                "dataset_a": dataset_a,
                "dataset_b": dataset_b,
                "error": "Unable to read one or both datasets.",
            },
        )

    summary_a = get_basic_summary(df_a)
    summary_b = get_basic_summary(df_b)

    structure_comparison = compare_structure(summary_a, summary_b)
    dtype_mismatches = compare_dtypes(summary_a, summary_b)
    missing_comparison = compare_missing_values(summary_a, summary_b)

    context = {
        "dataset_a": dataset_a,
        "dataset_b": dataset_b,
        "structure": structure_comparison,
        "dtype_mismatches": dtype_mismatches,
        "missing_comparison": missing_comparison,
    }

    return render(request, "core/compare_detail.html", context)