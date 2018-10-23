import warnings
import numpy as np
import pandas as pd
from hmmlearn import hmm
from matplotlib import cm, pyplot as plt
from collections import Counter
import matplotlib.dates as dates
from datetime import date, datetime, time, timedelta


# Set seed for RNG in Gaussian
np.random.seed(1)

# Set the number of state
state_number = 2
#buy_state = 0
#sell_state = 1

# Set parameters for HMM
'''
covariance type:
spherical” — each obs uses a single variance value that applies to all features.
diag” — each obs uses a diagonal covariance matrix.
full” — each obs uses a full (i.e. unrestricted) covariance matrix.
tied” — all obs use the same full covariance matrix.
'''
cova_type = 'diag'
iteration_number = 2000

# Set the trade fee
trade_fee = 0

# Set the trade type:
# 0 means one-day raw data, such as Close, Volume, Close - Open and so on
# 1 means short term, such as Close today vs yesterday, Volume today vs yesterday
# 2 means long term, such as 5-day or 20-day
trade_type = 1

# To determine which state is buy
initial_period = 20

# Set initial state probability
# start_state_prob = np.zeros(state_number, dtype=int)
start_state_prob = np.array([1.0, 0.0])
start_trans_prob = np.array([[0.8, 0.1, 0.1],
                             [0.1, 0.8, 0.1],
                             [0.1, 0.1, 0.8]])
#print(start_state_prob)

# Set the initial cash
start_cash = 100000
current_cash = start_cash
current_shares = 0



# Define stock index
#stock_index = 'ANZ.AX' # ANZ is a bad choice, because the data is different from US and price is too low
stock_index = 'GOOG'



# Set the range of total data and training and testing data
# ATTENTION: The date must exist in the raw data
train_start_date = '2016-07-01'      # only hmm
#train_start_date = '2018-09-12'     # with sentiment


#train_end_date = '2017-01-03'
#train_end_date = '2017-06-30'
#train_end_date = '2017-07-03'
train_end_date = '2017-10-02'        # only hmm
#train_end_date = '2018-09-28'       # with sentiment


#test_end_date = '2017-07-05'
#test_end_date = '2017-07-20'
test_end_date = '2018-10-12'        # end of raw data


# Define the file name to read or write
#file_name_raw = "stock_data_raw/" + stock_index + ".csv"
file_name_processed = 'stock_data_processed/' + stock_index + '.csv'
file_name_trade = 'stock_data_trade/' + stock_index + "_" + train_start_date + '_' + train_end_date + '_' + \
                  test_end_date + '.csv'
#file_name_senti = "stock_data_senti/" + stock_index + ".csv"

#print(file_name_processed)


# Convert all the user config date strings into pandas datetime format
train_start_datetime = pd.to_datetime(train_start_date)
train_end_datetime = pd.to_datetime(train_end_date)
test_end_datetime = pd.to_datetime(test_end_date)
#print(train_start_date)



# Read the file for prepared stock data
# data_process should never be changed, since the index are based on it
data_processed = pd.read_csv(file_name_processed, header=0)
#print(data_processed)


# Set index as Date
#data = data.set_index('Date')
#print(data.index)


# Convert Date string into datetime format
#data.index = pd.to_datetime(data.index)
data_processed.Date = pd.to_datetime(data_processed.Date)
#print(data.Date)


# Calculate index for further operation. All the index is based on the data_processed dataframe
train_start_index = data_processed[data_processed['Date'] == train_start_date].index.values.item(0)
#print(train_start_index)

train_end_index = data_processed[data_processed['Date'] == train_end_date].index.values.item(0)
#print(train_end_index)

test_end_index = data_processed[data_processed['Date'] == test_end_date].index.values.item(0)
#print(test_end_index)

# Get data for testing with time period
data_test = data_processed.loc[train_end_index:(test_end_index+1), ['Date', 'Close']]
#print(data_test)

# Get the intrinsic price references
start_price = data_processed.loc[train_end_index, 'Close']
end_price = data_processed.loc[test_end_index, 'Close']
start_shares = int(start_cash / start_price)

data_test.loc[:, 'State'] = 3
#data_test['State'] = np.nan
data_test.loc[:, 'Signal'] = 0
#data_test['Signal'] = ''
data_test.loc[:, 'Shares'] = 0
#data_test['Shares'] = ''
data_test.loc[:, 'Cash'] = 0.0
#data_test['Cash'] = ''
data_test.loc[:, 'Total'] = 0.0
#data_test['Total'] = ''
data_test.loc[:, 'Ref'] = 0.0
#data_test['Ref'] = ''
#print(data_test)

# Calculate length of train set and test set
#train_length = train_end_index - train_start_index + 1
#test_length = test_end_index - train_end_index + 1
#print(test_length)

