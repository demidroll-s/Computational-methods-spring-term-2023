import random

import numpy as np
import matplotlib.pyplot as plt

def plot(x, t, T):
    x = np.array(x)
    t = np.array(t)
    X, Yt = np.meshgrid(x, t)
    T = np.array(T)


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Yt, T)


    ax.set_xlabel('x')
    ax.set_ylabel('t')
    ax.set_zlabel('T')

    # Add a title for the plot
    plt.title('Temp 3D graph')

    # Display the plot
    plt.show()

def solver(case=1, scheme_type='explicit', alpha_tempurature_dependency=False, plot_key=False, result_in_x_key=False, x1=0):
    """
    Вроде соотвествует запросу из дз
    :param case: четыре варианта условий (согласно дз) и их нужно править в самом коде
    :param scheme_type: есть две схемы (согласно дз)
    :param alpha_tempurature_dependency: зависит ли альфа от температуры линейно или нет?
    :param plot_key: строить график или нет?
    :param result_in_x_key: возвращать все решение или только в точке x1?
    :param x1: точка нашего особого интереса
    :return: зависит от ключа result_in_x_key и возвращает приведенные температуры (может все вернуть или точку)
    """
    fun = __solver
    x, t, T = fun(scheme_type, case, alpha_tempurature_dependency, x1)
    if plot_key == True:
        plot(x, t, T)
    if result_in_x_key == False:
        return T
    else:
        x = np.array(x)
        index = np.where(x == x1)
        T = np.array(T)
        return T[:, index]


