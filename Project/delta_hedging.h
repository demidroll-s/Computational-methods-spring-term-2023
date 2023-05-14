#pragma once

#include <iostream>
#include <fstream>
#include <memory>

#include "bsm.h"
#include "call_option.h"

class HedgingSimulator {
public:
    HedgingSimulator();
    HedgingSimulator(double maturity, BlackScholesModel out_model, size_t n_steps);
    
    void SetToHedge(std::shared_ptr <CallOption> to_hedge);
    void SetSimulationModel(std::shared_ptr <BlackScholesModel> simulation_model);
    void SetPricingModel(std::shared_ptr <BlackScholesModel> pricing_model);
    void SetNumberSteps(size_t n_steps);
    
    std::vector<double> RunSimulations(size_t n_simulations) const;
    double RunSimulation() const;
    double ChooseCharge(double stock_price) const;
    double SelectStockQuantity(double date, double stock_price) const;
private:
    /* Option for hedging */
    std::shared_ptr <CallOption> to_hedge_;
    /* Model to simulate stock price */
    std::shared_ptr<BlackScholesModel> simulation_model_;
    /* Model to calculate deltas and prices */
    std::shared_ptr<BlackScholesModel> pricing_model_;
    /* Number of iterations for hedging */
    size_t n_steps_;
};

void TestHedging();