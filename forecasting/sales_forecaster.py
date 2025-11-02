import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from typing import Optional, Dict, Union, List, Any
from datetime import datetime
import logging
from sqlalchemy.sql import text
import altair as alt
import os
from datetime import datetime
from contextlib import contextmanager

try:
    from database.connection import engine
except ModuleNotFoundError:  # Allow running module directly from package directory
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from database.connection import engine

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    def __init__(self):
        """Wrap shared SQLAlchemy engine for forecasting module reuse"""
        self.engine = engine

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        connection = self.engine.connect()
        try:
            yield connection
            logger.info("Database connection successful")
        except Exception as e:
            logger.error(f"Database connection error: {str(e)}")
            raise
        finally:
            connection.close()
            logger.info("Database connection closed")

class SalesForecaster:
    def __init__(self):
        """Initialize the forecaster with database connection"""
        self.db = DatabaseConnection()
        self._validate_connection()

    def _validate_connection(self):
        """Validate database connection"""
        try:
            with self.db.get_connection() as conn:
                df = pd.read_sql('SELECT @@version', conn)
                logger.info(f"Connected to SQL Server version: {df.iloc[0,0]}")
        except Exception as e:
            logger.error(f"Failed to validate database connection: {str(e)}")
            raise

    def _build_query(self,
                    sales_org: Optional[str] = None,
                    country: Optional[str] = None,
                    region: Optional[str] = None,
                    city: Optional[str] = None,
                    state: Optional[str] = None,
                    product_line: Optional[str] = None,
                    product_category: Optional[str] = None) -> tuple[str, dict]:
        """
        Build SQL query based on filters
        
        Returns:
            Tuple of (query string, parameters dictionary)
        """
        query = """
        SELECT 
            [Calendar DueDate],
            [Revenue EUR],
            [Sales Amount],
            [Sales Organisation],
            [Sales Country],
            [Sales Region],
            [Sales City],
            [Sales State],
            [Product Line],
            [Product Category]
        FROM [DataSet_Monthly_Sales_and_Quota]
        WHERE 1=1
        """
        
        params = {}
        if sales_org:
            query += " AND [Sales Organisation] = :sales_org"
            params['sales_org'] = sales_org
        if country:
            query += " AND [Sales Country] = :country"
            params['country'] = country
        if region:
            query += " AND [Sales Region] = :region"
            params['region'] = region
        if city:
            query += " AND [Sales City] = :city"
            params['city'] = city
        if state:
            query += " AND [Sales State] = :state"
            params['state'] = state
        if product_line:
            query += " AND [Product Line] = :product_line"
            params['product_line'] = product_line
        if product_category:
            query += " AND [Product Category] = :product_category"
            params['product_category'] = product_category
            
        query += " ORDER BY [Calendar DueDate]"
        
        return query, params

    def get_filtered_data(self,
                         sales_org: Optional[str] = None,
                         country: Optional[str] = None,
                         region: Optional[str] = None,
                         city: Optional[str] = None,
                         state: Optional[str] = None,
                         product_line: Optional[str] = None,
                         product_category: Optional[str] = None) -> pd.DataFrame:
        """
        Get filtered data from database with validation
        """
        query, params = self._build_query(
            sales_org, country, region, city, state, product_line, product_category
        )
        
        try:
            with self.db.get_connection() as conn:
                # Use text() to properly handle parameter binding
                sql = text(query)
                df = pd.read_sql_query(sql, conn, params=params)
                df['Calendar DueDate'] = pd.to_datetime(df['Calendar DueDate'])
                
                # Check minimum data requirements
                if len(df) < 24:  # Mindestens 2 Jahre an Daten
                    filters_used = [f"{k}: {v}" for k, v in {
                        'Sales Organization': sales_org,
                        'Country': country,
                        'Region': region,
                        'City': city,
                        'State': state,
                        'Product Line': product_line,
                        'Product Category': product_category
                    }.items() if v is not None]
                    
                    raise ValueError(
                        f"Insufficient data for forecast. Found only {len(df)} data points with filters:\n"
                        f"{chr(10).join('- ' + f for f in filters_used)}\n"
                        f"Need at least 24 monthly data points for reliable forecasting."
                    )
                
                logger.info(f"Retrieved {len(df)} records from database")
                return df
                
        except Exception as e:
            logger.error(f"Error retrieving data: {str(e)}")
            raise

    def prepare_time_series(self, filtered_df: pd.DataFrame) -> pd.Series:
        """
        Prepare time series data for forecasting
        """
        # Group by date and sum revenue
        ts = filtered_df.groupby('Calendar DueDate')['Revenue EUR'].sum()
        ts.index = pd.DatetimeIndex(ts.index)
        ts = ts.sort_index()
        
        # Check for missing dates and fill them
        date_range = pd.date_range(start=ts.index.min(), end=ts.index.max(), freq='ME')
        ts = ts.reindex(date_range, fill_value=0)
        
        return ts

    def _save_chart(self, chart: alt.Chart, filename: str, save_path: str) -> None:
        """Helper method to save Altair charts"""
        os.makedirs(save_path, exist_ok=True)
        filepath = os.path.join(save_path, filename)
        try:
            chart.save(filepath)
            logger.info(f"Chart saved successfully to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save chart: {str(e)}")
            raise

    def plot_historical_data(self, filtered_data: pd.DataFrame, save_path: str = './', filename: str = None) -> alt.Chart:
        """
        Create an Altair visualization of historical sales data
        """
        # Prepare data
        df_melted = pd.melt(
            filtered_data.groupby('Calendar DueDate').agg({
                'Revenue EUR': 'sum',
                'Sales Amount': 'sum'
            }).reset_index(),
