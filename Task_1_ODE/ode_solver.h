#pragma once

#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>
#include <numeric>
#include <algorithm>

class  ODE_Solver {
public:
    ///Constructors and destructors
    ODE_Solver();
    ODE_Solver(const double x_0, const double h, const size_t n);
    ~ODE_Solver();

    double f(const double x, const double y) {
        return x * x - 2 * y;
    }

    double exactSolution(const double x) {
        return (2 * x * x - 2 * x + 3 * std::exp(-2 * x) + 1) / 4.0;
    }

    ///Computational methods to find ODE soltution
    void eulerSolve(const double y_0);
    void hoineSolve(const double y_0);
    void rungeSolve(const double y_0);

    ///Reset solution to zero
    void reset();

    ///IO manipulations
    void printSolution();
    void printExactSolution();
    
    void writeExactFile(const std::string& filename);
    void writeEulerFile(const double y_0, const std::string& filename);
    void writeHoineFile(const double y_0, const std::string& filename);
    void writeRungeFile(const double y_0, const std::string& filename);
private:
    double x_0_;
    double h_;
    size_t n_;
    std::vector<double> x_arr_;
    std::vector<double> y_arr_;
};