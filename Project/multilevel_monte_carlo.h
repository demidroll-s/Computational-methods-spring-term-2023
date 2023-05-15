#pragma once

#include "matlib.h"

#include "bsm.h"
#include "continuous_time_option.h"

struct SumStruct {
    double a;
    double b;
};

class MultilevelMonteCarloPricer {
public:
    //MultilevelMonteCarloPricer();
    MultilevelMonteCarloPricer(size_t l_min, size_t l_max, 
        size_t n_scenarios_initial, double accuracy);

    size_t GetMinLevelRefinement() const;
    size_t GetMaxLevelRefinement() const;
    size_t GetNumberScenariosInitial() const;
    double GetAccuracy() const;

    void RoutineLower(size_t l, size_t dNl, std::vector<double>& sums);
    double Routine(double alpha_0, double beta_0, double gamma_0, 
        std::vector<size_t>& Nl, std::vector<double>& Cl);
private:
    size_t l_min_;
    size_t l_max_;
    size_t n_scenarios_initial_;
    double accuracy_;
};