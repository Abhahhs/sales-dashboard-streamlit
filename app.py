import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuration and Data Loading ---

# Set up the page configuration
st.set_page_config(
    page_title="Sales Performance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to load and prepare data
@st.cache_data
def load_data():
    # Load the cleaned data file named 'sales_data.csv'
    try:
        df = pd.read_csv('sales_data.csv')
    except FileNotFoundError:
        st.error("Error: 'sales_data.csv' not found. Please ensure the data file is committed to your GitHub repository.")
        return pd.DataFrame()

    # --- CRITICAL DATA CLEANING FIX ---
    # The KeyError occurs because column names have spaces, but the code uses underscores.
    df = df.rename(columns={
        'Emp Code': 'Emp_Code',
        'Sales Executive': 'Sales_Executive',
        'Total Sales': 'Total_Sales',
        'Target Hit %': 'Target_Hit_Pct',
        'Away From Target %': 'Away_From_Target_Pct'
    })

    # Convert percentage columns (like '67.80%') from strings to floats (0.678)
    for col in ['Target_Hit_Pct', 'Away_From_Target_Pct']:
        if col in df.columns and df[col].dtype == 'object':
            # Remove the '%' sign and divide by 100 to get the decimal representation
            df[col] = df[col].str.replace('%', '').astype(float) / 100
    
    return df

# Load the data
df = load_data()

# Stop the app if data failed to load
if df.empty:
    st.stop()

# --- Title and Filters (Sidebar) ---

st.sidebar.title("🧭 Dashboard Controls")

# 1. State/Region Multi-Select Filter
all_states = ['All Regions'] + sorted(df['Region'].unique().tolist())
selected_states = st.sidebar.multiselect(
    "Filter by State/Region:",
    options=all_states,
    default=['All Regions']
)

# 2. Performance Threshold Slider (for conditional formatting in table)
target_threshold = st.sidebar.slider(
    'Highlight Salesmen with Target Hit % Below:',
    min_value=0.0,
    max_value=1.0,
    value=0.6,
    step=0.05,
    format='{:.0%}'
)

# --- Data Filtering Logic ---

# Apply State/Region filter
if 'All Regions' not in selected_states:
    df_filtered = df[df['Region'].isin(selected_states)]
else:
    df_filtered = df.copy()

# --- Main Dashboard Layout ---

st.title("📊 Sales Performance Dashboard - Abhay Singh Rawat")
st.markdown("An interactive view of salesman and regional performance.")
st.markdown("---")

# --- ROW 1: Key Performance Indicators (KPIs) ---
col1, col2, col3, col4 = st.columns(4)

# These column accesses now work because the names were corrected in load_data()
total_sales = df_filtered['Total_Sales'].sum()
avg_target_hit = df_filtered['Target_Hit_Pct'].mean() * 100
total_salesmen = df_filtered['Emp_Code'].nunique()
target_achieved_count = df_filtered[df_filtered['Target_Hit_Pct'] >= 1.0].shape[0]


with col1:
    st.metric("Total Sales (Selected)", f"${total_sales:,.0f}")
with col2:
    st.metric("Avg. Target Hit %", f"{avg_target_hit:.1f}%")
with col3:
    st.metric("Total Salesmen", total_salesmen)
with col4:
    st.metric("Salesmen Meeting Target", target_achieved_count)

st.markdown("---")

# --- ROW 2: Charts ---
chart_col1, chart_col2 = st.columns(2)

# Chart 1: Top 5 and Bottom 5 Salesmen (Bar Chart)
with chart_col1:
    st.subheader("Top 5 & Bottom 5 Salesmen by Total Sales")

    # Aggregate data for ranking
    salesmen_rank = df_filtered.sort_values(by='Total_Sales', ascending=False)

    top_5 = salesmen_rank.head(5)
    bottom_5 = salesmen_rank.tail(5)

    # Combine for visualization
    top_bottom_df = pd.concat([top_5, bottom_5])
    
    # Use Sales Executive name for the y-axis and sort by sales
    fig_bar = px.bar(
        top_bottom_df,
        x='Total_Sales',
        y='Sales_Executive',
        orientation='h',
        color='Total_Sales',
        color_continuous_scale=px.colors.sequential.Plotly3,
        title='Sales Executive Ranking'
    )
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_bar, use_container_width=True)

# Chart 2: State-level Target Achievement (Bar Chart by Region)
with chart_col2:
    st.subheader("Regional Target Hit %")

    # Aggregate by Region
    region_agg = df_filtered.groupby('Region').agg(
        Avg_Target_Hit=('Target_Hit_Pct', 'mean'),
        Total_Sales=('Total_Sales', 'sum')
    ).reset_index()

    fig_region = px.bar(
        region_agg.sort_values(by='Avg_Target_Hit', ascending=False),
        x='Region',
        y='Avg_Target_Hit',
        color='Avg_Target_Hit',
        color_continuous_scale=px.colors.sequential.Viridis,
        title='Average Target Hit % by Region'
    )
    # Highlight bars based on whether region hit its average target
    fig_region.update_traces(marker_color=['green' if x >= 1.0 else 'red' for x in region_agg['Avg_Target_Hit']])
    st.plotly_chart(fig_region, use_container_width=True)

st.markdown("---")

# --- ROW 3: Detailed Table and Insights ---

st.subheader(f"Salesmen Requiring Support (Target Hit % < {target_threshold*100:.0f}%)")

df_support = df_filtered[df_filtered['Target_Hit_Pct'] < target_threshold].sort_values(by='Target_Hit_Pct', ascending=True)

if not df_support.empty:
    st.dataframe(
        df_support[['Sales_Executive', 'Region', 'Total_Sales', 'Target', 'Target_Hit_Pct', 'Away_From_Target_Pct']]
        .style.format({
            # Uses '$' to avoid the Streamlit 'sprintf' error
            'Total_Sales': "${:,.0f}",  
            'Target': "${:,.0f}",
            'Target_Hit_Pct': "{:.1%}",
            'Away_From_Target_Pct': "{:.1%}"
        })
        .background_gradient(subset=['Target_Hit_Pct'], cmap='Reds', vmin=0.0, vmax=target_threshold),
        use_container_width=True
    )
else:
    st.info("Great work! No salesmen currently fall below the set performance threshold.")

# Final Insight/Conclusion
st.markdown("---")
st.markdown("""
**Conclusion:** This interactive dashboard, powered by Python and Streamlit, provides immediate, data-driven insights to identify high-potential employees and those requiring targeted support plans.
""")
