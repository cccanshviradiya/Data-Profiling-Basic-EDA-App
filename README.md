# 📊 Universal Data Profiling & Basic EDA App

A comprehensive Streamlit web application for automatic data profiling and exploratory data analysis (EDA) that works with datasets from any domain.

## 🎯 Features

### 1️⃣ File Upload
- ✅ Support for CSV and Excel files (.csv, .xlsx, .xls)
- ✅ Automatic file type detection
- ✅ Graceful error handling for invalid/corrupted files

### 2️⃣ Dataset Overview
- Total number of rows and columns
- File type information
- Memory usage statistics
- Preview of first 5 rows

### 3️⃣ Feature Summary
- Comprehensive table with:
  - Column name
  - Data type
  - Feature type (Numerical/Categorical)
  - Number of unique values
  - Number and percentage of null values
- Visual highlighting of columns with missing data

### 4️⃣ Data Quality Checks
- ✅ Identifies columns with missing values
- ✅ Highlights columns with >30% missing data
- ✅ Detects columns with all zero values
- ✅ Finds constant features (only 1 unique value)
- ✅ Identifies type mismatches (numeric data stored as categorical)
- ✅ Counts duplicate rows

### 5️⃣ Descriptive Statistics
For numerical features:
- Count
- Mean
- Median
- Standard deviation
- Min and Max values

### 6️⃣ Correlation Analysis
- Correlation matrix table
- Interactive correlation heatmap
- Automatic detection of strong correlations (|r| > 0.7)
- Textual insights summarizing key correlations

### 7️⃣ Distribution & Outlier Analysis
**For Numerical Columns:**
- Histogram showing distribution
- Box plot for outlier detection
- Key statistics (mean, median, std dev, outlier count)

**For Categorical Columns:**
- Bar chart of value counts (top 20)
- Unique value count
- Most frequent value and its frequency

### 8️⃣ Missing Value Visualization
- Bar chart showing missing values per column
- Total missing value count
- Missing percentage across entire dataset
- Number of columns affected

## 🚀 Installation

1. **Clone or download this repository**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## 💻 Usage

1. **Run the Streamlit app:**
```bash
streamlit run app.py
```

2. **Upload your dataset:**
   - Click "Browse files" in the sidebar
   - Select a CSV or Excel file
   - The app will automatically analyze your data

3. **Explore the results:**
   - Navigate through different sections
   - Use the column selector in Distribution Analysis
   - Review quality checks and insights

## 📋 Requirements

- Python 3.8+
- streamlit
- pandas
- numpy
- matplotlib
- seaborn
- plotly
- openpyxl (for Excel support)

## 🎨 User Interface

The app features:
- Clean, organized layout with clear sections
- Color-coded alerts (warnings, errors, success messages)
- Interactive visualizations using Plotly
- Responsive design that works on different screen sizes
- Styled metrics and data tables

## 🔧 Code Structure

The application is modular with well-defined functions:

- `load_data()` - Handles file upload and validation
- `classify_feature_type()` - Determines if a column is numerical or categorical
- `create_feature_summary()` - Generates comprehensive feature summary
- `perform_data_quality_checks()` - Runs all quality checks
- `get_descriptive_statistics()` - Computes statistics for numerical features
- `compute_correlation_analysis()` - Analyzes correlations and generates insights
- `plot_*()` - Various plotting functions for visualizations

## 🛡️ Error Handling

The app handles various edge cases:
- Empty datasets
- Corrupted files
- Datasets with no numerical columns
- Datasets with no categorical columns
- Very small datasets
- Files with unsupported formats

## 📊 Example Use Cases

- **Data Scientists:** Quick EDA before model building
- **Business Analysts:** Understanding dataset characteristics
- **Data Engineers:** Data quality validation
- **Students:** Learning about data analysis
- **Anyone:** Quick insights into any CSV/Excel dataset

## 🎯 Best Practices

1. **File Size:** For large datasets (>100MB), consider sampling first
2. **Missing Data:** Review the quality checks section carefully
3. **Correlations:** Pay attention to strong correlations for feature engineering
4. **Outliers:** Use the box plots to identify and investigate outliers

## 📝 Notes

- The app automatically limits categorical bar charts to top 20 values for readability
- Correlation analysis requires at least 2 numerical columns
- Outliers are calculated using the IQR method (1.5 × IQR)
- All visualizations are interactive (zoom, pan, hover for details)

## 🤝 Contributing

Feel free to enhance this app by:
- Adding more statistical tests
- Implementing additional visualizations
- Adding export functionality for reports
- Supporting more file formats

## 📄 License

This project is open source and available for educational and commercial use.

---

**Built with ❤️ using Streamlit**
