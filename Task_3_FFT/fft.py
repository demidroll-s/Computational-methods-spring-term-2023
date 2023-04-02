import numpy as np
from math import log, ceil

import image_converter as ic

def phase_factor(n : int, m : int):
    return np.exp(2.0 * np.pi * 1j * m / n)

def padding(signal : np.ndarray):
   """
   Padding the 1D array to next nearest power of two
   """
   pow = 0
   while 2**pow < len(signal):
      pow += 1
   return np.concatenate((signal, np.zeros_like(shape=(signal - 2**pow))))

def fft(signal : np.ndarray):
    """
    Implements Fast Fourier Transform for 1D signal
    """
    n = np.shape(signal)[0]
    if n == 1:
        return signal
    
    fft_even, fft_odd = fft(signal[0::2]), fft(signal[1::2])
    fft_result = np.full(shape=np.shape(signal), fill_value=complex(0, 0))

    for m in range(n // 2):
        fft_result[m] = fft_even[m] + phase_factor(n, -m) * fft_odd[m]
        fft_result[m + n // 2] = fft_even[m] - phase_factor(n, -m) * fft_odd[m]

    return fft_result

def inverse_fft(fft_signal : np.ndarray):
    """
    Implements Inversed Fast Fourier Transform for 1D signal
    """
    fft_signal_conj = [np.conjugate(val)  for val in fft_signal] 
    signal = fft(fft_signal_conj) 
    signal = [np.conjugate(val) / len(fft_signal) for val in signal]
    return np.array(signal)

"""
def padding_2d(signal : np.ndarray):
    '''
    Scales 2D array for dimensions 
    that are powers of two
    '''
    n_x, n_y = np.shape(signal)
    n_x_logscale = 2**int(np.ceil(np.log2(n_x))) 
    n_y_logscale = 2**int(np.ceil(np.log2(n_y)))
    template = np.zeros(shape=(n_x_logscale, n_y_logscale), dtype=signal.dtype)
    template[0:n_x, 0:n_y] = signal
    return template, n_x, n_y

def fft_2d(signal : np.ndarray):
    '''
    Implements Fast Fourier Transform for 2D signal
    '''
    template, n_x, n_y = padding_2d(signal)
    fft_xaxis = fft(template)
    fft_yaxis = fft(np.transpose(fft_xaxis))
    return np.transpose(fft_yaxis), n_x, n_y
"""

def pad2(x):
   m, n = np.shape(x)
   M, N = 2 ** int(ceil(log(m, 2))), 2 ** int(ceil(log(n, 2)))
   F = np.zeros((M,N), dtype = x.dtype)
   F[0:m, 0:n] = x
   return F, m, n

def fft_2d(f):
   '''FFT of 2-d signals/images with padding
   usage X, m, n = fft2(x), where m and n are dimensions of original signal'''

   f, m, n = pad2(f)
   return np.transpose(fft(np.transpose(fft(f)))), m, n

def inverse_fft_2d(fft_signal : np.ndarray, n_x : int, n_y : int):
    """
    Implements Inversed Fast Fourier Transform for 2D signal
    """
    signal, n_fft_x, n_fft_y = fft_2d(np.conj(fft_signal))
    signal = np.array(np.real(np.conj(signal))) / (n_fft_x * n_fft_y)
    return signal[0:n_x, 0:n_y]

def fft_shift(fft_signal : np.ndarray):
   """
   Shifts the centre of FFT of 2D signals
   """
   n_fft_x, n_fft_y = fft_signal.shape
   R1, R2 = fft_signal[0 : n_fft_x // 2, 0 : n_fft_y // 2], \
            fft_signal[n_fft_x // 2 : n_fft_x, 0 : n_fft_y // 2]
   R3, R4 = fft_signal[0 : n_fft_x // 2, n_fft_y // 2 : n_fft_y], \
            fft_signal[n_fft_x // 2 : n_fft_x, n_fft_y // 2 : n_fft_y]
   shifted_fft = np.zeros(shape = fft_signal.shape, dtype = fft_signal.dtype)
   shifted_fft[n_fft_x // 2 : n_fft_x, n_fft_y // 2 : n_fft_y], \
    shifted_fft[0 : n_fft_x // 2, 0 : n_fft_y // 2] = R1, R4
   shifted_fft[n_fft_x // 2 : n_fft_x, 0 : n_fft_y // 2], \
    shifted_fft[0 : n_fft_x // 2, n_fft_y // 2 : n_fft_y] = R3, R2
   
   return shifted_fft

