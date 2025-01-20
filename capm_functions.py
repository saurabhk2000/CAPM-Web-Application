
import plotly.express as px
import numpy as np
import pandas as pd


def interactive_plot(df):
    fig = px.line()
    for i in df.columns:
        if i != 'Date':  # Exclude 'Date' column explicitly
            fig.add_scatter(x=df['Date'], y=df[i], name=i)
    fig.update_layout(
        width=450, 
        margin=dict(l=20, r=20, t=50, b=20), 
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    return fig


def normalize(df_2):
    df = df_2.copy()
    for i in df.columns:
        if i != 'Date':  # Exclude 'Date' column explicitly
            df[i] = pd.to_numeric(df[i], errors='coerce')  # Convert to numeric
            df[i] = df[i] / df[i].iloc[0]  # Normalize
    return df


def daily_return(df):
    df_daily_return = df.copy()
    for i in df.columns:
        if i != 'Date':  # Exclude 'Date' column explicitly
            df_daily_return[i] = df[i].pct_change() * 100  # Calculate daily return
            df_daily_return[i].iloc[0] = 0  # Set the first value to 0
    return df_daily_return


def calculate_beta(stocks_daily_return, stock):
    # Ensure consistent capitalization
    stocks_daily_return = stocks_daily_return.rename(columns=lambda x: x.upper())
    
    # Handle missing values
    stocks_daily_return = stocks_daily_return.dropna(subset=['SP500', stock])

    # Market return calculation
    rm = stocks_daily_return['SP500'].mean() * 252

    # Linear regression for beta
    b, a = np.polyfit(stocks_daily_return['SP500'], stocks_daily_return[stock], 1)

    return b, a
