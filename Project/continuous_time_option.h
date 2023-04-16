#pragma once

#include <iostream>
#include <vector>

#include "priceable.h"

class ContinuousTimeOption : 
    public Priceable {
public:
    virtual ~ContinuousTimeOption() {};
    virtual double GetMaturity() const = 0;
    virtual double Payoff(const std::vector<double>& stock_prices) const = 0;
    virtual bool IsPathDependent() const = 0;
};