# E-Commerce Business Analytics - Refactored EDA

## Overview

This project provides a comprehensive, configurable framework for analyzing e-commerce business performance. The refactored analysis improves upon the original EDA with better structure, reusable code, and enhanced visualizations.

## Project Structure

```
lesson7_files/
├── EDA_Refactored.ipynb     # Main analysis notebook
├── business_metrics.py      # Business metrics calculation functions  
├── data_loader.py           # Data loading and preprocessing utilities
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── ecommerce_data/         # Data directory
    ├── orders_dataset.csv
    ├── order_items_dataset.csv
    ├── products_dataset.csv
    ├── customers_dataset.csv
    └── order_reviews_dataset.csv
```

## Key Features

### 🔧 **Configurable Analysis Framework**
- Easily analyze different time periods by modifying configuration parameters
- Support for yearly, monthly, or custom date range analysis
- No hardcoded dates - fully parameterized approach

### 📊 **Comprehensive Business Metrics**
- **Revenue Analysis**: YoY growth, monthly trends, seasonal patterns
- **Product Performance**: Category analysis, revenue contribution
- **Geographic Analysis**: State-level performance with choropleth maps
- **Customer Experience**: Delivery time, satisfaction scores, correlation analysis
- **Order Analytics**: Volume trends, AOV changes, status distribution

### 🎨 **Enhanced Visualizations**
- Professional charts with consistent color schemes
- Interactive Plotly visualizations
- Multi-panel dashboards for comprehensive insights
- Business-oriented formatting and labeling

### 🛠 **Code Quality Improvements**
- Reusable functions with comprehensive docstrings
- Modular architecture with separate data loading and metrics modules
- Elimination of pandas warnings through proper data handling
- Type hints and error handling

## Quick Start

### 1. Installation

```bash
# Install required dependencies
pip install -r requirements.txt

# Or install individual packages
pip install pandas numpy matplotlib seaborn plotly jupyter
```

### 2. Configuration

Open `EDA_Refactored.ipynb` and modify the analysis configuration:

```python
ANALYSIS_CONFIG = {
    'current_year': 2023,        # Year to analyze
    'previous_year': 2022,       # Comparison year  
    'analysis_month': None,      # Specific month (1-12) or None for full year
    'data_path': 'ecommerce_data'
}
```

### 3. Run Analysis

Launch Jupyter notebook and run all cells:

```bash
jupyter notebook EDA_Refactored.ipynb
```

## Usage Examples

### Analyze Full Year Performance
```python
ANALYSIS_CONFIG = {
    'current_year': 2023,
    'previous_year': 2022,
    'analysis_month': None,  # Full year analysis
    'data_path': 'ecommerce_data'
}
```

### Analyze Specific Month
```python
ANALYSIS_CONFIG = {
    'current_year': 2023,
    'previous_year': 2022,
    'analysis_month': 12,    # December analysis
    'data_path': 'ecommerce_data'
}
```

### Custom Date Range Analysis
```python
# In the notebook, use the data loader's filter functionality
filtered_data = loader.filter_by_date_range(
    analysis_data, 
    start_date='2023-06-01', 
    end_date='2023-08-31'
)
```

## Module Documentation

### business_metrics.py

Contains reusable functions for calculating key business metrics:

- `calculate_revenue_metrics()` - Revenue and growth analysis
- `calculate_monthly_growth()` - Month-over-month growth trends  
- `calculate_average_order_value()` - AOV analysis and comparison
- `calculate_product_category_performance()` - Product category insights
- `calculate_geographic_performance()` - Geographic revenue analysis
- `calculate_customer_experience_metrics()` - Delivery and satisfaction metrics

### data_loader.py

Provides the `EcommerceDataLoader` class for data management:

- `load_raw_data()` - Load CSV files into DataFrames
- `prepare_sales_data()` - Create analysis-ready sales dataset
- `filter_by_date_range()` - Filter data by various time criteria
- `create_analysis_dataset()` - Generate comprehensive analysis dataset
- `validate_data_quality()` - Perform data quality checks

## Key Improvements Over Original

### 1. **Structure & Documentation**
- ✅ Clear table of contents and section organization
- ✅ Comprehensive markdown documentation
- ✅ Business context and objective explanations
- ✅ Data dictionary with column descriptions

### 2. **Code Quality**
- ✅ Elimination of SettingWithCopyWarnings
- ✅ Reusable functions with docstrings
- ✅ Consistent naming conventions
- ✅ Modular architecture

### 3. **Visualization Enhancements**  
- ✅ Professional color schemes and formatting
- ✅ Clear titles with date ranges
- ✅ Proper axis labels with units
- ✅ Interactive Plotly visualizations
- ✅ Multi-panel dashboards

### 4. **Configurability**
- ✅ Parameterized analysis periods
- ✅ Flexible date range filtering
- ✅ General-purpose metric calculations
- ✅ Reusable across different datasets

## Business Insights Generated

The refactored analysis provides comprehensive insights including:

- **Revenue Performance**: YoY growth trends and monthly patterns
- **Product Strategy**: Best and worst performing categories  
- **Geographic Opportunities**: High-value markets and expansion potential
- **Customer Experience**: Delivery performance impact on satisfaction
- **Operational Efficiency**: Order fulfillment and status analysis

## Extensibility

The modular design makes it easy to:

- Add new business metrics to `business_metrics.py`
- Extend data loading capabilities in `data_loader.py`
- Create new visualization sections in the notebook
- Apply the framework to different e-commerce datasets
- Integrate with other data sources or APIs

## Troubleshooting

### Common Issues

1. **Missing Data Files**: Ensure CSV files are in the `ecommerce_data` directory
2. **Import Errors**: Verify all requirements are installed via `pip install -r requirements.txt`
3. **Memory Issues**: For large datasets, consider filtering by date range first
4. **Plotly Display**: If charts don't display, ensure Plotly is properly installed

### Performance Tips

- Filter data early for large datasets using date range parameters
- Use the `limit` parameters in data loader functions for testing
- Consider sampling for initial exploration of very large datasets

## Contributing

To extend this analysis framework:

1. Add new metrics functions to `business_metrics.py`
2. Enhance data loading capabilities in `data_loader.py`  
3. Create additional visualization sections in the notebook
4. Update documentation and examples

---

**Note**: This framework is designed to be maintainable and extensible. The configurable approach ensures it can be applied to different time periods and similar e-commerce datasets with minimal modifications.