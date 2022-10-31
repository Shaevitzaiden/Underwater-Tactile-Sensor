import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def process_set(data, hard_cutoff, mesh):
    pressures = data[:,2:10].copy()
    pressures_no_outliers = np.zeros((8,))
    for i in range(8):
        pressures_no_outliers[i] = np.mean(remove_outliers(pressures[:,i], hard_cutoff))
    if mesh:
        return np.array([data[0,0], data[0,1], np.max(pressures_no_outliers)])
    else:
        p = pressures_no_outliers
        return np.array([data[0,0], data[0,1], p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7]])

def remove_outliers(data, hard_cutoff):
    if hard_cutoff is not None and (data>hard_cutoff).any():
        not_outlier = data < hard_cutoff
        data = data[not_outlier]
    mean = np.mean(data)
    standard_deviation = np.std(data)
    distance_from_mean = abs(data - mean)
    max_deviations = 1
    not_outlier = distance_from_mean < max_deviations * standard_deviation
    no_outliers = data[not_outlier]
    return no_outliers

def preprocess1(data, hard_cutoff=None, mesh=True):
    bad_data = data.copy()
    bad_data[:,:,2:10] = bad_data[:,:,2:10].copy() - bad_data[:,:,10:18].copy()
    if mesh:
        data = np.zeros((bad_data.shape[0], 3))
    else:
        data = np.zeros((bad_data.shape[0], 10))
    for i, set in enumerate(bad_data[:]):
        data[i,:] = process_set(set, hard_cutoff, mesh)
    # data = np.flip(data,axis=0)
    return data

def preprocess_mesh(data):
    data_delta = data.copy()
    data_delta[:,:,2:10] = data_delta[:,:,2:10].copy() - data_delta[:,:,10:18].copy()
    data_delta = np.mean(data_delta, axis=1)
    data_max_delta = np.array([data_delta[:,0], data_delta[:,1], np.max(data_delta[:,2:10],axis=1)]).T
    return data_max_delta

def make_mesh(*data_sets, colors=("white","red","yellow"), edgecolors=('grey',"black"), line=None, fig=None, ax=None, pre=False):
     # Plot X,Y,Z
    if fig is None:
        fig = plt.figure()
    if ax is None:
        ax = fig.add_subplot(111, projection='3d')
    if line != None:
        ax.plot3D(line[0], line[1], line[2], "black", linewidth="5", alpha=1)
    for i, data in enumerate(data_sets):
        X = data[:,0]
        Y = data[:,1]
        if pre:
            Z = np.max(data[:,2:],axis=1)
        else:
            Z = data[:,2]
        ax.plot_trisurf(X, Y, Z, color=colors[i], edgecolors=edgecolors[0], alpha=0.3)
    plt.show()

def filter_and_interp(data, thresh, thresh_bot=-0.5, thresh_top=1):
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

            while np.abs(data[i,j] - np.mean(check_list_vals)) > thresh:
                data[i,j] = np.mean(check_list_vals)
                
    return data

def make_heatmaps(data1, pre_filtered=False):
    if not pre_filtered:
        Z1 = data1[:,2]

        # find the dimensions for x and y by adding vals to a set
        x_set = set()
        y_set = set()
        for x, y in data1[:,0:2]:
            x_set.add(x)
            y_set.add(y)
        x_dim = len(x_set)
        y_dim = len(y_set)

        Z1 = filter_and_interp(Z1.reshape((y_dim, x_dim)), 5, thresh_bot=-0.5, thresh_top=4)
    else:
        Z1 = np.max(data1[:,2:], axis=1)
        print(Z1)
        print(Z1.shape)
        x_set = set()
        y_set = set()
        for x, y in data1[:,0:2]:
            x_set.add(x)
            y_set.add(y)
        x_dim = len(x_set)
        y_dim = len(y_set)
        Z1 = Z1.reshape((y_dim,x_dim))


    min_val = np.min(Z1)
    max_val = np.max(Z1)
   
    f, ax1 = plt.subplots()
    pos = ax1.imshow(Z1, cmap='Spectral')
    f.colorbar(pos, ax=ax1)
    ax1.set_xlabel('mm')
    ax1.set_ylabel('mm')
    
    # Make tick spacing
    # xt = np.arange()
    # ax1.set_xticks()

    plt.show()

