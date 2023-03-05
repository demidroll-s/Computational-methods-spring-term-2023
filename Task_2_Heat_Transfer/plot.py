import numpy as np
import matplotlib.pyplot as plt

size_x = 200
size_time = int(1e3)

time = np.zeros(shape=(size_time + 1))
u = np.zeros(shape=(size_time + 1, size_x + 1))

def read_data(filename : str):
    time = np.zeros(shape=(size_time + 1))
    u = np.zeros(shape=(size_time + 1, size_x + 1))
    
    n = 0

    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines:
        if (line[0:6] == "TIME ="):
            data = line.split()
            timestep = float(data[-1])
            time[n] = timestep
        elif (line[0:5] == "-----" or line == ""):
            continue
        else:
            data = line.split()
            for m, s in enumerate(data):
                val = float(s)
                u[n][m] = val
            n += 1
    return time, u

time, u = read_data('data/implicit_solution.txt')

fig, ax = plt.subplots(figsize=(12, 8))

ax.plot(range(0, size_x + 1), u[1, :], color='red', label='Exact solution')

ax.legend(loc='upper right')
plt.savefig('result.png', dpi=300)