
# Stock Performance Analysis Tool

This Python script is designed to perform a detailed comparison of stock market performances, focusing on the top 25 performing stocks from the S&P 500 index against the overall S&P 500 returns on a quarterly basis over the past decade. The analysis aims to identify trends and the potential for higher returns by investing in these top performers compared to the broader market.

## Analysis Procedure

1. **Data Collection:**
   - For each year from 2019 to 2023, identify the top 25 performing stocks from the S&P 500's historical components.
   - Calculate the average annual percentage change for each stock.
   - Obtain the S&P 500 (GSPC) returns for the same years.

2. **Performance Analysis:**
   - Compare the returns of these top 25 stocks against the S&P 500's returns annually.
3. **Trend Visualization:**
   - Plot the performance trends to visually compare the growth of the top-25 investment versus the S&P 500 index.

4. **Investment Simulation:**
   - Simulate the investment of $1,000,000 in both the top-25 stocks and the S&P 500 index, tracking their performance (not included in the analysis as of now).

## Features

- Download historical stock data using Yahoo Finance.
- Calculate the annual percentage change for each stock.
- Plot the yearly performance of top-25 stocks and the S&P 500 index.

## Installation

To run this script, you need Python 3.x and the following packages:
- yfinance
- pandas
- matplotlib

You can install the dependencies with the following command:

```bash
pip install yfinance pandas matplotlib
```

## Input File

The script requires an input CSV file named `S&P 500 Historical Components & Changes.csv` that contains historical data of S&P 500 components. This file should have the following columns:
- `date`: The date of the data entry.
- `tickers`: A comma-separated list of stock tickers included in the S&P 500 on that date.

Ensure this file is located in the `data` directory relative to the script, or modify the script to point to the correct location of your input file.

## Output File

The script will generate an output CSV file named `stock_analysis.csv` that contains the following columns:
- **Columns:** ['Ticker', '2020', '2021', '2022', '2023']
- **Values:** The annual percentage change for each stock for the specified time range.
- **Rows:** Includes the all the tickers (and their corresponding percentage changes) in the input file and the S&P 500 (GSPC) for each year.
- **Example:**
```
---------------------------------------------------------------------
Ticker | 2020   | 2021   | 2022   | 2023
AAPL   | 134.15 | 134.15 | 134.15 | 138.45
TSLA   | 103.95 | 103.95 | 103.95 | 103.56
MSFT   | 162.55 | 162.55 | 162.55 | 162.55       
GOOGL  | 180.65 | 180.65 | 180.65 | 180.65
---------------------------------------------------------------------
```


## Usage

Modify the `ticker`, `start_year`, and `end_year` variables in the script to analyze different stocks and time periods. Then run the script:

```bash
python stock_analysis.py
```

## Contributing

Feel free to fork the repository and submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
