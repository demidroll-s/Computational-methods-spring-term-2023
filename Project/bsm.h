#pragma once

#include <vector>

#include "matlib.h"

class BlackScholesModel {
public:
    BlackScholesModel();
    BlackScholesModel(double drift, double stock_price, double volatility, 
        double risk_free_rate, double date);

    std::vector<double> GeneratePricePath(double to_date, int n_steps, double drift) const;
private:
    double drift_;
    double stock_price_;
    double volatility_;
    double risk_free_date_;
    double date_;  
};