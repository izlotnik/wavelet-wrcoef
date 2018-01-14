# -*- coding: utf-8 -*-
import pywt
from wrcoef import wavedec, wrcoef


# Question 1

# Generate input data
DATA = range(10)

# Define wavelet parameters
N_LEVELS = 2
WAVELET_NAME = 'sym4'

# Define wavelet
w = pywt.Wavelet(WAVELET_NAME)

# Decompose input signal
C, L = wavedec(DATA, wavelet=w, level=N_LEVELS)

# Reconstruct all the coefficients
for n in range(len(L)-2):
    D = wrcoef(C, L, wavelet=w, level=n+1)
    print(n+1, D)


# Question 2

# Generate input data
DATA = range(18)

# Define wavelet parameters
N_LEVELS = 4
WAVELET_NAME = 'sym2'

# Define wavelet
w = pywt.Wavelet(WAVELET_NAME)

# Decompose input signal
C, L = wavedec(DATA, wavelet=w, level=N_LEVELS)

# Reconstruct all the coefficients
for n in range(len(L)-2):
    D = wrcoef(C, L, wavelet=w, level=n+1)
    print(n+1, D)
