# -*- coding: utf-8 -*-

import math
import numpy as np
import pywt


def wavedec(data, wavelet, mode='symmetric', level=1, axis=-1):
    """
    Multiple level 1-D discrete fast wavelet decomposition

    Calling Sequence
    ----------------
    [C, L] = wavedec(data, wavelet, mode, level, axis)
    [C, L] = wavedec(data, wavelet)
    [C, L] = wavedec(data, 'sym3')

    Parameters
    ----------
    data: array_like
        Input data
    wavelet : Wavelet object or name string
        Wavelet to use
    mode : str, optional
        Signal extension mode, see Modes (default: 'symmetric')
    level : int, optional
        Decomposition level (must be >= 0). Default is 1.
    axis: int, optional
        Axis over which to compute the DWT. If not given, the
        last axis is used.

    Returns
    -------
    C: list
        Ordered list of flattened coefficients arrays (N=level):
        C = [app. coef.(N)|det. coef.(N)|... |det. coef.(1)]

    L: list
        Ordered list of individual lengths of coefficients arrays.
        L(1)   = length of app. coef.(N)
        L(i)   = length of det. coef.(N-i+2) for i = 2,...,N+1
        L(N+2) = length(X).

    Description
    -----------
    wavedec can be used for multiple-level 1-D discrete fast wavelet
    decomposition using a specific wavelet name or instance of the
    Wavelet class instance.

    The coefficient vector C contains the approximation coefficient at level N
    and all detail coefficient from level 1 to N

    The first entry of L is the length of the approximation coefficient,
    then the length of the detail coefficients are stored and the last
    value of L is the length of the signal vector.

    The approximation coefficient can be extracted with C(1:L(1)).
    The detail coefficients can be obtained with C(L(1):sum(L(1:2))),
    C(sum(L(1:2)):sum(L(1:3))),.... until C(sum(L(1:length(L)-2)):sum(L(1:length(L)-1)))

    The implementation of the function is based on pywt.wavedec
    with the following minor changes:
        - checking of the axis is dropped out
        - checking of the maximum possible level is dropped out
          (as for Matlab's implementation)
        - returns format is modified to Matlab's internal format:
          two separate lists of details coefficients and
          corresponding lengths

    Examples
    --------
    >>> C, L = wavedec([3, 7, 1, 1, -2, 5, 4, 6], 'sym3', level=2)
    >>> C
    array([  7.38237875   5.36487594   8.83289608   2.21549896  11.10312807
            -0.42770133   3.72423411   0.48210099   1.06367045  -5.0083641
            -2.11206142  -2.64704675  -3.16825651  -0.67715519   0.56811154
             2.70377533])
    >>> L
    array([5, 5, 6, 8])

    """
    data = np.asarray(data)

    if not isinstance(wavelet, pywt.Wavelet):
        wavelet = pywt.Wavelet(wavelet)

    # Initialization
    coefs, lengths = [], []

    # Decomposition
    lengths.append(len(data))
    for i in range(level):
        data, d = pywt.dwt(data, wavelet, mode, axis)

        # Store detail and its length
        coefs.append(d)
        lengths.append(len(d))

    # Add the last approximation
    coefs.append(data)
    lengths.append(len(data))

    # Reverse (since we've appended to the end of list)
    coefs.reverse()
    lengths.reverse()

    return np.concatenate(coefs).ravel(), lengths


