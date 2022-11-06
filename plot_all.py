#!/usr/bin/env python3

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

def preprocess(data):
    bad_data = data.copy()
    bad_data[:,:,2] = bad_data[:,:,2].copy() - bad_data[:,:,3].copy()
    data = np.zeros((bad_data.shape[0],bad_data.shape[2]))
    for i, set in enumerate(bad_data[:]):
        data[i,:] = process_set(set)
    # data = np.flip(data,axis=0)
    return data

def make_mesh(*data_sets, colors=("white","red","yellow"), edgecolors=("white", "red", "yellow"), line=None, fig=None, ax=None, slice=False):
    # Plot X,Y,Z
    print(data_sets)
    if slice:
        data = []
        for d in data_sets:
            dim = d.shape[0]
            data.append(d[:(int(dim/2)+10),:])
    else:
        data = data_sets
    if fig is None:
        fig = plt.figure()
    if ax is None:
        ax = fig.add_subplot(111, projection='3d')
    if line != None:
        ax.plot3D(line[0], line[1], line[2], "black",linewidth="5", alpha=1)
    for i, d in enumerate(data):
        X = d[:,0]
        Y = d[:,1]
        Z = d[:,2]
        ax.plot_trisurf(X, Y, Z, alpha=0.95)
    ax.view_init(4,20)
    ax.set_axis_off()
    plt.savefig("meshes.png", transparent=True)
    plt.show()

def make_mesh2(*data_sets, colors=("white","red","yellow"), edgecolors=('grey',"black"), line=None, fig=None, ax=None, slice=False):
    # Plot X,Y,Z
    print(data_sets)
    if slice:
        data = []
        for d in data_sets:
            dim = d.shape[0]
            data.append(d[:(int(dim/2)),:])
    else:
        data = data_sets.copy()
    if fig is None:
        fig = plt.figure()
    if ax is None:
        ax = fig.add_subplot(111, projection='3d')
    if line != None:
        ax.plot3D(line[0], line[1], line[2], "black",linewidth="5", alpha=1)
    for i, d in enumerate(data):
        xd, yd = d.shape
        X = np.tile(np.arange(yd), (xd,1))
        Y = X
        Z = d
        print(X.shape, Y.shape, Z.shape)
        ax.plot_surface(X, Y, Z)

    plt.show()

def filter_and_interp(data, scale, thresh_bot=-0.5, thresh_top=1):
    data_cp = data.copy()
    check_list = []
    for i in range(data.shape[0]):  # cycle through rows
        for j in range(data.shape[1]): # cycle through columns
            if (i == 0) and (j == 0): # Top left corner
                check_list = [(i,j+1), (i+1,j+1), (i+1,j)]
            elif (i == data.shape[0]-1) and (j == data.shape[1]-1): # Bottom right corner
                check_list = [(i,j-1), (i-1,j), (i-1,j-1)]
            elif (i == 0) and (j == data.shape[1]-1): # Top right corner
                check_list = [(i,j-1), (i+1,j), (i+1,j-1)]
            elif (i == data.shape[0]-1) and (j == 0): # Bottom left corner
                check_list = [(i,j+1), (i-1,j), (i-1,j+1)]
            elif i == 0: # Top
                check_list = [(i,j-1), (i,j+1), (i+1,j), (i+1,j-1), (i+1,j+1)]
            elif j == 0: # Left
                check_list = [(i-1,j), (i+1,j), (i,j+1), (i-1,j+1), (i+1,j+1)]
            elif i == (data.shape[0]-1): # bottom
                check_list = [(i,j-1), (i,j+1), (i-1,j), (i-1,j-1), (i-1,j+1)]
            elif j == (data.shape[1]-1): # right
                check_list = [(i-1,j), (i+1,j), (i,j-1), (i-1,j-1), (i+1,j-1)]
            else: # Anywhere in the middle
                check_list = [(i-1,j-1), (i-1,j), (i-1,j+1), (i,j-1), (i,j+1), (i+1,j-1), (i+1,j), (i+1,j+1)]
            
            check_list_vals = np.array([data[idx[0],idx[1]] for idx in check_list])
            if (data[i,j] > thresh_top) or (data[i,j] < thresh_bot):    
                more_than_thresh_bot = check_list_vals > thresh_bot
                check_list_vals = check_list_vals[more_than_thresh_bot]
                less_than_thresh_top = check_list_vals < thresh_top
                check_list_vals = check_list_vals[less_than_thresh_top]
                
                data[i,j] = np.mean(check_list_vals)

    
            
            check_vals_gt = (data[i,j] - np.abs(check_list_vals)) > scale
            if np.any(check_vals_gt):
                data[i,j] = np.mean(check_list_vals[check_vals_gt])

           
          
            # good_check_list = check_list_vals > 0
            # check_list_vals = check_list_vals[good_check_list]
            # if np.abs(data[i,j]) > scale*np.mean(check_list_vals):
            #     data[i,j] = np.mean(check_list_vals)
                
    return data          

