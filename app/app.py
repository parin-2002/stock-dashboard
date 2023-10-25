import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
from dash import dash_table
import yfinance as yf
from datetime import datetime, timedelta
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.graph_objs import Scatter, Candlestick
import plotly.graph_objects as go




# Create a dictionary mapping symbols to country names and codes
symbol_to_country = {
    '^GSPC': ('USA', 'USD', 'USA'),
    '^DJI': ('USA', 'USD', 'USA'),
    '^IXIC': ('USA', 'USD', 'USA'),
    '^NYA': ('USA', 'USD', 'USA'),
    '^XAX': ('Canada', 'CAD', 'CAN'),
    '^BUK100P': ('UK', 'GBP', 'GBR'),
    '^RUT': ('USA', 'USD', 'USA'),
    '^VIX': ('USA', 'USD', 'USA'),
    '^FTSE': ('UK', 'GBP', 'GBR'),
    '^GDAXI': ('Germany', 'EUR', 'DEU'),
    '^FCHI': ('France', 'EUR', 'FRA'),
    '^STOXX50E': ('Europe', 'EUR', 'EU'),
    '^N100': ('Europe', 'EUR', 'EU'),
    '^BFX': ('Belgium', 'EUR', 'BEL'),
    'IMOEX.ME': ('Russia', 'RUB', 'RUS'),
    '^N225': ('Japan', 'JPY', 'JPN'),
     '^HSI': ('Hong Kong', 'HKD', 'HKG'),
    '000001.SS': ('China', 'CNY', 'CHN'),
    '399001.SZ': ('China', 'CNY', 'CHN'),
    '^STI': ('Singapore', 'SGD', 'SGP'),
    '^AXJO': ('Australia', 'AUD', 'AUS'),
    '^AORD': ('Australia', 'AUD', 'AUS'),
    '^BSESN': ('India', 'INR', 'IND'),
    '^JKSE': ('Indonesia', 'IDR', 'IDN'),
    '^KLSE': ('Malaysia', 'MYR', 'MYS'),
    '^NZ50': ('New Zealand', 'NZD', 'NZL'),
    '^KS11': ('South Korea', 'KRW', 'KOR'),
    '^TWII': ('Taiwan', 'TWD', 'TWN'),
    '^GSPTSE': ('Canada', 'CAD', 'CAN'),
    '^BVSP': ('Brazil', 'BRL', 'BRA'),
    '^MXX': ('Mexico', 'MXN', 'MEX'),
    '^IPSA': ('Chile', 'CLP', 'CHL'),
    '^MERV': ('Argentina', 'ARS', 'ARG'),
    '^TA125.TA': ('Israel', 'ILS', 'ISR'),
    '^CASE30': ('Egypt', 'EGP', 'EGY'),
    '^JN0U.JO': ('South Africa', 'ZAR', 'ZAF')
}

def update_data():
    # Retrieving List of World Major Stock Indices from Yahoo! Finance
    df_list = pd.read_html('https://finance.yahoo.com/world-indices/')
    majorStockIdx = df_list[0]
    majorStockIdx = majorStockIdx.drop(columns=["Intraday High/Low", "52 Week Range","Day Chart"])
    
    # Add new 'Country Name' and 'Currency Code' columns based on the mapping
    majorStockIdx['Country Name'] = majorStockIdx['Symbol'].map(lambda x: symbol_to_country[x][0])
    majorStockIdx['Currency Code'] = majorStockIdx['Symbol'].map(lambda x: symbol_to_country[x][1])
    majorStockIdx['Country Code'] = majorStockIdx['Symbol'].map(lambda x: symbol_to_country[x][2])
    
    return majorStockIdx


# Read the 'tickers.xlsx' file
data = pd.read_csv('https://raw.githubusercontent.com/parin-2002/STOCK-APP-AS-2/main/app/tickers.csv?token=GHSAT0AAAAAACIDZ4JAPBU7MAO4ABIUQKKKZJY3ZTQ')  #use read_excel if needed 

