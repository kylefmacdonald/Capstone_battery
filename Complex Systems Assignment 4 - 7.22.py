import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# # part (a) Competing Dynamics Model
#
delta = 0.1 # time step
#
# x_arr = np.random.uniform(low=0, high=3, size=(100,))
# y_arr = np.random.uniform(low=0, high=2, size=(100,))
#
# for i in range(len(x_arr)):
#     # for each random x and y starting point use the euler step method to create phase curve
#     # create empty array for x and y
#     X = np.empty([0, 1])
#     Y = np.empty([0, 1])
#     for j in range(100):
#         if j == 0:
#             X = np.append(X,x_arr[i])
#             Y = np.append(Y,y_arr[i])
#         else:
#             x_val = X[j-1] + delta * (3 - X[j-1] - 2 * Y[j-1]) * X[j-1]
#             X = np.append(X,x_val)
#             y_val = Y[j-1] + delta * (2 - Y[j-1] - X[j-1])*Y[j-1]
#             Y = np.append(Y, y_val)
#     plt.plot(X, Y,color = 'blue',alpha = 0.5,linewidth=1)
#
# # plot starting points
# plt.scatter(x_arr,y_arr,label = 'Starting Point',s = 10,c = 'firebrick')
#
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.title('Part (A) - Competing Dynamics Model')
# plt.legend()
# plt.show()
#
# # Part (b) Classic Predator-Prey Model
#
# theta = 2
#
# delta = 0.1 # time step
#
# x_arr = np.random.uniform(low=0, high=1, size=(100,))
# y_arr = np.random.uniform(low=0, high=1, size=(100,))
#
# for i in range(len(x_arr)):
#     # for each random x and y starting point use the euler step method to create phase curve
#     # create empty array for x and y
#     X = np.empty([0, 1])
#     Y = np.empty([0, 1])
#     for j in range(100):
#         if j == 0:
#             X = np.append(X,x_arr[i])
#             Y = np.append(Y,y_arr[i])
#         else:
#             x_val = X[j-1] + delta * (1 - Y[j-1]) * X[j-1]
#             X = np.append(X,x_val)
#             y_val = Y[j-1] + delta * theta * (X[j-1] - 1)*Y[j-1]
#             Y = np.append(Y, y_val)
#     plt.plot(X, Y,color = 'blue',alpha = 0.5,linewidth=1)
#
#
# # plot starting points
# plt.scatter(x_arr,y_arr,label = 'Starting Point',s = 10,c = 'firebrick')
#
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.title('Part (B) - Classic Predator-Prey Model')
# plt.legend()
# plt.show()
#
# part (c) Selkov model

theta_arr = np.linspace(0,1,100)

# (i) see hand solution

# (ii) plot behaviour of trace and determinant for range of theta

theta = np.linspace(0,1,1000)

x = theta
y = theta / (theta ** 2 + 0.1)
trace = (-1 + 2 * x * y) + (-0.1 - x ** 2)
determinant = (-1 + 2 * x * y) * (-0.1 - x ** 2) - (0.1 + x ** 2) * (-2 * x * y)

plt.plot(theta,determinant,label = 'Determinant')
plt.plot(theta, trace,label = 'Trace')
plt.legend()
plt.xlabel('theta')
plt.ylabel('Trace-Determinant')
plt.title('Part (C) - Selkov Model (ii)')
plt.axhline(color='black')
plt.axvline(color='black')
plt.show()

# (iii)

x_lst = []
y_lst = []
tr_lst = []
det_lst = []
for i in range(len(theta_arr)):
    theta = theta_arr[i]
    x = theta
    y = theta / (theta ** 2 + 0.1)
    trace = (-1+2*x*y) + (-0.1-x**2)
    determinant = (-1+2*x*y)*(-0.1-x**2) - (0.1+x**2)*(-2*x*y)
    x_lst = x_lst + [x]
    y_lst = y_lst + [y]
    tr_lst = tr_lst + [trace]
    det_lst = det_lst + [determinant]

det_arr = np.linspace(0,1.2,100)
sprial = np.sqrt(4*det_arr)

# plot behaviour of theta
plt.plot(det_lst,tr_lst,label = 'Trace-Determinant')
plt.plot(det_arr,sprial,label = 'unstable star')
plt.plot(det_arr,-1*sprial,label = 'stable star')
plt.xlabel('Determinant')
plt.ylabel('Trace')
plt.title('Part (C) - Selkov Model - Trace Determinant Plot')
plt.legend()
plt.axhline(color='black')
plt.axvline(color='black')

# determine the theta values for ranges of trace determinant plot
tr = -0.711 # stable star intercept
tr = 0 #

theta = sp.symbols('theta')

x = theta
y = theta / (theta ** 2 + 0.1)

eq = (-1+2*x*y) + (-0.1-x**2) - tr

solution = sp.solve(eq)
print(solution)
plt.show()

# part (iv)

theta_ls = [0.1,0.5,1]

x_arr = np.random.uniform(low=0, high=1, size=(5,))
y_arr = np.random.uniform(low=0, high=1, size=(5,))

colour_ls = ['midnightblue','maroon','lightseagreen']

for k in range(len(theta_ls)):
    theta = theta_ls[k]
    colour = colour_ls[k]
    for i in range(len(x_arr)):
        # for each random x and y starting point use the euler step method to create phase curve
        # create empty array for x and y
        X = np.empty([0, 1])
        Y = np.empty([0, 1])
        for j in range(1000):
            if j == 0:
                X = np.append(X,x_arr[i])
                Y = np.append(Y,y_arr[i])
            else:
                x_val = X[j-1] + delta * (- X[j-1] + 0.1*Y[j-1] + Y[j-1]*(X[j-1])**2)
                X = np.append(X,x_val)
                y_val = Y[j-1] + delta * (theta - 0.1*Y[j-1] - Y[j-1]*(X[j-1])**2)
                Y = np.append(Y, y_val)
        plt.plot(X, Y,color = colour,linewidth=1)
        # plot starting points
        plt.xlabel('X')
        plt.ylabel('Y')
        text = 'Part (C) - Selkov Model (iv) theta = ' + str(theta)
        plt.title(text)
    plt.scatter(x_arr, y_arr, label='Starting Point', s=10, c='firebrick')
    plt.legend()
    plt.show()



