%% Stackoverflow questions
% https://stackoverflow.com/questions/45051106/multilevel-partial-wavelet-reconstruction-with-pywavelets/47591523
% and
% https://dsp.stackexchange.com/questions/42358/multilevel-partial-wavelet-reconstruction-with-pywavelets/42372
clc; clear all; format short

%% Question 1
DATA = 0:9;
N_LEVELS = 2;
WAVELET_NAME = 'sym4';
[C, L] = wavedec(DATA, N_LEVELS, WAVELET_NAME);
for n=1:max(1, length(L)-2), disp(n)
    D = wrcoef('d', C, L, WAVELET_NAME, n);
    disp(D)
end


%% Question 2
DATA = 0:17;
N_LEVELS = 4;
WAVELET_NAME = 'sym2';
[C, L] = wavedec(DATA, N_LEVELS, WAVELET_NAME); 
for n=1:max(1, length(L)-2), disp(n)
    D = wrcoef('d', C, L, WAVELET_NAME, n);
    disp(D)
end