
#include <iostream>
#include <cmath>
#include <random>
#include <vector>
#include <algorithm>
#include <cassert>

std::vector<double> LinSpace(double start, double finish, size_t n_points);
double Sum(const std::vector<double>& v);
double Mean(const std::vector<double>& v);
double StandardDeviation(const std::vector<double>& v, bool unbiasedness = false);
double Min(const std::vector<double>& v);
double Max(const std::vector<double>& v);

static std::mt19937 mersenne_twister;

void RandNumberGenerator(const std::string& description);
std::vector<double> RandUniform(size_t n);
std::vector<double> RandNormal(size_t n);

double NormCdf(double x);
double NormInv(double x);