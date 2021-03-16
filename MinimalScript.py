
# Script to load the compressed .npz file containing x1, x2, y1, and y2 after preprocessing 

import numpy as np
from mne.decoding import CSP

loaded = np.load('preprocessingoutput.npz')

CSP(n_components=5, reg=1e-4).fit(loaded['x1'], loaded['y1'])