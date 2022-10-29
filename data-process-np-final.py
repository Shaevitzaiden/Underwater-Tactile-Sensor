from cProfile import label
from pickletools import optimize
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


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
        ax.plot3D(line[0], line[1], line[2], "black",linewidth="5", alpha=1)
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

def generate_circle_array(radius, center, height):
    angles = np.linspace(0, 2*np.pi, 200)
    x = radius * np.cos(angles) + center[0]
    y = radius * np.sin(angles) + center[1]
    z = height * np.ones(x.shape)
    return x, y, z

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


class NeuralNet(nn.Module):
    def __init__(self, hidden1, hidden2) -> None:
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(8, hidden1)
        self.l2 = nn.Linear(hidden1, hidden2)
        self.l3 = nn.Linear(hidden2, 2)

    def forward(self, x):
        x = torch.sigmoid(self.l1(x))
        # x = self.l2(x)
        x = torch.sigmoid(self.l2(x))
        x = self.l3(x)
        return x


def train_net(net, x, y, x_dev, y_dev, iterations, lr=0.1):
    criterion = nn.MSELoss()
    optimizer = optim.Adam(net.parameters(), lr=lr)
    loss_ot_t = []
    loss_ot_dev = []
    for i in range(iterations):
        net.zero_grad()
        output = net(x)
        output_dev = net(x_dev)
        loss = criterion(output, y)
        loss_dev = criterion(output_dev, y_dev)
        loss_ot_t.append(loss.detach().numpy())
        loss_ot_dev.append(loss_dev.detach().numpy())
        loss.backward()
        optimizer.step()
    return loss_ot_t, loss_ot_dev
 


