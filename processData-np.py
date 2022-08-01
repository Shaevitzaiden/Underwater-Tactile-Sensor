#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

def preprocess(data):
    print('===========================================================================')
    data[:,:,2] = data[:,:,2] #- data[:,:,3]
    
    print('--------------------------------------------------------------')

    # Average all samples at the location
    data = np.mean(data, axis=1)
    print(data)
    # Shift axes with sensor location as (0,0)
    data[:,0:2] -= 15/2
    # # Flip y-axis so that direction is consistent with plot
    data = np.flip(data,axis=0)

    # remove any outliers --- should maybe move above so it removes unaveraged outlier points
    outlier_idx = []
    for i in range(data.shape[0]):
        if np.abs(data[i,2]) > 40:
            print("removing outlier")
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
    data = np.load("test_data_multi-sample/DS10_100g_atm-PSI_delta-0.5mm_thick-8mm_single-barometer_multi-sample.npy")
    data = preprocess(data)
    # data_lines = open('test_data/DS10_100g_atm_delta-0.5mm_thick-8mm-single.csv').readlines()
    # data_DS10_atm = np.array([line.strip().split(",") for line in data_lines], dtype=np.float16)

    # data_lines = open('test_data/DS20_100g_atm_delta-0.5mm_thick-8mm-single.csv').readlines()
    # data_DS20_atm = np.array([line.strip().split(",") for line in data_lines], dtype=np.float16)

    # data_lines = open('test_data/DS10_100g_30PSIG_delta-0.5mm_thick-8mm-single.csv').readlines()
    # data_DS10_30PSIG = np.array([line.strip().split(",") for line in data_lines], dtype=np.float16)
    
    # data_lines = open('test_data/DS20_100g_30PSIG_delta-0.5mm_thick-8mm-single.csv').readlines()
    # data_DS20_30PSIG = np.array([line.strip().split(",") for line in data_lines], dtype=np.float16)

    # data_lines = open('test_data/DS30_100g_30PSIG_delta-0.5mm_thick-8mm-single.csv').readlines()
    # data_DS30_30PSIG = np.array([line.strip().split(",") for line in data_lines], dtype=np.float16)

    # data_DS10_atm = preprocess(data_DS10_atm)
    # data_DS10_30PSIG = preprocess(data_DS10_30PSIG)
    # data_DS20_30PSIG = preprocess(data_DS20_30PSIG)
    # data_DS20_atm = preprocess(data_DS20_atm)

    fig, ax = make_mesh(data)
    plt.xlabel("X")
    # fig, ax = make_mesh(data_DS20_30PSIG, color="orange", edgecolors='blue', fig=fig, ax=ax)

    # # fig, ax = make_mesh(data_DS10_30PSIG, color="red", edgecolors='black', fig=fig, ax=ax)
    # # fig, ax = make_mesh(data_DS20_30PSIG, color="orange", edgecolors='blue', fig=fig, ax=ax)
    # # fig, ax = make_mesh(data_DS30_30PSIG, color="yellow", edgecolors='purple', fig=fig, ax=ax)
    # # ax.scatter(0,0,1,s=100)
    plt.show()
