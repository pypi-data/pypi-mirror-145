import numpy as np


def pack_data_swap(data):
    s = 60
    s2 = 3
    container = []
    for i in range(int(len(data) / s)):
        arr = np.flip(data[i * s: (i * s) + s])
        for j in range(int(len(arr) / s2)):
            container.append(np.flip(arr[j * s2: (j * s2) + s2]))

    return np.reshape(container, -1)
