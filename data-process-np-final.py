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
        x = torch.sigmoid(self.l2(x))
        x = self.l3(x)
        # x = F.relu(self.l2(x))
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
    
    data_10 = np.load("test_data_multi-sample\\DS20_atm_9.9_10_samples_cast-bond_trial1.npy")
    data_10_prep = preprocess1(data_10, mesh=False)

    data_10_25 = np.load("test_data_multi-sample\\DS20_25PSI_9.9_10_samples_cast-bond_trial1.npy")
    data_10_25_prep = preprocess1(data_10, mesh=False)
    
    data_10_50 = np.load("test_data_multi-sample\\DS20_50PSI_9.9_10_samples_cast-bond_trial1.npy")
    data_10_50_prep = preprocess1(data_10, mesh=False)
    
    Z = data_10_prep.copy()
    
    # Trim boundaries
    cutoff_left = 4
    cutoff_right = 1.5
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
    Z_dev_idx = np.random.choice(Z.shape[0], size=int(Z.shape[0]/10), replace=False)
    Z_dev = Z[Z_dev_idx].copy()
    Z_train = np.delete(Z, Z_dev_idx, axis=0)
    
    X_train = Z_train[:,2:]
    Y_train = Z_train[:,:2]
    
    X_dev = Z_dev[:,2:]
    Y_dev = Z_dev[:,:2]

    # make_heatmaps(np.hstack((Y,X)), pre_filtered=True)
    # plt.show()
    # # print(X.shape)
    # # print(Y.dtype)


    net = NeuralNet(16,12)
    
    X_train_tensor = torch.from_numpy(X_train).float()
    Y_train_tensor = torch.from_numpy(Y_train).float()
    X_dev_tensor = torch.from_numpy(X_dev).float()
    Y_dev_tensor = torch.from_numpy(Y_dev).float()
    loss_ot_t, loss_ot_dev = train_net(net,X_train_tensor,Y_train_tensor, X_dev_tensor, Y_dev_tensor, 5000, lr=0.05)
    print("loss at end of training: {0}, {1}".format(loss_ot_t[-1], loss_ot_dev[-1]))

    # Z = np.hstack((Y_dev,X_dev))
    rand_rows = np.random.choice(Y_dev.shape[0], size=20, replace=False)
    rand_samples = Z_dev[rand_rows,:]

    X_rand = torch.from_numpy(rand_samples[:,2:]).float()
    Y_rand = rand_samples[:,:2]


    predictions = net.forward(X_rand).detach().numpy()
    plt.plot(loss_ot_t)
    plt.plot(loss_ot_dev)
    plt.show()
    for i in range(predictions.shape[0]):
        plt.plot(Y_rand[i,0],Y_rand[i,1],'ko')
        plt.plot(predictions[i,0],predictions[i,1],'r*')
    ax = plt.gca()
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    ax.set_aspect('equal', adjustable='box')
    # plt.xticks(np.arange(0,1, step=(x_max-x_min)/(x_dim/2)))
    plt.show()
    