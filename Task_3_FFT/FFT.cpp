#include <iostream>
#include <vector>
#include <iterator>
#include <complex>
#include <cmath>

const double PI = 3.1415926536;

unsigned int BitReverse(unsigned int x, int log2n) {
    int n = 0;
    int mask = 0x1;
    for (int i = 0; i < log2n; i++) {
        n <<= 1;
        n |= (x & 1);
        x >>= 1;
    }
    return n;
}

template <typename Iter_T>
void FFT(Iter_T& a, Iter_T& b, int log2n) {
    const std::complex<double> J(0, 1);
    int n = 1 << log2n;
    for (unsigned int i = 0; i < n; ++i) {
        b[BitReverse(i, log2n)] = a[i];
    }
    for (int s = 1; s <= log2n; ++s) {
        int m = 1 << s;
        int m2 = m >> 1;
        std::complex<double> w(1, 0);
        std::complex<double> wm = exp(-J * (PI / m2));
        for (int j = 0; j < m2; ++j) {
            for (int k = j; k < n; k += m) {
                std::complex<double> t = w * b[k + m2];
                std::complex<double> u = b[k];
                b[k] = u + t;
                b[k + m2] = u - t;
            }
            w *= wm;
        }
    }
}

int main() {
    typedef std::complex<double> cx;
    std::vector<cx> a = { cx(0,0), cx(1,1), cx(3,3), cx(4,4), cx(4, 4), cx(3, 3), cx(1,1), cx(0,0) };
    std::vector<cx> b;
    b.resize(8);

    FFT(a, b, 3);
    for (int i=0; i<8; ++i) {
        std::cout << b[i] << std::endl;
    }

    return 0;  
}