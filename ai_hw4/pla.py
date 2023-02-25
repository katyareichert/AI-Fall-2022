import pandas as pd
import numpy as np
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import sys
import csv

def main():
    # run as $ python3 pla.py data1.csv results1.csv
    data = pd.read_csv(sys.argv[1], header=None)

    f = open(sys.argv[2], 'w')
    writer = csv.writer(f)

    final_weights = perceptron(data, writer)
    plot_boundary(data, final_weights)
    print(final_weights)

    writer.writerow(final_weights)

    f.close()

def perceptron(data, writer):
    m, n = data.shape
    weights = np.ones((n, 1))    
    i = 0
    total_iterations = 0
    while i < m:
        if total_iterations > 10000:
            print('Did not converge.')
            return np.ones((n, 1))

        *row, label  = data.iloc[i].tolist()
        row = np.insert(np.array(row), 0, 1).reshape(-1,1)
        predict = np.squeeze(np.dot(row.T, weights))
        
        if predict*label <= 0:
            weights += label*row
            writer.writerow(list(np.squeeze(weights)))
            i = 0
        else:
            i += 1
        
        total_iterations += 1

    return list(np.squeeze(weights))

def plot_boundary(df, weights):
    colors = pd.Series(['r' if label > 0 else 'b' for label in df[2]])
    ax = df.plot(x=0, y=1, kind='scatter', c=colors)
    
    for i, row in df.iterrows():
        ax.annotate(i, row[:-1])
        
    # Compute and draw line. w1*x + w2*y + b = 0  =>  y = -a/b*x - c/b
    a = weights[1] # weight 1
    b = weights[2] # weight 2
    c = weights[0] # b

    def y(x, m):
        if b == 0:
            return -a*x - c
        return (-a/b)*x - c/b
    
    xmin, xmax = ax.get_xlim()
    
    line_start = (xmin, xmax)
    line_end = (y(xmin, 0), y(xmax, 1))
    line = mlines.Line2D(line_start, line_end, color='red')
    ax.add_line(line)
    
    plt.show()

if __name__ == "__main__":
    """DO NOT MODIFY"""
    main()