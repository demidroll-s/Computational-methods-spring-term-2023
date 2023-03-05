#pragma once

#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>
#include <numeric>
#include <algorithm>

#include "linear_solver.h"

class  HeatTransferEquation_Solver {
public:
    ///Constructors and destructors
    HeatTransferEquation_Solver();
    HeatTransferEquation_Solver(const double h, const double tau, 
        const size_t size_x, const size_t size_time);
    ~HeatTransferEquation_Solver();

    double a_conductivity(const double x, const double t, const double u) {
        return 1.0;
    }

    double q(const double x, const double t) {
        return 0.0;
    }

    ///Computational methods to find soltution
    void ExplicitScheme(size_t n);
    void ExplicitSchemeSolution(const std::string& filename);

    void ImplicitScheme(size_t n);
    void ImplicitSchemeSolution(const std::string& filename);

    ///Overwrite the solution on the explicit and implicit layer
    void Overwrite();

    ///IO manipulations
    void WriteExplicitLayer(std::ofstream& file, const double time);
private:
    double h_;
    double tau_;
    size_t size_x_;
    size_t size_time_;
    std::vector<double> x_;
    std::vector<double> time_;
    std::vector<double> u_0_;
    std::vector<double> u_1_;

    double t_0_ = 250.0; ///initial temperature
    double t_1_ = 300.0; ///temperature on the left border
    double t_2_ = 400.0; ///temperature on the right border
};