import matplotlib.pyplot as plt
import numpy as np

import image_converter as ic
import fft

# Test 1 - Check 1D forward fast Fourier transform
eps = 1e-7
signal = np.sin(np.linspace(-2 * np.pi, 2 * np.pi, 128))
fft_signal1 = np.fft.fft(signal)
fft_signal2 = fft.fft(signal)

for i in range(len(fft_signal1)):
    assert abs(fft_signal1[i] - fft_signal2[i]) < eps, 'Test 1 - Failed'
print('Tets 1 - OK!')

# Test 2 - Check 1D inverse fast Fourier transform
eps = 1e-7
signal2 = fft.inverse_fft(fft_signal2)

for i in range(len(signal)):
    assert abs(signal2[i] - signal[i]) < eps, 'Test 2 - Failed'
print('Tets 2 - OK!')

#Test 3 - Check 2D fast Fourier transform
signal = np.array([[1, 2], [2, 1]])
fft_signal1 = np.fft.fft2(signal)
fft_signal2, n_x, n_y = fft.fft_2d(signal)

for i in range(len(fft_signal1)):
    for j in range(len(fft_signal1[i])):
        assert abs(fft_signal1[i][j] - fft_signal2[i][j]) < eps, 'Test 3 - Failed'
print('Tets 3 - OK!')

#Visualize 2D fast fourier transform
path_data = 'data/'
images_names = ['grating-1.png', 'grating-2.png', 'grating-3.png', 'stinkbug.png']
n_images = len(images_names)

for i in range(len(images_names)):
    fig, axes = plt.subplots(ncols=2, figsize=(12, 8))
    path_image = path_data + images_names[i]
    image_signal = ic.convert_image_to_hex_array(image_filename=path_image)
    axes[0].imshow(image_signal, cmap='gray')
    fft_image_signal, m, n = fft.fft_2d(image_signal)
    fft_image_signal = fft.fft_shift(fft_image_signal)
    axes[1].imshow(abs(fft_image_signal), cmap='gray')
    axes[1].set_xlim([492, 532])
    axes[1].set_ylim([532, 492])
    plt.savefig('fft-results/fft-results-' + images_names[i], dpi=300)