"""
Business Metrics Module

This module contains functions for calculating various e-commerce business metrics
including revenue analysis, growth calculations, and customer experience metrics.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any


def calculate_revenue_metrics(sales_data: pd.DataFrame, 
                            current_year: int, 
                            previous_year: int) -> Dict[str, Any]:
    """
    Calculate revenue metrics for current year vs previous year.
    
    Args:
        sales_data: DataFrame with columns ['price', 'year']
        current_year: Year to analyze
        previous_year: Year to compare against
        
    Returns:
        Dictionary containing revenue metrics
    """
    current_revenue = sales_data[sales_data['year'] == current_year]['price'].sum()
    previous_revenue = sales_data[sales_data['year'] == previous_year]['price'].sum()
    
    if previous_revenue > 0:
        revenue_growth = (current_revenue - previous_revenue) / previous_revenue * 100
    else:
        revenue_growth = 0
    
    return {
        'current_year_revenue': current_revenue,
        'previous_year_revenue': previous_revenue,
        'revenue_growth_percent': revenue_growth
    }


def calculate_monthly_growth(sales_data: pd.DataFrame, year: int) -> pd.Series:
    """
    Calculate month-over-month growth for a specific year.
    
    Args:
        sales_data: DataFrame with columns ['price', 'month', 'year']
        year: Year to analyze
        
    Returns:
        Series with monthly growth percentages
    """
    year_data = sales_data[sales_data['year'] == year]
    monthly_revenue = year_data.groupby('month')['price'].sum()
    return monthly_revenue.pct_change()


def calculate_average_order_value(sales_data: pd.DataFrame, 
                                current_year: int, 
                                previous_year: int) -> Dict[str, Any]:
    """
    Calculate average order value for current year vs previous year.
    
    Args:
        sales_data: DataFrame with columns ['order_id', 'price', 'year']
        current_year: Year to analyze
        previous_year: Year to compare against
        
    Returns:
        Dictionary containing AOV metrics
    """
    current_aov = (sales_data[sales_data['year'] == current_year]
                   .groupby('order_id')['price'].sum().mean())
    previous_aov = (sales_data[sales_data['year'] == previous_year]
                    .groupby('order_id')['price'].sum().mean())
    
    if previous_aov > 0:
        aov_growth = (current_aov - previous_aov) / previous_aov * 100
    else:
        aov_growth = 0
    
    return {
        'current_year_aov': current_aov,
        'previous_year_aov': previous_aov,
        'aov_growth_percent': aov_growth
    }


def calculate_order_volume_metrics(sales_data: pd.DataFrame, 
                                 current_year: int, 
                                 previous_year: int) -> Dict[str, Any]:
    """
    Calculate order volume metrics for current year vs previous year.
    
    Args:
        sales_data: DataFrame with columns ['order_id', 'year']
        current_year: Year to analyze
        previous_year: Year to compare against
        
    Returns:
        Dictionary containing order volume metrics
    """
    current_orders = sales_data[sales_data['year'] == current_year]['order_id'].nunique()
    previous_orders = sales_data[sales_data['year'] == previous_year]['order_id'].nunique()
    
    if previous_orders > 0:
        order_growth = (current_orders - previous_orders) / previous_orders * 100
    else:
        order_growth = 0
    
    return {
        'current_year_orders': current_orders,
        'previous_year_orders': previous_orders,
        'order_growth_percent': order_growth
    }


def calculate_product_category_performance(sales_data: pd.DataFrame, 
                                         products_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate revenue by product category, sorted by performance.
    
    Args:
        sales_data: DataFrame with columns ['product_id', 'price']
        products_data: DataFrame with columns ['product_id', 'product_category_name']
        
    Returns:
        DataFrame with category performance metrics
    """
    sales_with_categories = pd.merge(
        sales_data[['product_id', 'price']], 
        products_data[['product_id', 'product_category_name']],
        on='product_id'
    )
    
    category_performance = (sales_with_categories
                           .groupby('product_category_name')['price']
                           .agg(['sum', 'count', 'mean'])
                           .round(2))
    category_performance.columns = ['total_revenue', 'total_orders', 'avg_order_value']
    
    return category_performance.sort_values('total_revenue', ascending=False)