def make_heatmaps(data1, data2, data3, d4, d5, d6, c1=None, c2=None, c3=None):
    Z1 = data1[:,2]
    Z2 = data2[:,2]
    Z3 = data3[:,2]
    Z4 = d4[:,2]
    Z5 = d5[:,2]
    Z6 = d6[:,2]

    grid_phys_dims_x = (np.min(data1[:,0]), np.max(data1[:,0]))
    grid_phys_dims_y = (np.min(data1[:,1]), np.max(data1[:,1]))
    grid_dim = int(np.sqrt(data1.shape[0]))
    Z1 = filter_and_interp(Z1.reshape((grid_dim, grid_dim)), scale=5)
    Z2 = filter_and_interp(Z2.reshape((grid_dim, grid_dim)), scale=5)
    Z3 = filter_and_interp(Z3.reshape((grid_dim, grid_dim)), scale=5, thresh_top=1.4)
    ds10_atm_max = np.max(Z1)
    ds10_50_max = np.max(Z3)

    Z4 = filter_and_interp(Z4.reshape((grid_dim, grid_dim)), scale=2, thresh_top=6)
    Z5 = filter_and_interp(Z5.reshape((grid_dim, grid_dim)), scale=2, thresh_top=5)
    Z6 = filter_and_interp(Z6.reshape((grid_dim, grid_dim)), scale=1.5, thresh_top=5)
    ds20_atm_max = np.max(Z4)
    ds20_50_max = np.max(Z6)

    # print(ds10_atm_max, ds10_50_max, (ds10_50_max-ds10_atm_max)/ds10_atm_max)
    # print(ds20_atm_max, ds20_50_max, (ds20_50_max-ds20_atm_max)/ds20_atm_max)
    min_val1 = np.min(np.hstack([Z1, Z2, Z3]))
    max_val1 = np.max(np.hstack([Z1, Z2, Z3]))

    min_val2 = np.min(np.hstack([Z4, Z5, Z6]))
    max_val2 = np.max(np.hstack([Z4, Z5, Z6]))

    dims = Z1.shape

    fig = plt.figure()
    gs = fig.add_gridspec(2,4, width_ratios=[1,1,1,0.1], height_ratios=[1,1])
    ax1 = fig.add_subplot(gs[0,0])
    ax2 = fig.add_subplot(gs[0,1])
    ax3 = fig.add_subplot(gs[0,2])
    ax4 = fig.add_subplot(gs[1,0])
    ax5 = fig.add_subplot(gs[1,1])
    ax6 = fig.add_subplot(gs[1,2])
    cax1 = fig.add_subplot(gs[0,3])
    cax2 = fig.add_subplot(gs[1,3])

    # f,(ax1,ax2,ax3, cax) = plt.subplots(2,4,gridspec_kw={'width_ratios': [4,4,4,1], "height_ratios": [1]})
    # # ax1.get_shared_y_axes().join(ax2,ax3)
    c = "Spectral"
    lp = 7
    fs = 12

    g1 = sns.heatmap(Z1,cmap=c,cbar=False,ax=ax1,square=True, vmin=min_val1, vmax=max_val1)
    g1.set_ylabel('Dragonskin 10', labelpad=lp, fontsize=fs)
    g1.set_xlabel('a', fontsize=5)
    g1.xaxis.set_label_position('top')
    g1.xaxis.label.set_color('white')
    g1.set_title('Atm', fontsize=fs)
    
    tick_locs = np.arange(0, grid_dim, 10)
    tick_vals = np.linspace(0, grid_phys_dims_y[1]-grid_phys_dims_y[0], num=(np.size(tick_locs))).round(0).astype(np.int16)
    g1.set_yticks(tick_locs)
    g1.set_yticklabels(tick_vals)

    tick_locs_x = np.arange(0, grid_dim, 10)
    tick_vals_x = np.linspace(0, grid_phys_dims_x[1]-grid_phys_dims_x[0], num=(np.size(tick_locs_x))).round(0).astype(np.int16)
    g1.set_xticks(tick_locs_x)
    g1.set_xticklabels(tick_vals_x)
    
    g2 = sns.heatmap(Z2,cmap=c,cbar=False,ax=ax2,square=True, vmin=min_val1, vmax=max_val1)
    g2.set_xlabel('a', fontsize=5)
    g2.xaxis.set_label_position('top')
    g2.xaxis.label.set_color('white')
    g2.set_title('25 PSIG', fontsize=fs)
    g2.set_yticks([])
    g2.set_xticks(tick_locs_x)
    g2.set_xticklabels(tick_vals_x)

    g3 = sns.heatmap(Z3,cmap=c,ax=ax3,square=True,cbar_ax=cax1,vmin=min_val1, vmax=max_val1)
    g3.set_ylabel('')
    g3.set_xlabel('a', fontsize=5)
    g3.xaxis.set_label_position('top')
    g3.xaxis.label.set_color('white')
    g3.set_title('50 PSIG', fontsize=fs)
    g3.set_yticks([])
    g3.set_xticks(tick_locs_x)
    g3.set_xticklabels(tick_vals_x)

    g4 = sns.heatmap(Z4,cmap=c,cbar=False,ax=ax4,square=True,vmin=min_val2, vmax=max_val2)
    g4.set_ylabel('Dragonskin 20', labelpad=lp, fontsize=fs)
    g4.set_xlabel('')
    g4.set_yticks(tick_locs)
    g4.set_yticklabels(tick_vals)
    g4.set_xticks(tick_locs_x)
    g4.set_xticklabels(tick_vals_x)

    g5 = sns.heatmap(Z5,cmap=c,cbar=False,ax=ax5,square=True,vmin=min_val2, vmax=max_val2)
    g5.set_ylabel('')
    g5.set_xlabel('')
    g5.set_yticks([])
    g5.set_xticks(tick_locs_x)
    g5.set_xticklabels(tick_vals_x)

    g6 = sns.heatmap(Z6,cmap=c,ax=ax6,square=True,cbar_ax=cax2,vmin=min_val2, vmax=max_val2)
    g6.set_ylabel('')
    g6.set_xlabel('')
    g6.set_yticks([])
    g6.set_xticks(tick_locs_x)
    g6.set_xticklabels(tick_vals_x)


    plt.tight_layout()
    plt.show()

    return (Z1, Z2, Z3, Z4, Z5, Z6)



