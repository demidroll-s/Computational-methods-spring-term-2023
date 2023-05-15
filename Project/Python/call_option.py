from mlmc_test import mlmc_test
from mlmc_plot import mlmc_plot

import matplotlib.pyplot as plt
import numpy as np
import numpy.random
from math import sqrt

class CallType(object):
    def __init__(self, name, q_ref, M, L, Eps):
        self.name = name
        self.q_ref = q_ref # refinement cost factor
        self.M = M # samples for convergence tests
        self.L = L # levels for convergence tests
        self.Eps = Eps

calltypes = [CallType("European", 4, 2000000, 4, [0.005, 0.01, 0.02, 0.05, 0.1])]

def opre_gbm(l, M, calltype, randn=numpy.random.randn):
    q_ref = calltype.q_ref # refinement factor

    time_option_expiration = 1.0  # interval
    r = 0.05
    sigma = 0.2
    k = 100.0

    n_fine = q_ref**l
    h_fine = time_option_expiration / n_fine

    n_coarse = max(n_fine / q_ref, 1)
    h_coarse = time_option_expiration / n_coarse

    sums = np.zeros(6)

    for m1 in range(1, M + 1, 10000):
        m2 = min(10000, M - m1 + 1)

        X_0 = k
        X_fine = X_0 * np.ones(m2)
        X_coarse = X_0 * np.ones(m2)

        A_fine = 0.5 * h_fine * X_fine
        A_coarse = 0.5 * h_coarse * X_coarse

        M_fine = np.array(X_fine)
        M_coarse = np.array(X_coarse)

        if l == 0:
            dW_fine = sqrt(h_fine) * randn(1, m2)
            X_fine[:] = X_fine + r * X_fine * h_fine + sigma * X_fine * dW_fine
            A_fine[:] = A_fine + 0.5 * h_fine * X_fine
            M_fine[:] = np.minimum(M_fine, X_fine)
        else:
            for n in range(int(n_coarse)):
                dW_coarse = numpy.zeros((1, m2))

                for _ in range(q_ref):
                    dW_fine = sqrt(h_fine) * randn(1, m2)
                    dW_coarse[:] = dW_coarse + dW_fine
                    X_fine[:] = (1.0 + r * h_fine) * X_fine + sigma * X_fine * dW_fine
                    A_fine[:] = A_fine + h_fine * X_fine
                    M_fine[:] = np.minimum(M_fine, X_fine)

                X_coarse[:] = X_coarse + r * X_coarse * h_coarse + sigma * X_coarse * dW_coarse
                A_coarse[:] = A_coarse + h_coarse * X_coarse
                M_coarse[:] = np.minimum(M_coarse, X_coarse)

            A_fine[:] = A_fine - 0.5 * h_fine * X_fine
            A_coarse[:] = A_coarse - 0.5 * h_coarse * X_coarse

        if calltype.name == "European":
            P_fine = numpy.maximum(0, X_fine - k)
            P_coarse = numpy.maximum(0, X_coarse - k)
        else:
            raise ValueError("Error: this program can execute only Eupopean type of call-option!")

        P_fine = numpy.exp(-r * time_option_expiration) * P_fine
        P_coarse = numpy.exp(-r * time_option_expiration) * P_coarse

        if l == 0:
            P_coarse = 0

        sums += numpy.array([numpy.sum(P_fine - P_coarse),
                             numpy.sum((P_fine - P_coarse)**2),
                             numpy.sum((P_fine - P_coarse)**3),
                             numpy.sum((P_fine - P_coarse)**4),
                             numpy.sum(P_fine),
                             numpy.sum(P_fine**2)])

        cost = M * n_fine # cost defined as number of fine timesteps

    return (numpy.array(sums), cost)

if __name__ == "__main__":
    M0 = 1000  # initial samples on coarse levels
    L_min = 2  # minimum refinement level
    L_max = 6  # maximum refinement level

    for (i, calltype) in enumerate(calltypes):
        def opre_l(l, N):
            return opre_gbm(l, N, calltype)

        filename = "opre_gbm" + str(i + 1) +  ".txt"
        #logfile = open(filename, "w")
        #mlmc_test(opre_l, calltype.M, calltype.L, M0, calltype.Eps, L_min, L_max, logfile)
        #del logfile
        mlmc_plot(filename, nvert=3)
        plt.savefig(filename.replace('.txt', '.png'), dpi=300)