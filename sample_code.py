# -*- coding: utf-8 -*-
import pywt
from wrcoef import wavedec, wrcoef


# Define wavelet parameters
wavelet_type = 'sym3'
wavelet_level = 5

# Generate input data
N = 9
signal = range(N)

# Define wavelet
w = pywt.Wavelet(wavelet_type)
# print([w.dec_lo, w.dec_hi, w.rec_lo, w.rec_hi])

# Decompose input signal
C, L = wavedec(signal, wavelet=w, level=wavelet_level)

# Reconstruct all the coefficients
for n in range(len(L)-2):
    D = wrcoef(C, L, wavelet=w, level=n+1)
    print(n+1, D)
