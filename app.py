"""
Universal Data Profiling & Basic EDA App
A Streamlit application for comprehensive exploratory data analysis
"""

import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import warnings

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Universal Data Profiling & EDA",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
        background-color: #f8f9fa;
    }
    
    /* Section cards */
    .section-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* Metrics styling */
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stMetric label {
        color: white !important;
        font-weight: 600;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 24px !important;
        font-weight: bold;
    }
    
    /* Headers */
    h1 {
        color: #2d3748;
        padding: 20px 0;
        border-bottom: 3px solid #667eea;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 {
        color: #2d3748;
        margin-top: 30px;
        margin-bottom: 15px;
        font-weight: 600;
        padding-left: 10px;
        border-left: 4px solid #667eea;
    }
    
    h3 {
        color: #4a5568;
        font-weight: 600;
    }
    
    /* Alert boxes */
    .highlight-warning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffe8a1 100%);
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #ffc107;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .highlight-danger {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #dc3545;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .highlight-success {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #28a745;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .highlight-info {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #17a2b8;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: white;
        border-radius: 10px;
        padding: 20px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #e2e8f0;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f7fafc;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    </style>
""", unsafe_allow_html=True)


def load_data(uploaded_file):
    """
    Load data from uploaded file (CSV or Excel)
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        tuple: (DataFrame, file_type, error_message)
    """
    try:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
            file_type = "CSV"
        elif file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file)
            file_type = "Excel"
        else:
            return None, None, "Unsupported file format. Please upload CSV or Excel files."
        
        # Check if dataframe is empty
        if df.empty:
            return None, None, "The uploaded file is empty."
        
        return df, file_type, None
        
    except Exception as e:
        return None, None, f"Error loading file: {str(e)}"


def classify_feature_type(series):
    """
    Classify a pandas Series as Numerical or Categorical
    
    Args:
        series: pandas Series
        
    Returns:
        str: 'Numerical' or 'Categorical'
    """
    if pd.api.types.is_numeric_dtype(series):
        return 'Numerical'
    else:
        return 'Categorical'


def create_feature_summary(df):
    """
    Create a comprehensive feature summary table
    
    Args:
        df: pandas DataFrame
        
    Returns:
        pandas DataFrame with feature summary
    """
    summary_data = []
    
    for col in df.columns:
        null_count = df[col].isnull().sum()
        null_percentage = (null_count / len(df)) * 100
        
        summary_data.append({
            'Column Name': col,
            'Data Type': str(df[col].dtype),
            'Feature Type': classify_feature_type(df[col]),
            'Unique Values': df[col].nunique(),
            'Null Values': null_count,
            'Null %': round(null_percentage, 2)
        })
    
    summary_df = pd.DataFrame(summary_data)
    return summary_df


def perform_data_quality_checks(df):
    """
    Perform comprehensive data quality checks
    
    Args:
        df: pandas DataFrame
        
    Returns:
        dict: Dictionary containing various quality check results
    """
    quality_report = {
        'columns_with_missing': [],
        'columns_high_missing': [],
        'columns_all_zeros': [],
        'constant_features': [],
        'type_mismatch': [],
        'duplicate_rows': 0
    }
    
    for col in df.columns:
        # Missing values
        null_count = df[col].isnull().sum()
        null_percentage = (null_count / len(df)) * 100
        
        if null_count > 0:
            quality_report['columns_with_missing'].append((col, null_count, null_percentage))
        
        if null_percentage > 30:
            quality_report['columns_high_missing'].append((col, null_percentage))
        
        # All zeros
        if pd.api.types.is_numeric_dtype(df[col]):
            if (df[col].dropna() == 0).all():
                quality_report['columns_all_zeros'].append(col)
        
        # Constant features
        if df[col].nunique() == 1:
            quality_report['constant_features'].append(col)
        
        # Type mismatch (numeric values stored as categorical)
        if df[col].dtype == 'object':
            try:
                # Try to convert to numeric
                pd.to_numeric(df[col].dropna())
                quality_report['type_mismatch'].append(col)
            except:
                pass
    
    # Duplicate rows
    quality_report['duplicate_rows'] = df.duplicated().sum()
    
    return quality_report


def get_descriptive_statistics(df):
    """
    Get descriptive statistics for numerical features
    
    Args:
        df: pandas DataFrame
        
    Returns:
        pandas DataFrame with descriptive statistics
    """
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numerical_cols) == 0:
        return None
    
    stats_df = df[numerical_cols].describe().T
    stats_df['median'] = df[numerical_cols].median()
    
    # Reorder columns
    stats_df = stats_df[['count', 'mean', 'median', 'std', 'min', 'max']]
    stats_df = stats_df.round(2)
    
    return stats_df


def compute_correlation_analysis(df):
    """
    Compute correlation matrix and identify strong correlations
    
    Args:
        df: pandas DataFrame
        
    Returns:
        tuple: (correlation_matrix, strong_correlations_list, insights)
    """
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numerical_cols) < 2:
        return None, None, "Not enough numerical columns for correlation analysis."
    
    corr_matrix = df[numerical_cols].corr()
    
    # Find strong correlations (excluding diagonal)
    strong_correlations = []
    insights = []
    
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_value = corr_matrix.iloc[i, j]
            if abs(corr_value) > 0.7:
                col1 = corr_matrix.columns[i]
                col2 = corr_matrix.columns[j]
                strong_correlations.append((col1, col2, corr_value))
                
                if corr_value > 0.7:
                    insights.append(f"Strong positive correlation ({corr_value:.2f}) between **{col1}** and **{col2}**")
                elif corr_value < -0.7:
                    insights.append(f"Strong negative correlation ({corr_value:.2f}) between **{col1}** and **{col2}**")
    
    if not insights:
        insights.append("No strong correlations (|r| > 0.7) found between numerical features.")
    
    return corr_matrix, strong_correlations, insights


def plot_correlation_heatmap(corr_matrix):
    """
    Create correlation heatmap using plotly
    
    Args:
        corr_matrix: pandas DataFrame correlation matrix
        
    Returns:
        plotly figure
    """
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title="Correlation Heatmap",
        xaxis_title="Features",
        yaxis_title="Features",
        height=600,
        width=800
    )
    
    return fig


def plot_histogram(df, column):
    """
    Create histogram with marginal box plot for numerical column
    
    Args:
        df: pandas DataFrame
        column: column name
        
    Returns:
        plotly figure
    """
    fig = px.histogram(
        df, 
        x=column, 
        nbins=30,
        title=f"Distribution & Outlier Analysis: {column}",
        labels={column: column, 'count': 'Frequency'},
        color_discrete_sequence=['#667eea'],
        marginal="box", # Adds the box plot above the histogram
        height=500
    )
    
    fig.update_layout(
        showlegend=False,
        bargap=0.1
    )
    
    return fig


def plot_boxplot(df, column):
    """
    Create box plot for numerical column
    
    Args:
        df: pandas DataFrame
        column: column name
        
    Returns:
        plotly figure
    """
    fig = px.box(
        df, 
        y=column,
        title=f"Box Plot of {column}",
        color_discrete_sequence=['#2ca02c']
    )
    
    fig.update_layout(
        showlegend=False,
        height=400
    )
    
    return fig


def plot_categorical_bar(df, column):
    """
    Create bar chart for categorical column
    
    Args:
        df: pandas DataFrame
        column: column name
        
    Returns:
        plotly figure
    """
    value_counts = df[column].value_counts().head(20)  # Limit to top 20
    
    fig = px.bar(
        x=value_counts.index,
        y=value_counts.values,
        title=f"Value Counts for {column} (Top 20)",
        labels={'x': column, 'y': 'Count'},
        color_discrete_sequence=['#ff7f0e']
    )
    
    fig.update_layout(
        showlegend=False,
        height=400,
        xaxis_tickangle=-45
    )
    
    return fig


def plot_missing_values(df):
    """
    Create bar chart for missing values
    
    Args:
        df: pandas DataFrame
        
    Returns:
        plotly figure
    """
    missing_counts = df.isnull().sum()
    missing_counts = missing_counts[missing_counts > 0].sort_values(ascending=False)
    
    if len(missing_counts) == 0:
        return None
    
    fig = px.bar(
        x=missing_counts.index,
        y=missing_counts.values,
        title="Missing Values by Column",
        labels={'x': 'Column', 'y': 'Missing Count'},
        color_discrete_sequence=['#d62728']
    )
    
    fig.update_layout(
        showlegend=False,
        height=400,
        xaxis_tickangle=-45
    )
    
    return fig




def generate_comprehensive_report(df, file_type, summary_df, quality_report, stats_df, corr_matrix):
    """Generate a comprehensive Excel report with all analysis results"""
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Sheet 1: Overview
        overview_data = {
            'Metric': ['File Type', 'Total Rows', 'Total Columns', 'Memory Usage (MB)', 
                      'Duplicate Rows', 'Columns with Missing Values'],
            'Value': [
                file_type,
                len(df),
                len(df.columns),
                f"{df.memory_usage(deep=True).sum() / 1024**2:.2f}",
                quality_report['duplicate_rows'],
                len(quality_report['columns_with_missing'])
            ]
        }
        pd.DataFrame(overview_data).to_excel(writer, sheet_name='Overview', index=False)
        
        # Sheet 2: Feature Summary
        summary_df.to_excel(writer, sheet_name='Feature Summary', index=False)
        
        # Sheet 3: Data Quality Issues
        quality_data = []
        for col, count, pct in quality_report['columns_with_missing']:
            quality_data.append({'Issue Type': 'Missing Values', 'Column': col, 'Details': f"{count} missing ({pct:.2f}%)"})
        for col in quality_report['constant_features']:
            quality_data.append({'Issue Type': 'Constant Feature', 'Column': col, 'Details': 'Only 1 unique value'})
        for col in quality_report['columns_all_zeros']:
            quality_data.append({'Issue Type': 'All Zeros', 'Column': col, 'Details': 'All values are zero'})
        for col in quality_report['type_mismatch']:
            quality_data.append({'Issue Type': 'Type Mismatch', 'Column': col, 'Details': 'Numeric stored as categorical'})
        
        if quality_data:
            pd.DataFrame(quality_data).to_excel(writer, sheet_name='Quality Issues', index=False)
        
        # Sheet 4: Descriptive Statistics
        if stats_df is not None:
            stats_df.to_excel(writer, sheet_name='Descriptive Stats')
        
        # Sheet 5: Correlation Matrix
        if corr_matrix is not None:
            corr_matrix.to_excel(writer, sheet_name='Correlation Matrix')
        
        # Sheet 6: Data Preview
        df.head(100).to_excel(writer, sheet_name='Data Preview', index=False)
    
    output.seek(0)
    return output


def main():
    """Main application function"""
    
    # Title and description with better styling
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h1 style='font-size: 3em; margin-bottom: 10px;'>📊 Data Profiling & EDA</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("<h2 style='color: white; text-align: center;'>📁 Upload Dataset</h2>", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a CSV or Excel file",
            type=['csv', 'xlsx', 'xls'],
            help="Upload your dataset for analysis"
        )
        
        st.markdown("---")
        
        # Show file info if uploaded
        if uploaded_file is not None:
            st.markdown("<h3 style='color: white;'>📄 File Information</h3>", unsafe_allow_html=True)
            file_size = uploaded_file.size / 1024  # KB
            if file_size > 1024:
                file_size_str = f"{file_size/1024:.2f} MB"
            else:
                file_size_str = f"{file_size:.2f} KB"
            
            st.markdown(f"""
                <div style='color: white; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;'>
                    <p><strong>Name:</strong> {uploaded_file.name}</p>
                    <p><strong>Size:</strong> {file_size_str}</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
        

    
    # Main content
    if uploaded_file is None:
        # Welcome screen with feature cards
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div style='background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; height: 250px;'>
                    <div style='font-size: 3em; margin-bottom: 25px;'>📋</div>
                    <h3 style='color: #667eea; margin-bottom: 0;'>Data Overview</h3>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div style='background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; height: 250px;'>
                    <div style='font-size: 3em; margin-bottom: 25px;'>🔍</div>
                    <h3 style='color: #667eea; margin-bottom: 0;'>Quality Checks</h3>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div style='background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; height: 250px;'>
                    <div style='font-size: 3em; margin-bottom: 25px;'>📊</div>
                    <h3 style='color: #667eea; margin-bottom: 0;'>Visual Analysis</h3>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Instructions
        st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; text-align: center; color: white;'>
                <h2 style='color: white; margin-bottom: 0;'>👈 Get Started</h2>
            </div>
        """, unsafe_allow_html=True)
        
        return
    
    # Load data
    with st.spinner("🔄 Loading and analyzing your dataset..."):
        df, file_type, error = load_data(uploaded_file)
    
    if error:
        st.error(f"❌ {error}")
        return
    
    # Store in session state
    st.session_state['df'] = df
    st.session_state['file_type'] = file_type
    
    # Quick Stats Bar at the top
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
            <h3 style='color: white; margin: 0; text-align: center;'>📈 Quick Statistics</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # ===== SECTION 1: DATASET OVERVIEW =====
    st.header("1️⃣ Dataset Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Rows", f"{len(df):,}")
    
    with col2:
        st.metric("Total Columns", f"{len(df.columns):,}")
    
    with col3:
        st.metric("File Type", file_type)
    
    with col4:
        memory_usage = df.memory_usage(deep=True).sum() / 1024**2
        st.metric("Memory Usage", f"{memory_usage:.2f} MB")
    
    st.subheader("Dataset Preview (First 5 Rows)")
    st.dataframe(df.head(), use_container_width=True)
    
    # ===== SECTION 2: FEATURE SUMMARY =====
    st.header("2️⃣ Feature Summary")
    
    summary_df = create_feature_summary(df)
    
    # Add download button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("")
    with col2:
        csv = summary_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Summary",
            data=csv,
            file_name="feature_summary.csv",
            mime="text/csv",
        )
    
    # Highlight rows with issues
    def highlight_issues(row):
        if row['Null %'] > 30:
            return ['background-color: #f8d7da'] * len(row)
        elif row['Null %'] > 0:
            return ['background-color: #fff3cd'] * len(row)
        else:
            return [''] * len(row)
    
    styled_summary = summary_df.style.apply(highlight_issues, axis=1)
    st.dataframe(styled_summary, use_container_width=True)
    
    # Summary statistics in colored cards
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        num_features = len(summary_df[summary_df['Feature Type'] == 'Numerical'])
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; text-align: center; color: white;'>
                <h2 style='color: white; margin: 0;'>{num_features}</h2>
                <p style='margin: 5px 0 0 0;'>Numerical Features</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        cat_features = len(summary_df[summary_df['Feature Type'] == 'Categorical'])
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 10px; text-align: center; color: white;'>
                <h2 style='color: white; margin: 0;'>{cat_features}</h2>
                <p style='margin: 5px 0 0 0;'>Categorical Features</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        cols_with_nulls = len(summary_df[summary_df['Null Values'] > 0])
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #ffa751 0%, #ffe259 100%); padding: 20px; border-radius: 10px; text-align: center; color: white;'>
                <h2 style='color: white; margin: 0;'>{cols_with_nulls}</h2>
                <p style='margin: 5px 0 0 0;'>Columns with Nulls</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_unique = int(summary_df['Unique Values'].mean())
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 20px; border-radius: 10px; text-align: center; color: white;'>
                <h2 style='color: white; margin: 0;'>{avg_unique}</h2>
                <p style='margin: 5px 0 0 0;'>Avg Unique Values</p>
            </div>
        """, unsafe_allow_html=True)
    
    # ===== SECTION 3: DATA QUALITY CHECKS =====
    st.header("3️⃣ Data Quality Checks")
    
    quality_report = perform_data_quality_checks(df)
    
    # Quality summary cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        issue_count = len(quality_report['columns_with_missing'])
        color = "#28a745" if issue_count == 0 else "#ffc107"
        st.markdown(f"""
            <div style='background: {color}; padding: 20px; border-radius: 10px; text-align: center; color: white;'>
                <h2 style='color: white; margin: 0;'>{issue_count}</h2>
                <p style='margin: 5px 0 0 0;'>Missing Value Cols</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        dup_count = quality_report['duplicate_rows']
        color = "#28a745" if dup_count == 0 else "#dc3545"
        st.markdown(f"""
            <div style='background: {color}; padding: 20px; border-radius: 10px; text-align: center; color: white;'>
                <h2 style='color: white; margin: 0;'>{dup_count}</h2>
                <p style='margin: 5px 0 0 0;'>Duplicate Rows</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        const_count = len(quality_report['constant_features'])
        color = "#28a745" if const_count == 0 else "#ffc107"
        st.markdown(f"""
            <div style='background: {color}; padding: 20px; border-radius: 10px; text-align: center; color: white;'>
                <h2 style='color: white; margin: 0;'>{const_count}</h2>
                <p style='margin: 5px 0 0 0;'>Constant Features</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        mismatch_count = len(quality_report['type_mismatch'])
        color = "#28a745" if mismatch_count == 0 else "#ffc107"
        st.markdown(f"""
            <div style='background: {color}; padding: 20px; border-radius: 10px; text-align: center; color: white;'>
                <h2 style='color: white; margin: 0;'>{mismatch_count}</h2>
                <p style='margin: 5px 0 0 0;'>Type Mismatches</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Detailed quality checks in expanders
    with st.expander("🔍 Missing Values Details", expanded=True):
        if quality_report['columns_with_missing']:
            missing_df = pd.DataFrame(
                quality_report['columns_with_missing'],
                columns=['Column', 'Missing Count', 'Missing %']
            )
            st.dataframe(missing_df, use_container_width=True)
            
            if quality_report['columns_high_missing']:
                st.markdown(f"""
                <div class="highlight-danger">
                🚨 <strong>High Missing Data (>30%):</strong> {', '.join([col for col, _ in quality_report['columns_high_missing']])}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ No missing values detected")
    
    with st.expander("⚠️ Other Quality Issues"):
        issues_found = False
        
        if quality_report['constant_features']:
            issues_found = True
            st.markdown(f"""
            <div class="highlight-warning">
            ⚠️ <strong>Constant Features (only 1 unique value):</strong> {', '.join(quality_report['constant_features'])}
            </div>
            """, unsafe_allow_html=True)
        
        if quality_report['columns_all_zeros']:
            issues_found = True
            st.markdown(f"""
            <div class="highlight-warning">
            ⚠️ <strong>Columns with All Zeros:</strong> {', '.join(quality_report['columns_all_zeros'])}
            </div>
            """, unsafe_allow_html=True)
        
        if quality_report['type_mismatch']:
            issues_found = True
            st.markdown(f"""
            <div class="highlight-warning">
            ⚠️ <strong>Potential Type Mismatch (numeric stored as categorical):</strong> {', '.join(quality_report['type_mismatch'])}
            </div>
            """, unsafe_allow_html=True)
        
        if not issues_found:
            st.success("✅ No other quality issues detected")
    
    # Data Actions Section
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🛠️ Data Actions", expanded=False):
        st.markdown("**Quick data cleaning operations**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Remove duplicates button
            if quality_report['duplicate_rows'] > 0:
                if st.button(f"🗑️ Remove {quality_report['duplicate_rows']} Duplicate Rows", key="remove_dups"):
                    df_cleaned = df.drop_duplicates()
                    st.session_state['df'] = df_cleaned
                    st.success(f"✅ Removed {quality_report['duplicate_rows']} duplicate rows!")
                    st.info("💡 Refresh the page (F5) to see updated analysis")
            else:
                st.info("✅ No duplicate rows to remove")
        
        with col2:
            # Download cleaned data
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Current Dataset",
                data=csv,
                file_name=f"cleaned_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                help="Download the current state of the dataset"
            )

        # Missing Value Handling Tool
        st.markdown("---")
        st.subheader("🧩 Handle Missing Values")
        
        # Identify columns with missing values
        missing_cols = [col for col in df.columns if df[col].isnull().sum() > 0]
        
        if missing_cols:
            check_col1, check_col2, check_col3 = st.columns([1, 1, 1])
            
            with check_col1:
                target_col = st.selectbox(
                    "Select Column with Missing Values", 
                    options=missing_cols,
                    key="missing_target"
                )
                
            with check_col2:
                # determine options based on column type
                if pd.api.types.is_numeric_dtype(df[target_col]):
                    method_options = [
                        "Fill with 0 (e.g., No Sales)",
                        "Fill with Mean (Average)", 
                        "Fill with Median (Middle Value)",
                        "Dropping Rows",
                        "Drop Column"
                    ]
                else:
                    method_options = [
                        "Fill with Mode (Most Frequent)", 
                        "Fill with 'Unknown'", 
                        "Dropping Rows",
                        "Drop Column"
                    ]
                
                fill_method = st.selectbox(
                    "Choose Strategy", 
                    options=method_options,
                    key="fill_strategy"
                )
                
            with check_col3:
                st.write("") # Spacer text for alignment
                st.write("") 
                if st.button("Apply Fix", key="apply_fill"):
                    if "Dropping Rows" in fill_method:
                        df_cleaned = df.dropna(subset=[target_col])
                        msg = f"Removed rows with missing values in '{target_col}'"
                    elif "Drop Column" in fill_method:
                        df_cleaned = df.drop(columns=[target_col])
                        msg = f"Dropped column '{target_col}'"
                    elif "0" in fill_method:
                        df_cleaned = df.copy()
                        df_cleaned[target_col] = df_cleaned[target_col].fillna(0)
                        msg = f"Filled missing values in '{target_col}' with 0"
                    elif "Mean" in fill_method:
                        val = df[target_col].mean()
                        df_cleaned = df.copy()
                        df_cleaned[target_col] = df_cleaned[target_col].fillna(val)
                        msg = f"Filled missing values in '{target_col}' with Mean ({val:.2f})"
                    elif "Median" in fill_method:
                        val = df[target_col].median()
                        df_cleaned = df.copy()
                        df_cleaned[target_col] = df_cleaned[target_col].fillna(val)
                        msg = f"Filled missing values in '{target_col}' with Median ({val:.2f})"
                    elif "Mode" in fill_method:
                        val = df[target_col].mode()[0]
                        df_cleaned = df.copy()
                        df_cleaned[target_col] = df_cleaned[target_col].fillna(val)
                        msg = f"Filled missing values in '{target_col}' with Mode ('{val}')"
                    elif "Unknown" in fill_method:
                        df_cleaned = df.copy()
                        df_cleaned[target_col] = df_cleaned[target_col].fillna("Unknown")
                        msg = f"Filled missing values in '{target_col}' with 'Unknown'"
                    
                    st.session_state['df'] = df_cleaned
                    st.success(f"✅ Success! {msg}")
                    st.info("🔄 Refresh (F5) to update all analysis charts")
        else:
            st.success("✨ Great! No missing values detected in the dataset.")
    
    # ===== SECTION 4: DESCRIPTIVE STATISTICS =====
    st.header("4️⃣ Descriptive Statistics")
    
    stats_df = get_descriptive_statistics(df)
    
    if stats_df is not None:
        st.dataframe(stats_df, use_container_width=True)
    else:
        st.warning("⚠️ No numerical columns found in the dataset")
    
    # ===== SECTION 5: CORRELATION ANALYSIS =====
    st.header("5️⃣ Correlation Analysis")
    
    corr_matrix, strong_corr, insights = compute_correlation_analysis(df)
    
    if corr_matrix is not None:
        # Display correlation table
        st.subheader("Correlation Matrix")
        st.dataframe(corr_matrix.style.background_gradient(cmap='RdBu', vmin=-1, vmax=1), use_container_width=True)
        
        # Display heatmap
        st.subheader("Correlation Heatmap")
        fig = plot_correlation_heatmap(corr_matrix)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Not enough numerical columns for correlation analysis (minimum 2 required)")
    
    # Generate and offer download of comprehensive report
    # Add this in sidebar after all analysis is done
    with st.sidebar:
        st.markdown("---")
        st.markdown("<h3 style='color: white;'>📊 Download Report</h3>", unsafe_allow_html=True)
        
        # Generate the report
        report_excel = generate_comprehensive_report(
            df, 
            file_type, 
            summary_df, 
            quality_report, 
            stats_df, 
            corr_matrix
        )
        
        st.download_button(
            label="📥 Download Full Analysis Report",
            data=report_excel,
            file_name=f"data_analysis_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Download comprehensive Excel report with all analysis results"
        )

    
    # ===== SECTION 6: DISTRIBUTION & OUTLIER ANALYSIS =====
    st.header("6️⃣ Distribution & Outlier Analysis")
    
    # Advanced settings for unique ID handling
    with st.expander("⚙️ Analysis Settings (Handle Duplicates/Repeated Items)", expanded=False):

        unique_id_col = st.selectbox(
            "Select Unique ID Column (e.g., Product ID, SKU):",
            options=["None"] + list(df.columns),
            index=0,
            help="Select a column to drop duplicate values based on this identifier."
        )
    
    # Determine the dataframe to analyze
    if unique_id_col != "None":
        plot_df = df.drop_duplicates(subset=unique_id_col)
        st.success(
            f"✅ Analyzing **{len(plot_df)}** unique entries based on '{unique_id_col}' "
            f"(Excluded {len(df) - len(plot_df)} duplicate rows)"
        )
    else:
        plot_df = df

    # Analysis Section (Single Column Only)
    selected_column = st.selectbox(
        "Select a column to analyze",
        options=plot_df.columns,
        help="Choose a column to view its distribution",
        key="single_col"
    )
    
    if selected_column:
        feature_type = classify_feature_type(plot_df[selected_column])
        
        st.subheader(f"Analysis of: {selected_column} ({feature_type})")
        
        if feature_type == 'Numerical':
            # Display combined distribution and box plot
            st.plotly_chart(plot_histogram(plot_df, selected_column), use_container_width=True)
            
            
            # Additional statistics
            st.markdown("#### Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Mean", f"{plot_df[selected_column].mean():.2f}")
            
            with col2:
                st.metric("Median", f"{plot_df[selected_column].median():.2f}")
            
            with col3:
                st.metric("Std Dev", f"{plot_df[selected_column].std():.2f}")
            
            with col4:
                # Calculate outliers using IQR method
                Q1 = plot_df[selected_column].quantile(0.25)
                Q3 = plot_df[selected_column].quantile(0.75)
                IQR = Q3 - Q1
                outliers = plot_df[(plot_df[selected_column] < (Q1 - 1.5 * IQR)) | (plot_df[selected_column] > (Q3 + 1.5 * IQR))]
                st.metric("Outliers", len(outliers))
        
        else:  # Categorical
            st.plotly_chart(plot_categorical_bar(plot_df, selected_column), use_container_width=True)
            
            # Additional statistics
            st.markdown("#### Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Unique Values", plot_df[selected_column].nunique())
            
            with col2:
                st.metric("Most Frequent", plot_df[selected_column].mode()[0] if len(plot_df[selected_column].mode()) > 0 else "N/A")
            
            with col3:
                most_frequent_count = plot_df[selected_column].value_counts().iloc[0] if len(plot_df[selected_column]) > 0 else 0
                st.metric("Frequency", most_frequent_count)
    
    # ===== SECTION 7: NUMERICAL VS CATEGORICAL COMPARISON =====
    st.header("7️⃣ Compare Numerical vs Categorical")
    
    st.info("💡 **Use this to understand**: How does a numerical value (e.g., Sales, Price) vary across different categories (e.g., Product Type, Region)?")
    
    # Get numerical and categorical columns
    numerical_cols = plot_df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = plot_df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if len(numerical_cols) > 0 and len(categorical_cols) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            num_col = st.selectbox(
                "Select Numerical Column (Y-axis)",
                options=numerical_cols,
                help="Choose the numerical value to analyze",
                key="num_compare"
            )
        
        with col2:
            cat_col = st.selectbox(
                "Select Categorical Column (X-axis)",
                options=categorical_cols,
                help="Choose the category to group by",
                key="cat_compare"
            )
        
        if num_col and cat_col:
            # Filter to top categories if too many
            top_n = 10
            if plot_df[cat_col].nunique() > top_n:
                st.warning(f"⚠️ Showing top {top_n} categories only (out of {plot_df[cat_col].nunique()} total)")
                top_categories = plot_df[cat_col].value_counts().head(top_n).index.tolist()
                compare_df = plot_df[plot_df[cat_col].isin(top_categories)]
            else:
                compare_df = plot_df
            
            # Box Plot - Distribution per category
            st.subheader(f"📊 Distribution of {num_col} by {cat_col}")
            fig_box = px.box(
                compare_df,
                x=cat_col,
                y=num_col,
                title=f"{num_col} Distribution Across {cat_col}",
                color=cat_col,
                height=500
            )
            fig_box.update_layout(showlegend=False, xaxis_tickangle=-45)
            st.plotly_chart(fig_box, use_container_width=True)
            
            # Bar Chart - Mean per category
            st.subheader(f"📈 Average {num_col} by {cat_col}")
            grouped_stats = compare_df.groupby(cat_col)[num_col].agg(['mean', 'median', 'count']).reset_index()
            grouped_stats = grouped_stats.sort_values('mean', ascending=False)
            
            fig_bar = px.bar(
                grouped_stats,
                x=cat_col,
                y='mean',
                title=f"Average {num_col} by {cat_col}",
                labels={'mean': f'Average {num_col}'},
                color='mean',
                color_continuous_scale='Viridis',
                height=400
            )
            fig_bar.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # Statistics Table
            st.subheader("📋 Detailed Statistics by Category")
            stats_table = compare_df.groupby(cat_col)[num_col].agg([
                ('Count', 'count'),
                ('Mean', 'mean'),
                ('Median', 'median'),
                ('Std Dev', 'std'),
                ('Min', 'min'),
                ('Max', 'max')
            ]).round(2).reset_index()
            stats_table = stats_table.sort_values('Mean', ascending=False)
            st.dataframe(stats_table, use_container_width=True)
            
    elif len(numerical_cols) == 0:
        st.warning("⚠️ No numerical columns found in the dataset")
    elif len(categorical_cols) == 0:
        st.warning("⚠️ No categorical columns found in the dataset")
    else:
        st.warning("⚠️ Need both numerical and categorical columns for comparison")




if __name__ == "__main__":
    main()