# Get the list of available countries and remove null values
available_countries = data['Country'].dropna().unique()

# Sample stock data 
majorStockIdx=update_data() 

# Initialize the Dash app
app = dash.Dash(__name__)

# Create a Choropleth map using Plotly Express with equirectangular projection
app.layout = html.Div([
    html.H1("Interactive world map to analyse world stock market", style={'text-align': 'center'}),  # Center the title
    dcc.Graph(id='choropleth-map', figure={}, style={'margin': 'auto', 'display': 'block'}),  # Center the map
    html.H2("Select more indices:"), 
    dcc.Dropdown(
        id='index-dropdown',
        options=[
            {'label': f"{row['Name']}({row['Country Name']})", 'value': idx}
            for idx, row in majorStockIdx.iterrows()
        ],
        multi=True,
        value=[0]  # Initialize with the first index
    ),
    dcc.Graph(id='line-plot', style={'margin': 'auto', 'display': 'block', 'width': '100%', 'height': '600px'}),
    
    #####
    html.H2("Select a Country:"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in available_countries],
        value="USA",  # Initialize with a default selected country
    ),
    html.H2("Select Stocks (Limit: 2):"),
    dcc.Dropdown(id='stock-dropdown', multi=True),
    html.H2("Selected Stocks", style={'text-align': 'center'}),
    dash_table.DataTable(
        id='selected-stocks-table',
        columns=[
            {"name": "Ticker", "id": "Ticker"},
            {"name": "Name", "id": "Name"},
            {"name": "Country", "id": "Country"},
            {"name": "Exchange", "id": "Exchange"},
        ],
        style_table={'height': '200px', 'overflowY': 'auto'},
        style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
        ],
        style_header={'backgroundColor': 'rgb(230, 230, 230)'},
    ),
    
    ####
    
    html.H1("Stock Comparison or stock individual Plot", style={'text-align': 'center'}),
    html.H2("Select Duration:"),
    dcc.Dropdown(
        id='duration-dropdown',
        options=[
            {'label': '1 Month', 'value': 30},
            {'label': '3 Months', 'value': 90},
            {'label': '6 Months', 'value': 180},
            {'label': '1 Year', 'value': 365},
            {'label': '3 Years', 'value': 3 * 365},
            {'label': '5 Years', 'value': 5 * 365},
        ],
        value=365,  # Initialize with a default selected duration (1 Year)
    ),
    dcc.Graph(id='stock-comparison-plot'),
    
    
    html.H1("Financial Plot", style={'text-align': 'center'}),
    # Dropdown for selecting yearly or quarterly statements
    html.H2("Select Statements Type:"),
    dcc.Dropdown(
        id='stmt-type-dropdown',
        options=[
            {'label': 'Yearly Statements', 'value': 'yearly'},
            {'label': 'Quarterly Statements', 'value': 'quarterly'},
        ],
        value='yearly',  # Initialize with 'Yearly Statements'
    ),
    dcc.Graph(id='income-statements-plot'),
    
    dcc.Graph(id='balance-sheet-plot'),
    ####
    
])

@app.callback(
    Output('choropleth-map', 'figure'),
    Output('index-dropdown', 'value'),
    Input('choropleth-map', 'clickData')
)
def update_map(clickData):
    if clickData is not None:
        selected_country_code = clickData['points'][0]['location']

        # Find the corresponding index for the selected country code
        selected_index = majorStockIdx[majorStockIdx['Country Code'] == selected_country_code].index[0]

        # Create a new value for the dropdown containing the selected index
        dropdown_value = [selected_index]

        # Return the updated figure and dropdown value
        return update_choropleth_map(majorStockIdx, dropdown_value), dropdown_value

    return update_choropleth_map(majorStockIdx, [0]), [0]

