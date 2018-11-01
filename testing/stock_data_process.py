
import pandas as pd


# Read the prepared row stock data

# Define stock index
#stock_index = "ANZ.AX"
stock_index = "GOOG"

# Define file names
#file_name_raw = "stock_data_raw/" + stock_index + ".csv"
#print(file_name_raw)
file_name_senti = "stock_data_senti/" + stock_index + ".csv"
#print(file_name_senti)
file_name_processed = "stock_data_processed/" + stock_index + ".csv"
#print(file_name_processed)

# Read from file
data_processed = pd.read_csv(file_name_senti, header=0)
print(data_processed)

# Set date column as the index
data_processed = data_processed.set_index('Date')

# Read change the index into datetime object
data_processed.index = pd.to_datetime(data_processed.index)
#data_processed = data_processed[start_date:end_date]


# ----------------- Get the observation sequences -----------------

# Vibration trends: difference between high and low within a day
data_processed['HL_Diff'] = (data_processed['High']/data_processed['Low'])-1
#print(data_processed['HL_Diff'])
#print(data_processed)

# Volume trends: Volume over 10-day moving average volume
data_processed['V/A10'] = data_processed['Volume']/(data_processed['Volume'].rolling(10).mean())-1
#print(data['V/A10'])

# Volume trends: Volume over 2-day moving average volume
data_processed['V/A2'] = data_processed['Volume']/(data_processed['Volume'].rolling(2).mean())-1
#print(data_processed['V/A2'])

# Volume trends: Volume difference
data_processed['V_Diff'] = data_processed['Volume']/(data_processed['Volume'].shift()) -1


# Volume trends: Volume difference, Volume today vs yesterday
#data_processed['V_Diff'] = ( data_processed['Volume'] - data_processed['Volume'].shift() ) / data_processed['Volume'].shift()

# Price trends: Close over 5-day moving average of Close
data_processed['C/A5'] = ( data_processed['Close']/(data_processed['Close'].rolling(5).mean()) )-1
#data_processed['C/A5'] = data_processed['Close']/(data_processed['Close'].rolling(5).mean())

# Price trends: Close over 20-day moving average of Close
data_processed['C/A20']= ( data_processed['Close']/(data_processed['Close'].rolling(20).mean()) )-1
#data_processed['C/A20']= data_processed['Close']/(data_processed['Close'].rolling(20).mean())

# Price trends: Close difference, Close today vs yesterday
data_processed['C_Diff'] = data_processed['Close'] / data_processed['Close'].shift() - 1

# Price trends: Close over Open
#data_processed['OC_Diff'] = (data_processed['Close'] - data_processed['Open']) / data_processed['Open']
data_processed['OC_Diff'] = data_processed['Close'] / data_processed['Open'] -1

# Price trends: High over low
data_processed['HL_Diff'] = data_processed['High'] / data_processed['Low'] -1

# Sentiment Trends: Sentiment index today vs yesterday
#data_processed['Pola2'] = data_processed['Pola'].rolling(2)
#data_processed['Subj2'] = data_processed['Subj'].rolling(2)

print(data_processed)
# Write to another csv
data_processed.to_csv(file_name_processed, header=True, float_format='%.6f')
