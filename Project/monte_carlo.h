#pragma once

#include "matlib.h"

#include "bsm.h"
#include "continuous_time_option.h"

class MonteCarloPricer {
public:
    MonteCarloPricer();
    MonteCarloPricer(size_t n_scenarios, size_t n_steps);

    double Price(const ContinuousTimeOption& option, const BlackScholesModel& model);
private:
    size_t n_scenarios_;
    size_t n_steps_;
};