if __name__ == "__main__":
    center = (-0.05, -0.03)

    data_10_atm = np.load("test_data_multi-sample\DS10_atm_single_21x21_0.5mm_10-samples_cast-bond_trial1.npy")
    data_10_atm_prep = preprocess(data_10_atm)

    data_10_25 = np.load("test_data_multi-sample\DS10_25PSI_single_21x21_0.5mm_10-samples_cast-bond_trial3.npy")
    data_10_25_prep = preprocess(data_10_25)

    data_10_50 = np.load("test_data_multi-sample\DS10_50PSI_single_21x21_0.5mm_10-samples_cast-bond_trial2.npy")
    data_10_50_prep = preprocess(data_10_50)
   
    data_20_atm = np.load("test_data_multi-sample\DS20_atm_single_21x21_0.5mm_10-samples_cast-bond_trial1.npy")
    data_20_atm_prep = preprocess(data_20_atm)

    data_20_25 = np.load("test_data_multi-sample\DS20_25PSI_single_21x21_0.5mm_10-samples_cast-bond_trial1.npy")
    data_20_25_prep = preprocess(data_20_25)

    data_20_50 = np.load("test_data_multi-sample\DS20_50PSI_single_21x21_0.5mm_10-samples_cast-bond_trial1.npy")
    data_20_50_prep = preprocess(data_20_50)

    print(data_10_50_prep.shape)

    Z = make_heatmaps(data_10_atm_prep, data_10_25_prep, data_10_50_prep, data_20_atm_prep, data_20_25_prep, data_20_50_prep)
    # make_mesh(data_10_atm_prep, data_10_25_prep, data_10_50_prep)   
    # make_mesh(data_10_atm_prep, slice=True)   
    
    # make_mesh2(Z[1], Z[2], Z[3], slice=True)    
    
    # plt.xlabel("X")
    # X = data_10_prep[:,0]
    # Y = data_10_prep[:,1]
    # make_std_plot([data_10, data_20, data_30], X,Y, num=1)

    
    plt.show()