def update_choropleth_map(data, selected_indices):
    # Define a color scale based on the sign of "Change"
    color_scale = {'Positive': "green", 'Negative': "red"}

    # Map "Change" column to colors
    data['Color'] = data['Change'].apply(lambda x: 'Positive' if x > 0 else 'Negative')

    fig = px.choropleth(data, locations="Country Code", color="Color", color_discrete_map=color_scale,
                        hover_data=["Country Name", "Symbol", "Name", "Last Price", "Change", "% Change"],
                        title="Hover over a country")

    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="white",
        showocean=True,
        oceancolor="lightblue",
    )

    fig.update_layout(
        geo=dict(
            showcoastlines=True,
            coastlinecolor="Black",
            showland=True,
            landcolor="white",
            showocean=True,
            oceancolor="lightblue",
            center=dict(lon=0, lat=0),
            projection_scale=1,
        ),
        width=1200,
        height=800,
    )

    return fig

@app.callback(
    Output('line-plot', 'figure'),
    Input('index-dropdown', 'value')
)
def update_line_plot(selected_indices):
    line_fig = px.line(title=f"Selected indices Growth Trend analysis")
    legends = {}  # Dictionary to keep track of legends

    for idx in selected_indices:
        if idx not in legends:
            selected_data = majorStockIdx.iloc[idx]
            symbol = selected_data['Symbol']
            end_date = datetime.now()
            start_date = end_date - timedelta(days=1825)

            stock_data = yf.download(symbol, start=start_date, end=end_date)

            legend = f"{selected_data['Name']}({selected_data['Currency Code']})"
            while legend in legends.values():
                legend += " (Copy)"

            line_fig.add_scatter(x=stock_data.index, y=stock_data['Close'], mode='lines+markers', name=legend)
            legends[idx] = legend

    line_fig.update_xaxes(title_text="Date")
    line_fig.update_yaxes(title_text="Closing Price")

    return line_fig

#####

# Define a callback to update the stock dropdown based on the selected country
@app.callback(
    Output('stock-dropdown', 'options'),
    Input('country-dropdown', 'value'),
    State('country-dropdown', 'options')
)
def update_stock_dropdown(selected_country, country_options):
    if selected_country:
        stocks_for_country = data[data['Country'] == selected_country]
        stock_options = [{'label': f'{row["Name"]} - {row["Exchange"]}', 'value': row["Ticker"]}
                        for _, row in stocks_for_country.iterrows()]
        return stock_options
    else:
        return []

# Define a callback to limit stock selection to two
@app.callback(
    Output('stock-dropdown', 'value'),
    Input('stock-dropdown', 'value')
)
def limit_stock_selection(selected_stocks):
    if selected_stocks and len(selected_stocks) > 2:
        return selected_stocks[:2]
    return selected_stocks

# Define a callback to update the selected stocks table based on the selected stocks
@app.callback(
    Output('selected-stocks-table', 'data'),
    Input('stock-dropdown', 'value')
)
def update_selected_stocks_table(selected_stocks):
    if selected_stocks and isinstance(selected_stocks, list):
        selected_stocks_data = data[data['Ticker'].isin(selected_stocks)]
        return selected_stocks_data.to_dict('records')
    else:
        return []
    

    
#####

# Define a callback to create and update the stock comparison plot
@app.callback(
    Output('stock-comparison-plot', 'figure'),
    Input('stock-dropdown', 'value'),
    Input('duration-dropdown', 'value')
)
def update_stock_comparison_plot(selected_stocks, selected_duration):
    if selected_stocks:
        fig = px.line()
        fig.update_xaxes(title_text='Date')
        fig.update_yaxes(title_text='Stock Price')
        fig.update_layout(title='Stock Price Plot', xaxis_title='Date', yaxis_title='Stock Price')

        if len(selected_stocks) == 1:
            # Calculate the start date based on the selected duration
            end_date = datetime.today().strftime('%Y-%m-%d')
            start_date = (datetime.today() - timedelta(days=selected_duration)).strftime('%Y-%m-%d')

            # Fetch historical stock data for a single stock using Yahoo Finance
            stock_data = yf.download(selected_stocks[0], start=start_date, end=end_date)
            fig.add_scatter(x=stock_data.index, y=stock_data['Adj Close'], name=f'{selected_stocks[0]} Price')
        elif len(selected_stocks) == 2:
            # Calculate the start date based on the selected duration
            end_date = datetime.today().strftime('%Y-%m-%d')
            start_date = (datetime.today() - timedelta(days=selected_duration)).strftime('%Y-%m-%d')

            for stock in selected_stocks:
                # Fetch historical stock data for each selected stock
                stock_data = yf.download(stock, start=start_date, end=end_date)
                fig.add_scatter(x=stock_data.index, y=stock_data['Adj Close'], name=f'{stock} Price')
        
        # Customize the legend
        fig.update_layout(legend_title_text='Stocks')
        fig.update_layout(legend=dict(orientation='v', x=1.1))
        
        return fig
    else:
        return {}
    


