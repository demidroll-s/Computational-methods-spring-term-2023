#pragma once
 
#include "continuous_time_option_base.h"
 
class PathIndependentOption:
    public ContinuousTimeOptionBase {
public:
    virtual ~PathIndependentOption() {}
    virtual double Payoff(double final_stock_price) const = 0;
    double Payoff(const std::vector<double>& stock_prices) const {
        return Payoff(stock_prices.back());
    }
    bool IsPathDependent() const {
        return false;
    };
};