def tridiag(a, b, c):
    """
    Строит матрицу по трем данным диагоналям
    :param a: под главной (size = n-1)
    :param b: главная (size = n)
    :param c: над главной (size = n-1)
    :return: матрица (n x n)
    """
    return np.diag(a, k=-1) + np.diag(b, k=0) + np.diag(c, k=1)


def progonka(a, b, c, f):
    """
    Метод прогонки
    :param a: диагональ, лежащая под главной (size = n-1)
    :param b: главная диагональ (size = n)
    :param c: диагональ, лежащая над главной (size = n-1)
    :param f: вектор свободных членов (size = n)
    :return: вектор неизвестых y
    """
    n = len(f)
    alpha = np.zeros(n-1)
    beta = np.zeros(n)
    alpha[0] = c[0] / b[0]
    beta[0] = f[0] / b[0]

    # прямая прогонка
    for i in range(1, n-1):
        alpha[i] = c[i] / (b[i] - a[i-1]*alpha[i-1])
        beta[i] = (f[i] - a[i-1]*beta[i-1]) / (b[i] - a[i-1]*alpha[i-1])
    
    beta[n-1] = (f[n-1] - a[-1]*beta[n-2]) / (b[n-1] - a[-1]*alpha[-1])
    
    # обратная прогонка
    y = np.zeros(n)
    y[-1] = beta[-1]
    
    for i in range(n-2, -1, -1):
        y[i] = beta[i] - alpha[i] * y[i+1]
        
    return y




def test():
    a = np.array([3, 1, 3]) 
    b = np.array([10, 10, 7, 4])
    c = np.array([2, 4, 5])
    d = np.array([3, 4, 5, 6])
    
    
    Matrix = np.array([])

