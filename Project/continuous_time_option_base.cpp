#include "continuous_time_option_base.h"

// Getting methods
double ContinuousTimeOptionBase::GetMaturity() const {
    return maturity_;
}

double ContinuousTimeOptionBase::GetStrike() const {
    return strike_;
}

// Setting methods
void ContinuousTimeOptionBase::SetMaturity(double maturity) {
    this->maturity_ = maturity;
}

void ContinuousTimeOptionBase::SetStrike(double strike) {
    this->strike_ = strike;
}


