import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from celluloid import Camera


def Euler_explicit(u_prev, u_temp, u_next, a_prev, a_temp, a_next, q_temp, dx, dt):
    a_minus = (a_prev + a_temp) / 2
    a_plus = (a_temp + a_next) / 2
    u_new = dt / (dx ** 2) * (a_plus * u_next - (a_plus + a_minus) * u_temp + a_minus * u_prev) + dt * q_temp + u_temp
    return u_new


def explicit_method(U, Q, N, M, var):
    for t in range(0, M - 1):
        if var == 2:
            for x in range(N):
                a[x] = coef_a(U[t][x])
        for x in range(1, N - 1):
            U[t + 1][x] = Euler_explicit(U[t][x - 1], U[t][x], U[t][x + 1], a[x - 1], a[x], a[x + 1], Q[t][x], dx, dt)

    return U


def implicit_method(U, Q, N, M, var):
    for t in range(M - 1):

        A = np.zeros(N)
        B = np.zeros(N)
        C = np.zeros(N)
        F = np.zeros(N)

        alpha = np.zeros(N - 1)
        beta = np.zeros(N - 1)
        if var == 2:
            for x in range(N):
                a[x] = coef_a(U[t][x])

        for x in range(N):
            if x == 0:
                a_minus = a[x]
            else:
                a_minus = (a[x - 1] + a[x]) / 2
                A[x] = - a_minus / dx ** 2

            if x == N - 1:
                a_plus = a[x]
            else:
                a_plus = (a[x + 1] + a[x]) / 2
                C[x] = - a_plus / dx ** 2

            B[x] = (1 / dt + (a_minus + a_plus) / dx ** 2)

            F[x] = Q[t][x] + U[t][x] / dt

        alpha[0] = 0
        beta[0] = U[t + 1][0]

        for x in range(1, N - 1):
            alpha[x] = - C[x] / (A[x] * alpha[x - 1] + B[0])
            beta[x] = (F[x] - A[x] * beta[x - 1]) / (A[x] * alpha[x - 1] + B[0])

        for x in range(N - 2, -1, -1):
            U[t + 1][x] = alpha[x] * U[t + 1][x + 1] + beta[x]
    return U


def plot_2d(U):  # построить график температуры в стержне от каждого момента времени
    fig = plt.figure(figsize=(10, 8))
    ax = sns.heatmap(U.T, square=True)
    ax.invert_xaxis()
    plt.xlim(0, U.shape[0])
    plt.ylim(0, U.shape[1])

    plt.xlabel("Время t")
    plt.ylabel("Координата x")

    ax.set_xticks(np.arange(0, U.shape[0], 0.01))
    ax.set_yticks(np.arange(0, U.shape[1], 0.01))

    plt.show()

def printer(U, title, file_name, N, M, x0, xmax):  # построить гифку температуры в стержне от времени
    fig = plt.figure(figsize=(10, 6))
    plt.title(title, fontsize=15)
    plt.xlabel("Значение координаты")
    plt.ylabel("Температура")
    ax = fig.gca()
    plt.grid()
    camera = Camera(fig)
    for t in range(M):
        plt.plot(np.linspace(x0, xmax, N), U[t], "-", color='blue')
        camera.snap()
    animation = camera.animate()
    animation.save(file_name, writer = 'imagemagick')
    return 0

def initial_values(var, N, M):
    C1 = np.array([50.0 for x in range(N)])
    C2 = np.array([160.0 for t in range(M)])
    C3 = np.array([570.0 for t in range(M)])
    C_Q = np.array([30.0 for t in range(M)])
    x1 = 0.1

    def f(M):
        return np.linspace(80.0, 310.0, num=M)

    def g(M):
        return np.linspace(0.0, 50.0, num=M)

    match var:
        case 1:
            return C1, C2, C3, None, None
        case 2:
            return C1, f(M), C3, None, None
        case 3:
            return C1, C2, C3, C_Q, x1
        case 4:
            return C1, C2, C3, g(M), x1


def initial_values_lam(var_coef, N):
    match var_coef:
        case 1:  # коэффициент теплопроводности в случае 1
            return np.random.randint(40, 50, N)
        case 2:  # коэффициент теплопроводности в случае 2 пересчитывается на каждом новом слое по времени
            return np.zeros(N)

def coef_a(T):
    a = 1 / 100
    b = 20
    return (T * a + b) / (c * ro)


if __name__ == '__main__':

    x0, xmax = 0.0, 0.2  # координата начала и конца стержня
    t0, tmax = 0.0, 60.0  # время начала и конца расчетов
    dx, dt = 0.01, 3.0  # шаг по координате, шаг по времени
    N, M = int((xmax - x0) / dx), int((tmax - t0) / dt)  # количество шагов по координате и по времени

    ##################################################################
    var = 1  # выбери начальные значения
    ##################################################################

    T_t0, T_x0, T_xmax, Q_x1, x1 = initial_values(var, N, M)
    Q = np.array([np.array([0.0 for x in range(N)]) for t in range(M)])  # источник
    for t in range(M):
        if (x1 != None):
            Q[t][int((x1 - x0) / dx)] = Q_x1[t]

    ##################################################################
    var_coef = 1  # выбери значение для коэффициента теплопроводности
    ##################################################################

    lam = initial_values_lam(var_coef, N)  # стальной стержень
    c = 460  # Теплоемкость
    ro = 7800  # Плотность

    a = np.zeros(N)
    for x in range(N):
        a[x] = lam[x] / (c * ro)

    U = np.array([np.array([0.0 for x in range(N)]) for t in range(M)])  # сетка

    for x in range(N):  # НУ
        U[0][x] = T_t0[x]

    for t in range(M):
        U[t][0] = T_x0[t]  # ГУ
        U[t][N - 1] = T_xmax[t]  # ГУ

    U1 = np.array([np.array([0.0 for x in range(N)]) for t in range(M)])
    U1 = explicit_method(U, Q, N, M, var_coef)  # Решение явной схемой
    printer(U1, "Изменение температуры стержня, явная схема\nНачальные значения: случай " + str(var) + "\nКоэффициент теплопроводности: случай " + str(var_coef),
            "Temp_explicit_values_" + str(var) + "_coef_" + str(var_coef) + ".gif", N, M, x0, xmax)
    #plot_2d(U1)

    U2 = np.array([np.array([0.0 for x in range(N)]) for t in range(M)])
    U2 = implicit_method(U, Q, N, M, var_coef)  # Решение неявной схемой
    printer(U2, "Изменение температуры стержня, неявная схема\nНачальные значения: случай " + str(var) + "\nКоэффициент теплопроводности: случай " + str(var_coef),
            "Temp_implicit_values_" + str(var) + "_coef_" + str(var_coef) + ".gif", N, M, x0, xmax)
    # plot_2d(U2)