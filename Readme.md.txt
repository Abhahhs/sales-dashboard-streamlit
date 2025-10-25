# 🐍 Sales Performance Dashboard – Python & Streamlit Project

## 🙋 Created By: Abhay Singh Rawat

## 🧭 Project Objective

This project reimagines the Sales Performance Dashboard using Python to deliver a **web-based, interactive data application** (dashboard). The objective remains to visualize and assess individual sales performance across states, maintaining the rule of **one salesman per state**.

The Streamlit dashboard allows stakeholders to:
- Identify **top and bottom performing employees**
- Track **sales target achievement**
- Analyze **state-level performance**
- **Interactively filter** and view results using **dynamic widgets**.

---

## Dashboard (Example Placeholder)
[A screenshot of your Streamlit/Dash app would go here]
*(Note: You will replace the Excel screenshot with a screenshot of your Python dashboard)*

---

## ⚙️ Process Overview – My Python Approach

### 1. Data Preparation & Loading (Pandas)
- **I loaded** the raw Excel data into a **Pandas DataFrame**.
- **I performed** data cleaning (e.g., ensuring correct data types, checking for duplicate entries).
- **I engineered** key performance indicator (KPI) columns, such as `Target Hit %` and `Away From Target %`.

### 2. Data Aggregation (Pandas Pivot/Groupby)
- **I used Pandas' powerful `.pivot_table()` and `.groupby()` functions** to calculate the required metrics for visualization, replacing the functionality of Excel Pivot Tables.
    - Aggregations included: Total Sales, Target Achievement Rate, and Sales Executive ranking.

### 3. Interactive Visualization (Plotly/Matplotlib)
- **I developed 3 core, interactive charts** using **Plotly Express** (or Matplotlib/Seaborn):
    - **Bar Chart:** Top 5 and Bottom 5 salesmen by total sales.
    - **Gauge/Pie Chart:** Overall Target Achievement Percentage.
    - **Line Chart:** Performance trend over time (if daily data is available).

### 4. Web Application Development (Streamlit)
- **I built the user interface using the Streamlit framework**, allowing the dashboard to run as a local web application.
- **I implemented dynamic filtering using Streamlit widgets** (e.g., `st.selectbox` and `st.multiselect`) to allow users to filter the entire dashboard by State/Region, replacing the original VBA checkbox functionality.

### 5. Deployment (Optional but Recommended)
- The application is ready for deployment on platforms like Streamlit Cloud or Heroku, making it accessible via a web link.

---

## 🔍 Key Python Libraries Used

- **Pandas:** Data manipulation and analysis.
- **Streamlit (or Dash):** Building the interactive web application interface.
- **Plotly (or Matplotlib/Seaborn):** Generating the dynamic and static visualizations.

---