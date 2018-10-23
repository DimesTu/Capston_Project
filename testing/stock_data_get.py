from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import requests

ticker = ['AAPL']

start_date = '2010-01-01'
end_date = '2016-12-31'

panel_data = data.DataReader('INPX', 'google', start_date, end_date)