def make_heatmaps_multi(data_sets_pre):
    data_sets = []
    dims = []
    mms = []
    for i, d in enumerate(data_sets_pre):
        Z = np.max(d[:,2:], axis=1)
        x_set = set()
        y_set = set()
        for x, y in d[:,0:2]:
            x_set.add(x)
            y_set.add(y)
        x_dim = len(x_set)
        y_dim = len(y_set)
        dims.append((x_dim, y_dim))
        mms.append((min(y_set), max(y_set), min(x_set), max(x_set)))
        data_sets.append(Z.reshape((y_dim,x_dim)))

    
    min_val1 = np.min(np.hstack(data_sets[:3]))
    max_val1 = np.max(np.hstack(data_sets[:3]))
    print(max_val1)

    min_val2 = np.min(np.hstack(data_sets[3:]))
    max_val2 = np.max(np.hstack(data_sets[3:]))
    print(max_val2)

    # dims = data.shape

    fig = plt.figure()
    gs = fig.add_gridspec(2,4, width_ratios=[1,1,1,0.1], height_ratios=[dims[0][1], dims[3][1]])
    ax1 = fig.add_subplot(gs[0,0])
    ax2 = fig.add_subplot(gs[0,1])
    ax3 = fig.add_subplot(gs[0,2])
    ax4 = fig.add_subplot(gs[1,0])
    ax5 = fig.add_subplot(gs[1,1])
    ax6 = fig.add_subplot(gs[1,2])
    cax1 = fig.add_subplot(gs[0:2,3])
    # cax2 = fig.add_subplot(gs[1,3])

    c = "Spectral"
    lp = 7
    fs = 12

    g1 = sns.heatmap(data_sets[0],cmap=c,cbar=False,ax=ax1,square=True, vmin=min_val1, vmax=max_val2)
    g1.set_ylabel('Dragonskin 10', labelpad=lp, fontsize=fs)
    g1.set_xlabel('a', fontsize=5)
    g1.xaxis.set_label_position('top')
    g1.xaxis.label.set_color('white')
    g1.set_title('Atm', fontsize=fs)
    
    tick_locs = np.arange(0, dims[0][1], 10)
    tick_vals = np.linspace(0, mms[0][1]-mms[0][0], num=(np.size(tick_locs))).round(0).astype(np.int16)
    g1.set_yticks(tick_locs)
    g1.set_yticklabels(tick_vals)

    tick_locs_x = np.arange(0, dims[0][0], 10)
    tick_vals_x = np.linspace(0, mms[0][3]-mms[0][2], num=(np.size(tick_locs_x))).round(0).astype(np.int16)
    g1.set_xticks(tick_locs_x)
    g1.set_xticklabels(tick_vals_x)
    
    g2 = sns.heatmap(data_sets[1],cmap=c,cbar=False,ax=ax2,square=True, vmin=min_val1, vmax=max_val2)
    g2.set_ylabel('')
    g2.set_xlabel('a', fontsize=5)
    g2.xaxis.set_label_position('top')
    g2.xaxis.label.set_color('white')
    g2.set_title('25 PSIG', fontsize=fs)
    g2.set_yticks([])
    g2.set_xticks(tick_locs_x)
    g2.set_xticklabels(tick_vals_x)

    g3 = sns.heatmap(data_sets[2],cmap=c,ax=ax3,square=True,cbar=False,vmin=min_val1, vmax=max_val2)
    g3.set_ylabel('')
    g3.set_xlabel('a', fontsize=5)
    g3.xaxis.set_label_position('top')
    g3.xaxis.label.set_color('white')
    g3.set_title('50 PSIG', fontsize=fs)
    g3.set_yticks([])
    g3.set_xticks(tick_locs_x)
    g3.set_xticklabels(tick_vals_x)

    g4 = sns.heatmap(data_sets[3],cmap=c,cbar=False,ax=ax4,square=True,vmin=min_val1, vmax=max_val2)
    g4.set_ylabel('Dragonskin 20', labelpad=lp, fontsize=fs)
    g4.set_xlabel('')
    tick_locs = np.arange(0, dims[3][1], 10)
    tick_vals = np.linspace(0, mms[3][1]-mms[3][0], num=np.size(tick_locs)).round(0).astype(np.int16)
    g4.set_yticks(tick_locs)
    g4.set_yticklabels(tick_vals)

    tick_locs_x = np.arange(0, dims[3][0], 10)
    tick_vals_x = np.linspace(0, mms[3][3]-mms[0][2], num=(np.size(tick_locs_x))).round(0).astype(np.int16)
    g4.set_xticks(tick_locs_x)
    g4.set_xticklabels(tick_vals_x)

    g5 = sns.heatmap(data_sets[4],cmap=c,cbar=False,ax=ax5,square=True,vmin=min_val1, vmax=max_val2)
    g5.set_ylabel('')
    g5.set_xlabel('')
    g5.set_yticks([])
    g5.set_xticks(tick_locs_x)
    g5.set_xticklabels(tick_vals_x)

    g6 = sns.heatmap(data_sets[5],cmap=c,ax=ax6,square=True,cbar_ax=cax1,vmin=min_val1, vmax=max_val2)
    g6.set_ylabel('')
    g6.set_xlabel('')
    g6.set_yticks([])
    g6.set_xticks(tick_locs_x)
    g6.set_xticklabels(tick_vals_x)
    
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    data_10 = np.load("test_data_multi-sample\\DS10_atm_6.75_10_samples_cast-bond_trial1.npy")
    data_10_prep = preprocess1(data_10, mesh=False)

    data_10_25 = np.load("test_data_multi-sample\\DS10_25PSI_6.75_10_samples_cast-bond_trial1.npy")
    data_10_25_prep = preprocess1(data_10_25, mesh=False)
    
    data_10_50 = np.load("test_data_multi-sample\\DS10_50PSI_6.75_10_samples_cast-bond_trial1.npy")
    data_10_50_prep = preprocess1(data_10_50, mesh=False)
    
    data_20 = np.load("test_data_multi-sample\\DS20_atm_9.9_10_samples_cast-bond_trial1.npy")
    data_20_prep = preprocess1(data_20, mesh=False)

    data_20_25 = np.load("test_data_multi-sample\\DS20_25PSI_9.9_10_samples_cast-bond_trial1.npy")
    data_20_25_prep = preprocess1(data_20_25, mesh=False)
    
    data_20_50 = np.load("test_data_multi-sample\\DS20_50PSI_9.9_10_samples_cast-bond_trial1.npy")
    data_20_50_prep = preprocess1(data_20_50, mesh=False)

    data_sets = [data_10_prep, data_10_25_prep, data_10_50_prep, data_20_prep, data_20_25_prep, data_20_50_prep]
    data_sets_meshes = []
    pressure_strs = ["atm", "25PSI", "50PSI", "atm", "25PSI", "50PSI"]
    pressure_colors = ["*k", "ob", ".r", "*k", "ob", ".r"]

    up_threshes = [5, 2.7, 5, 5.5, 3.7, 4]
    threshes = [5, 5, 5, 5, 2.6, 2.5]

    for ds_idx, ds in enumerate(data_sets):
        Z = ds.copy()
        # Trim boundaries
        if ds_idx <= 2: # dragonskin 10
            cutoff_left = 4.4
            cutoff_right = 3.3
        else: #dragonskin 20
            cutoff_left = 3
            cutoff_right = 0.95
        Z = Z[Z[:,0]>cutoff_left,:]
        x_max = np.max(Z[:,0])
        Z = Z[Z[:,0]<(x_max-cutoff_right)]

        # Determine matrix dimensions for reshaping
        x_set = set()
        y_set = set()
        for x, y in Z[:,0:2]:
            x_set.add(x)
            y_set.add(y)
        x_dim = len(x_set)
        y_dim = len(y_set)
        x_min = min(x_set)
        x_max = max(x_set)
        y_min = min(y_set)
        y_max = max(y_set)

        # Filter and interpolate every sensors mesh
        for i in range(8):
            Z[:,i+2] = filter_and_interp(Z[:,i+2].reshape((y_dim, x_dim)), threshes[ds_idx], 
                        thresh_bot=-0.5, thresh_top=up_threshes[ds_idx]).flatten()
        p_max = np.max(Z[:,2:])
        Z[:,2:] = (Z[:,2:]-np.min(Z[:,2:],axis=0))/(np.max(Z[:,2:],axis=0)-np.min(Z[:,2:],axis=0))
        Z[:,2:] = Z[:,2:] * p_max # undo normalization by scaling back to original
        data_sets_meshes.append(Z.copy())

    make_heatmaps_multi(data_sets_meshes)
    plt.show()


    