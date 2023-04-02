# from TDMA import progonka, tridiag
# import numpy as np

# L = 4  # граница по координате
# t_max = 1  # граница по времени

# h = 1e-2  # шаг по координате 
# tau = 1e-3  # шаг по времени

# # k = 0.5  # g(x, t) = k * U^alpha
# # alpha = 5

# n_x = int(L / h) + 1
# n_t = int(t_max / tau) + 1
# u = np.zeros((n_t, n_x))



# Q = np.zeros((n_t, n_x))  # создается полностью заполненным


# # grid initialization
# x = np.zeros(n_x)
# t = np.zeros(n_t)

# # grid x
# for i in range(len(x)):
#     x[i] = i * h
    
# # grid t
# for i in range(len(t)):
#     t[i] = i * tau
    
    
    
# def T_x_0(x):
#     """Начальное условие T(x, 0)"""
#     return 1 + np.exp((-(x-2)**2) / 0.1)

# def T_0_t(t):
#     """
#     Граничное условие слева T(0, t)
#     """
#     return 1

# def T_x_max_t(t):
#     """
#     Граничное условие справа T(x_max, t)
#     """
#     return 1



# def set_Lambda(u):
#     """Штука под правым дифференциалом"""
#     return 5 * u




# u[0] = T_x_0(x)  # начальное условие


# u[:, 0] = T_0_t(t)  # граничные условия слева

# u[:, -1] = T_x_max_t(t)  # граничные условия справа

  
# Lambda = set_Lambda(u)



# for n in range(0, n_t-1):
    
#     A = np.zeros(n_x)
#     B = np.zeros(n_x)
#     C = np.zeros(n_x)
#     F = np.zeros(n_x)
    
#     Lambda = set_Lambda(u)  # обязательно пересчитывать Lambda, если она зависит от u !!!!
    
#     for i in range(1, n_x-1):
#         A[i] = (1/(h**2)) * ((Lambda[n, i] + Lambda[n, i+1]) / 2)
#         B[i] = (1/(h**2)) * ((Lambda[n, i] + Lambda[n, i-1]) / 2)
#         C[i] = A[i] + B[i] + (1 / tau)
        
#         F[i] = Q[n, i] + (u[n, i] / tau)
        
#     A = A[1:]  # выкидываем ненужный
#     A[-1] = 0  # дополнение граничными условиями
    
#     C[0] = 1  # дополнение граничными условиями
#     C[-1] = 1  # дополнение граничными условиями
    
#     B[0] = 0  # дополнение граничными условиями
#     B = B[:-1]  # выкидываем ненужный
    
#     F[0] = T_0_t(t)  # граничные условия слева
#     F[-1] = T_x_max_t(t)  # граничные условия справа
    
# #     Matrix = tridiag(-A, C, -B)
# #     u[n+1] = np.linalg.solve(Matrix, F)
    
#     u[n+1] = progonka(-A, C, -B, F)
    

