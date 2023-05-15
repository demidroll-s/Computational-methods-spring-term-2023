import numpy as np

class WeakConvergenceFailure(Exception):
    pass

def mlmc(L_min, L_max, M0, eps, mlmc_fn, alpha_0, beta_0, gamma_0, *args, **kwargs):
    """
    Multilevel Monte Carlo estimation

    (P, Ml, Cl) = mlmc(...)

    Inputs:
        M0:   initial number of samples    >  0
        eps:  desired accuracy (rms error) >  0
        L_min: minimum level of refinement  >= 2
        L_max: maximum level of refinement  >= Lmin

        mlmc_fn: the user low-level routine for level l estimator. Its interface is

            (sums, cost) = mlmc_fn(l, N, *args, **kwargs)

            Inputs: 
                l: level
                N: number of paths
                *args, **kwargs: optional additional user variables

            Outputs: 
                sums[0]: sum(Y)
                sums[1]: sum(Y**2)
                where Y are iid samples with expected value
                    E[P_0]            on level 0
                    E[P_l - P_{l-1}]  on level l > 0
                cost: cost of N samples

        alpha ->  weak error is  O(2^{-alpha*l})
        beta  ->  variance is    O(2^{-beta*l})
        gamma ->  sample cost is O(2^{ gamma*l})

        If alpha, beta are not positive then they will be estimated.

        *args, **kwargs = optional additional user variables to be passed to mlmc_fn

    Outputs:
        P:  value
        Ml: number of Monte Carlo samples at each level l
        Cl: cost of Monte Carlo samples at each level
    """
    # 1 - Check arguments
    if L_min < 2:
        raise ValueError("Minimum level of refinement L_min should not be less than 2")
    if L_max < L_min:
        raise ValueError("Maximum level of refinement L_max should not be less than minimum level of refinement L_min")
    if M0 <= 0:
        raise ValueError("Initial number of Monte Carlo samples M0 should be higher than 0")
    if eps <= 0.0:
        raise ValueError("Desired accuacy eps should be higher than 0.0")

    # 2 - Initialisation procedure
    alpha = max(0, alpha_0)
    beta  = max(0, beta_0)
    gamma = max(0, gamma_0)

    theta = 0.25

    L_ref = L_min

    M_l = np.zeros(L_ref + 1)
    sum_l = np.zeros((2, L_ref + 1))
    cost_l = np.zeros(L_ref + 1)
    dM_l  = M0 * np.ones(L_ref + 1)

    while sum(dM_l) > 0:
        # Update sample sums
        for l in range(0, L_ref + 1):
            if dM_l[l] > 0:
                (sums, cost) = mlmc_fn(l, int(dM_l[l]), *args, **kwargs)
                M_l[l]        = M_l[l] + dM_l[l]
                sum_l[0, l]   = sum_l[0, l] + sums[0]
                sum_l[1, l]   = sum_l[1, l] + sums[1]
                cost_l[l]     = cost_l[l] + cost

        # Compute absolute average, variance and cost
        A_l = np.abs(sum_l[0, :] / M_l)
        V_l = np.maximum(0, sum_l[1, :] / M_l - A_l**2)
        C_l = cost_l / M_l

        # Fix to cope with possible zero values for m_l and V_l
        # (can happen in some applications when there are few samples)
        for l in range(3, L_ref + 2):
            A_l[l-1] = max(A_l[l-1], 0.5 * A_l[l-2] / 2**alpha)
            V_l[l-1] = max(V_l[l-1], 0.5 * V_l[l-2] / 2**beta)

        # Use linear regression to estimate alpha, beta, gamma if not given
        if alpha_0 <= 0:
            A = np.ones((L_ref, 2)); A[:, 0] = range(1, L_ref + 1)
            x = np.linalg.lstsq(A, np.log2(A_l[1:]))[0]
            alpha = max(0.5, -x[0])

        if beta_0 <= 0:
            A = np.ones((L_ref, 2)); A[:, 0] = range(1, L_ref + 1)
            x = np.linalg.lstsq(A, np.log2(V_l[1:]))[0]
            beta = max(0.5, -x[0])

        if gamma_0 <= 0:
            A = np.ones((L_ref, 2)); A[:, 0] = range(1, L_ref + 1)
            x = np.linalg.lstsq(A, np.log2(C_l[1:]))[0]
            gamma = max(0.5, x[0])

        # Set optimal number of additional samples
        M_s = np.ceil(np.sqrt(V_l / C_l) * sum(np.sqrt(V_l * C_l)) / ((1 - theta) * eps**2))
        dM_l = np.maximum(0, M_s - M_l)

        # If (almost) converged, estimate remaining error and decide
        # whether a new level is required

        if sum(dM_l > 0.01 * M_l) == 0:
            rang = list(range(min(3, L_ref)))
            rem = (np.amax(A_l[[L_ref - x for x in rang]] / 2.0**(np.array(rang)*alpha))
                    / (2.0**alpha - 1.0))
            # rem = ml[L] / (2.0**alpha - 1.0)

            if rem > np.sqrt(theta) * eps:
                if L_ref == L_max:
                    print(L_ref)
                    raise WeakConvergenceFailure("Failed to achieve weak convergence")
                else:
                    L_ref = L_ref + 1
                    V_l = np.append(V_l, V_l[-1] / 2.0**beta)
                    M_l = np.append(M_l, 0.0)
                    sum_l = np.column_stack([sum_l, [0, 0]])
                    C_l = np.append(C_l, C_l[-1] * 2**gamma)
                    cost_l = np.append(cost_l, 0.0)

                    M_s = np.ceil(np.sqrt(V_l / C_l) * sum(np.sqrt(V_l * C_l)) / ((1 - theta) * eps**2))
                    dM_l = np.maximum(0, M_s - M_l)

    # Finally, evaluate the multilevel estimator
    P = sum(sum_l[0,:] / M_l)

    return (P, M_l, C_l)