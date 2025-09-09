"""
Data Loader Module

This module handles loading, cleaning, and preprocessing of e-commerce data
from CSV files and preparing it for business analysis.
"""

import pandas as pd
import os
from typing import Dict, Tuple, Optional, List
import warnings

warnings.filterwarnings('ignore')


class EcommerceDataLoader:
    """
    A class to handle loading and preprocessing of e-commerce data.
    """
    
    def __init__(self, data_path: str = 'ecommerce_data'):
        """
        Initialize the data loader with path to data directory.
        
        Args:
            data_path: Path to the directory containing CSV files
        """
        self.data_path = data_path
        self.raw_data = {}
        self.processed_data = {}
        
    def load_raw_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load all raw CSV files into DataFrames.
        
        Returns:
            Dictionary mapping dataset names to DataFrames
        """
        file_mapping = {
            'orders': 'orders_dataset.csv',
            'order_items': 'order_items_dataset.csv',
            'products': 'products_dataset.csv',
            'customers': 'customers_dataset.csv',
            'reviews': 'order_reviews_dataset.csv'
        }
        
        for name, filename in file_mapping.items():
            filepath = os.path.join(self.data_path, filename)
            try:
                self.raw_data[name] = pd.read_csv(filepath)
                print(f"Loaded {name}: {self.raw_data[name].shape}")
            except FileNotFoundError:
                print(f"Warning: {filepath} not found")
                
        return self.raw_data
    
    def clean_datetime_columns(self, df: pd.DataFrame, datetime_cols: List[str]) -> pd.DataFrame:
        """
        Convert specified columns to datetime format.
        
        Args:
            df: DataFrame to process
            datetime_cols: List of column names to convert
            
        Returns:
            DataFrame with converted datetime columns
        """
        df_copy = df.copy()
        for col in datetime_cols:
            if col in df_copy.columns:
                df_copy[col] = pd.to_datetime(df_copy[col], errors='coerce')
        return df_copy
    
    def extract_time_features(self, df: pd.DataFrame, timestamp_col: str) -> pd.DataFrame:
        """
        Extract year, month, and other time features from timestamp column.
        
        Args:
            df: DataFrame containing timestamp column
            timestamp_col: Name of the timestamp column
            
        Returns:
            DataFrame with additional time feature columns
        """
        df_copy = df.copy()
        if timestamp_col in df_copy.columns:
            df_copy['year'] = df_copy[timestamp_col].dt.year
            df_copy['month'] = df_copy[timestamp_col].dt.month
            df_copy['day_of_week'] = df_copy[timestamp_col].dt.dayofweek
            df_copy['quarter'] = df_copy[timestamp_col].dt.quarter
        return df_copy
    
    def prepare_sales_data(self, 
                          order_status_filter: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Create merged sales dataset from orders and order_items.
        
        Args:
            order_status_filter: List of order statuses to include (default: ['delivered'])
            
        Returns:
            Merged and cleaned sales DataFrame
        """
        if order_status_filter is None:
            order_status_filter = ['delivered']
            
        # Merge order items with orders
        sales_data = pd.merge(
            self.raw_data['order_items'][['order_id', 'order_item_id', 'product_id', 'price', 'freight_value']],
            self.raw_data['orders'][['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp', 
                                    'order_delivered_customer_date', 'order_estimated_delivery_date']],
            on='order_id'
        )
        
        # Filter by order status
        sales_data = sales_data[sales_data['order_status'].isin(order_status_filter)]
        
        # Clean datetime columns
        datetime_cols = ['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date']
        sales_data = self.clean_datetime_columns(sales_data, datetime_cols)
        
        # Extract time features
        sales_data = self.extract_time_features(sales_data, 'order_purchase_timestamp')
        
        # Calculate delivery metrics
        if 'order_delivered_customer_date' in sales_data.columns:
            sales_data['delivery_days'] = (
                sales_data['order_delivered_customer_date'] - 
                sales_data['order_purchase_timestamp']
            ).dt.days
        
        return sales_data
    
    def filter_by_date_range(self, 
                           df: pd.DataFrame, 
                           start_date: Optional[str] = None, 
                           end_date: Optional[str] = None,
                           year: Optional[int] = None,
                           month: Optional[int] = None,
                           timestamp_col: str = 'order_purchase_timestamp') -> pd.DataFrame:
        """
        Filter DataFrame by date range or specific year/month.
        
        Args:
            df: DataFrame to filter
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format
            year: Specific year to filter by
            month: Specific month to filter by (requires year)
            timestamp_col: Name of the timestamp column to filter on
            
        Returns:
            Filtered DataFrame
        """
        df_filtered = df.copy()
        
        # Filter by date range
        if start_date:
            df_filtered = df_filtered[df_filtered[timestamp_col] >= start_date]
        if end_date:
            df_filtered = df_filtered[df_filtered[timestamp_col] <= end_date]
        
        # Filter by year
        if year:
            df_filtered = df_filtered[df_filtered['year'] == year]
            
        # Filter by month (requires year to be set)
        if month and year:
            df_filtered = df_filtered[df_filtered['month'] == month]
        
        return df_filtered
    
    def get_data_summary(self) -> Dict[str, Dict]:
        """
        Generate summary statistics for all loaded datasets.
        
        Returns:
            Dictionary containing summary info for each dataset
        """
        summary = {}
        for name, df in self.raw_data.items():
            summary[name] = {
                'shape': df.shape,
                'columns': list(df.columns),
                'missing_values': df.isnull().sum().to_dict(),
                'dtypes': df.dtypes.to_dict()
            }
        return summary
    
    def validate_data_quality(self) -> Dict[str, List[str]]:
        """
        Perform basic data quality checks.
        
        Returns:
            Dictionary mapping dataset names to list of quality issues
        """
        issues = {}
        
        for name, df in self.raw_data.items():
            dataset_issues = []
            
            # Check for missing values in key columns
            if name == 'orders' and df['order_id'].isnull().sum() > 0:
                dataset_issues.append("Missing order_id values")
            
            if name == 'order_items' and df['price'].isnull().sum() > 0:
                dataset_issues.append("Missing price values")
                
            # Check for negative prices
            if name == 'order_items' and (df['price'] < 0).any():
                dataset_issues.append("Negative price values found")
            
            # Check for duplicate order IDs in orders table
            if name == 'orders' and df['order_id'].duplicated().sum() > 0:
                dataset_issues.append("Duplicate order IDs found")
            
            issues[name] = dataset_issues
            
        return issues
    
    def create_analysis_dataset(self, 
                              year: Optional[int] = None,
                              month: Optional[int] = None,
                              include_geographic: bool = True,
                              include_product_info: bool = True,
                              include_reviews: bool = True) -> pd.DataFrame:
        """
        Create a comprehensive dataset for analysis with all relevant joins.
        
        Args:
            year: Filter by specific year
            month: Filter by specific month (requires year)
            include_geographic: Whether to include customer geographic data
            include_product_info: Whether to include product category information
            include_reviews: Whether to include review scores
            
        Returns:
            Comprehensive analysis-ready DataFrame
        """
        # Start with sales data
        analysis_df = self.prepare_sales_data()
        
        # Filter by date if specified
        if year or month:
            analysis_df = self.filter_by_date_range(analysis_df, year=year, month=month)
        
        # Add product information
        if include_product_info and 'products' in self.raw_data:
            analysis_df = pd.merge(
                analysis_df,
                self.raw_data['products'][['product_id', 'product_category_name']],
                on='product_id',
                how='left'
            )
        
        # Add customer geographic information
        if include_geographic and 'customers' in self.raw_data:
            analysis_df = pd.merge(
                analysis_df,
                self.raw_data['customers'][['customer_id', 'customer_state', 'customer_city']],
                on='customer_id',
                how='left'
            )
        
        # Add review information
        if include_reviews and 'reviews' in self.raw_data:
            analysis_df = pd.merge(
                analysis_df,
                self.raw_data['reviews'][['order_id', 'review_score']],
                on='order_id',
                how='left'
            )
        
        return analysis_df