# Start iteration for each test trading day
for i in range(train_end_index, test_end_index+1):
    #print('The i now is', i )
    print('The datetime now is', data_processed.loc[i, 'Date'])

    # Get data for training and test with time period
    data_train = data_processed.loc[train_start_index:(i + 1)]
    #print(data_train)

    # Observation Matrix, each column is a feature
    if trade_type == 0:
        # Only 1-day intrinsic data.
        # This might not be good if one or more features keep same changing tendency
        obs_matrix = np.column_stack([
            data_train['Open'], data_train['Close'], data_train['High'], data_train['Low'], data_train['Volume']
        ])
    elif trade_type == 1:
        # Very short term relative data
        obs_matrix = np.column_stack([
            # data_train['Pola']
            # data_train['C_Diff'], data_train['OC_Diff'], data_train['V_Diff']
            data_train['C_Diff'], data_train['C/A5'], data_train['OC_Diff']

        ])
    elif trade_type == 2:
        # Very long term relative data
        obs_matrix = np.column_stack([
            data_train['C/A5']
        ])

    #print(obs_matrix)


    # Train the model
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        print('train Starts')
        # Fit the model with Gaussian Distribution
        model = hmm.GaussianHMM(n_components=state_number, covariance_type=cova_type, n_iter=iteration_number)

        # Set initial state and trans probability
        model.startprob_ = start_state_prob
        #print(model.startprob_)
        #model.transmat_ = start_trans_prob
        #print(model.transmat_)

        # Train the model
        model.fit(obs_matrix)

        # Show the hidden states
        hidden_states = model.predict(obs_matrix)
        # print(hidden_states)
        # print(hidden_states[0:20])
        # print(hidden_states[-8:])


        #print(hidden_states[0:initial_period])
        one_state_num = np.count_nonzero(hidden_states[0:initial_period])
        zero_state_num = initial_period - one_state_num
        if zero_state_num >= one_state_num :
            buy_state = 0
        else :
            buy_state = 1
        sell_state = 1 - buy_state
        #print(buy_state, sell_state)

        #print(model.startprob_)
        #trans_prob = model.transmat_
        #print(trans_prob)
        print('Train ends')


    # Trade according to the signal
    # Columns: Date, Close, State, Signal, Shares, Cash, Total, Ref
    data_test.loc[i, 'State'] = hidden_states[-1]
    #print(data_test)

    current_price = data_test.loc[i, 'Close']
    #print(current_price)

    # Define the buy and sell signal from the states
    # If the hidden state means buy
    if data_test.loc[i, 'State'] == buy_state :
        data_test.loc[i, 'Signal'] = 1
        shares_number = int( (current_cash-trade_fee) / current_price )
        # If at least can buy 1 share, buy
        if shares_number >= 1 :
            current_cash = current_cash - trade_fee - shares_number*current_price
            current_shares = int(current_shares + shares_number)
    # If the hidden state means sell
    elif data_test.loc[i, 'State'] == sell_state :
        data_test.loc[i, 'Signal'] = -1
        # If at least have 1 share to sell and the earning is larger than trade fee
        if (current_shares >= 1) and (current_shares*current_price >= trade_fee) :
            current_cash = current_cash + current_shares*current_price - trade_fee
            current_shares = 0
    # If the hidden state means hold
    else :
        # Column 1 is State, Column 2 is Signal
        data_test.loc[i, 'Signal'] = 0

    # Store the current assets and the reference price
    data_test.loc[i, 'Shares'] = current_shares
    data_test.loc[i, 'Cash'] = current_cash
    current_total = current_cash + current_shares * current_price
    data_test.loc[i, 'Total'] = current_total
    ref_price = (current_total / start_cash) * start_price
    data_test.loc[i, 'Ref'] = ref_price

    # Shift the training set index
    #train_start_index = train_start_index + 1
    #train_end_index = train_end_index + 1

    #print(data_train)
    #print('The hidden states sequence is: ')
    #print(hidden_states)

    #print(data_test)

print('data_test is\n', data_test)
print('data_train is\n', data_train)
print('hidden states is\n', hidden_states)




# Calculate the performance

current_shares = int( (start_cash - trade_fee) / start_price )
current_cash = (start_cash - trade_fee) % start_price
ref_total = current_cash + current_shares*end_price

print("The final asset is: ", data_test.iloc[-1, -2])
print("The reference is:", ref_total)

# Write to test result csv
data_test.to_csv(file_name_trade, header=True, index=False, float_format='%.6f')
#data_test.to_csv(file_name_trade, header=True)


plt.interactive(False)

# Color the states
fig1 = plt.figure(figsize=(25, 16))
plt.ylabel('Close Price')
plt.xlabel('Date')



# To print color as hidden states
for i in range(state_number):
    flag = (hidden_states == i)
    #print(flag)
    plt.plot_date(data_train.Date[flag], data_train['Close'][flag], '.', label='Hidden State %d' %i, lw=10)
    plt.legend(loc='upper left')
plt.plot_date(data_test['Date'], data_test['Ref'], '-', label='Performance Ref', lw=1)
plt.legend(loc='upper left')

'''
# To print color as trading signal,
# Bugs so far: the length of data_test is about half of data_train
for i in [-1, 1]:
    flag = (data_test['Signal'] == i)
    #plt.plot(data_test.Date[flag], data_test['Close'][flag], '.', label='Hidden state %d' %i, lw=10)
    plt.plot_date(data_train.Date[flag], data_train['Close'][flag], '.', label='Hidden State %d' %i, lw=10)
    plt.legend(loc='upper left')
plt.plot_date(data_test['Date'], data_test['Ref'], '-', label='Performance Ref', lw=1)
plt.legend(loc='upper left')
print('flag is\n', flag)
'''


# Save the figure
figure_name = 'stock_data_trade_fig/' + stock_index + '_' + str(int(data_test.iloc[-1, -2])) + '_' + str(trade_type) + \
              '_' + cova_type + '_' + train_start_date + '_' + train_end_date + "_" + test_end_date + '.png'
fig1.savefig(figure_name)
plt.show()



#fig2 = plt.figure(figsize=(25, 16))
#plt.ylabel('Close Price Reference')
#plt.xlabel('Date')

#plt.plot_date(data_test['Date'], data_test['Close'], '-', label='Close Price', lw=1)
#plt.legend(loc='upper left')

#plt.plot_date(data_test['Date'], data_test['Ref'], '-', label='Reference Price', lw=1)
#plt.legend(loc='upper left')
#plt.show()
