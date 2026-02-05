# 📖 User Guide - Data Profiling & EDA App

## 🚀 Getting Started

### Step 1: Launch the Application
```bash
streamlit run app.py
```
The app will open in your default browser at `http://localhost:8501`

### Step 2: Upload Your Dataset
1. Click on **"Browse files"** in the sidebar
2. Select a CSV or Excel file (.csv, .xlsx, .xls)
3. The app will automatically load and analyze your data

---

## 📊 Understanding Each Section

### 1️⃣ Dataset Overview
**What you'll see:**
- Total rows and columns
- File type and memory usage
- Preview of first 5 rows

**Use this to:**
- Quickly understand dataset size
- Verify data loaded correctly
- Get initial glimpse of your data

---

### 2️⃣ Feature Summary
**What you'll see:**
- Comprehensive table with all columns
- Data types and feature classifications
- Unique values and null percentages
- Color-coded rows (yellow = some nulls, red = >30% nulls)

**Key Metrics Cards:**
- 🟣 Numerical Features
- 🔴 Categorical Features  
- 🟠 Columns with Nulls
- 🔵 Average Unique Values

**Actions:**
- Click **"📥 Download Summary"** to export as CSV

**Use this to:**
- Identify data types
- Spot columns with missing data
- Understand feature diversity

---

### 3️⃣ Data Quality Checks
**Summary Cards (Color-Coded):**
- 🟢 Green = No issues
- 🟡 Yellow = Warning
- 🔴 Red = Critical

**Expandable Sections:**

**🔍 Missing Values Details** (expanded by default)
- Shows all columns with missing data
- Displays count and percentage
- Highlights columns with >30% missing

**⚠️ Other Quality Issues**
- Constant features (only 1 unique value)
- Columns with all zeros
- Type mismatches (numbers stored as text)

**Use this to:**
- Identify data quality problems
- Prioritize data cleaning tasks
- Understand data completeness

---

### 4️⃣ Descriptive Statistics
**What you'll see:**
- Statistics for numerical columns only
- Count, Mean, Median, Std Dev, Min, Max

**Use this to:**
- Understand central tendencies
- Identify value ranges
- Spot potential outliers

---

### 5️⃣ Correlation Analysis
**What you'll see:**
- Correlation matrix table (color-coded)
- Interactive heatmap visualization

**Color Guide:**
- 🔴 Red = Negative correlation
- ⚪ White = No correlation
- 🔵 Blue = Positive correlation

**Use this to:**
- Find relationships between variables
- Identify multicollinearity
- Guide feature selection

---

### 6️⃣ Distribution & Outlier Analysis

#### Tab 1: 📊 Single Column Analysis

**For Numerical Columns:**
- Histogram (distribution shape)
- Box plot (outliers and quartiles)
- Statistics: Mean, Median, Std Dev, Outlier count

**For Categorical Columns:**
- Bar chart (top 20 values)
- Statistics: Unique values, Most frequent, Frequency

**Use this to:**
- Understand data distribution
- Identify outliers
- Check for skewness

#### Tab 2: 📈 Compare Multiple Columns (NEW!)

**Features:**
- Select 2+ numerical columns
- Overlapping histograms
- Side-by-side box plots
- Comparison statistics table

**Use this to:**
- Compare distributions across features
- Identify similar patterns
- Understand relative scales

---

## 💡 Tips & Best Practices

### 📁 File Upload
- **Recommended size:** < 100MB for best performance
- **Supported formats:** CSV, Excel (.xlsx, .xls)
- **Large files:** Consider sampling first

### 🔍 Data Quality
1. Check the quality summary cards first
2. Expand "Missing Values Details" to see specifics
3. Address high missing data (>30%) before analysis

### 📊 Analysis Workflow
1. **Start with Overview** - Understand your data
2. **Check Quality** - Identify issues
3. **Review Statistics** - Understand distributions
4. **Explore Correlations** - Find relationships
5. **Deep Dive** - Use distribution analysis

### 📈 Correlation Analysis
- Focus on correlations > 0.7 or < -0.7
- Use heatmap for visual patterns
- Consider removing highly correlated features

### 📊 Distribution Analysis
- Use **Single Column** for detailed analysis
- Use **Compare Multiple** to find patterns across features
- Check box plots for outliers (points beyond whiskers)

---

## 🎯 Common Use Cases

### 1. Initial Data Exploration
1. Upload dataset
2. Review Dataset Overview
3. Check Feature Summary
4. Identify data types

### 2. Data Quality Assessment
1. Go to Data Quality Checks
2. Review summary cards
3. Expand sections for details
4. Download summary for reporting

### 3. Feature Selection
1. Check Correlation Analysis
2. Identify highly correlated features
3. Review Descriptive Statistics
4. Use Distribution Analysis for outliers

### 4. Preparing for ML
1. Identify missing values
2. Check for constant features
3. Find type mismatches
4. Analyze distributions for normalization needs

---

## 📥 Export Options

### Feature Summary
- Click **"📥 Download Summary"** button
- Saves as `feature_summary.csv`
- Contains all column metadata

---

## ⚠️ Troubleshooting

### File Won't Upload
- Check file format (CSV or Excel only)
- Ensure file isn't corrupted
- Try with a smaller sample

### No Numerical Columns Warning
- Your dataset has no numeric data
- Correlation and some analyses won't work
- Consider converting appropriate columns

### Slow Performance
- Large datasets take longer
- Consider sampling your data
- Close other browser tabs

### Missing Visualizations
- Check if column has enough data
- Ensure proper data types
- Look for error messages

---

## 🎨 Understanding Color Codes

### Quality Cards
- 🟢 **Green (#28a745)** - All good, no issues
- 🟡 **Yellow (#ffc107)** - Warning, needs attention
- 🔴 **Red (#dc3545)** - Critical, immediate action needed

### Feature Summary Table
- **No highlight** - Clean data
- **Yellow background** - Some missing values
- **Red background** - >30% missing values

### Correlation Heatmap
- **Dark Blue** - Strong positive correlation (close to +1)
- **White** - No correlation (close to 0)
- **Dark Red** - Strong negative correlation (close to -1)

---

## 🔄 Workflow Example

**Scenario: Analyzing a customer dataset**

1. **Upload** `customers.csv`
2. **Overview**: 10,000 rows, 15 columns ✓
3. **Feature Summary**: 
   - 8 numerical, 7 categorical
   - 2 columns with nulls
   - Download summary for documentation
4. **Quality Checks**:
   - 50 duplicate rows found
   - 'phone' column has 40% missing
   - 'country' is constant (all 'USA')
5. **Statistics**: 
   - Age: mean 35, median 33
   - Income: high std dev, check outliers
6. **Correlation**:
   - Age & Years_Customer: 0.85 (strong)
   - Income & Purchase_Amount: 0.72 (strong)
7. **Distribution**:
   - Age: Normal distribution
   - Income: Right-skewed, outliers present
   - Compare Age vs Years_Customer (similar patterns)

**Next Steps:**
- Remove duplicate rows
- Handle phone nulls (impute or drop)
- Remove 'country' (constant)
- Investigate income outliers
- Consider feature engineering with correlated vars

---

## 📞 Need Help?

- Check the sidebar for feature list
- Hover over ℹ️ icons for tooltips
- Review this guide for detailed explanations
- Ensure data is properly formatted

---

**Happy Analyzing! 📊✨**
