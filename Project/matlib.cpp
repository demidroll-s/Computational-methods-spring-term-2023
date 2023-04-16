#include "matlib.h"

std::vector<double> LinSpace(double start, double finish, size_t n_points) {
    assert(n_points >= 2);
    
    std::vector<double> v(n_points, 0);
    double step = (start - finish) / (n_points - 1);
    double current = start;
    for (size_t i = 0; i < n_points; ++i) {
        v[i] = current;
        current += step;
    }

    return v;
}

double Sum(const std::vector<double>& v) {
    double total = 0.0;
    for (size_t i = 0; i < v.size(); ++i) {
        total += v[i];
    }

    return total;
}

double Mean(const std::vector<double>& v) {
    size_t n = v.size();
    assert(n > 0);
    return Sum(v) / n;
}

double Min(const std::vector<double>& v) {
    size_t n = v.size();
    assert(n > 0);
    double min = v[0];
    for (size_t i = 0; i < n; ++i) {
        if (v[i] < min)
            min = v[i];
    }
    return min;
}

double StandardDeviation(const std::vector<double>& v, bool unbiasedness) {
    int n = v.size();
    double total = 0.0;
    double total_sqr = 0.0;

    for (size_t i = 0; i < n; ++i) {
        total += v[i];
        total_sqr += v[i] * v[i];
    }

    if (!unbiasedness) {
        assert(n > 0);
        return sqrt((total_sqr - total * total / n) / n);
    }
    else {
        assert(n > 1);
        return sqrt((total_sqr - total * total / n) / (n - 1));
    }
}

double Max(const std::vector<double>& v) {
    size_t n = v.size();
    assert(n > 0);
    double max = v[0];
    for (size_t i = 0; i < n; ++i) {
        if (v[i] > max)
            max = v[i];
    }
    return max;
}

void RandNumberGenerator(const std::string& description) {
    assert(description == "default");
    
    mersenne_twister.seed(std::mt19937::default_seed);    
}

std::vector<double> RandUniform(const size_t n) {
    std::vector<double> v(n, 0.0);
    for (size_t i = 0; i < n; ++i) {
        v[i] = (mersenne_twister() + 0.5) / (mersenne_twister.max() + 1.0);
    }
    
    return v;
}

std::vector<double> RandNormal(const size_t n) {
    std::vector<double> v = RandUniform(n);
    for(size_t i = 0; i < n; ++i) {
        v[i] = NormInv(v[i]);
    }

    return v;
}

static inline double Horner(double x, double a0, double a1) {
    return a0 + x * a1;
}

static inline double Horner(double x, double a0, double a1, double a2) {
    return a0 + x * Horner(x, a1, a2);
}

static inline double Horner(double x, double a0, double a1, double a2, double a3) {
    return a0 + x * Horner(x, a1, a2, a3);
}

static inline double Horner(double x, double a0, double a1, double a2, double a3, 
    double a4) {
    return a0 + x * Horner(x, a1, a2, a3, a4);
}

static inline double Horner(double x, double a0, double a1, double a2, double a3, 
    double a4, double a5) {
    return a0 + x * Horner(x, a1, a2, a3, a4, a5);
}

static inline double Horner(double x, double a0, double a1, double a2, double a3, 
    double a4, double a5, double a6) {
    return a0 + x * Horner(x, a1, a2, a3, a4, a5, a6);
}

static inline double Horner(double x, double a0, double a1, double a2, double a3, 
    double a4, double a5, double a6, double a7) {
    return a0 + x * Horner(x, a1, a2, a3, a4, a5, a6, a7);
}

static inline double Horner(double x, double a0, double a1, double a2, double a3, 
    double a4, double a5, double a6, double a7, double a8) {
    return a0 + x * Horner(x, a1, a2, a3, a4, a5, a6, a7, a8);
}

/* Constants required for Moro's algorithm */
static const double a0 = 2.50662823884;
static const double a1 = -18.61500062529;
static const double a2 = 41.39119773534;
static const double a3 = -25.44106049637;
static const double b1 = -8.47351093090;
static const double b2 = 23.08336743743;
static const double b3 = -21.06224101826;
static const double b4 = 3.13082909833;
static const double c0 = 0.3374754822726147;
static const double c1 = 0.9761690190917186;
static const double c2 = 0.1607979714918209;
static const double c3 = 0.0276438810333863;
static const double c4 = 0.0038405729373609;
static const double c5 = 0.0003951896511919;
static const double c6 = 0.0000321767881768;
static const double c7 = 0.0000002888167364;
static const double c8 = 0.0000003960315187;

double NormCdf(double x) {
    if (x < 0)
        return 1 - NormCdf(-x);
    double k = 1 / (1 + 0.2316419 * x);
    double poly = Horner(k, 0.0, 0.319381530, -0.356563782, 1.781477937, -1.821255978, 1.330274429);
    double approx = 1.0 - 1.0 / sqrt(2 * M_PI) * exp(-0.5 * x * x) * poly;
    return approx;
}

double NormInv(const double x) {
    double y = x - 0.5;
    if (y < 0.42 && y > -0.42) {
        double r = y * y;
        return y * Horner(r, a0, a1, a2, a3) / Horner(r, 1.0, b1, b2, b3, b4);
    }
    else {
        double r;
        if (y < 0.0)
            r = x;
        else
            r = 1.0 - x;

        double s = log(-log(r));
        double t = Horner(s, c0, c1, c2, c3 ,c4 ,c5 ,c6 ,c7 ,c8);

        if (x > 0.5)
            return t;
        else
            return -t;
    }
}