# MARKETING_PROFITABILITY
## Project Setup & Execution Instructions

### 1. Introduction

This guide explains how to set up and run the Marketing Campaign Profitability Analysis & Budget Optimization project using Python, MySQL, and Microsoft Excel.

The project includes data cleaning, exploratory analysis, KPI calculations, profitability analysis, budget optimization, visualizations, and reporting.

### 2. System Requirements

**Required Software**

- Python 3.11 or later
- Visual Studio Code
- MySQL Server
- MySQL Workbench
- Microsoft Excel
- Microsoft PowerPoint (for viewing the presentation)

**Python Libraries**

- pandas
- numpy
- matplotlib
- seaborn
- openpyxl
- python-pptx
- Pillow

### 3. Project Directory

The main project structure is:

```text
MARKETING_PROFITABILITY/
├── 01_Dataset/
│   ├── raw/
│   ├── processed/
│   └── data_dictionary/
├── 02_Excel/
├── 03_SQL/
├── 04_Python/
│   └── outputs/
├── 05_Visualizations/
├── 06_Reports/
├── 07_Presentation/
├── 08_Documentation/
├── 09_Database/
└── README.md
```

### 4. Open the Project

Open Visual Studio Code.

Select **File → Open Folder** and choose the `MARKETING_PROFITABILITY` project directory.

Open a PowerShell terminal in VS Code.

### 5. Create a Python Virtual Environment

From the project root, execute:

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If activation is restricted by PowerShell policy, you can execute Python directly using:

```powershell
.\.venv\Scripts\python.exe --version
```

### 6. Install Python Dependencies

Install the required libraries:

```powershell
.\.venv\Scripts\python.exe -m pip install pandas numpy matplotlib seaborn openpyxl python-pptx Pillow
```

Verify installation:

```powershell
.\.venv\Scripts\python.exe -m pip list
```

In VS Code, select the project's `.venv` interpreter using **Python: Select Interpreter**.

### 7. Prepare the Datasets

Ensure the following CSV files exist inside `01_Dataset/raw/`:

- `campaigns.csv`
- `daily_spend.csv`
- `leads.csv`
- `conversions.csv`

The processed datasets will be stored in `01_Dataset/processed/`.

### 8. MySQL Database Setup

Open MySQL Workbench and connect to your local MySQL server.

Create or select the database:

```sql
CREATE DATABASE IF NOT EXISTS marketing_profitability_db;
USE marketing_profitability_db;
```

Execute the table creation script:

`03_SQL/01_create_tables.sql`

Import the four CSV datasets into their corresponding tables, ensuring the correct data types and relationships.

After importing the data, run:

`03_SQL/02_data_validation.sql`

**Expected Record Counts**

| Table | Records |
|---|---:|
| campaigns | 120 |
| daily_spend | 11,240 |
| leads | 261,684 |
| conversions | 39,696 |

### 9. Run SQL Analysis

Execute the remaining SQL scripts in the following order:

1. `03_marketing_performance.sql`
2. `04_customer_acquisition.sql`
3. `05_revenue_profitability.sql`
4. `06_advanced_analysis.sql`
5. `07_budget_optimization.sql`

These scripts evaluate campaign engagement, customer acquisition, revenue, profitability, and budget allocation opportunities.

### 10. Run Python Analysis

Execute the Python scripts in the following sequence from the project root.

If the Python scripts are located directly inside `04_Python/`, use:

```powershell
.\.venv\Scripts\python.exe .\04_Python\01_data_loading.py
.\.venv\Scripts\python.exe .\04_Python\02_data_cleaning.py
.\.venv\Scripts\python.exe .\04_Python\03_exploratory_analysis.py
.\.venv\Scripts\python.exe .\04_Python\04_marketing_kpis.py
.\.venv\Scripts\python.exe .\04_Python\05_customer_acquisition.py
.\.venv\Scripts\python.exe .\04_Python\06_profitability_analysis.py
.\.venv\Scripts\python.exe .\04_Python\07_budget_optimization.py
.\.venv\Scripts\python.exe .\04_Python\08_data_visualizations.py
```

**Note:** If your Python files are stored in a `04_Python/scripts/` subfolder, update these commands to include `scripts/`.

### 11. Review Python Outputs

The Python analysis generates CSV reports in:

`04_Python/outputs/`

These include:

- Marketing KPI summaries.
- Channel and campaign profitability.
- Customer acquisition analysis.
- Monthly trends.
- Budget optimization scorecards.
- Budget reallocation scenarios.

### 12. Review Visualizations

The project generates eight PNG charts in:

`05_Visualizations/`

The charts include revenue, ROAS, conversion rates, acquisition costs, marketing profit, and budget optimization comparisons.

### 13. Generate the PowerPoint Presentation

From the project root, execute:

```powershell
.\.venv\Scripts\python.exe .\07_Presentation\create_presentation.py
```

The script generates:

`07_Presentation/Marketing_Profitability_Project_Presentation.pptx`

The presentation contains 13 slides covering the business problem, methodology, KPIs, findings, and recommendations.

### 14. Review Reports and Documentation

The business reports are stored in:

`06_Reports/`

The technical documentation is stored in:

`08_Documentation/`

The main project overview and visualizations are accessible through `README.md`.

### 15. Troubleshooting

**Problem: Python import warnings**

Verify that VS Code is using the correct `.venv` interpreter and that the required libraries are installed.

**Problem: FileNotFoundError**

Check the project directory, filenames, and paths used in the Python scripts.

**Problem: MySQL connection error**

Verify that MySQL Server is running and the correct database connection is selected.

**Problem: Missing visualization**

Run the visualization script and confirm that the required analysis CSV files exist.

**Problem: PowerPoint generation error**

Install `python-pptx` and `Pillow`, then rerun the presentation script.

### 16. Conclusion

Following these instructions allows the project workflow to be reproduced from the source datasets through SQL analysis, Python processing, visualizations, and business reporting.

The project demonstrates practical data analytics skills in data preparation, relational querying, KPI development, profitability analysis, and analytical communication.