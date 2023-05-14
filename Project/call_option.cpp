#include "call_option.h"

double CallOption::Payoff(double stock_at_maturity) const {
    if(stock_at_maturity > GetStrike())
        return stock_at_maturity - GetStrike();
    else
        return 0.0;
}

double CallOption::Price(const BlackScholesModel& model) const {
    double S = model.GetStockPrice();
    double K = GetStrike();
    double sigma = model.GetVolatility();
    double r = model.GetRiskFreeRate();
    double T = GetMaturity() - model.GetDate();
    
    double numerator = log(S / K) + (r + sigma * sigma * 0.5) * T;
    double denominator = sigma * sqrt(T);
    
    double d1 = numerator / denominator;
    double d2 = d1 - denominator;
    
    return S * NormCdf(d1) - exp((-1) * r * T) * K * NormCdf(d2);
}

double CallOption::Delta(const BlackScholesModel& model) const {
    double S = model.GetStockPrice();
    double K = GetStrike();
    double sigma = model.GetVolatility();
    double r = model.GetRiskFreeRate();
    double T = GetMaturity() - model.GetDate();

    double numerator = log (S / K) + (r + sigma * sigma *0.5) * T;
    double denominator = sigma * sqrt(T);

    double d1 = numerator / denominator;
    return NormCdf(d1);
}