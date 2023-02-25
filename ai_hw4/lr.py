
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

import sys
import csv


def main():
    """
    YOUR CODE GOES HERE
    Implement Linear Regression using Gradient Descent, with varying alpha values and numbers of iterations.
    Write to an output csv file the outcome betas for each (alpha, iteration #) setting.
    Please run the file as follows: python3 lr.py data2.csv, results2.csv
    """
    #start file writer
    f = open(sys.argv[2], 'w')
    writer = csv.writer(f)

    # get df
    data = pd.read_csv(sys.argv[1], header=None)

    # normalize columns
    age_weight = data.iloc[:,:-1]
    data.iloc[:,:-1] = (age_weight - age_weight.mean()) / age_weight.std()

    # prep data
    m, n = data.shape
    xs = np.hstack((np.ones(m).reshape(m,1),data.iloc[:, 0:2].to_numpy()))
    ys = data.iloc[:, -1:].to_numpy().reshape((m, 1))
    betas = np.zeros((xs.shape[1], 1))

    for lr in [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]:
        final_weights = gradient_descent(xs, ys, betas, lr, 100)
        # visualize_3d(data, lin_reg_weights=final_weights, alpha=lr)

        # α, num iters, bias, b age, b weight,
        row = [lr, 100] + list(np.squeeze(final_weights))
        writer.writerow(row)


    # my choices
    my_lr = 0.1
    my_itr = 50

    final_weights = gradient_descent(xs, ys, betas, my_lr, my_itr)
    visualize_3d(data, lin_reg_weights=final_weights, alpha=my_lr)

    row = [my_lr, my_itr] + list(np.squeeze(final_weights))
    writer.writerow(row)
    
    f.close() 

def gradient_descent(x, y, beta, lr=1, iter=100):
    beta = np.zeros((x.shape[1], 1))
    n, _ = x.shape

    for i in range(iter): 
        prediction = np.matmul(x, beta)
        error = (1/n)*(np.matmul(x.T, (prediction - y)))
        beta -= lr*error

    return beta


# errors = (0.5*m) * np.sum(np.square(prediction - np.squeeze(actuals)))

#         deriv_betas = (1/m) * np.sum(np.matmul((prediction - actuals).T, feats), axis=0)
#         #print(deriv_betas)
#         j = deriv_betas
#         betas -= lr*j

def visualize_3d(df, lin_reg_weights=[1,1,1], feat1=0, feat2=1, labels=2,
                 xlim=(-1, 1), ylim=(-1, 1), zlim=(0, 3),
                 alpha=0., xlabel='age', ylabel='weight', zlabel='height',
                 title=''):
    """ 
    3D surface plot. 
    Main args:
      - df: dataframe with feat1, feat2, and labels
      - feat1: int/string column name of first feature
      - feat2: int/string column name of second feature
      - labels: int/string column name of labels
      - lin_reg_weights: [b_0, b_1 , b_2] list of float weights in order
    Optional args:
      - x,y,zlim: axes boundaries. Default to -1 to 1 normalized feature values.
      - alpha: step size of this model, for title only
      - x,y,z labels: for display only
      - title: title of plot
    """

    # Setup 3D figure
    ax = plt.axes(projection='3d')

    # Add scatter plot
    ax.scatter(df[feat1], df[feat2], df[labels])

    # Set axes spacings for age, weight, height
    axes1 = np.arange(xlim[0], xlim[1], step=.05)  # age
    axes2 = np.arange(xlim[0], ylim[1], step=.05)  # weight
    axes1, axes2 = np.meshgrid(axes1, axes2)
    axes3 = np.array( [lin_reg_weights[0] +
                       lin_reg_weights[1]*f1 +
                       lin_reg_weights[2]*f2  # height
                       for f1, f2 in zip(axes1, axes2)] )
    plane = ax.plot_surface(axes1, axes2, axes3, cmap=cm.Spectral,
                            antialiased=False, rstride=1, cstride=1, alpha=0.5)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    ax.set_xlim3d(xlim)
    ax.set_ylim3d(ylim)
    ax.set_zlim3d(zlim)

    if title == '':
        title = 'LinReg Height with Alpha %f' % alpha
    ax.set_title(title)

    plt.show()

if __name__ == "__main__":
    main()