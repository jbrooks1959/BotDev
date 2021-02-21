# BotDev
Developing BOT for trading
This BOT will identify trends and trend reversals to trade with the trend.
Note: I am currently gathering feedback on what to include in this package, this is not "final". I will add more packages based on feedback and eventually freeze the versions. Let me know your thoughts.

Intro:
This project is intended to be done in phases

TASK LIST - No all inclusive

1) task connect to exchange - Done
2) Create websocket to receive data - done
3) Parse data - done
4) Read userid from exchange - done
5) Read account balance for all coins - done
6) Shut down BOT if user isn't using referral link and print message that reads "NO BOT FOR FREELOADERS. Won't use referral link No BOT for YOU! FUCK OFF" - done
7) Stream data for all coins into a postgresql database (Open, high , low, close, volume) - working on it
8) Calculate VWAP, EMA's, WMA's
9) Create strategy - done
10) Code strategy into Python - Working  on it
11) Write code to check and see if in position
12) Calculate % of balance to use in trade from input
13) Write code to make buy based on strategy
14) Set BUY and SELL Conditions
15) Create functions and Classes to organize code and make it modular
16) Write code to place limit sell order for percent profit % or $ amount wanted
17) Option 2 write code to place sell at time of next flag (sell flag if bought, buy flag if shorting). 
18) Capture execution of order, price, and time on entering trade
19) Capture execution of order, price and time at close of trade send both to database, calculate percent gain per trade, daily, weekly and monthly. 
20) Create web interface for inputs
21) Show activity on web interface.  
22) One bot do all calculations and send signals to slave bots, that way BOTS can be shut down remotely if users don't pay.  
23) User logins for their BOT or run each bot in separate docker container.
24) Write code for stop loss and stop loss time delay

Server Components

Debian Linux 10 - a stable and dependable linux distribution for servers
Python 3.8 - the most popular language for data science, analysis, and machine learning
PostgreSQL 12 - the world's most advanced open source database
TimeScaleDB 2.0 - open source time-series database built on top of PostgreSQL

Web Frameworks

FastAPI - FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

Data Analysis

pandas - library for data analysis and manipulation of numerical tables and time series
NumPy - library for multi-dimensional arrays and matrices, mathematical functions
SciPy - modules for linear algebra, integration, FFT, signal and image processing
pandas-datareader - remote data access for pandas

Data Visualization

matplotlib - comprehensive library for creating static, animated, and interactive visualizations in Python
plotly - provides online graphing, analytics, and statistics tools for individuals and collaboration, as well as scientific graphing libraries for Python
dash - build & deploy beautiful analytic web apps using Python
mplfinance - matplotlib utilities for the visualization, and visual analysis, of financial data

Technical Analysis

ta - Technical Analysis Library in Python based on pandas
TA-Lib - Python wrapper for TA-Lib
bta-lib - backtrader ta-lib
pandas-ta - Pandas Technical Analysis (Pandas TA) is an easy to use library that leverages the Pandas library with more than 120 Indicators and Utility functions
tulipy - Python bindings for Tulip Indicators

Database Libraries and Data Storage

psycopg2 - most popular PostgreSQL database adapter for the Python programming language.
sqlalchemy - SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
redis - open source, in-memory data structure store, used as a database, cache, and message broker
h5py - Pythonic interface to the HDF5 binary data format

Broker APIs

alpaca-trade-api - python library for the Alpaca Commission Free Trading API. It allows rapid trading algo development easily, with support for both REST and streaming data interfaces.
python-binance - unofficial Python wrapper for the Binance exchange REST API v3
tda-api - tda-api is an unofficial wrapper around the TD Ameritrade APIs. It strives to be as thin and unopinionated as possible, offering an elegant programmatic interface over each endpoint
ib_insync - The goal of the IB-insync library is to make working with the Trader Workstation API from Interactive Brokers as easy as possible.

Data Providers

intrinio-sdk - Intrinio provides US market data, company fundamentals data, options data and SEC data, powered by advanced data quality technology
polygon-api-client - python client for Polygon.io, provider of real-time and historical financial market data APIs
iexfinance - Python SDK for IEX Cloud. Easy-to-use toolkit to obtain data for Stocks, ETFs, Mutual Funds, Forex/Currencies, Options, Commodities, Bonds, and Cryptocurrencies
yfinance - yfinance offers a reliable, threaded, and Pythonic way to download historical market data from Yahoo! finance.
quandl - source for financial, economic, and alternative datasets, serving investment professionals
alpha-vantage - The Alpha Vantage Stock API provides free JSON access to the stock market, plus a comprehensive set of technical indicators
sec-edgar-downloader - package for downloading company filings from the SEC EDGAR database
robin-stocks - simple to use functions to interact with the Robinhood Private API

Backtesting

backtrader - feature-rich Python framework for backtesting and trading
pyalgotrade - Python Algorithmic Trading Library with focus on backtesting and support for paper-trading and live-trading
bt - bt is a flexible backtesting framework for Python used to test quantitative trading strategies
backtesting - Backtesting.py is a Python framework for inferring viability of trading strategies on historical (past) data

Portfolio and Performance Analysis

pyfolio - library for performance and risk analysis of financial portfolios developed by Quantopian
finquant - program for financial portfolio management, analysis and optimisation

Web Server, Task Queue

uvicorn - lightning-fast ASGI server implementation
gunicorn - Python WSGI HTTP Server for UNIX
celery - simple, flexible, distributed task queue

Networking

requests - elegant and simple HTTP library for Python
boto3 - Amazon Web Services (AWS) SDK for Python. It enables Python developers to create, configure, and manage AWS services, such as EC2 and S3.
urllib3 - powerful, user-friendly HTTP client for Python
websocket-client - websocket client for python. This provide the low level APIs for WebSocket
websockets - library for building WebSocket servers and clients in Python

Utilities

beautifulsoup4 - library for screen-scraping
pendulum - package to assist with date and time manipulation
click - package for creating beautiful command line interfaces in a composable way with as little code as necessary
passlib - password hashing library

Machine Learning

tensorflow - open source library to help you develop and train ML models
scikit-learn - machine learning library
keras - deep learning framework
pytorch - optimized tensor library for deep learning using GPUs and CPUs
opencv-python - open source computer vision library