if __name__ == "__main__":
    center = (-0.05, -0.03)
    """
    # data_10 = np.load("test_data_multi-sample\\DS20_50PSI_9.9_10_samples_cast-bond_trial1.npy")
    # data_10_prep_mesh = preprocess1(data_10, mesh=True)
    # data_10_prep_train = preprocess1(data_10, hard_cutoff=1.5, mesh=False)

    # locs = data_10_prep_train[:,0:2]
    # sens = data_10_prep_train[:,2:]

    # np.savetxt("train_data/DS10_atm_8.75_10-samples_train.csv", data_10_prep_train, delimiter=',')

    # print(radius_of_sensing)
    # data_20 = np.load("test_data_multi-sample/DS20_100g_50-PSI_delta-0.5mm_thick-8mm_single-barometer-16_multi-sample-10.npy")
    # data_20_prep = preprocess(data_20)

    # data_30 = np.load("test_data_multi-sample/DS10_100g_30-PSI_delta-0.5mm_thick-8mm_single-barometer-16_multi-sample-5.npy")
    # data_30_prep = preprocess(data_30)
    

    # make_heatmaps(data_10_prep_mesh)
    # make_mesh(data_10_prep_mesh)
    """
    # -----------------------------------------------------------------------------------
    
    data_10 = np.load("test_data_multi-sample\\DS10_atm_6.75_10_samples_cast-bond_trial1.npy")
    data_10_prep = preprocess1(data_10, mesh=False)

    data_10_25 = np.load("test_data_multi-sample\\DS10_25PSI_6.75_10_samples_cast-bond_trial1.npy")
    data_10_25_prep = preprocess1(data_10, mesh=False)
    
    data_10_50 = np.load("test_data_multi-sample\\DS10_50PSI_6.75_10_samples_cast-bond_trial1.npy")
    data_10_50_prep = preprocess1(data_10, mesh=False)
    
    data_sets = [data_10_prep, data_10_25_prep, data_10_50_prep]
    pressure_strs = ["atm", "25PSI", "50PSI"]
    pressure_colors = ["*k", "ob", ".r"]
    num_network_trials = 100
    network_mses = np.zeros((num_network_trials,3))
    network_mses_plot = np.zeros((num_network_trials,3))
    
    for ds_idx, ds in enumerate(data_sets):
        Z = ds.copy()
        # Trim boundaries
        cutoff_left = 4.25
        cutoff_right = 3.25
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
            Z[:,i+2] = filter_and_interp(Z[:,i+2].reshape((y_dim, x_dim)), 7, thresh_bot=-0.5, thresh_top=5).flatten()

        #  np.savetxt('DS20_atm_9.9_10_samples_cast-bond_trial1.csv', Z, delimiter=',')
        # Shuffle data
        # np.random.shuffle(Z)
        Z[:,2:] = (Z[:,2:]-np.min(Z[:,2:],axis=0))/(np.max(Z[:,2:],axis=0)-np.min(Z[:,2:],axis=0))
        
        for i in range(num_network_trials):
            Z_dev_idx = np.random.choice(Z.shape[0], size=int(Z.shape[0]/10), replace=False)
            Z_dev = Z[Z_dev_idx].copy()
            Z_train = np.delete(Z, Z_dev_idx, axis=0)
            
            X_train = Z_train[:,2:]
            Y_train = Z_train[:,:2]
            
            X_dev = Z_dev[:,2:]
            Y_dev = Z_dev[:,:2]

            # make_heatmaps(np.hstack((Z[:,:2],Z[:,2:])), pre_filtered=True)
            # plt.show()
            # print(X.shape)
            # print(Y.dtype)


            net = NeuralNet(10,10)
            
            X_train_tensor = torch.from_numpy(X_train).float()
            Y_train_tensor = torch.from_numpy(Y_train).float()
            X_dev_tensor = torch.from_numpy(X_dev).float()
            Y_dev_tensor = torch.from_numpy(Y_dev).float()
            loss_ot_t, loss_ot_dev = train_net(net,X_train_tensor,Y_train_tensor, X_dev_tensor, Y_dev_tensor, 4000, lr=0.05)
            print("loss at end of training for {0} #{1}: {2}, {3}".format(pressure_strs[ds_idx], i, loss_ot_t[-1], loss_ot_dev[-1]))
            network_mses[i, ds_idx] = loss_ot_dev[-1]
            # network_mses_plot[i, ds_idx] = ds_idx
            plt.plot(ds_idx, loss_ot_dev[-1], pressure_colors[ds_idx])
    
    network_mses = np.sqrt(network_mses)
    means = np.mean(network_mses,axis=0)
    print(means)
    std_errors = np.std(network_mses,axis=0)
    print(std_errors)
    # plt.xticks(np.arange(3), pressure_strs)
    # plt.xlabel("Pressure (PSIG)")
    # plt.ylabel("MSE")
    # plt.show()
    

    # # ----------------------------------------------------------------------------------------------------
    # Z = data_10_50_prep.copy()
    # # Trim boundaries
    # cutoff_left = 4
    # cutoff_right = 2.75
    # Z = Z[Z[:,0]>cutoff_left,:]
    # x_max = np.max(Z[:,0])
    # Z = Z[Z[:,0]<(x_max-cutoff_right)]

    # # Determine matrix dimensions for reshaping
    # x_set = set()
    # y_set = set()
    # for x, y in Z[:,0:2]:
    #     x_set.add(x)
    #     y_set.add(y)
    # x_dim = len(x_set)
    # y_dim = len(y_set)
    # x_min = min(x_set)
    # x_max = max(x_set)
    # y_min = min(y_set)
    # y_max = max(y_set)

    # # Filter and interpolate every sensors mesh
    # for i in range(8):
    #     Z[:,i+2] = filter_and_interp(Z[:,i+2].reshape((y_dim, x_dim)), 7, thresh_bot=-0.5, thresh_top=5).flatten()

    # # np.savetxt('DS20_atm_9.9_10_samples_cast-bond_trial1.csv', Z, delimiter=',')
    # # Shuffle data
    # # np.random.shuffle(Z)
    # Z[:,2:] = (Z[:,2:]-np.min(Z[:,2:],axis=0))/(np.max(Z[:,2:],axis=0)-np.min(Z[:,2:],axis=0))
    
    
    # Z_dev_idx = np.random.choice(Z.shape[0], size=int(Z.shape[0]/10), replace=False)
    # Z_dev = Z[Z_dev_idx].copy()
    # Z_train = np.delete(Z, Z_dev_idx, axis=0)
    
    # X_train = Z_train[:,2:]
    # Y_train = Z_train[:,:2]
    
    # X_dev = Z_dev[:,2:]
    # Y_dev = Z_dev[:,:2]

    # make_heatmaps(Z, pre_filtered=True)
    # make_mesh(Z, pre=True)
    # plt.show()
    # print(X.shape)
    # print(Y.dtype)


    # net = NeuralNet(10,10)
    
    # X_train_tensor = torch.from_numpy(X_train).float()
    # Y_train_tensor = torch.from_numpy(Y_train).float()
    # X_dev_tensor = torch.from_numpy(X_dev).float()
    # Y_dev_tensor = torch.from_numpy(Y_dev).float()
    # loss_ot_t, loss_ot_dev = train_net(net,X_train_tensor,Y_train_tensor, X_dev_tensor, Y_dev_tensor, 4000, lr=0.05)
    # # print("loss at end of training for {0} #{1}: {2}, {3}".format(pressure_strs[ds_idx], i, loss_ot_t[-1], loss_ot_dev[-1]))
    # # network_mses[i, ds_idx] = loss_ot_dev[-1]

    # # --------- prediction plot -----------
    # Z_dev_random = Z_dev[np.random.choice(Z_dev.shape[0], size=10, replace=False), :]
    # X_dev = Z_dev_random[:,2:]
    # Y_dev = Z_dev_random[:,:2]
    # X_dev_tensor = torch.from_numpy(X_dev).float()
    
    # predictions = net.forward(X_dev_tensor).detach().numpy()
    # # plt.plot(loss_ot_t)
    # # plt.plot(loss_ot_dev)
    # # plt.show()
    # # for i in range(predictions.shape[0]):
    # plt.plot(Y_dev[:,0],Y_dev[:,1],'ko', label="Ground truth")
    # plt.plot(predictions[:,0],predictions[:,1],'r*', label="Predicted")
    # plt.legend()
    # ax = plt.gca()
    # plt.xlim(x_min, x_max)
    # plt.ylim(y_min, y_max)
    # print(x_min, x_max)
    # ax.set_aspect('equal', adjustable='box')
    # # #
    # # s = (x_max-x_min)/5
    # # plt.xticks(np.arange(x_min,x_max, step=s), [0, int(s*1), int(s*2), int(s*3), int(s*4)])
    
    # # sy = (y_max-y_min)/8
    # # plt.xticks(np.arange(y_min,y_max, step=s), [0, int(sy*1), int(sy*2), int(sy*3), int(sy*4), int(sy*5), int(sy*6)])
    # plt.ylabel('mm')
    # plt.xlabel('mm')
    # plt.title('FFNN Contact Localization')
    # plt.show()

    