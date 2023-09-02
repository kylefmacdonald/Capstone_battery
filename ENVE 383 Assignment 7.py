import pandas as pd
import numpy as np
import sympy as sp
import math
from sympy import Eq, var, solve, symbols,nsolve,S
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# pd print settings #
pd.set_option('display.max_rows', 300)
pd.set_option('display.max_columns', 60)
pd.set_option('display.width', 0)
pd.set_option('display.precision', 3)

def channel_calc(Q,So,n,Bo,z,D,init_guess,type):
    print('channel type: ' + type)
    # variables
    g = 9.81
    Yn = symbols('Yn', real=True,positive=True)  # create Yn variable
    if type == 'Circular':
        T = 2*(D*Yn-Yn**2)**0.5
        A = ((D**2)/4) * sp.acos(1-2*Yn/D) - (D/2-Yn)*(D*Yn-Yn**2)**0.5
        P = D*sp.acos(1-2*Yn/D)
        R = A / P  # hydraulic radius [m]
    else:
        T = Bo + 2 * z * Yn  # top width [m]
        A = (Bo + z * Yn) * Yn  # area [m2]
        P = Bo + 2 * Yn * np.sqrt(1 + z ** 2)  # wetted perimeter [m]
        R = A / P  # hydraulic radius [m]

    # Yn using mannings equation:
    eq = A / n * R ** (2 / 3) * abs(So) ** (1 / 2) - Q
    if type == 'Circular':
        solution = nsolve(eq, Yn,init_guess)
        Yn_sol = solution
    else:
        solution = nsolve(eq, Yn, init_guess)
        Yn_sol = solution
    print('Normal Depth:', round(Yn_sol, 3), '[m]')


    # Froude Number
    if type == 'Circular':
        T = 2*(D*Yn_sol-Yn_sol**2)**0.5
    else:
        T = Bo + 2 * z * Yn_sol  # top width [m]
        A = (Bo + z * Yn_sol) * Yn_sol  # area [m2]
    Fr_sol = (Q / A) / math.sqrt(g * A/T)
    print('Froude Number: ', round(Fr_sol, 3), '[-]')


    # critical depth
    Yc = symbols('Yc',positive=True,reals=True)         # create Yc variable
    if type == 'Circular':
        Tc = 2*(D*Yc-Yc**2)**(0.5)
        Ac = ((D**2)/4) * sp.acos(1-2*Yc/D) - (D/2-Yc)*(D*Yc-Yc**2)**(0.5)
    else:
        Tc = Bo + 2 * z * Yc  # top width [m]
        Ac = (Bo + z * Yc) * Yc  # area [m2]
    FR = (Q/Ac)/(sp.sqrt(g*(Ac/Tc))) - 1                 # Froude number
    if type == 'Circular':
        solution = nsolve(FR, Yc, init_guess)
        Yc_sol = solution
    else:
        solution = sp.solveset(FR, Yc)
        Yc_sol = solution.args[0].args[0]

    print('The critical flow depth is: ', round(Yc_sol,3), '[m]')

    # Flow Regime
    if Yn_sol > Yc_sol:
        regime = 'The flow regime is sub-critical'
    elif Yn_sol < Yc_sol:
        regime = 'The flow regime is super-critical'
    print(regime)

    # # New So (comment out for Q2)
    # Sc = symbols('Sc', real=True, positive=True)  # create Yn variable
    # Ac = (Bo + z * Yc_sol) * Yc_sol  # area [m2]
    # Pc = Bo + 2 * Yc_sol * np.sqrt(1 + z ** 2)  # wetted perimeter [m]
    # Rc = Ac / Pc  # hydraulic radius [m]
    # eq = Ac / n * Rc ** (2 / 3) * Sc ** (1 / 2) - Q
    # if type == 'Circular':
    #     solution = nsolve(eq, Sc, init_guess)
    # else:
    #     solution = nsolve(eq, Sc, init_guess)
    # Sc_sol = solution
    # print('Critical slope:', round(Sc_sol, 3), '[-]')

    # Flow Profile
    if Yn_sol > Yc_sol:
        profile = 'Mild [M]'
        print('The channel profile is: '+profile)
    if So == 0:
        profile = 'Horizontal [H]'
        print('The channel profile is: '+profile)
    if Yn_sol == Yc_sol:
        profile = 'Critical [C]'
        print('The channel profile is: '+profile)
    if Yn_sol < Yc_sol:
        profile = 'Steep [S]'
        print('The channel profile is: '+profile)
    if So < 0:
        profile = 'Adverse [A]'
        print('The channel profile is: '+profile)


    return Yn_sol, Fr_sol, Yc_sol, regime

# --- inputs --- #

Q = 7.5*10**-4
So = 7.5*10**(-4)                          # bed slope [-]
Bo = 9                              # channel wdith [m]
D = 2.5                               # channel diameter [m]
n = 0.025
g = 9.81                            # acceleration due to gravity
init_guess = 0.4                    # tweak for some parameters
z = 1

print('----------------------------------------- Question 1A -----------------------------------------')

channel = channel_calc(Q, So, n, Bo, z, D, init_guess, 'Circular')
Yn1 = channel[0]