def calculate_geographic_performance(sales_data: pd.DataFrame,
                                   orders_data: pd.DataFrame,
                                   customers_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate revenue by geographic region (state).
    
    Args:
        sales_data: DataFrame with columns ['order_id', 'price']
        orders_data: DataFrame with columns ['order_id', 'customer_id']
        customers_data: DataFrame with columns ['customer_id', 'customer_state']
        
    Returns:
        DataFrame with geographic performance metrics
    """
    # Merge sales with customer location
    sales_with_customers = pd.merge(sales_data[['order_id', 'price']], 
                                   orders_data[['order_id', 'customer_id']], 
                                   on='order_id')
    
    sales_with_states = pd.merge(sales_with_customers, 
                                customers_data[['customer_id', 'customer_state']], 
                                on='customer_id')
    
    geographic_performance = (sales_with_states
                             .groupby('customer_state')['price']
                             .agg(['sum', 'count', 'mean'])
                             .round(2))
    geographic_performance.columns = ['total_revenue', 'total_orders', 'avg_order_value']
    
    return geographic_performance.sort_values('total_revenue', ascending=False)


def categorize_delivery_speed(days: int) -> str:
    """
    Categorize delivery speed into buckets.
    
    Args:
        days: Number of delivery days
        
    Returns:
        String category for delivery speed
    """
    if days <= 3:
        return '1-3 days'
    elif days <= 7:
        return '4-7 days'
    else:
        return '8+ days'


def calculate_customer_experience_metrics(sales_data: pd.DataFrame,
                                        reviews_data: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate customer experience metrics including delivery speed and satisfaction.
    
    Args:
        sales_data: DataFrame with delivery and order info
        reviews_data: DataFrame with review scores
        
    Returns:
        Dictionary containing customer experience metrics
    """
    # Calculate delivery speed
    sales_data['delivery_speed_days'] = (
        pd.to_datetime(sales_data['order_delivered_customer_date']) - 
        pd.to_datetime(sales_data['order_purchase_timestamp'])
    ).dt.days
    
    # Merge with reviews
    sales_with_reviews = pd.merge(sales_data, 
                                 reviews_data[['order_id', 'review_score']], 
                                 on='order_id')
    
    # Remove duplicates for unique orders
    unique_orders = sales_with_reviews[['order_id', 'delivery_speed_days', 'review_score']].drop_duplicates()
    
    # Categorize delivery speed
    unique_orders['delivery_time_category'] = unique_orders['delivery_speed_days'].apply(categorize_delivery_speed)
    
    # Calculate metrics
    avg_delivery_days = unique_orders['delivery_speed_days'].mean()
    avg_review_score = unique_orders['review_score'].mean()
    
    # Review score by delivery speed
    delivery_satisfaction = (unique_orders
                           .groupby('delivery_time_category')['review_score']
                           .mean()
                           .round(3))
    
    return {
        'avg_delivery_days': avg_delivery_days,
        'avg_review_score': avg_review_score,
        'delivery_satisfaction_by_speed': delivery_satisfaction.to_dict()
    }


def calculate_order_status_distribution(orders_data: pd.DataFrame, year: int) -> pd.Series:
    """
    Calculate order status distribution for a specific year.
    
    Args:
        orders_data: DataFrame with columns ['order_status', 'order_purchase_timestamp']
        year: Year to analyze
        
    Returns:
        Series with order status proportions
    """
    orders_data['year'] = pd.to_datetime(orders_data['order_purchase_timestamp']).dt.year
    year_orders = orders_data[orders_data['year'] == year]
    
    return year_orders['order_status'].value_counts(normalize=True).round(4)


def generate_business_summary(revenue_metrics: Dict[str, Any],
                            aov_metrics: Dict[str, Any],
                            order_metrics: Dict[str, Any],
                            cx_metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a comprehensive business summary from various metrics.
    
    Args:
        revenue_metrics: Revenue analysis results
        aov_metrics: Average order value results
        order_metrics: Order volume results
        cx_metrics: Customer experience results
        
    Returns:
        Dictionary containing business summary
    """
    return {
        'revenue_summary': {
            'current_revenue': revenue_metrics['current_year_revenue'],
            'revenue_growth': f"{revenue_metrics['revenue_growth_percent']:.2f}%"
        },
        'order_summary': {
            'current_orders': order_metrics['current_year_orders'],
            'current_aov': f"${aov_metrics['current_year_aov']:.2f}",
            'order_growth': f"{order_metrics['order_growth_percent']:.2f}%"
        },
        'customer_experience': {
            'avg_delivery_days': f"{cx_metrics['avg_delivery_days']:.1f} days",
            'avg_satisfaction': f"{cx_metrics['avg_review_score']:.2f}/5.0"
        }
    }