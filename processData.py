#!/usr/bin/env python3
 
import numpy as np
import matplotlib.pyplot as plt


def preprocess(data):
    # Normalize pressure fluctuations
    start_pres = data[0,3]
    data[:,2] += start_pres - data[:,3]

    # Shift axes with sensor location as (0,0)
    data[:,0:2] -= 12.46/2

    # Flip y-axis so that direction is consistent with plot
    data = np.flip(data,axis=0)

    # remove any outliers
    outlier_idx = []
    for i in range(data.shape[0]):
        if np.abs(data[i,2]) > 40:
            print("yahoo")
            outlier_idx.append(i)
    data = np.delete(data,outlier_idx,axis=0)
    return data

def make_mesh(data, color="white", edgecolors='grey', fig=None, ax=None):
    X = data[:,0]
    Y = data[:,1]
    Z = data[:,2]

    # Plot X,Y,Z
    if fig is None:
        fig = plt.figure()
    if ax is None:
        ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(X, Y, Z, color=color, edgecolors=edgecolors, alpha=0.5)
    # ax.scatter(X, Y, Z, c='red')
    return fig, ax


if __name__ == "__main__":
    data_lines = open('test_data/DS10_100g_atm_delta-0.5mm_thick-8mm-single.csv').readlines()
    data_atm = np.array([line.strip().split(",") for line in data_lines], dtype=np.float16)

    data_lines = open('test_data/DS10_100g_30PSIG_delta-0.5mm_thick-8mm-single.csv').readlines()
    data_30PSIG = np.array([line.strip().split(",") for line in data_lines], dtype=np.float16)
    
    data_atm = preprocess(data_atm)
    data_30PSIG = preprocess(data_30PSIG)
    
    fig, ax = make_mesh(data_atm)
    fig, ax = make_mesh(data_30PSIG, color="red", edgecolors='black', fig=fig, ax=ax)
    plt.show()