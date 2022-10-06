import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor

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

def generate_circle_array(radius, center, height):
    angles = np.linspace(0, 2*np.pi, 200)
    x = radius * np.cos(angles) + center[0]
    y = radius * np.sin(angles) + center[1]
    z = height * np.ones(x.shape)
    return x, y, z

def make_heatmaps(data1):
    Z1 = data1[:,2]

    min_val = np.min(Z1)
    max_val = np.max(Z1)

    x_min = np.min(data1[:,0])
    x_max = np.max(data1[:,0])
    y_min = np.min(data1[:,1])
    y_max = np.max(data1[:,1])

    # find the dimensions for x and y by adding vals to a set
    x_set = set()
    y_set = set()
    for x, y in data1[:,0:2]:
        x_set.add(x)
        y_set.add(y)
    x_dim = len(x_set)
    y_dim = len(y_set)

    Z1 = Z1.reshape((y_dim, x_dim))

    f, ax1 = plt.subplots()
    pos = ax1.imshow(Z1, cmap='Spectral')
    f.colorbar(pos, ax=ax1)
    ax1.set_xlabel('mm')
    ax1.set_ylabel('mm')
    
    # Make tick spacing
    # xt = np.arange()
    # ax1.set_xticks()

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
    center = (-0.05, -0.03)

    data_10 = np.load("C:\\Users\\Aiden\\Documents\\Research\\UnderwaterTactileSensor\\Underwater-Tactile-Sensor\\test_data_multi-sample\DS10_50PSI_6.75_10_samples_trial1.npy")
    data_10_prep_mesh = preprocess1(data_10, hard_cutoff=5, mesh=True)
    # data_10_prep_train = preprocess1(data_10, hard_cutoff=1.5, mesh=False)

    # locs = data_10_prep_train[:,0:2]
    # sens = data_10_prep_train[:,2:]

    # np.savetxt("train_data/DS10_atm_8.75_10-samples_train.csv", data_10_prep_train, delimiter=',')

    # print(radius_of_sensing)
    # data_20 = np.load("test_data_multi-sample/DS20_100g_50-PSI_delta-0.5mm_thick-8mm_single-barometer-16_multi-sample-10.npy")
    # data_20_prep = preprocess(data_20)

    # data_30 = np.load("test_data_multi-sample/DS10_100g_30-PSI_delta-0.5mm_thick-8mm_single-barometer-16_multi-sample-5.npy")
    # data_30_prep = preprocess(data_30)
    


    # # --------------------------- 
    make_heatmaps(data_10_prep_mesh)
    make_mesh(data_10_prep_mesh)
    
    
    plt.show()
