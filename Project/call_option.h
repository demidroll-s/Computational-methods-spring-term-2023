#pragma once
 
#include "bsm.h"
#include "path_independent_option.h"

class CallOption:
    public PathIndependentOption {
public:
    double Payoff(double stock_at_maturity) const;
    double Price(const BlackScholesModel& model) const;
    double Delta(const BlackScholesModel& model) const;
};