# Financial Statement Analysis of Nifty 50 Stocks

Welcome to the Nifty 50 Stock Financial Statement Analysis project! This project aims to provide a comprehensive analysis of the financial statements of the Nifty 50 stocks from 2013 to 2022. By analyzing key financial indicators and ratios, this analysis helps stakeholders make informed decisions about potential investments.

Project URL: [https://nifty-50-stock-analysis.onrender.com/](https://nifty-50-stock-analysis.onrender.com/)

## Table of Contents

- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Data Collection](#data-collection)
- [Data Pre-processing](#data-pre-processing)
- [Financial Ratio Calculation](#financial-ratio-calculation)
- [Data Analysis](#data-analysis)
- [Data Visualization](#data-visualization)
- [Statistical Analysis](#statistical-analysis)
- [Getting Started](#getting-started)
- [Contributing](#contributing)


## Project Overview

The primary objective of this project is to analyze and compare the financial statements, including the income statement and balance sheet, of all Nifty 50 stocks from 2013 to 2022. By calculating and evaluating liquidity ratios, profitability ratios, and long-term solvency ratios, this analysis provides insights into the financial health and performance of each company. The project offers a user-friendly interface to view individual stock data, compare financial ratios, and make data-driven decisions.

## Technologies Used

- Python
- Beautiful Soup
- Requests
- MongoDB
- Flask
- Pandas
- Numpy
- Matplotlib
- HTML
- CSS
- BOOTSTRAP

# Project Structure

## Data Collection

The financial data for all Nifty 50 stocks was collected using web scraping techniques. Python's Beautiful Soup and Requests library were used to scrape income statement and balance sheet data from secondary sources. The data collection process was automated using an algorithm that can be scheduled to run once a year (typically in March-April) to collect the latest available annual financial data. The collected data was stored in MongoDB for efficient storage and retrieval.

## Data Pre-processing

The collected data underwent pre-processing to ensure accuracy and consistency. This involved cleaning the data to remove any inconsistencies, handling missing values, and addressing outliers. Financial statements were standardized to enable meaningful comparisons across companies.

## Financial Ratio Calculation

After pre-processing, various financial ratios were calculated to assess the performance and financial health of each company. Liquidity ratios such as working capital and current ratio, profitability ratios such as return on assets (ROA) and return on equity (ROE), and long-term solvency ratio such as debt to equity ratio were calculated for each stock.

## Data Analysis

The calculated financial ratios were analyzed and compared to evaluate the financial status of each company. By comparing the ratios, it was possible to identify which companies performed best in terms of each ratio. This comprehensive analysis considered multiple aspects of a company's financial performance.

## Data Visualization

To facilitate easy understanding and decision-making, the project utilized various data visualization techniques. Bar graphs, line charts, and tables were created to visualize the calculated ratios and their comparisons. These visualizations were designed to present the data in an easy-to-understand format, enabling stakeholders to make informed decisions based on the analysis.

## Statistical Analysis

In addition to financial ratio calculations, statistical analysis techniques such as mean, median, and standard deviation were applied to gain further insights from the data. These techniques helped identify trends, patterns, and anomalies, leading to more meaningful conclusions.

## Getting Started

To get started with the project, follow the steps below:

1. Clone the repository to your local machine:

```bash
git clone <repository-url>
```

2. Navigate to the project directory: Install the required dependencies using pip and the provided requirements.txt file:

```bash
pip install -r requirements.txt
```

3. Once the dependencies are installed, go to the src directory:

```bash
cd src
```

4. Run the Flask application using the app.py file:

```bash
python app.py
```

This will start the Flask server, and you should see the application running on `http://localhost:5000`.

If you want to visit the deployed version of the project, simply visit the provided URL: [Web_URL](https://nifty-50-stock-analysis.onrender.com/), to access the application.

## Contributing

Contributions to this project are welcome! If you have any suggestions, improvements, or bug fixes, please feel free to submit a pull request. Together, we can enhance the analysis and make it more valuable to stakeholders.