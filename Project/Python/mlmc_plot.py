import matplotlib.pyplot as plt
import numpy as np
import os
import re
from cycler import cycler

import seaborn as sns
sns.set()

plt.rcParams['text.usetex'] = True

def mlmc_plot(filename, nvert, error_bars=False):
    """
    Utility to generate MLMC diagnostic plots based on
    input text file generated by MLMC driver code mlmc_test.

    mlmc_plot(filename, nvert, error_bars=False)

    Inputs:
        filename: string, (base of) filename with output from mlmc_test routine
        nvert   : int, number of vertical plots <= 3
                    nvert == 1   generates fig1: (1),(2) fig2: (5),(6)
                    nvert == 2   generates fig1: (1),(2),(5),(6)
                    nvert == 3   generates fig1: (1)-(6)
      error_bars: bool, flag to add error bars in plots of level differences

    Outputs:
        Matplotlib figure(s) for
            Convergence tests
            (1) Var[P_l - P_{l-1}] per level
            (2) E[|P_l - P_{l-1}|] per level
            (3) cost per level
            (4) kurtosis per level
        Complexity tests
            (5) number of samples per level
            (6) normalised cost per accuracy target
    """

    # 1 - Read data from .txt file
    # Default file extension is .txt if none supplied
    if not os.path.splitext(filename)[1]:
        file = open(filename + ".txt", "r")
    else:
        file = open(filename, "r")

    # Declare lists for data
    del1 = []
    del2 = []
    var1 = []
    var2 = []
    kur1 = []
    chk1 = []
    cost = []
    l    = []

    epss = []
    mlmc_cost = []
    std_cost = []
    M_s = []
    l_s = []

    # Default values for number of samples and file_version
    M = 0

    complexity_flag = False # first read convergence tests rather than complexity tests
    for line in file:
        # Recognise number of samples line from the fact that it starts with '*** using'
        if line[0:9] == '*** using':
            numbers_in_line = [int(s) for s in re.findall(r'\b\d+\b', line)]
            M = numbers_in_line[0]

        # Recognise whether we should switch to reading complexity tests
        if line[0:19] == '*** MLMC complexity':
            complexity_flag = True # now start to read complexity tests

        # Recognise MLMC complexity test lines from the fact that line[0] is an integer
        # Also need complexity_flag == True because line[0] is an integer also identifies
        # the convergence test lines
        if '0' <= line[0] <= '9' and complexity_flag:
            splitline = [float(x) for x in line.split()]
            epss.append(splitline[0])
            mlmc_cost.append(splitline[2])
            std_cost.append(splitline[3])
            M_s.append(splitline[5:])
            l_s.append(list(range(0,len(splitline[5:]))))

        # Recognise convergence test lines from the fact that line[1] is an integer
        # and possibly also line[0] (or line[0] is whitespace)
        if (line[0] == ' ' or '0' <= line[0] <= '9') and '0' <= line[1] <= '9':
            splitline = [float(x) for x in line.split()]
            l.append(splitline[0])
            del1.append(splitline[1])
            del2.append(splitline[2])
            var1.append(splitline[3])
            var2.append(splitline[4])
            kur1.append(splitline[5])
            chk1.append(splitline[6])
            cost.append(splitline[7])
            continue

    # Compute variance of variance ( correct up to O(1/N) )
    if (error_bars):
        vvr1 = [ v**2 * (kur - 1.0) for (v, kur) in zip(var1, kur1)]

    # 2 - Plot figures

    # Fudge to get comparable size to default MATLAB fig size
    fig, axes = plt.subplots(2, 2, figsize = (10, 8))
    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.3,
                        hspace=0.4)

    # 2.1 - Var[P_l - P_{l-1}] per level
    axes[0][0].plot(l, np.log2(var2), label=r'$\widehat{P}_{l}$', lw=1.0, color='darkblue')
    axes[0][0].scatter(l, np.log2(var2), color='darkblue', s=15)
    axes[0][0].plot(l[1:], np.log2(var1[1:]), label=r'$\widehat{P}_{l} - \widehat{P}_{l-1}$', lw=1.0, color='sienna')
    axes[0][0].scatter(l[1:], np.log2(var1[1:]), color='sienna', s=15)
    
    axes[0][0].set_xlabel(r'level $l$', size=12)
    axes[0][0].set_ylabel(r'$\log_2($variance$)$', size=12)
    axes[0][0].set_title(r'Variances of $\widehat{P}_{l}$ and $\widehat{P}_{l}$ - $\widehat{P}_{l - 1}$', size=14)
    axes[0][0].set_xticks(range(0, int(max(l)) + 1), [fr'${i}$' for i in range(0, int(max(l)) + 1)])
    axes[0][0].legend(loc='lower left', fontsize='medium')

    """
    if (error_bars):
        print('True')
        plt.plot(l[1:], np.log2(np.maximum(np.abs(np.array(var1[1:]) -
            3.0 * np.sqrt(vvr1[1:])/np.sqrt(M)), 1e-10)), '-r.', clip_on=False)
        plt.plot(l[1:], np.log2(np.abs(np.array(var1[1:]) +
            3.0 * np.sqrt(vvr1[1:])/np.sqrt(M))), '-r.', clip_on=False)
    """

    # 2.2 - E[|P_l - P_{l-1}|] per level
    axes[0][1].plot(l, np.log2(np.abs(del2)), label=r'$\widehat{P}_{l}$', lw=1.0, color='darkblue')
    axes[0][1].scatter(l, np.log2(np.abs(del2)), color='darkblue', s=15)
    axes[0][1].plot(l[1:], np.log2(np.abs(del1[1:])), label=r'$\widehat{P}_{l} - \widehat{P}_{l-1}$', lw=1.0, color='sienna')
    axes[0][1].scatter(l[1:], np.log2(np.abs(del1[1:])), color='sienna', s=15)
    
    axes[0][1].set_xlabel(r'level $l$', size=12)
    axes[0][1].set_ylabel(r'$\log_2(|$average$|)$', size=12)
    axes[0][1].set_title(r'Averages of $|\widehat{P}_{l}$ - $\widehat{P}_{l - 1}|$', size=14)
    axes[0][1].set_xticks(range(0, int(max(l)) + 1), [fr'${i}$' for i in range(0, int(max(l)) + 1)])
    axes[0][1].legend(loc='lower left', fontsize='medium')
    
    """
    if (error_bars):
        plt.plot(l[1:], numpy.log2(numpy.maximum(numpy.abs(numpy.array(del1[1:]) -
            3.0*numpy.sqrt(var1[1:])/numpy.sqrt(N)), 1e-10)), '-r.', clip_on=False)
        plt.plot(l[1:], numpy.log2(              numpy.abs(numpy.array(del1[1:]) +
            3.0*numpy.sqrt(var1[1:])/numpy.sqrt(N))        ), '-r.', clip_on=False)
    """
    
    # 2.3 - number of samples per level
    colors = ['purple', 'darkblue', 'mediumblue', 'blue', 'royalblue']
    color_idx = 0
    for eps, l_l, m in zip(epss, l_s, M_s):
         axes[1][0].plot(l_l, m, label= r'$\varepsilon = $ {:.1e}'.format(eps), lw=1.0, color=colors[color_idx])
         axes[1][0].scatter(l_l, m, s=15, color=colors[color_idx])
         color_idx += 1
    
    
    axes[1][0].set_yscale('log', base=10)
    axes[1][0].set_xlabel(r'level $l$', size=14)
    axes[1][0].set_ylabel(r'$M_l$', size=14)
    axes[1][0].set_title(r'Number of MLMC samples $M_l$ for different $\varepsilon$', size=14)
    axes[1][0].set_xticks(range(0, int(max(l)) + 1), [fr'${i}$' for i in range(0, int(max(l)) + 1)])
    axes[1][0].legend(loc='upper right', frameon=True, fontsize='small')

    # 2.4 - normalised cost for given accuracy
    eps = np.array(epss)
    std_cost = np.array(std_cost)
    mlmc_cost = np.array(mlmc_cost)
    idx_sorted = np.argsort(eps)

    axes[1][1].plot(eps[idx_sorted], eps[idx_sorted]**2 * std_cost[idx_sorted], label=r'standard MC', lw=1.0, color='darkblue')
    axes[1][1].scatter(eps[idx_sorted], eps[idx_sorted]**2 * std_cost[idx_sorted], s=15, color='darkblue')
    axes[1][1].plot(eps[idx_sorted], eps[idx_sorted]**2 * mlmc_cost[idx_sorted], label=r'MLMC', lw=1.0, color='sienna')
    axes[1][1].scatter(eps[idx_sorted], eps[idx_sorted]**2 * mlmc_cost[idx_sorted], s=15, color='sienna')
    
    axes[1][1].set_ylim(min(eps[idx_sorted]**2 * mlmc_cost[idx_sorted]) / 5, max(eps[idx_sorted]**2 * std_cost[idx_sorted]) * 5)
    axes[1][1].set_xscale('log', base=10)
    axes[1][1].set_yscale('log', base=10)
    axes[1][1].set_xlabel(r'accuracy $\varepsilon$', size=14)
    axes[1][1].set_ylabel(r'$\varepsilon^2$ cost', size=14)
    axes[1][1].set_title(r'Normalized cost for standard MC and MLMC', size=14)
    axes[1][1].legend(fontsize='medium')