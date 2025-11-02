import gradio as gr
import pandas as pd
import os
import logging
from datetime import datetime
import time

try:
    from sales_forecaster import SalesForecaster
except ModuleNotFoundError:
    from .sales_forecaster import SalesForecaster

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SalesForecastApp:
    def __init__(self):
        self.forecaster = SalesForecaster()
        # Create output directory with parents if it doesn't exist
        self.output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info(f"Output directory initialized at: {self.output_dir}")
        
        # Load and cache the complete dataset for filter dependencies
        with self.forecaster.db.get_connection() as conn:
            self.df = pd.read_sql("""
                SELECT DISTINCT 
                    [Sales Organisation],
                    [Sales Country],
                    [Sales Region],
                    [Sales State],
                    [Sales City],
                    [Product Line],
                    [Product Category]
                FROM [DataSet_Monthly_Sales_and_Quota]
            """, conn)

    def get_dependent_values(self, 
                           sales_org=None, 
                           country=None, 
                           region=None, 
                           state=None):
        """Get filtered values based on previous selections"""
        df = self.df.copy()
        
        if sales_org and sales_org != "All":
            df = df[df['Sales Organisation'] == sales_org]
        if country and country != "All":
            df = df[df['Sales Country'] == country]
        if region and region != "All":
            df = df[df['Sales Region'] == region]
        if state and state != "All":
            df = df[df['Sales State'] == state]
            
        return {
            'countries': ["All"] + sorted(df['Sales Country'].unique().tolist()),
            'regions': ["All"] + sorted(df['Sales Region'].unique().tolist()),
            'states': ["All"] + sorted(df[df['Sales State'].notna()]['Sales State'].unique().tolist()),
            'cities': ["All"] + sorted(df['Sales City'].unique().tolist()),
            'product_lines': ["All"] + sorted(df['Product Line'].unique().tolist()),
            'product_categories': ["All"] + sorted(df['Product Category'].unique().tolist())
        }

    def update_countries(self, sales_org):
        values = self.get_dependent_values(sales_org=sales_org)
        return gr.Dropdown(choices=values['countries'], value="All")

    def update_regions(self, sales_org, country):
        values = self.get_dependent_values(sales_org=sales_org, country=country)
        return gr.Dropdown(choices=values['regions'], value="All")

    def update_states(self, sales_org, country, region):
        values = self.get_dependent_values(sales_org=sales_org, country=country, region=region)
        return gr.Dropdown(choices=values['states'], value="All")

    def update_cities(self, sales_org, country, region, state):
        """Update cities dropdown and check data availability"""
        values = self.get_dependent_values(sales_org=sales_org, country=country, region=region, state=state)
        
        # Check data availability for each city
        available_cities = ["All"]
        df = self.df.copy()
        
        if sales_org and sales_org != "All":
            df = df[df['Sales Organisation'] == sales_org]
        if country and country != "All":
            df = df[df['Sales Country'] == country]
        if region and region != "All":
            df = df[df['Sales Region'] == region]
        if state and state != "All":
            df = df[df['Sales State'] == state]
            
        for city in sorted(df['Sales City'].unique()):
            # Get data for this city
            try:
                city_data = self.forecaster.get_filtered_data(
                    sales_org=sales_org if sales_org != "All" else None,
                    country=country if country != "All" else None,
                    region=region if region != "All" else None,
                    state=state if state != "All" else None,
                    city=city
                )
                if len(city_data) >= 24:  # Mindestens 2 Jahre Daten
                    available_cities.append(city)
            except:
                continue
        
        return gr.Dropdown(
            choices=available_cities,
            value="All",
            label="City (Only showing cities with sufficient data)"
        )

    def update_product_categories(self, product_line):
        df = self.df.copy()
        if product_line and product_line != "All":
            df = df[df['Product Line'] == product_line]
        return gr.Dropdown(choices=["All"] + sorted(df['Product Category'].unique().tolist()), value="All")

    def create_forecast_analysis(
        self,
        sales_org,
        country,
        region,
        state,
        city,
        product_line,
        product_category,
        forecast_periods,
        confidence_interval
    ):
        try:
            # Ensure output directory exists before generating files
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Get filtered data
            filtered_data = self.forecaster.get_filtered_data(
                sales_org=sales_org if sales_org != "All" else None,
                country=country if country != "All" else None,
                region=region if region != "All" else None,
                state=state if state != "All" else None,
                city=city if city != "All" else None,
                product_line=product_line if product_line != "All" else None,
                product_category=product_category if product_category != "All" else None
            )

            # Create timestamp ONCE and pass it to all methods
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Define file paths
            historical_plot_path = os.path.join(self.output_dir, f'historical_data_{timestamp}.png')
            forecast_plot_path = os.path.join(self.output_dir, f'forecast_{timestamp}.png')
            seasonal_plot_path = os.path.join(self.output_dir, f'seasonal_patterns_{timestamp}.png')
            
            # Generate plots with explicit filenames
            self.forecaster.plot_historical_data(
                filtered_data, 
                save_path=self.output_dir,
                filename=f'historical_data_{timestamp}.png'
            )
            
            forecast_results = self.forecaster.create_forecast(filtered_data, forecast_periods, confidence_interval)
            
            self.forecaster.plot_forecast(
                forecast_results,
                title='Sales Forecast for Selected Filters',
                save_path=self.output_dir,
                filename=f'forecast_{timestamp}.png'
            )
            
            self.forecaster.plot_seasonal_patterns(
                filtered_data,
                save_path=self.output_dir,
                filename=f'seasonal_patterns_{timestamp}.png'
            )

            # Create forecast DataFrame for display
            forecast_df = pd.DataFrame({
                'Date': forecast_results['forecast'].index,
                'Forecast': forecast_results['forecast'].values,
                'Lower Bound': forecast_results['confidence_intervals'].iloc[:, 0],
                'Upper Bound': forecast_results['confidence_intervals'].iloc[:, 1]
            })
            forecast_csv_path = os.path.join(self.output_dir, f'forecast_results_{timestamp}.csv')
            forecast_df.to_csv(forecast_csv_path, index=False)
            
            # Save Excel file in background
            self.forecaster.export_results(
                filtered_data, 
                forecast_results, 
                save_path=self.output_dir,
                filename=f'forecast_results_{timestamp}.xlsx'
            )
            
            # Wait for files with proper error handling
            max_retries = 5
            retry_delay = 2  # seconds
            
            for _ in range(max_retries):
                if (os.path.exists(historical_plot_path) and 
                    os.path.exists(forecast_plot_path) and 
                    os.path.exists(seasonal_plot_path)):
                    break
                time.sleep(retry_delay)
            
            # Create a summary table
            summary_df = pd.DataFrame({
                'Metric': ['Forecast File', 'Historical Plot', 'Forecast Plot', 'Seasonal Plot'],
                'Path': [
                    os.path.join(self.output_dir, f'forecast_results_{timestamp}.xlsx'),
                    historical_plot_path,
                    forecast_plot_path,
                    seasonal_plot_path
                ]
            })
            
            return (
                forecast_results['forecast'],
                forecast_results['confidence_intervals'],
                historical_plot_path,
                forecast_plot_path,
                seasonal_plot_path,
                forecast_csv_path,
                os.path.join(self.output_dir, f'forecast_results_{timestamp}.xlsx'),
                summary_df
            )
            
        except Exception as e:
            logger.error(f"Error in forecast analysis: {str(e)}")
            return (
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                pd.DataFrame({'Error': [str(e)]})
            )

    def launch(self):
        """Launch the Gradio interface"""
        with gr.Blocks(title="Sales Forecast Analyzer") as interface:
            gr.Markdown("# Sales Forecast Analyzer")
            gr.Markdown("Select filters to generate forecasts, plots, and downloadable reports.")
            
            with gr.Row():
                with gr.Column():
                    sales_org = gr.Dropdown(
                        choices=self.get_dependent_values()['countries'],
                        label="Sales Organization",
                        value="All"
                    )
                    country = gr.Dropdown(
                        choices=self.get_dependent_values()['countries'],
                        label="Country",
                        value="All"
                    )
                    region = gr.Dropdown(
                        choices=self.get_dependent_values()['regions'],
                        label="Region",
                        value="All"
                    )
                    state = gr.Dropdown(
                        choices=self.get_dependent_values()['states'],
                        label="State",
                        value="All"
                    )
                    city = gr.Dropdown(
                        choices=["All"],
                        label="City",
                        value="All"
                    )
                
                with gr.Column():
                    product_line = gr.Dropdown(
                        choices=self.get_dependent_values()['product_lines'],
                        label="Product Line",
                        value="All"
                    )
                    product_category = gr.Dropdown(
                        choices=self.get_dependent_values()['product_categories'],
                        label="Product Category",
                        value="All"
                    )
                    forecast_periods = gr.Slider(
                        minimum=6, maximum=36, value=12, step=1,
                        label="Forecast Horizon (Months)"
                    )
                    confidence_interval = gr.Slider(
                        minimum=80, maximum=99, value=95, step=1,
                        label="Confidence Interval (%)"
                    )
            
            forecast_btn = gr.Button("Generate Forecast", variant="primary")
            
            forecast_output = gr.LinePlot(
                label="Forecasted Values",
                y_title="Sales Amount",
                x_title="Date"
            )
            confidence_output = gr.DataFrame(label="Confidence Intervals")
            historical_plot = gr.Image(label="Historical Data Plot")
            forecast_plot = gr.Image(label="Forecast Plot")
            seasonal_plot = gr.Image(label="Seasonal Patterns Plot")
            forecast_csv = gr.File(label="Download Forecast CSV")
            forecast_excel = gr.File(label="Download Forecast Excel")
            summary_table = gr.DataFrame(label="Generated Assets")
            
            # Event handlers
            sales_org.change(
                fn=self.update_countries,
                inputs=sales_org,
                outputs=country
            )
            country.change(
                fn=self.update_regions,
                inputs=[sales_org, country],
                outputs=region
            )
            region.change(
                fn=self.update_states,
                inputs=[sales_org, country, region],
                outputs=state
            )
            state.change(
                fn=self.update_cities,
                inputs=[sales_org, country, region, state],
                outputs=city
            )
            product_line.change(
                fn=self.update_product_categories,
                inputs=product_line,
                outputs=product_category
            )
            
            forecast_btn.click(
                fn=self.create_forecast_analysis,
                inputs=[
                    sales_org,
                    country,
                    region,
                    state,
                    city,
                    product_line,
                    product_category,
                    forecast_periods,
                    confidence_interval
                ],
                outputs=[
                    forecast_output,
                    confidence_output,
                    historical_plot,
                    forecast_plot,
                    seasonal_plot,
                    forecast_csv,
                    forecast_excel,
                    summary_table
                ]
            )
        
        # Try ports in range 7860-7870
        for port in range(7860, 7871):
            try:
                interface.launch(
                    share=False,
                    server_name="0.0.0.0",
                    server_port=port
                )
                break  # Exit loop if launch successful
            except OSError:
                if port == 7870:  # If we've tried all ports
                    logger.error("Could not launch the app - no available ports")
                continue

if __name__ == "__main__":
    app = SalesForecastApp()
    app.launch()
