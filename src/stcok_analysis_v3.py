import datetime
import logging
import yfinance as yf
import pandas as pd


def get_tickers_data_by_year(tickers, year):
    '''Downloads yearly data for given tickers.

    '''
    try:
        data = yf.download(" ".join(tickers), start=f"{year}-01-01", end=f"{year+1}-02-01",
                           group_by="ticker", interval='1mo')
        data.to_csv(f'data/raw_data/raw_data_{year}.csv')
        print(f'{year} data downloaded...')
        logging.info(f"{year} data downloaded...")
    except Exception as e:
        print(e)
        logging.error(f"{year} data download has some issues:{e}")


def prepare_combined_file(start_year, end_year):
    """Reads the S&P 500 data from the CSV files.
    Prepares a final combined CSV file.
    """
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
    # List of file paths for the uploaded CSV files
    file_paths = [
        f'data/raw_data/raw_data_{year}.csv' for year in range(start_year, end_year)]

    # Initialize an empty DataFrame to hold all yearly differences
    all_years_difference = pd.DataFrame()

    for file_path in file_paths:
        # Extract year from file name for indexing
        year = file_path.split('_')[-1].split('.')[0]

        try:
            # Load the CSV file
            data = pd.read_csv(file_path)

            # Drop the first two rows which don't contain relevant data and reset the index
            data_cleaned = data.drop(index=[0, 1]).reset_index(drop=True)

            # Initialize an empty DataFrame for this year's reformatted data
            reformatted_data = pd.DataFrame()

            # Every 6th column starting from the 5th column (index 3) is a 'Close' column
            # Identify columns that are exactly named 'Close'
            close_columns = [data_cleaned.columns[i]
                             for i in range(5, len(data_cleaned.columns), 6)]

            # Iterate over each close column to calculate the difference
            for close_column in close_columns:
                # Extract ticker name from column header
                ticker = close_column.split('.')[0]

                # Convert to numeric and handle any non-numeric entries gracefully
                close_values = pd.to_numeric(
                    data_cleaned[close_column], errors='coerce')

                # Drop NaN values that might arise from conversion
                close_values = close_values.dropna()

                # Calculate difference % Change from year start to end
                if not close_values.empty:
                    yearly_difference = (
                        (close_values.iloc[-1] - close_values.iloc[0])/close_values.iloc[0])*100
                    reformatted_data[ticker] = [yearly_difference]

            # Set the index to the year for the reformatted data
            reformatted_data.index = [year]

            # Concatenate this year's data to the all years DataFrame
            all_years_difference = pd.concat(
                [all_years_difference, reformatted_data])

        except Exception as e:
            print(e)
            logging.error(f"{year} data read has some issues:{e}")

    # Transpose the final DataFrame to match the desired format
    all_years_difference = all_years_difference.transpose()

    # Ensure the columns are sorted by year
    all_years_difference = all_years_difference.sort_index(axis=1)

    # Save the final DataFrame to a CSV file
    try:
        df = all_years_difference.reset_index()
        df.rename(columns={'index': 'Ticker'}, inplace=True)
        df.to_csv(
            f'data/final_data/{start_year}_{end_year-1}_stock_data.csv', index=False, header=True)
    except Exception as e:
        print(e)
        logging.error(f"final data write has some issues:{e}")


def get_tickers_by_year(filename, year):
    """Reads the S&P 500 data from the CSV file."""
    df = pd.read_csv(filename)
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['date'].dt.year == year]
    tickers = df.head(1)['tickers'].values[0].split(',')
    tickers.append('^GSPC')
    return tickers


if __name__ == "__main__":
    start_year = 2018
    end_year = 2023
    tickers_file = 'data/S&P 500 Historical Components & Changes(12-30-2023).csv'

    # Configure logging
    logging.basicConfig(filename=f'logs/tickers_download_{datetime.datetime.now()}.log', level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')
    start_time = datetime.datetime.now()

    # Start the program
    logging.info(f"Starting the program at {start_time}")
    # download entire tickers  data at once and save it as individual csv files
    for year in range(start_year, end_year+1):
        tickers = get_tickers_by_year(tickers_file, year)
        get_tickers_data_by_year(tickers, year)

    # read these files, clean data, stitch them together and save it as a csv file
    prepare_combined_file(start_year, end_year+1)
    logging.info(f"Finished the program at {datetime.datetime.now()}")
    logging.info(f"Total time taken: {datetime.datetime.now() - start_time}")
