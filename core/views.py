from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Dataset
import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')  # IMPORTANT: non-GUI backend
import matplotlib.pyplot as plt

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
    #--Simple error catching before pandas read
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return render(request, 'core/dataset_detail.html', {
            'dataset': dataset,
            'error': 'Unable to read CSV file. The file may be corrupted or invalid.'
    })

    # ---- BASIC INSIGHTS ----
    num_rows, num_cols = df.shape
    columns = df.columns.tolist()
    dtypes = df.dtypes.astype(str).to_dict()
    missing_values = df.isnull().sum().to_dict()

    # ---- CHARTS DIRECTORY ----
    charts_dir = os.path.join(settings.MEDIA_ROOT, 'charts')
    os.makedirs(charts_dir, exist_ok=True)

    # ---- CHART 1: Missing Values Bar Chart ----
    missing_chart_path = os.path.join(charts_dir, f'missing_{dataset.id}.png')

    if not os.path.exists(missing_chart_path):
        plt.figure(figsize=(12, 5))
        plt.bar(
            missing_values.keys(),
            missing_values.values(),
            color='#4C72B0'
        )
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('Columns')
        plt.ylabel('Number of Missing Values')
        plt.title('Missing Values per Column')
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig(missing_chart_path)
        plt.close()

    # ---- CHART 2: Histogram for First Numeric Column ----
    numeric_cols = df.select_dtypes(include='number').columns

    histogram_path = None
    if len(numeric_cols) > 0:
        col = numeric_cols[0]
        histogram_path = os.path.join(charts_dir, f'hist_{dataset.id}.png')

        if not os.path.exists(histogram_path):
            plt.figure(figsize=(8, 5))
            plt.hist(
                df[col].dropna(),
                bins=30,
                color='#55A868',
                edgecolor='black'
            )
            plt.title(f'Distribution of {col}')
            plt.xlabel(col)
            plt.ylabel('Frequency')
            plt.grid(axis='y', linestyle='--', alpha=0.6)
            plt.tight_layout()
            plt.savefig(histogram_path)
            plt.close()

    context = {
        'dataset': dataset,
        'num_rows': num_rows,
        'num_cols': num_cols,
        'columns': columns,
        'dtypes': dtypes,
        'missing_values': missing_values,
        'missing_chart_url': settings.MEDIA_URL + f'charts/missing_{dataset.id}.png',
        'histogram_url': settings.MEDIA_URL + f'charts/hist_{dataset.id}.png' if histogram_path else None,
    }

    return render(request, 'core/dataset_detail.html', context)