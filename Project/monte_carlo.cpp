#include "monte_carlo.h"

MonteCarloPricer::MonteCarloPricer() :
    n_scenarios_(1000), n_steps_(10) {}

MonteCarloPricer::MonteCarloPricer(size_t n_scenarios, size_t n_steps) :
    n_scenarios_(n_scenarios), n_steps_(n_steps) {}

double MonteCarloPricer::Price(const ContinuousTimeOption& option, const BlackScholesModel& model) {
    size_t n_steps = this->n_steps_;
    if(!option.IsPathDependent())
        n_steps = 1;

    double total = 0.0;
    for (size_t i = 0; i < n_scenarios_; ++i) {
        std::vector<double> path = model.GenerateRiskNeutralPricePath(option.GetMaturity(), n_steps);
        double payoff = option.Payoff(path);
        total += payoff;
    }

    double mean = total / n_scenarios_;
    double r = model.GetRiskFreeRate();
    double T = option.GetMaturity() - model.GetDate();
    
    return exp(-r * T) * mean;
}