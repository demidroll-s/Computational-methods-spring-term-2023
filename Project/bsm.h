#pragma once

#include <vector>

#include "matlib.h"

class BlackScholesModel {
public:
    BlackScholesModel();
    BlackScholesModel(double drift, double stock_price, double volatility, 
        double risk_free_rate, double date);

    double GetRiskFreeRate() const;
    double GetDate() const;
 
    std::vector<double> GeneratePricePath(double to_date, size_t n_steps) const;
    std::vector<double> GenerateRiskNeutralPricePath(double to_date, size_t n_steps) const;
private:
    double drift_;
    double stock_price_;
    double volatility_;
    double risk_free_rate_;
    double date_;

    std::vector<double> GeneratePricePath(double to_date, size_t n_steps, double drift) const;
};