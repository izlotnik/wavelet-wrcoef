%% Stackoverflow questions
% https://stackoverflow.com/questions/45051106/multilevel-partial-wavelet-reconstruction-with-pywavelets/47591523#47591523
% and
% https://dsp.stackexchange.com/questions/42358/multilevel-partial-wavelet-reconstruction-with-pywavelets/42372


%% Question 1
DATA = 0:9;
N_LEVELS = 2;
WAVELET_NAME = 'db4';
[C, L] = wavedec(DATA, N_LEVELS, WAVELET_NAME);
% A2 = wrcoef('a', C, L, WAVELET_NAME, 2)
D2 = wrcoef('d', C, L, WAVELET_NAME, 2);
D1 = wrcoef('d', C, L, WAVELET_NAME, 1);
D2, D1


%% Question 2
% level = 4
% X = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
% coeffs = pywt.wavedec(X, 'db1', level=level)
% A4 = wrcoef(X, 'a', coeffs, 'db1', level)
% D4 = wrcoef(X, 'd', coeffs, 'db1', level)
% D3 = wrcoef(X, 'd', coeffs, 'db1', 3)
% D2 = wrcoef(X, 'd', coeffs, 'db1', 2)
% D1 = wrcoef(X, 'd', coeffs, 'db1', 1)
% print A4 + D4 + D3 + D2 + D1
DATA = 0:17;
N_LEVELS = 4;
WAVELET_NAME = 'db1';
[C, L] = wavedec(DATA, N_LEVELS, WAVELET_NAME); 
% A4 = wrcoef('a', C, L, WAVELET_NAME, N_LEVELS);
D4 = wrcoef('d', C, L, WAVELET_NAME, N_LEVELS);
D3 = wrcoef('d', C, L, WAVELET_NAME, 3);
D2 = wrcoef('d', C, L, WAVELET_NAME, 2);
D1 = wrcoef('d', C, L, WAVELET_NAME, 1);

D4, D3, D2, D1