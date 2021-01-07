from tdms import read_tdms_to_nparray
# Implementation of matplotlib function
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm

def heatmap_from_tdms(name):
    data = read_tdms_to_nparray(name)
    heatmap = plt.imshow(data)
    plt.colorbar(heatmap)
    return heatmap
