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

def make_mesh(*data_sets, colors=("white","red","yellow"), edgecolors=('grey',"black"), line=None, fig=None, ax=None):
     # Plot X,Y,Z
    if fig is None:
        fig = plt.figure()
    if ax is None:
        ax = fig.add_subplot(111, projection='3d')
    if line != None:
        ax.plot3D(line[0], line[1], line[2], "black",linewidth="5", alpha=1)
    for i, data in enumerate(data_sets):
        X = data[:,0]
        Y = data[:,1]
        Z = data[:,2]
        ax.plot_trisurf(X, Y, Z, color=colors[i], edgecolors=edgecolors[0], alpha=0.3)
    plt.show()

def generate_circle_array(radius, center, height):
    angles = np.linspace(0, 2*np.pi, 200)
    x = radius * np.cos(angles) + center[0]
    y = radius * np.sin(angles) + center[1]
    z = height * np.ones(x.shape)
    return x, y, z

def filter_and_interp(data, scale, thresh_bot=-0.5, thresh_top=10):
    data_cp = data.copy()
    check_list = []
    for i in range(data.shape[0]):  # cycle through rows
        for j in range(data.shape[1]): # cycle through columns
            if (data[i,j] > thresh_top) or (data[i,j] < thresh_bot):
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
                more_than_thresh_bot = check_list_vals > thresh_bot
                check_list_vals = check_list_vals[more_than_thresh_bot]
                less_than_thresh_top = check_list_vals < thresh_top
                check_list_vals = check_list_vals[less_than_thresh_top]
                
                data[i,j] = np.mean(check_list_vals)
            
            # good_check_list = check_list_vals > 0
            # check_list_vals = check_list_vals[good_check_list]
            # if np.abs(data[i,j]) > scale*np.mean(check_list_vals):
            #     data[i,j] = np.mean(check_list_vals)
                
    return data
            



def make_heatmaps(data1, data2, data3, c1=None, c2=None, c3=None):
    Z1 = data1[:,2]
    Z2 = data2[:,2]
    Z3 = data3[:,2]



    grid_dim = int(np.sqrt(data1.shape[0]))
    Z1 = filter_and_interp(Z1.reshape((grid_dim, grid_dim)), scale=2)
    # print(Z1)
    # for i in range(0):
    #     Z1 = filter_and_interp(Z1, scale=2)
    #     print(Z1)
    Z2 = filter_and_interp(Z2.reshape((grid_dim, grid_dim)), scale=2)
    Z3 = filter_and_interp(Z3.reshape((grid_dim, grid_dim)), scale=2)

    min_val = np.min(np.hstack([Z1, Z2, Z3]))
    max_val = np.max(np.hstack([Z1, Z2, Z3]))

    dims = Z1.shape
    f,(ax1,ax2,ax3, cax) = plt.subplots(1,4,gridspec_kw={'width_ratios': [4,4,4,1], "height_ratios": [1]}) #, gridspec_kw={'width_ratios':[1,1,1,0.08]})
    # ax1.get_shared_y_axes().join(ax2,ax3)

    g1 = sns.heatmap(Z1,cmap="YlGnBu",cbar=False,ax=ax1,square=True, vmin=min_val, vmax=max_val)
    if c1 != None:
        ax1.plot(c1[0]+dims[0]/2, c1[1]+dims[1]/2)
        ax1.plot(dims[0]/2, dims[1]/2,'*k')
    g1.set_ylabel('')
    g1.set_xlabel('')
    g2 = sns.heatmap(Z2,cmap="YlGnBu",cbar=False,ax=ax2,square=True, vmin=min_val, vmax=max_val)
    if c2 != None:
        ax2.plot(c2[0]+dims[0]/2, c2[1]+dims[1]/2)
        ax2.plot(dims[0]/2, dims[1]/2,'*k')
    g2.set_ylabel('')
    g2.set_xlabel('')
    g2.set_yticks([])
    g3 = sns.heatmap(Z3,cmap="YlGnBu",ax=ax3,square=True,cbar_ax=cax,vmin=min_val, vmax=max_val)
    if c3 != None:
        ax3.plot(c3[0]+dims[0]/2, c3[1]+dims[1]/2)
        ax3.plot(dims[0]/2, dims[1]/2,'*k')
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

def plot_line_series(data):
    plt.plot(data[:,0],data[:,2])
    plt.show()
        