def get_data_dictionary() -> Dict[str, Dict[str, str]]:
    """
    Returns data dictionary explaining all columns and business terms.
    
    Returns:
        Nested dictionary with dataset and column descriptions
    """
    return {
        'orders': {
            'order_id': 'Unique identifier for each order',
            'customer_id': 'Unique identifier for the customer who placed the order',
            'order_status': 'Current status of the order (delivered, shipped, canceled, etc.)',
            'order_purchase_timestamp': 'Date and time when the order was placed',
            'order_approved_at': 'Date and time when the order was approved',
            'order_delivered_carrier_date': 'Date when order was delivered to carrier',
            'order_delivered_customer_date': 'Date when order was delivered to customer',
            'order_estimated_delivery_date': 'Estimated delivery date provided to customer'
        },
        'order_items': {
            'order_id': 'Reference to the order this item belongs to',
            'order_item_id': 'Sequential number of the item within the order',
            'product_id': 'Unique identifier for the product',
            'seller_id': 'Unique identifier for the seller',
            'shipping_limit_date': 'Latest date seller can ship the item',
            'price': 'Item price in USD',
            'freight_value': 'Shipping cost for this item in USD'
        },
        'products': {
            'product_id': 'Unique identifier for each product',
            'product_category_name': 'Product category (e.g., electronics, books_media)',
            'product_name_length': 'Number of characters in product name',
            'product_description_length': 'Number of characters in product description',
            'product_photos_qty': 'Number of product photos available',
            'product_weight_g': 'Product weight in grams',
            'product_length_cm': 'Product length in centimeters',
            'product_height_cm': 'Product height in centimeters',
            'product_width_cm': 'Product width in centimeters'
        },
        'customers': {
            'customer_id': 'Unique identifier for each customer',
            'customer_unique_id': 'Unique identifier across all orders (privacy-focused)',
            'customer_zip_code_prefix': 'First digits of customer zip code',
            'customer_city': 'Customer city',
            'customer_state': 'Customer state (2-letter abbreviation)'
        },
        'reviews': {
            'review_id': 'Unique identifier for each review',
            'order_id': 'Reference to the order being reviewed',
            'review_score': 'Customer satisfaction score (1-5, where 5 is best)',
            'review_comment_title': 'Title of the review comment',
            'review_comment_message': 'Full text of the review',
            'review_creation_date': 'Date when review was created',
            'review_answer_timestamp': 'Date when review was answered by seller'
        }
    }