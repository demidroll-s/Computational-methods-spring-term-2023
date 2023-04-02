import matplotlib.pyplot as plt
import numpy as np

def save_image_without_borders(data : np.ndarray, filename : str):
    sizes = np.shape(data)
    height = float(sizes[0])
    width = float(sizes[1])
     
    fig = plt.figure()
    fig.set_size_inches(width / height, 1, forward=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
 
    ax.imshow(abs(data), cmap='gray')
    plt.savefig(filename, dpi=height) 
    plt.close()

#Generate different gratings
x = np.arange(-512, 512, 1)
x_mesh, y_mesh = np.meshgrid(x, x)

#Grating - 1
wavelength = 102.4
angle = 0
grating_1 = np.sin(2 * np.pi * (x_mesh * np.cos(angle) + y_mesh * np.sin(angle)) / wavelength)
save_image_without_borders(grating_1, 'data/grating-1.png')

#Grating - 2
wavelength = 102.4
angle = np.pi / 9
grating_2 = np.sin(2 * np.pi * (x_mesh * np.cos(angle) + y_mesh * np.sin(angle)) / wavelength)
save_image_without_borders(grating_2, 'data/grating-2.png')

#Grating - 3
grating_3 = grating_1 + grating_2
save_image_without_borders(grating_3, 'data/grating-3.png')

#Grating - 4
"""
amplitudes = [0.5, 0.25, 1, 0.75, 1]
wavelengths = [200, 100, 250, 300, 60]
angles = [0, np.pi / 4, np.pi / 9, np.pi / 2, np.pi / 12]

grating_4 = np.zeros(x_mesh.shape)
for amplitude, wavelength, angle in zip(amplitudes, wavelengths, angles):
    grating_4 += amplitude * np.sin(2 * np.pi * (x_mesh * np.cos(angle) + y_mesh * np.sin(angle)) / wavelength)

save_image_without_borders(grating_4, 'data/grating-4.png')
"""