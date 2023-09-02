import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys

np.set_printoptions(threshold=sys.maxsize)

# --- Problem 8.10 - Forest Fire --- #

# probability values

P = 0.01
F_lst = [0.0001,0.001,0.01]

# initial 200 x 200 matrix
N = 200 # grid size
n = 100 # number of state iterations (run through full grid 'n' times)
ash = 10
fire = 100
tree = 0

for v in range(len(F_lst)):
    F = F_lst[v]

    # create forest grid full of ash - try with small grid first
    forest = np.full((N, N), ash)

    # createing padding of ash values around grid for convolution
    forest = np.pad(forest, pad_width=1, mode='constant',
                    constant_values=ash)

    # store old forest grid to use to compare with current
    forest_lst = []
    forest_lst = forest_lst + [forest]

    # create empty list to count number of states at each iteration
    num_ash_lst = []
    num_tree_lst = []
    num_fire_lst = []

    # starting value (only ash)
    num_ash_lst = num_ash_lst + [np.count_nonzero(forest == ash)]
    num_tree_lst = num_tree_lst + [np.count_nonzero(forest == tree)]
    num_fire_lst = num_fire_lst + [np.count_nonzero(forest == fire)]
    for k in range(n):
        forest = forest_lst[k-1]
        # below is for one state map cycle, n
        for i in range(1,len(forest)-1): # iterate through each row
            for j in range(1,len(forest[i])-1): # iterate through each column in each row
                if forest_lst[k-1][i][j] == fire:
                    forest[i][j] = ash
                elif forest_lst[k-1][i][j] == ash:
                    forest[i][j] = np.random.choice(np.array([tree,ash]),p = [P,1-P])
                elif forest_lst[k-1][i][j] == tree:

                    # check adjacent trees if burning
                    row_past = forest_lst[k-1][i - 1][j - 1] + forest_lst[k-1][i - 1][j] + forest_lst[k-1][i - 1][j + 1]
                    row_current = forest_lst[k-1][i][j - 1] + forest_lst[k-1][i][j + 1]
                    row_next = forest_lst[k-1][i + 1][j - 1] + forest_lst[k-1][i + 1][j] + forest_lst[k-1][i + 1][j + 1]
                    adjacent_sum = row_past + row_current + row_next
                    if adjacent_sum > 8 * ash:
                        forest[i][j] = fire
                    else:
                        forest[i][j] = np.random.choice(np.array([fire, tree]), p=[F, 1 - F])
        forest_lst = forest_lst + [forest]

        # remove padding
        forest = np.delete(forest, 0, 0)
        forest = np.delete(forest, N, 0)
        forest = np.delete(forest, 0, 1)
        forest = np.delete(forest, N, 1)

        # count values at end of iteration
        num_ash_lst = num_ash_lst + [np.count_nonzero(forest == ash)]
        num_tree_lst = num_tree_lst + [np.count_nonzero(forest == tree)]
        num_fire_lst = num_fire_lst + [np.count_nonzero(forest == fire)]
    # plot behavior over each state iteration
    plt.plot(np.linspace(0,n,n+1),num_ash_lst,c = 'gray',label = 'ash')
    plt.plot(np.linspace(0, n, n + 1), num_tree_lst, c='green', label='tree')
    plt.plot(np.linspace(0, n, n + 1), num_fire_lst, c='orange', label='burning')
    plt.ylabel('Number of states observed in the forest')
    plt.xlabel('State iteration')
    plt.legend()
    plt.show()

    # create grid colour plot of forest state at iteration n
    fig, ax = plt.subplots(1, 1, tight_layout=True)
    # make color map
    my_cmap = matplotlib.colors.ListedColormap(['green', 'gray','black','black','black','black','black','black','black', 'orange'])
    for x in range(N + 1):
        ax.axhline(x, lw=0.01, color='k', zorder=5)
        ax.axvline(x, lw=0.01, color='k', zorder=5)

    # draw the boxes
    ax.imshow(forest, interpolation='none', cmap=my_cmap, extent=[0, N, 0, N], zorder=0, vmin=tree, vmax=fire)
    # turn off the axis labels
    ax.axis('off')
    plt.show()