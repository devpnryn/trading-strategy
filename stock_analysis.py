
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


def read_file_contents(filename):
    """Reads the input CSV file containing tickers for each year."""
    return pd.read_csv(filename)


def get_tickers_with_sp(tickers):
    """Appends S&P 500 index to the list of tickers for each year."""
    full_tickers = tickers[0].split(',')
    full_tickers.append('^GSPC')
    return full_tickers


def download_data_for_tickers(tickers, start_year, end_year):
    """Downloads yearly data for given tickers."""
    historical_data_dict = {}
    for ticker in tickers[495:]:
        # Ensure every year is initialized for the ticker
        if ticker not in historical_data_dict:
            historical_data_dict[ticker] = {
                str(year): None for year in range(start_year, end_year + 1)}
        for year in range(start_year, end_year + 1):
            try:
                # Download data for the start and end of each year from 2020 to 2025
                for year in range(start_year, end_year + 1):
                    start_date = f"{year}-01-01"
                    end_date = f"{year}-12-31"
                    historical_data = yf.Ticker(ticker).history(
                        interval='1mo', start=start_date, end=end_date)['Close']

                    print(f"Downloaded data for {ticker} in {year}")

                    if not historical_data.empty and len(historical_data) >= 12:
                        # Calculate the percentage change from the first to the last month
                        first_price = historical_data.iloc[0]
                        # Assuming the last index is December
                        last_price = historical_data.iloc[-1]
                        percentage_change = (
                            (last_price - first_price) / first_price) * 100
                        historical_data_dict[ticker][str(
                            year)] = percentage_change
                    else:
                        print(f"Not enough data for {ticker} in {year}")

            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")
                historical_data_dict[ticker][str(year)] = None
                continue

    return historical_data_dict


def modify_data_and_save(data, op_file):
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
    df = pd.DataFrame.from_dict(data, orient='index')
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Ticker'}, inplace=True)

    # Reordering DataFrame columns to match required format
    years = [str(year) for year in range(start_year, end_year + 1)]
    df = df[['Ticker'] + years]

    # Save the combined data to a CSV file
    df.to_csv(op_file)
    return df


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
    # print(df.head(1)['tickers'])
    return df.head(1)['tickers']


# Example usage
if __name__ == "__main__":
    filename = 'data/sp_tickers_2023.csv'
    fulldata = 'S&P 500 Historical Components & Changes(12-30-2023).csv'
    op_file = 'data/stock_analysis.csv'
    start_year = 2018
    end_year = 2019
    tickers_list_2018 = get_tickers_by_year(fulldata, start_year)
    tickers_list_2019 = get_tickers_by_year(fulldata, end_year)

    # diff_tickers = set(tickers_list_2018.values[0].split(',')).difference(
    #     set(tickers_list_2019.values[0].split(',')))
    # print(diff_tickers)

    input_df = read_file_contents(filename)
    full_tickers_list = get_tickers_with_sp(input_df['tickers'])
    data = download_data_for_tickers(full_tickers_list, start_year, end_year)
    df = modify_data_and_save(data, op_file)

    # read the finalized data(saved to disk)
    yearly_df = read_file_contents(op_file)

    top25_with_gspc_df = generate_yearly_top25_dataframe(
        yearly_df, start_year, end_year)

    # plot yearly top 25 performers vs GSPC
    plot_top25_vs_sp(top25_with_gspc_df, 2018)
    # plot_top25_vs_sp(top25_with_gspc_df, 2019)
    # plot_top25_vs_sp(top25_with_gspc_df, 2020)
    # plot_top25_vs_sp(top25_with_gspc_df, 2020)