@app.callback(
    Output('income-statements-plot', 'figure'),
    Input('stock-dropdown', 'value'),
    Input('stmt-type-dropdown', 'value')
)
def update_income_statements_plot(selected_stocks, stmt_type):
    if selected_stocks:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, subplot_titles=['Revenue Statement', 'Net Income Statement'])

        # Define custom colors for bars
        custom_colors = ['royalblue', 'green']  # Add more colors if needed

        for i, stock in enumerate(selected_stocks):
            stock_data = yf.Ticker(stock).income_stmt if stmt_type == 'yearly' else yf.Ticker(stock).quarterly_income_stmt
            color = custom_colors[i % len(custom_colors)]  # Cycle through custom colors
            fig.add_trace(go.Bar(x=stock_data.loc['Total Revenue'].index, y=stock_data.loc['Total Revenue'].values, name=f'{stock} Revenue', marker_color=color), row=1, col=1)
            fig.add_trace(go.Bar(x=stock_data.loc['Net Income'].index, y=stock_data.loc['Net Income'].values, name=f'{stock} Net Income', marker_color=color), row=2, col=1)

        fig.update_xaxes(title_text=f'{stmt_type.capitalize()}', row=2, col=1)
        fig.update_yaxes(title_text='Amount', row=1, col=1)
        fig.update_yaxes(title_text='Amount', row=2, col=1)
        fig.update_layout(title_text='Income and Revenue Statements', showlegend=True)

        return fig
    else:
        return {}



@app.callback(
    Output('balance-sheet-plot', 'figure'),
    Input('stock-dropdown', 'value'),
    Input('stmt-type-dropdown', 'value')
)
def update_balance_sheet_plot(selected_stocks, stmt_type):
    if selected_stocks:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, subplot_titles=['Total Assets', 'Total Liabilities Net Minority Interest'])

        # Define custom colors for bars
        custom_colors = ['blue', 'orange']  # Add more colors if needed

        for i, stock in enumerate(selected_stocks):
            stock_data = yf.Ticker(stock).balance_sheet if stmt_type == 'yearly' else yf.Ticker(stock).quarterly_balance_sheet
            color = custom_colors[i % len(custom_colors)]  # Cycle through custom colors
            
            # Extract data for Total Assets and Total Liabilities Net Minority Interest
            assets = stock_data.loc["Total Assets"].dropna()
            liabilities = stock_data.loc["Total Liabilities Net Minority Interest"].dropna()
            
            fig.add_trace(go.Bar(x=assets.index, y=assets.values, name=f'{stock} Total Assets', marker_color=color), row=1, col=1)
            fig.add_trace(go.Bar(x=liabilities.index, y=liabilities.values, name=f'{stock} Total Liabilities Net Minority Interest', marker_color=color), row=2, col=1)

        fig.update_xaxes(title_text=f'{stmt_type.capitalize()}', row=2, col=1)
        fig.update_yaxes(title_text='Amount', row=1, col=1)
        fig.update_yaxes(title_text='Amount', row=2, col=1)
        fig.update_layout(title_text=f'Assets and Liabilities Statements', showlegend=True)

        return fig
    else:
        return {}



#####


# Run the app
if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0")
