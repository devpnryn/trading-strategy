
# Stock Performance Analysis Tool

This Python script is designed to perform a detailed comparison of stock market performances, focusing on the top 25 performing stocks from the S&P 500 index against the overall S&P 500 returns on a quarterly basis over the past decade. The analysis aims to identify trends and the potential for higher returns by investing in these top performers compared to the broader market.



## Analysis Procedure

1. **Data Collection:**
   - For each year from 2018 to 2023, identify the top 25 performing stocks from the S&P 500's historical components.
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
- logging
- yfinance
- pandas
- matplotlib

You can install the dependencies with the following command:

```bash
pip install -r requirements.txt
```
## Project Structure

The project structure is as follows:

```
   ├── data
   |   └── final_data
   |   |   └── 2018_2023_stock_analysis.csv
   |   └── raw_data
   |   |   └── raw_data_2018.csv
   |   |   └── raw_data_2019.csv
   |   |   └── raw_data_2020.csv
   |   |   └── raw_data_2021.csv
   |   |   └── raw_data_2022.csv
   |   |   └── raw_data_2023.csv
   │   └── S&P 500 Historical Components & Changes(12-30-2023).csv
   ├── logs
   │   └── trickers_download_timestamp.log
   |   └── data_compare_timestamp.log
   ├── docs
   │   └── project_documentation.md
   ├── src
   │   └── stock_analysis.py
   |   └── stock_analysis_v3.py
   ├── tests
   │   └── validate_data.py
   ├── LICENSE
   ├── .gitignore
   ├── app.yaml
   ├── README.md
   └── requirements.txt
   
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

To download tickers in bulk:
```bash
python src/stock_analysis_v3.py
```
or 
To download tickers one by one 
```bash
python src/stock_analysis.py
```

## Testing
There are no tests per say but to test the downloaded data (via /src/stock_analysis_v3.py), run the following command:

```bash
python tests/validate_data.py
```
The above script checks one by one ticker data again makeing calls  to Yahoo Finance to get the data.  
### Note
This comparison only works if the data is downloaded and saved in the final_data folder.

## Logs
basic logging is configured in the script to log the time of data download and data comparisons. Logs are timestamped files and gets created in the logs directory.

Data comparison logs are going to give success and failed lists of tickers.


## Acknowledgments and References

This project builds upon the work done in [sp500](https://github.com/username/repository), courtesy of [fja05680](https://github.com/fja05680). Special thanks to him/her for the valuable contributions to the community.

### Note on Data Reference
One of the data files used in this project, `S&P 500 Historical Components & Changes(12-30-2023).csv`, has been directly utilized from [sp500](https://github.com/fja05680/sp500) to ensure consistency and reliability in data reference. We acknowledge and appreciate the original work and have included it with due respect to its author(s).


## Limitations

1. **Error Handling:**
   There are several errors unhandled. Its a rough draft. Given my expertise in python, I don't know how to optimize this further like better logging and errro handling. 

2. **Full Data:**
   I didn't run this for one decade as I wanted to keep the data size small. I have run this for 2018-2023.

3. **Plotting:**
   Plots are basic. nothing fancy. If you like, you can customise them get as much as possible visualisations fromt the dataset.

4. **Investment Simulation:**
   Finally, I didn't run this data through simulation with investment data like for example, how much I would have earned in 2022 had I invested 1 million into the top25 identified stocks vs S&P500 stock. 

   

## Contributing

Feel free to fork the repository and submit pull requests. I am opne to suggestions and contributions. 

## License

This project is licensed under the MIT License - see the LICENSE file for details.