def __solver(scheme_type, case, alpha_tempurature_dependency, x):
    """
    Вспомогательная функция, выполняет всю работу в плане расчетов
    :param scheme_type: есть две схемы (согласно дз)
    :param case: четыре варианта условий (согласно дз) и их нужно править в самом коде
    :param alpha_tempurature_dependency: зависит ли альфа от температуры линейно или нет?
    :param x: точка нашего особого интереса (приведенная)
    :return: зависит от ключа result_in_x_key и возвращает приведенные температуры (может все вернуть или точку)
    """
    if alpha_tempurature_dependency == True:
        delta_alpha = 0.000000001

    h = 0.01
    t = 0.00001

    array_x = [0 + i * h for i in range(int(1 / h) + 1)]
    if x not in array_x:
        array_x.append(x)
    array_x.sort()
    array_t = [0 + i * t for i in range(10000)]


    size_x = len(array_x)
    size_t = len(array_t)

    result = list()

 # что-то по условиям нужно менять здесь, они уже приведенные
    if case == 1:
        T_x_0 = 0
        T_0_t = 1
        T_1_t = 0.8
    elif case == 2:
        T_x_0 = 0
        T_0_t_start_point = 1
        delta_T = 0.0001
        T_1_t = 0.8
    elif case == 3:
        T_x_0 = 0
        T_0_t = 1
        T_1_t = 0.8
        x1 = 0.2
        Q_x1 = 0.5
    elif case == 4:
        T_x_0 = 0
        T_0_t = 1
        T_1_t = 0.8
        Q_start_point = 0.1
        delta_Q = 0.0000001

    if scheme_type == 'explicit':
        for count_t in range(size_t):
            if count_t == 0:
                if case == 1 or case == 2 or case == 3 or case == 4:
                    U_0 = [T_x_0 for i in range(size_x)]
                    result.append(U_0)
                if alpha_tempurature_dependency == True:
                    list_alpha_start = [random.random() for i in range(size_x)]
            else:
                # эти два массива представляют собой текущие значения и прошлые
                U_pres = list()
                U_prev = result[count_t-1]
                for count_x, value_x in enumerate(array_x):
                    if count_x == 0:
                        if case == 1 or case == 3 or case == 4:
                            U_pres.append(T_0_t)
                        elif case == 2:
                            U_pres.append(T_0_t_start_point + count_t * delta_T)
                    elif count_x != 0 and count_x != size_x - 1:
                        if case == 4:
                            Q = Q_start_point + delta_Q * count_t
                        elif case != 3 or value_x != x1:
                            Q = random.random()
                        else:
                            Q = Q_x1
                        if alpha_tempurature_dependency == False:
                            alpha_plus = random.random()
                            alpha_minus = random.random()
                        else:
                            alpha_plus = (list_alpha_start[count_x] + list_alpha_start[count_x + 1]) / 2 + delta_alpha
                            alpha_minus = (list_alpha_start[count_x] + list_alpha_start[count_x - 1]) / 2 + delta_alpha

                        u_pres_k = (U_prev[count_x] + t / h ** 2 * (alpha_plus * U_prev[count_x + 1]
                                                                    - (alpha_minus + alpha_plus) * U_prev[count_x]
                                                                    + alpha_minus * U_prev[count_x - 1]) + t * Q)
                        U_pres.append(u_pres_k)
                    if count_x == size_x - 1:
                        U_pres.append(T_1_t)
                result.append(U_pres)
    if scheme_type == 'implicit':
        for count_t in range(size_t):
            if count_t == 0:
                if case == 1 or case == 2 or case == 3 or case == 4:
                    U_0 = [T_x_0 for i in range(size_x)]
                    result.append(U_0)
                if alpha_tempurature_dependency == True:
                    list_alpha_start = [random.random() for i in range(size_x)]
            else:
                U_pres = list()
                U_prev = result[count_t - 1]
                alpha_k_list = list()
                beta_k_list = list()
                for count_x, value_x in enumerate(array_x):
                    if count_x == 0:
                        if case == 1 or case == 3 or case == 4:
                            U_pres.append(T_0_t)
                        elif case == 2:
                            U_pres.append(T_0_t_start_point + count_t * delta_T)
                        beta_0 = T_0_t if case != 2 else T_0_t_start_point + count_t * delta_T
                        alpha_0 = 0
                        alpha_k_list.append(alpha_0)
                        beta_k_list.append(beta_0)
                    elif count_x != 0 and count_x != size_x - 1:
                        if alpha_tempurature_dependency == False:
                            alpha_plus = random.random()
                            alpha_minus = random.random()
                        else:
                            alpha_plus = (list_alpha_start[count_x] + list_alpha_start[count_x + 1]) / 2 + delta_alpha
                            alpha_minus = (list_alpha_start[count_x] + list_alpha_start[count_x - 1]) / 2 + delta_alpha
                        if case == 4:
                            Q = Q_start_point + delta_Q * count_t
                        elif case != 3 or value_x != x1:
                            Q = random.random()
                        else:
                            Q = Q_x1
                        Ak = t / h ** 2 * alpha_minus
                        Ck = t / h ** 2 * alpha_plus
                        Bk = - 1 - t / h ** 2 * (alpha_plus + alpha_minus)
                        Fk = - t * Q - U_prev[count_x]
                        alpha_k = - Ck / (Ak * alpha_k_list[-1] + Bk)
                        beta_k = (Fk - Ak * beta_k_list[-1]) / (Ak * alpha_k_list[-1] + Bk)
                        alpha_k_list.append(alpha_k)
                        beta_k_list.append(beta_k)
                reversed_u_pres = list()
                for count_x in reversed(range(size_x)):
                    if count_x == size_x - 1:
                        reversed_u_pres.append(T_1_t)
                    else:
                        u_pres_k = alpha_k_list[count_x] * reversed_u_pres[-1] + beta_k_list[count_x]
                        reversed_u_pres.append(u_pres_k)
                reversed_u_pres.reverse()
                result.append(reversed_u_pres)


    return array_x, array_t, result


solver(case=1, scheme_type='explicit', alpha_tempurature_dependency=True, plot_key=True, result_in_x_key=False, x1=0)
solver(case=1, scheme_type='implicit', alpha_tempurature_dependency=True, plot_key=True, result_in_x_key=False, x1=0)

