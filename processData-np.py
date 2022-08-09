#!/usr/bin/env python3

from matplotlib import projections
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def process_set(data):
    pressures = data[:,2].copy()
    pressures_no_outliers = remove_outliers(pressures)
    p1 = data[:,3].copy()
    p1_no_outliers = remove_outliers(p1)
    p2 = data[:,4].copy()
    p2_no_outliers = remove_outliers(p2)
    
    data = np.mean(data,axis=0)
    data[2] = np.mean(pressures_no_outliers)
    data[3] = np.mean(p1_no_outliers)
    data[4] = np.mean(p2_no_outliers)
    return data

def remove_outliers(data):
    mean = np.mean(data)
    standard_deviation = np.std(data)
    distance_from_mean = abs(data - mean)
    max_deviations = 1
    not_outlier = distance_from_mean < max_deviations * standard_deviation
    no_outliers = data[not_outlier]
    return no_outliers

def preprocess(bad_data):
    print('===========================================================================')
    bad_data[:,:,2] = bad_data[:,:,2].copy() - bad_data[:,:,3].copy()
    data = np.zeros((bad_data.shape[0],bad_data.shape[2]))
    for i, set in enumerate(bad_data[:]):
        data[i,:] = process_set(set)
    print('--------------------------------------------------------------')
    # data[:,0:2] -= 8/2
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

def make_mesh(*data_sets, colors=("white","red","yellow"), edgecolors=('grey',"black"), fig=None, ax=None):
     # Plot X,Y,Z
    if fig is None:
        fig = plt.figure()
    if ax is None:
        ax = fig.add_subplot(111, projection='3d')
    
    for i, data in enumerate(data_sets):
        X = data[:,0]
        Y = data[:,1]
        Z = data[:,2]
        ax.plot_trisurf(X, Y, Z, color=colors[i], edgecolors=edgecolors[1], alpha=0.5)
    plt.show()

def make_heatmaps(data1, data2, data3):
    Z1 = data1[:,2]
    Z2 = data2[:,2]
    Z3 = data3[:,2]

    min_val = np.min(np.hstack([Z1, Z2, Z3]))
    max_val = np.max(np.hstack([Z1, Z2, Z3]))

    print(min_val)
    print(max_val) 

    grid_dim = int(np.sqrt(data1.shape[0]))
    Z1 = Z1.reshape((grid_dim, grid_dim))
    Z2 = Z2.reshape((grid_dim, grid_dim))
    Z3 = Z3.reshape((grid_dim, grid_dim))

    f,(ax1,ax2,ax3, cax) = plt.subplots(1,4,gridspec_kw={'width_ratios': [4,4,4,1], "height_ratios": [1]}) #, gridspec_kw={'width_ratios':[1,1,1,0.08]})
    # ax1.get_shared_y_axes().join(ax2,ax3)

    g1 = sns.heatmap(Z1,cmap="YlGnBu",cbar=False,ax=ax1,square=True, vmin=min_val, vmax=max_val)
    g1.set_ylabel('')
    g1.set_xlabel('')
    g2 = sns.heatmap(Z2,cmap="YlGnBu",cbar=False,ax=ax2,square=True, vmin=min_val, vmax=max_val)
    g2.set_ylabel('')
    g2.set_xlabel('')
    g2.set_yticks([])
    g3 = sns.heatmap(Z3,cmap="YlGnBu",ax=ax3,square=True,cbar_ax=cax,vmin=min_val, vmax=max_val)
    g3.set_ylabel('')
    g3.set_xlabel('')
    g3.set_yticks([])

    # may be needed to rotate the ticklabels correctly:
    for ax in [g1,g2,g3]:
        tl = ax.get_xticklabels()
        ax.set_xticklabels(tl, rotation=90)
        tly = ax.get_yticklabels()
        ax.set_yticklabels(tly, rotation=0)
    plt.show()

def make_std_plot(unprocessed_data_sets, X, Y, num=3):
    fig = plt.figure()
    ax = fig.add_subplot(111,projection="3d")
    for data in unprocessed_data_sets[0:num]:
        stds = np.std(data, axis=1)
        Z = stds[:,2]
        ax.plot_trisurf(X, Y, Z, color="white", edgecolors="black", alpha=0.5)
    plt.show()
        
        

if __name__ == "__main__":
    data_10 = np.load("test_data_multi-sample/DS20_100g_atm-PSI_delta-0.5mm_thick-8mm_single-barometer-16_multi-sample-20.npy")
    data_10_prep = preprocess(data_10)

    # data_20 = np.load("test_data_multi-sample/DS20_100g_atm-PSI_delta-0.5mm_thick-8mm_single-barometer-10_multi-sample-5.npy")
    # data_20_prep = preprocess(data_20)

    # data_30 = np.load("test_data_multi-sample/DS30_100g_atm-PSI_delta-0.5mm_thick-8mm_single-barometer-17_multi-sample-50.npy")
    # data_30_prep = preprocess(data_30)
   

    # ---------------------------
    make_heatmaps(data_10_prep, data_10_prep, data_10_prep)
    make_mesh(data_10_prep)#, data_20_prep)
    # plt.xlabel("X")
    X = data_10_prep[:,0]
    Y = data_10_prep[:,1]
    # make_std_plot([data_10, data_20, data_30], X,Y, num=1)

    
    plt.show()
