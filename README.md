![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)
![Python 3.5](https://img.shields.io/badge/python-3.5-blue.svg)
![License](https://img.shields.io/badge/license-MIT%20License-blue.svg)

# Description
Reconstruct the coefficients of a one-dimensional signal from a wavelet multiple level decomposition and implement Matlab's function wrcoef in Python

# Purpose
In Python we have two great libraries to deal with different types of wavelets: [PyWavelets](https://github.com/PyWavelets/pywt) and [PyYAWT](https://github.com/holgern/pyyawt). The latter one is not under active development now but could be used for inspirational purposes. Unfortunately, the function to reconstruct the signal from multilevel decomposition is not implemented in both packages, see, for example, the related source code of the [PyYAWT library](http://pyyawt.readthedocs.io/_modules/pyyawt/dwt1d.html#wrcoef). Hopefully, the related function is implemented in the Matlab Wavelet Toolbox, see [`wrcoef`](https://www.mathworks.com/help/wavelet/ref/wrcoef.html). So, we will reengineer the code of that function for one special family of wavelets, known as [Symlet Wavelets or Symlets](https://www.mathworks.com/help/wavelet/gs/introduction-to-the-wavelet-families.html#f3-1008627).

# Sample code
```Python
import pywt
from wrcoef import wavedec, wrcoef

x = range(10)
w = pywt.Wavelet('sym3')
C, L = wavedec(x, wavelet=w, level=3)
for n in range(len(L)-2):
    D = wrcoef(C, L, wavelet=w, level=n+1)
    print(D)
```

# Compare the returned values with Matlab implementation

### Python code
```Python
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

# Decompose input signal
C, L = wavedec(signal, wavelet=w, level=wavelet_level)

# Reconstruct all the coefficients
for n in range(len(L)-2):
    D = wrcoef(C, L, wavelet=w, level=n+1)
    print(n+1, D)
```
outputs
```
(1, array([-0.18001655, -0.02431181,  0.15421323, -0.06358005,  0.01171875, 0.0284238 , -0.05539205, -0.17840172,  0.30734641]))
(2, array([-0.31957935, -0.36604108, -0.20493612,  0.12679355,  0.15470611, 0.15528146,  0.02503992, -0.20584543, -0.05734058]))
(3, array([-1.61945151, -0.96063311, -0.57396359,  0.01898383,  0.33471306, 0.6003336 ,  1.08927648,  1.62040633,  1.20235446]))
(4, array([-1.22024672, -1.27239303, -1.27478749, -1.27132754, -0.89466989, -0.35120599,  0.18262275,  0.83003707,  1.40745885]))
(5, array([-0.63011608, -0.48929529, -0.3647863 , -0.22916039, -0.11662095, -0.01042247,  0.10814968,  0.22657073,  0.35613215]))
```

### Matlab code
```Matlab
clc; clear all; format short

% Define wavelet parameters
wavelet_type = 'sym3';
wavelet_level = 5;

% Generate input data
N = 9;
signal = 0:N-1;

% Decompose input signal
[C, L] = wavedec(signal, wavelet_level, wavelet_type);

% Reconstruct all the coefficients
for n=1:max(1, length(L)-2), disp(n)
    D = wrcoef('d', C, L, 'sym3', n);
    disp(D)
end
```
outputs
```
     1
   -0.1800   -0.0243    0.1542   -0.0636    0.0117    0.0284   -0.0554   -0.1784    0.3073
     2
   -0.3196   -0.3660   -0.2049    0.1268    0.1547    0.1553    0.0250   -0.2058   -0.0573
     3
   -1.6195   -0.9606   -0.5740    0.0190    0.3347    0.6003    1.0893    1.6204    1.2024
     4
   -1.2202   -1.2724   -1.2748   -1.2713   -0.8947   -0.3512    0.1826    0.8300    1.4075
     5
   -0.6301   -0.4893   -0.3648   -0.2292   -0.1166   -0.0104    0.1081    0.2266    0.3561
```

# Disclaimer
The code is free for academic/research purpose. Use it at your own risk and we are not responsible for any loss resulting from this code. Feel free to submit pull request for bug fixes.

# Author
[Ilya Zlotnik](https://scholar.google.ru/citations?hl=ru&user=gWphyBwAAAAJ) 2017
