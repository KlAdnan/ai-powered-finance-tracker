# AI-Powered Finance Tracker

An intelligent financial management system built with Python and Streamlit that helps users track expenses, plan investments, and achieve their financial goals.

## Features

- 📊 Smart Expense Tracking
- 💰 Investment Planning
- 📈 Portfolio Management
- 🎯 Goal Setting & Tracking
- 📱 Responsive Dashboard
- 🌙 Dark/Light Mode
- 📊 Advanced Analytics

## Prerequisites

Ensure you have the following installed before running the project:

1. **Python (>=3.8)**: Download and install Python from [python.org](https://www.python.org/downloads/).
2. **pip**: Ensure pip is installed and updated.
   ```bash
   python -m ensurepip --default-pip
   python -m pip install --upgrade pip
   ```
3. **Git**: Install Git if you want to clone the repository instead of downloading the ZIP file. [Download Git](https://git-scm.com/downloads).

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/KlAdnan/ai-powered-finance-tracker.git
```

### 2. Navigate to the Project Directory

```bash
cd ai-powered-finance-tracker
```

If you can't find the directory after cloning, verify the folder name using:
```bash
ls  # macOS/Linux
dir  # Windows
```
If needed, navigate manually to the correct directory.

### 3. Create a Virtual Environment (Recommended)

```bash
python -m venv venv  # Create a virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### 4. Install Required Packages

Run the following command to install all dependencies:

```bash
pip install -r requirements.txt
```

If you need to install dependencies manually, use:

```bash
pip install streamlit pandas numpy plotly yfinance streamlit-option-menu hashlib
```

### 5. Create a SQLite Database

Run the application once to initialize the database:

```bash
python realfinance.py
```

Alternatively, create the database manually:

```bash
python -c "import sqlite3; conn = sqlite3.connect('finance_tracker.db'); conn.close()"
```

## Running the Application

To start the Streamlit web app, run:

```bash
streamlit run realfinance.py
```

Then open `http://localhost:8501` in your browser.

## Project Structure

```
ai-powered-finance-tracker/
│
├── realfinance.py          # Main application script
├── requirements.txt        # Required dependencies
├── finance_tracker.db      # SQLite database file (auto-generated)
└── README.md               # Project documentation
```

## Version Control (Optional but Recommended)

To track changes using Git, initialize the repository and make the first commit:

```bash
git init
git add .
git commit -m "Initial commit"
```

To push changes to GitHub:

```bash
git remote add origin https://github.com/KlAdnan/ai-powered-finance-tracker.git
git branch -M main
git push -u origin main
```

## Troubleshooting

### 1. `ModuleNotFoundError`
If you get an error like `ModuleNotFoundError: No module named 'streamlit'`, make sure you have installed all dependencies by running:

```bash
pip install -r requirements.txt
```

### 2. Database Errors
If you face issues with the database, try deleting `finance_tracker.db` and rerunning the script to regenerate it:

```bash
rm finance_tracker.db  # macOS/Linux
del finance_tracker.db  # Windows
python realfinance.py
```

### 3. Streamlit Not Found
If the command `streamlit run` is not recognized, activate the virtual environment or install Streamlit globally:

```bash
pip install streamlit
```

### 4. Can't Find the Cloned Directory
If the repository directory is missing after cloning, try:

```bash
ls  # macOS/Linux
dir  # Windows
```
Manually navigate to the correct directory or ensure the repository was cloned properly.

## Contributing

Feel free to fork this repository, submit pull requests, or report issues. Contributions are welcome!

## Author

Developed by **Muhammed Adnan**  
📧 Contact: [kladnan321@gmail.com](mailto:kladnan321@gmail.com)

