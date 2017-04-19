#!/bin/python

import pickle

CATAGORIES_FILE = 'catagories.pickle'

catagories = {
    'cat1': []
}

with open(CATAGORIES_FILE, 'wb') as fh:
    pickle.dump(catagories, fh, protocol=pickle.HIGHEST_PROTOCOL)
