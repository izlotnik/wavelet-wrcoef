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