# 📊 PlotCore

PlotCore is a Django-based web application that allows users to upload CSV datasets, analyze them using Pandas, and visualize insights through dynamically generated charts.

It is designed as a **backend-focused data analytics tool**, showcasing file handling, data processing, caching, authentication, and visualization.

---

## 🚀 Features

- 🔐 User authentication (login/logout)
- 📁 Secure CSV file uploads
- 📊 Dataset analytics using Pandas
- 📈 Server-side visualizations using Matplotlib
- ⚡ File-based caching for performance
- 🎛️ User-controlled numeric column selection
- 🗑️ Safe dataset deletion (DB + files + charts)
- 🎨 Clean UI using Bootstrap
- 🔒 Per-user data isolation
- 🔍 Dataset Comparison

---

## 🧠 Tech Stack

- **Backend**: Django
- **Database**: SQLite (development)
- **Data Analysis**: Pandas
- **Visualization**: Matplotlib
- **UI Styling**: Bootstrap (CDN)
- **Version Control**: Git & GitHub

---

## 🏗️ Project Structure

```
insighthub/
│
├── core/
│ ├── views.py
│ ├── models.py
│ ├── analysis/
│ ├── templates/
│ ├── templatetags/
│
├── insighthub/
│ ├── settings.py
│ ├── urls.py
│
├── manage.py
├── db.sqlite3
└── .gitignore
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Dev-Am12/PlotCore.git
cd PlotCore
```

### 2️⃣ Create & activate virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies
```bash
pip install django pandas matplotlib
```

### 4️⃣ Run migrations
```bash
python manage.py migrate
```

### 5️⃣ Create superuser
```bash
python manage.py createsuperuser
```

### 6️⃣ Start the server
```bash
python manage.py runserver
```

Visit (After running server):
App: http://127.0.0.1:8000/
Admin: http://127.0.0.1:8000/admin/

---

## 📂 CSV Validation Rules

* Only .csv files allowed
* Empty files are rejected
* Invalid or corrupted CSVs handled gracefully

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
* Report bugs
* Suggest new features
* Submit pull requests

---

## 📄 License

This project is created for educational purposes. Feel free to use and modify as needed.

---

## 👨‍💻 Author

**Ashutosh Mishra**
* Github: [Dev-Am12](https://github.com/Dev-Am12)
* LinkedIn: [Ashutosh Mishra](https://www.linkedin.com/in/ashutosh-mishra-836b50367/)

> *Progress Day is Everyday*
