
import streamlit as st
import pandas as pd
import yfinance as yf
import capm_functions
import datetime

# Page Configuration
st.set_page_config(
    page_title="CAPM",
    page_icon="chart_with_upward_trend",
    layout="wide"
)

st.title("Capital Asset Pricing Model")

# User Input
col1, col2 = st.columns([1, 1])
with col1:
    stocks_list = st.multiselect(
        "Choose 4 stocks",
        ('TSLA', 'AAPL', 'NFLX', 'MSFT', 'MGM', 'AMZN', 'NVDA', 'GOOGL'),
        ['TSLA', 'AAPL', 'AMZN', 'GOOGL']
    )
with col2:
    year = st.number_input("Number of years", 1, 10)

# Date Range
end = datetime.date.today()
start = datetime.date(end.year - int(year), end.month, end.day)

# Download Data
sp500_data = yf.download('^GSPC', start=start, end=end)
SP500 = sp500_data[['Close']].reset_index()
SP500.columns = ['Date', 'SP500']

stocks_df = pd.DataFrame()
for stock in stocks_list:
    data = yf.download(stock, start=start, end=end)
    stocks_df[stock] = data['Close']

stocks_df.reset_index(inplace=True)
stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
SP500['Date'] = pd.to_datetime(SP500['Date'])

# Merge Data
stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

# Display Data
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("### Dataframe Head")
    st.dataframe(stocks_df.head(), use_container_width=True)
with col2:
    st.markdown("### Dataframe Tail")
    st.dataframe(stocks_df.tail(), use_container_width=True)

# Normalize and Plot
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("### Price of All Stocks")
    st.plotly_chart(capm_functions.interactive_plot(stocks_df))
with col2:
    st.markdown("### Price of All Stocks (Normalized)")
    normalized_df = capm_functions.normalize(stocks_df)
    fig = capm_functions.interactive_plot(normalized_df)
    st.plotly_chart(fig)

# Calculate Daily Returns
stocks_daily_return = capm_functions.daily_return(stocks_df)

# Calculate Beta and Alpha
beta = {}
alpha = {}
for i in stocks_daily_return.columns:
    if i != 'Date' and i != 'SP500':
        b, a = capm_functions.calculate_beta(stocks_daily_return, i)
        beta[i] = b
        alpha[i] = a

beta_df = pd.DataFrame({
    'Stock': beta.keys(),
    'Beta Value': [str(round(b, 2)) for b in beta.values()]
})

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown('### Calculated Beta Values')
    st.dataframe(beta_df, use_container_width=True)

# Calculate CAPM Return
rf = 0
rm = stocks_daily_return['SP500'].mean() * 252
return_df = pd.DataFrame({
    'Stock': stocks_list,
    'Return Value': [str(round(rf + (beta[stock] * (rm - rf)), 2)) for stock in stocks_list]
})

with col2:
    st.markdown('### CAPM Returns')
    st.dataframe(return_df, use_container_width=True)
