import timeit
from datetime import datetime
import numpy as np
from math import sqrt
import sys

from mlmc import mlmc

def mlmc_test(mlmc_fn, M, L, M0, Eps, L_min, L_max, logfile, *args, **kwargs):
    """
    Multilevel Monte Carlo test routine. Prints results to stdout and file.

    Inputs:
        mlmc_fn: the user low-level routine for level l estimator. Its interface is
            (sums, cost) = mlmc_fn(l, M, *args, **kwargs)

            Inputs:
                l: level
                M: number of samples
                *args, **kwargs: optional additional user variables

            Outputs: 
                sums[0]: sum(Y)
                sums[1]: sum(Y**2)
                sums[2]: sum(Y**3)
                sums[3]: sum(Y**4)
                sums[4]: sum(P_l)
                sums[5]: sum(P_l**2)
                where Y are iid samples with expected value
                    E[P_0]            on level 0
                    E[P_l - P_{l-1}]  on level l > 0
                cost: user-defined computational cost of N samples

        M:    number of samples for convergence tests
        L:    number of levels for convergence tests

        M0:   initial number of samples for MLMC calculations
        Eps:  desired accuracy (rms error) array for MLMC calculations
        L_min: minimum number of levels for MLMC calculations
        L_max: maximum number of levels for MLMC calculations

        logfile: file handle for printing to file
        *args, **kwargs: optional additional user variables to be passed to mlmc_fn
    """

    now = datetime.now().strftime("%d-%B-%Y %H:%M:%S")
    # First, convergence tests
    write(logfile, "\n");
    write(logfile, "**********************************************************\n")
    write(logfile, "***               Multilevel Monte Carlo               ***\n")
    write(logfile, "***   Python3 mlmc_test on %s   ***\n" % now )
    write(logfile, "**********************************************************\n")
    write(logfile, "\n")
    write(logfile, "**********************************************************\n")
    write(logfile, "*** Convergence tests, kurtosis, telescoping sum check ***\n")
    write(logfile, "*** using M = %7d samples                           **\n" % M)
    write(logfile, "**********************************************************\n")
    write(logfile, "\n l   average(P_fine-P_coarse)    average(P_fine)   var(P_fine-P_coarse)  var(P_fine)")
    write(logfile, "   kurtosis    check     cost\n-------------------------")
    write(logfile, "--------------------------------------------------------------------------------------------\n")

    del1 = []
    del2 = []
    var1 = []
    var2 = []
    kur1 = []
    chk1 = []
    cost = []

    for l in range(0, L + 1):
        (sums, cst) = mlmc_fn(l, M)
        cst = cst / M
        sums = sums / M

        if l == 0:
            kurt = 0.0
        else:
            kurt = (sums[3] - 4 * sums[2] * sums[0] + 6 * sums[1] * sums[0]**2 - 3 * sums[0] * sums[0]**3) / (sums[1] - sums[0]**2)**2

        cost.append(cst)
        del1.append(sums[0])
        del2.append(sums[4])
        var1.append(sums[1] - sums[0]**2)
        var2.append(max(sums[5] - sums[4]**2, 1.0e-10)) # fix for cases with var = 0
        kur1.append(kurt)

        if l == 0:
            check = 0
        else:
            check = abs(del1[l] + del2[l-1] - del2[l])
            check = check / (3.0 * (sqrt(var1[l]) + sqrt(var2[l-1]) + sqrt(var2[l])) / sqrt(M))
        chk1.append(check)

        write(logfile, "%2d  %11.4e %27.4e  %15.3e  %20.3e  %11.2e  %10.2e  %8.2e \n" % \
                      (l, del1[l], del2[l], var1[l], var2[l], kur1[l], chk1[l], cst))

    if kur1[-1] > 100.0:
        write(logfile, "\n WARNING: kurtosis on finest level = %f \n" % kur1[-1])
        write(logfile, " indicates MLMC correction dominated by a few rare paths. \n")

    if max(chk1) > 1.0:
        write(logfile, "\n WARNING: maximum consistency error = %f \n" % max(chk1))
        write(logfile, " indicates identity E[P_fine-P_coarse] = E[P_fine] - E[P_coarse] not satisfied; \n")
        write(logfile, " to be more certain, re-run mlmc_test with larger M \n\n")

    # Use linear regression to estimate alpha, beta and gamma
    L1 = 2
    L2 = L + 1
    pa = np.polyfit(range(L1 + 1, L2 + 1), np.log2(np.abs(del1[L1:L2])), 1)
    alpha = -pa[0]
    pb = np.polyfit(range(L1 + 1, L2 + 1), np.log2(np.abs(var1[L1:L2])), 1)
    beta  = -pb[0]
    pg = np.polyfit(range(L1 + 1, L2 + 1), np.log2(np.abs(cost[L1:L2])), 1)
    gamma =  pg[0]

    write(logfile, "\n******************************************************\n")
    write(logfile, "*** Linear regression estimates of MLMC parameters ***\n")
    write(logfile, "******************************************************\n")
    write(logfile, "\n alpha = %f  (exponent for MLMC weak convergence)\n" % alpha)
    write(logfile, " beta  = %f  (exponent for MLMC variance) \n" % beta)
    write(logfile, " gamma = %f  (exponent for MLMC cost) \n" % gamma)

    # Second, MLMC complexity tests
    write(logfile, "\n")
    write(logfile, "***************************** \n")
    write(logfile, "*** MLMC complexity tests *** \n")
    write(logfile, "***************************** \n\n")
    write(logfile, "eps        value       mlmc_cost  std_cost   savings      M_l: \n")
    write(logfile, "------------------------------------------------------------------------------------- \n")

    alpha = max(alpha, 0.5)
    beta  = max(beta, 0.5)
    theta = 0.25

    for eps in Eps:
       (P, M_l, C_l) = mlmc(L_min, L_max, M0, eps, mlmc_fn, alpha, beta, gamma, *args, **kwargs)
       l = len(M_l) - 1
       mlmc_cost = np.dot(M_l, C_l)
       std_cost  = var2[-1] * C_l[min(len(C_l) - 1, l)] / ((1.0 - theta) * eps**2)

       write(logfile, "%.3e %11.4e  %.3e  %.3e  %7.2f " % (eps, P, mlmc_cost, std_cost, std_cost / mlmc_cost))
       write(logfile, " ".join(["%9d" % n for n in M_l]))
       write(logfile, "\n")

    write(logfile, "\n")

def write(logfile, msg):
    """
    Write to both sys.stdout and to a logfile.
    """
    logfile.write(msg)
    sys.stdout.write(msg)