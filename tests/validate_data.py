
import datetime
import logging
import math
import yfinance as yf
import pandas as pd


if __name__ == "__main__":
    start_year = 2018
    end_year = 2023

    # Configure logging
    logging.basicConfig(filename=f'logs/data_compare_{datetime.datetime.now()}.log', level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')

    # checking data validity by randomly picking the ticker from the final output
    # and check if the data correctness by querying again yahoo finance API
    # for the same ticker and comparing the values

    # read the finalized data(saved to disk)
    start_time = datetime.datetime.now()
    logging.info(f"started comparison of data.{start_time}")
    df = pd.read_csv('data/final_data/2018_2023_stock_data.csv')

    # Rename the first column to 'Ticker'
    # Trim leading and trailing spaces from the 'Ticker' column before setting it as the index

    df.set_index('Ticker', inplace=True)

    success_count = 0
    failure_count = 0
    success_list = []
    failure_list = []

    # start_idx = sample(n=500)
    for row, columns in df.iterrows():
        # random_row = df.sample(n=1)
        # random_row = row

        # get ticker name
        ticker = row
        print(ticker)

        for year in columns._data.items:
            # randomly picking the ticker from the final output
            downloaded_avg = columns[year]
            if math.isnan(downloaded_avg):
                continue
            downloaded_avg = round(float(downloaded_avg), 2)
            year = int(year)
            start_date = f'{year}-01-01'
            end_date = f'{year+1}-02-01'

            # check if the data correctness by querying again yahoo finance API
            # for the same ticker and comparing the values
            try:
                current_avg = 0
                # get fresh data with API
                data = yf.Ticker(ticker).history(
                    interval='1mo', start=start_date, end=end_date)['Close']

                # calculate %change for the ticker
                if not data.empty and len(data) > 12:
                    first_price = data.iloc[0]
                    last_price = data.iloc[-1]
                    current_avg = round((
                        (last_price - first_price) / first_price) * 100, 2)

                    # compare
                    if ((current_avg - downloaded_avg) < 1):
                        print(f"% change for {ticker} in {year} is correct")
                        success_count += 1
                        success_list.append(ticker)
                        logging.info(
                            f"Success: % change for {ticker} in {year} is correct. downloaded: {downloaded_avg} == current: {current_avg}")
                    else:
                        print(
                            f"% change for {ticker}  in the {year} is incorrect")
                        failure_count += 1
                        failure_list.append(ticker)
                        logging.info(
                            f"Failed: % change for {ticker}  in  the {year} is incorrect. downloaded: {downloaded_avg} != current: {current_avg}")

                else:
                    logging.info(
                        f"{ticker} has less than 12 months of data.")

            except Exception as e:
                print(e)
                failure_count += 1
                failure_list.append(ticker)
                logging.error(
                    f"{ticker} data download has some issues:{e}")

    logging.info(
        f"{success_count} out of {success_count+failure_count} data is correct")
    logging.info(
        f"{failure_count} out of {success_count+failure_count} data is incorrect")
    logging.info(f"Success list: {success_list}")
    logging.info(f"Failure list: {failure_list}")
    logging.info('done commparing data')
    logging.info(f"Total time taken: {datetime.datetime.now() - start_time}")
