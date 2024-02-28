import datetime
import logging
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


def get_tickers_data_by_year(tickers, year):
    historical_data_dict = {}
    # No longer limiting to the first 5 tickers for broader applicability
    # for ticker in tickers[-100:]:
    for ticker in tickers:
        try:
            start_date = f"{year}-01-01"
            end_date = f"{year}-12-31"
            historical_data = yf.Ticker(ticker).history(
                interval='1mo', start=start_date, end=end_date)['Close']
            print(f"{ticker}: data downloaded...")
            if not historical_data.empty and len(historical_data) > 12:
                first_price = historical_data.iloc[0]
                last_price = historical_data.iloc[-1]
                percentage_change = (
                    (last_price - first_price) / first_price) * 100
                historical_data_dict[ticker] = percentage_change
            else:
                print(f"{ticker} has less than 12 months of data.")
                historical_data_dict[ticker] = None
        except Exception as e:
            error_message = f"Error for {ticker} in {year}: {e}. Skipping..."
            print(error_message)
            logging.error(error_message)  # Log the error
            historical_data_dict[ticker] = None
    return historical_data_dict


def get_tickers_data_by_years(start_year, end_year, tickers_filename):
    """Downloads yearly data for given tickers."""
    """Generates a DataFrame from the historical data dictionary.

        Ticker | 2020   | 2021   | 2022   | 2023
        AAPL   | 134.15 | 134.15 | 134.15 | 138.45
        TSLA   | 103.95 | 103.95 | 103.95 | 103.56
        MSFT   | 162.55 | 162.55 | 162.55 | 162.55       
        GOOGL  | 180.65 | 180.65 | 180.65 | 180.65
         ...
         ...
         ...
        ^GSPC  | 103.95 | 103.95 | 103.95 | 103.56

        --------------------------------------------------------------------- 
        columns: ['Ticker', '2020', '2021', '2022', '2023']
        rows: [s&p stocks + GSPC (S&P 500)]
    """
    all_data = {}

    # Iterate over each year, fetching tickers dynamically
    for year in range(start_year, end_year+1):
        tickers = get_tickers_by_year(tickers_filename, year)
        yearly_data = get_tickers_data_by_year(tickers, year)
        for ticker, change in yearly_data.items():
            if ticker not in all_data:
                all_data[ticker] = {}
            all_data[ticker][year] = change

    # Convert the nested dictionary into a DataFrame
    final_df = pd.DataFrame.from_dict(all_data, orient='index')
    final_df.columns = [str(year) for year in range(start_year, end_year+1)]

    # Reset index to turn the tickers into a column
    final_df.reset_index(inplace=True)
    final_df.rename(columns={'index': 'Ticker'}, inplace=True)
    return final_df


def generate_yearly_top25_dataframe(df, start_year, end_year):
    """Generates a new DataFrame for each year with top 25 stocks and S&P stock."""

    top25_per_year = {}
    years = [str(year) for year in range(start_year, end_year+1)]
    gspc_row = df[df['Ticker'] == '^GSPC']

    for year in years:
        # Sort and select top 25, excluding '^GSPC'
        top25 = df[df['Ticker'] != '^GSPC'].sort_values(
            by=year, ascending=False).head(25)
        # Append  '^GSPC' back to the frame
        top25 = pd.concat(
            [top25, gspc_row], ignore_index=True)
        top25_per_year[year] = top25
    return top25_per_year


def plot_top25_vs_sp(top25_df, year):
    """Plots yearly data from the DataFrame."""

    year = str(year)
    top25 = top25_df[year]

    # only gspc
    gspc_performance = top25[top25['Ticker'] == '^GSPC']

    # without gspc
    top25 = top25[top25['Ticker'] != '^GSPC']

    plt.figure(figsize=(10, 6))

    # Plot each of the top 25 stocks
    plt.bar(top25['Ticker'], top25[year], label='Top 25 Stocks')

    # Plot '^GSPC' for comparison
    plt.axhline(y=gspc_performance[year].values[0],
                color='r', linestyle='-', label='^GSPC')

    plt.xlabel('Ticker')
    plt.ylabel('Percentage Change')
    plt.title(f'Top 25 Performing Stocks vs ^GSPC in {year}')
    plt.xticks(rotation=90)  # Rotate tick labels for better readability
    plt.legend()
    plt.tight_layout()
    plt.show()


def get_tickers_by_year(filename, year):
    """Reads the S&P 500 data from the CSV file."""
    df = pd.read_csv(filename)
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['date'].dt.year == year]
    tickers = df.head(1)['tickers'].values[0].split(',')
    tickers.append('^GSPC')
    # print(tickers)
    return tickers


if __name__ == "__main__":

    # Configure logging
    logging.basicConfig(filename=f'logs/tickers_download_{datetime.datetime.now()}.log', level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')
    start_time = datetime.datetime.now()

    # Start the program
    logging.info(f"Starting the program at {start_time}")

    filename = 'data/sp_tickers_2023.csv'
    tickers_data = 'data/S&P 500 Historical Components & Changes(12-30-2023).csv'
    op_file = 'data/stock_analysis.csv'
    start_year = 2018
    end_year = 2023
    final_data = get_tickers_data_by_years(start_year, end_year, tickers_data)
    final_data.to_csv(op_file)

    # read the finalized data(saved to disk)
    yearly_df = pd.read_csv(op_file)

    top25_with_gspc_df = generate_yearly_top25_dataframe(
        yearly_df, start_year, end_year)

    # plot yearly top 25 performers vs GSPC: for example 2020
    plot_top25_vs_sp(top25_with_gspc_df, 2020)

    logging.info(f"Finished the program at {datetime.datetime.now()}")
    logging.info(f"Total time taken: {datetime.datetime.now() - start_time}")
