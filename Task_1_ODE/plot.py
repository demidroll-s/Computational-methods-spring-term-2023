import numpy as np
import matplotlib.pyplot as plt

x = []
y_euler = []
y_hoine = []
y_runge = []

def read_data(filename : str):
    x = []
    y = []
    
    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines:
        data = line.split()
        x.append(float(data[0]))
        y.append(float(data[1]))

    return x, y

x, y_exact = read_data('data/data_exact.txt')
x, y_euler = read_data('data/data_euler.txt')
x, y_hoine = read_data('data/data_hoine.txt')
x, y_runge = read_data('data/data_runge.txt')

fig, ax = plt.subplots(figsize=(12, 8))

ax.plot(x, y_exact, color='red', label='Exact solution')
ax.plot(x, y_euler, color='orange', label='Euler method')
ax.plot(x, y_hoine, color='green', label='Hoine method')
ax.plot(x, y_runge, color='darkblue', label='Runge-Kutta method')

ax.legend(loc='upper right')
plt.savefig('result.png', dpi=300)