def detcoef(coefs, lengths, levels=None):
    """
    1-D detail coefficients extraction

    Calling Sequence
    ----------------
    D = detcoef(C, L)
    D = detcoef(C, L, N)
    D = detcoef(C, L, [1, 2, 3])

    Parameters
    ----------
    coefs: list
        Ordered list of flattened coefficients arrays (N=level):
        C = [app. coef.(N)|det. coef.(N)|... |det. coef.(1)]
    lengths: list
        Ordered list of individual lengths of coefficients arrays.
        L(1)   = length of app. coef.(N)
        L(i)   = length of det. coef.(N-i+2) for i = 2,...,N+1
        L(N+2) = length(X).
    levels : int or list
        restruction level with N<=length(L)-2

    Returns
    ----------
    D : reconstructed detail coefficient

    Description
    -----------
    detcoef is for extraction of detail coefficient at different level
    after a multiple level decomposition. If levels is omitted,
    the detail coefficients will extract at all levels.

    The wavelet coefficients and lengths can be generated using wavedec.

    Examples
    --------
    >>> x = range(100)
    >>> w = pywt.Wavelet('sym3')
    >>> C, L = wavedec(x, wavelet=w, level=5)
    >>> D = detcoef(C, L, levels=len(L)-2)
    """
    if not levels:
        levels = range(len(lengths) - 2)

    if not isinstance(levels, list):
        levels = [levels]

    first = np.cumsum(lengths) + 1
    first = first[-3::-1]
    last = first + lengths[-2:0:-1] - 1

    x = []
    for level in levels:
        d = coefs[first[level - 1] - 1:last[level - 1]]
        x.append(d)

    if len(x) == 1:
        x = x[0]

    return x


def wrcoef(coefs, lengths, wavelet, level):
    """
    Restruction from single branch from multiple level decomposition

    Calling Sequence
    ----------------
    X = wrcoef(C, L, wavelet, level)

    Parameters
    ----------
    # type='a' is not implemented.
    # type : string
    #   approximation or detail, 'a' or 'd'.
    coefs: list
        Ordered list of flattened coefficients arrays (N=level):
        C = [app. coef.(N)|det. coef.(N)|... |det. coef.(1)]
    lengths: list
        Ordered list of individual lengths of coefficients arrays.
        L(1)   = length of app. coef.(N)
        L(i)   = length of det. coef.(N-i+2) for i = 2,...,N+1
        L(N+2) = length(X).
    wavelet : Wavelet object or name string
        Wavelet to use
    level : int
        restruction level with level<=length(L)-2

    Returns
    ----------
    X :
        vector of reconstructed coefficients

    Description
    -----------
    wrcoef is for reconstruction from single branch of multiple level
    decomposition from 1-D wavelet coefficients.

    The wavelet coefficients and lengths can be generated using wavedec.

    Examples
    --------
    >>> x = range(100)
    >>> w = pywt.Wavelet('sym3')
    >>> C, L = wavedec(x, wavelet=w, level=5)
    >>> X = wrcoef(C, L, wavelet=w, level=len(L)-2)
    """
    def upsconv(x, f, s):
        # returns an extended copy of vector x obtained by inserting zeros
        # as even-indexed elements of data: y(2k-1) = data(k), y(2k) = 0.
        y_len = 2 * len(x) + 1
        y = np.zeros(y_len)
        y[1:y_len:2] = x

        # performs the 1-D convolution of the vectors y and f
        y = np.convolve(y, f, 'full')

        # extracts the vector y from the input vector
        sy = len(y)
        d = (sy - s) / 2.0
        y = y[int(math.floor(d)):(sy - int(math.ceil(d)))]

        return y

    if not isinstance(wavelet, pywt.Wavelet):
        wavelet = pywt.Wavelet(wavelet)

    data = detcoef(coefs, lengths, level)

    idx = len(lengths) - level
    data = upsconv(data, wavelet.rec_hi, lengths[idx])
    for k in range(level-1):
        data = upsconv(data, wavelet.rec_lo, lengths[idx + k + 1])

    return data


if __name__ == '__main__':
    # Define wavelet parameters
    wavelet_type = 'sym3'
    wavelet_level = 3

    # Generate input data
    N = 9
    signal = range(N)

    # Define wavelet
    w = pywt.Wavelet(wavelet_type)
    # print([w.dec_lo, w.dec_hi, w.rec_lo, w.rec_hi])

    C, L = wavedec(signal, wavelet=w, level=wavelet_level)

    for n in range(len(L)-2):
        print(n+1)
        D = wrcoef(C, L, wavelet=w, level=n+1)
        print(D)
