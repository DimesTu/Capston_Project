import numpy as np
from hmmlearn import hmm

# Observation array
Obs = np.array([1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0])
print('The Coin Flipping Observation: ')
print(Obs)
Obs.shape = (len(Obs), 1)

# Discreet HMM with 2 states, starts from 0
model = hmm.MultinomialHMM(n_components=2)
# Seed of RNG
np.random.seed(1)
# Fit model
model.fit(Obs)

# Print result
# Row (1, :) means the emission prob of state 1 into different observation
print('The Emission Probability Matrix is: ')
print(model.emissionprob_)
# Matrix (1, 2) means transmission prob from state 1 to state 2
print('The Transmission Matrix is: ')
print(model.transmat_)
# The Hidden States sequence with max probability
print('The Hidden States with max probability is: ')
print(model.predict(Obs))
# The Hidden States probability
print('The Probability of each Hidden State is: ')
print(model.predict_proba(Obs))


