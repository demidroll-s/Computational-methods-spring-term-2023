from numpy import random, zeros, array
from numpy import sum as npsum
from time import time

def mlmc_fn(l, M, problems, coupled_problem=False, sampler=None, concurency_factor=1):
    """
    Inputs:
        l: level
        M: number of Monte Carlo paths
        problems: list of problems
            problems[l-1]: application-specific coarse problem (for l > 0)
            problems[l]: application-specific fine problem 
            Problems must have an evaluate method such that
            problems[l].evaluate(sample) returns output P_l.
            Optionally, user-defined problems.cost
        coupled_problem: if True,
             problems[l].evaluate(sample) returns both P_l and P_{l-1}.
        sampler: sampling function, by default standard Normal.
            input: N, l
            output: (samplef, samplec). The fine and coarse samples.
        M1: number of paths to generate concurrently.

    Outputs:
        (sums, cost) where sums is an array of outputs:
        sums[0] = sum(P_fine-P_coarse)
        sums[1] = sum((P_fine-P_coarse)**2)
        sums[2] = sum((P_fine-P_coarse)**3)
        sums[3] = sum((P_fine-P_coarse)**4)
        sums[4] = sum(P_fine)
        sums[5] = sum(P_fine**2)
        cost = user-defined computational cost. By default, time
    """

    if sampler is None:
        def sampler(M, l):
            sample = random.randn(M)
            return (sample, sample)

    sums = zeros(6)
    cpu_cost = 0.0
    problem_fine = problems[l]
    if l > 0:
        problem_coarse = problems[l-1]

    for i in range(1, M + 1, concurency_factor):
        m2 = min(concurency_factor, M - i + 1)

        sample_fine, sample_coarse = sampler(m2, l)

        start = time()
        if coupled_problem:
            P_fine, P_coarse = problems[l].evaluate(sample_fine) 
        else:
            P_fine = problem_fine.evaluate(sample_fine)
            if l == 0:
                P_coarse = 0.
            else:
                P_coarse = problem_coarse.evaluate(sample_coarse)
            
        end = time()
        cpu_cost += end - start # cost defined as total computational time
        sums += array([npsum(P_fine - P_coarse),
                       npsum((P_fine - P_coarse)**2),
                       npsum((P_fine - P_coarse)**3),
                       npsum((P_fine - P_coarse)**4),
                       npsum(P_fine),
                       npsum(P_fine**2)])

    problem_cost_defined = hasattr(problem_fine, 'cost')
    problem_cost_defined = problem_cost_defined and problem_fine.cost is not None

    if problem_cost_defined:
        cost = M * problem_fine.cost
        if l > 0:
            cost += M * problem_coarse.cost # user-defined problem-specific cost
    else:
        cost = cpu_cost

    return (sums, cost)