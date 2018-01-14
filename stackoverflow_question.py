# -*- coding: utf-8 -*-
import pywt
import numpy as np


def wrcoef(X, coef_type, coeffs, wavename, level):
    N = np.array(X).size
    a, ds = coeffs[0], list(reversed(coeffs[1:]))

    if coef_type == 'a':
        return pywt.upcoef('a', a, wavename, level=level)[:N]
    elif coef_type == 'd':
        return pywt.upcoef('d', ds[level-1], wavename, level=level)[:N]
    else:
        raise ValueError("Invalid coefficient type: {}".format(coef_type))


def decomposite(signal, coef_type='d', wname='db6', level=9):
    w = pywt.Wavelet(wname)
    a = signal
    ca = []
    cd = []
    for i in range(level):
        (a, d) = pywt.dwt(a, w)
        ca.append(a)
        cd.append(d)
    rec_a = []
    rec_d = []
    for i, coeff in enumerate(ca):
        coeff_list = [coeff, None] + [None] * i
        rec_a.append(pywt.waverec(coeff_list, w))
    for i, coeff in enumerate(cd):
        coeff_list = [None, coeff] + [None] * i
        rec_d.append(pywt.waverec(coeff_list, w))
    if coef_type == 'd':
        return rec_d
    return rec_a


if __name__ == '__main__':
    # # question
    # DATA = range(30)
    # N_LEVELS = 2
    # WAVELET_NAME = 'db4'
    # coeffs = pywt.wavedec(DATA, WAVELET_NAME, level=N_LEVELS)
    # # A2 = wrcoef(DATA, 'a', coeffs, WAVELET_NAME, N_LEVELS)
    # D2 = wrcoef(DATA, 'd', coeffs, WAVELET_NAME, N_LEVELS)
    # D1 = wrcoef(DATA, 'd', coeffs, WAVELET_NAME, 1)
    # print(D2, D1)

    # answer
    DATA = range(20)
    N_LEVELS = 4
    WAVELET_NAME = 'db1'
    coeffs = pywt.wavedec(DATA, WAVELET_NAME, level=N_LEVELS)
    # A4 = wrcoef(DATA, 'a', coeffs, WAVELET_NAME, N_LEVELS)
    D4 = wrcoef(DATA, 'd', coeffs, WAVELET_NAME, N_LEVELS)
    D3 = wrcoef(DATA, 'd', coeffs, WAVELET_NAME, 3)
    D2 = wrcoef(DATA, 'd', coeffs, WAVELET_NAME, 2)
    D1 = wrcoef(DATA, 'd', coeffs, WAVELET_NAME, 1)
    print(D4, D3, D2, D1)

    rec_d = decomposite(DATA, 'd', WAVELET_NAME, level=N_LEVELS)
    print(rec_d)
    # # Define wavelet parameters
    # wavelet_type = 'sym3'
    # wavelet_level = 3
    #
    # # Generate input data
    # N = 9
    # signal = range(N)
    #
    # # Define wavelet
    # w = pywt.Wavelet(wavelet_type)
    # # print([w.dec_lo, w.dec_hi, w.rec_lo, w.rec_hi])
    #
    # C, L = wavedec(signal, wavelet=w, level=wavelet_level)
    #
    # for n in range(len(L)-2):
    #     print(n+1)
    #     D = wrcoef(C, L, wavelet=w, level=n+1)
    #     print(D)