def diagonal_slice(data, plot=False, manual_max_trim=None):
    y_start = -100
    x_start = -100
    data_slice = []
    for sample in data[:]:
        if (sample[1] > y_start) and (sample[0] > x_start):
            y_start = sample[1].copy()
            x_start = sample[0].copy()
            data_slice.append(sample)
    data_slice = np.array(data_slice)
    if plot:
        data_slice_plot = data_slice.copy()
        if manual_max_trim != None:
            below_manul_max_idx = data_slice_plot[:,2] < manual_max_trim
            data_slice_plot = data_slice_plot[below_manul_max_idx]
        plt.plot(np.sqrt(data_slice_plot[:,0]**2+data_slice_plot[:,1]**2), data_slice_plot[:,2],'.')
        plt.hlines(0, 0, 10)
        plt.vlines(0, 0, np.max(data_slice_plot[:,2]))
        plt.show()
    return data_slice

def find_sensing_boundary(data_avg, threshold_percent, manual_max_trim=None):
    # data_avg = np.mean(data_slice, axis=1)
    # manually trim out bugged data for the purpose of identifying sensing radius
    data = data_avg.copy()
    if manual_max_trim is not None:
        print(data.shape)
        below_manual_max_idx = data[:,2] < manual_max_trim
        below_manual_max_idx = np.tile(below_manual_max_idx.reshape((np.size(below_manual_max_idx), 1)), (1,6))
        data = data[below_manual_max_idx]
        print(data.shape)
        data = data.reshape((int(data.shape[0]/6),6))
        print(data.shape)
    above_thresh_idx = threshold_percent*np.max(data[:,2]) < data[:,2] 
    above_thresh_idx = np.tile(above_thresh_idx.reshape((np.size(above_thresh_idx), 1)), (1,6))
    data_above_thresh = data[above_thresh_idx]
    data_above_thresh = data_above_thresh.reshape((int(data_above_thresh.shape[0]/6),6))
    radius = (np.sqrt(data_above_thresh[0,0]**2+data_above_thresh[0,1]**2) + np.sqrt(data_above_thresh[-1,0]**2+data_above_thresh[-1,1]**2)) / 2
    height = np.min(data_above_thresh[:,2])
    center_idx = np.argmax(data_above_thresh[:,2])
    return radius, height


if __name__ == "__main__":
    center = (-0.05, -0.03)

    # data_10 = np.load("test_data_multi-sample\DS20_100g_atm-PSI_delta-0.5mm_thick-8mm_single-barometer-16_multi-sample-20.npy")
    # data_10_prep = preprocess(data_10)

    # data_20 = np.load("test_data_multi-sample/DS20_100g_50-PSI_delta-0.5mm_thick-8mm_single-barometer-16_multi-sample-10.npy")
    # data_20_prep = preprocess(data_20)

    data_10 = np.load("test_data_multi-sample\DS20_atm_single_21x21_0.5mm_10-samples_cast-bond_trial1.npy")
    data_10_prep = preprocess(data_10)

    data_20 = np.load("test_data_multi-sample\DS20_25PSI_single_21x21_0.5mm_10-samples_cast-bond_trial1.npy")
    data_20_prep = preprocess(data_20)

    data_30 = np.load("test_data_multi-sample\DS20_50PSI_single_21x21_0.5mm_10-samples_cast-bond_trial1.npy")
    data_30_prep = preprocess(data_30)
   


    # # --------------------------- 
    # data_slice_10 = diagonal_slice(data_10_prep, plot=True)
    # radius_of_sensing_10, height_of_radius_10 = find_sensing_boundary(data_slice_10, 0.05)
    # circle_points_10 = generate_circle_array(radius_of_sensing_10, center, height_of_radius_10)
    # print("radius of sensing: ", radius_of_sensing_10)

    # data_slice_20 = diagonal_slice(data_20_prep, plot=True)
    # radius_of_sensing_20, height_of_radius_20 = find_sensing_boundary(data_slice_20, 0.05, manual_max_trim=4)
    # circle_points_20 = generate_circle_array(radius_of_sensing_20, center, height_of_radius_20)
    # print("radius of sensing: ",radius_of_sensing_20)

    make_heatmaps(data_10_prep, data_20_prep, data_30_prep)
    make_mesh(data_20_prep)    
    
    # # # plt.xlabel("X")
    # X = data_10_prep[:,0]
    # Y = data_10_prep[:,1]
    # make_std_plot([data_10, data_20, data_30], X,Y, num=1)

    
    plt.show()
