#pragma once

#include <iostream>
#include <vector>

#include "continuous_time_option.h"

class ContinuousTimeOptionBase : 
    public ContinuousTimeOption {
public:
    virtual ~ContinuousTimeOptionBase() {}
    
    double GetMaturity() const {
        return maturity_;
    }

    double GetStrike() const {
        return strike_;
    }

    void SetMaturity(double maturity) {
        this->maturity_ = maturity;
    }

    void SetStrike(double strike) {
        this->strike_ = strike;
    }
private:
    double maturity_;
    double strike_;
};