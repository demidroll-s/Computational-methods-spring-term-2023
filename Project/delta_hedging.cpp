#include "delta_hedging.h"

//#include "testing.h"
#include "matlib.h"

HedgingSimulator::HedgingSimulator() {
    std::shared_ptr<BlackScholesModel> model(new BlackScholesModel());
    model->SetStockPrice(1.0);
    model->SetDate(0.0);
    model->SetRiskFreeRate(0.05);
    model->SetVolatility(0.2);
    model->SetDrift(0.1);
 
    std::shared_ptr<CallOption> option = std::make_shared<CallOption>();
    option->SetStrike(model->GetStockPrice());
    option->SetMaturity(1.0);
 
    SetToHedge(option);
    SetSimulationModel(model);
    SetPricingModel(model);
    size_t n_steps = 10;
    SetNumberSteps(n_steps);
}

HedgingSimulator::HedgingSimulator(double maturity, BlackScholesModel out_model, size_t n_steps) {
    std::shared_ptr<BlackScholesModel> model(new BlackScholesModel());
    model->SetStockPrice(out_model.GetStockPrice());
    model->SetDate(out_model.GetDate());
    model->SetRiskFreeRate(out_model.GetRiskFreeRate());
    model->SetVolatility(out_model.GetVolatility());
    model->SetDrift(out_model.GetDrift());
 
    std::shared_ptr<CallOption> option = std::make_shared<CallOption>();
    option->SetStrike(model->GetStockPrice());
    option->SetMaturity(maturity);
 
    SetToHedge(option);
    SetSimulationModel(model);
    SetPricingModel(model);
    SetNumberSteps(n_steps);
}

void HedgingSimulator::SetToHedge(std::shared_ptr <CallOption> to_hedge) {
    this->to_hedge_ = to_hedge;
}

void HedgingSimulator::SetSimulationModel(std::shared_ptr <BlackScholesModel> simulation_model) {
    this->simulation_model_ = simulation_model;
}

void HedgingSimulator::SetPricingModel(std::shared_ptr <BlackScholesModel> pricing_model) {
    this->pricing_model_ = pricing_model;
}

void HedgingSimulator::SetNumberSteps(size_t n_steps) {
    this->n_steps_ = n_steps;
}

std::vector<double> HedgingSimulator::RunSimulations(size_t n_simulations) const {
    std::vector<double> result(n_simulations);
    for (size_t i = 0; i < n_simulations; ++i)
        result[i] = RunSimulation();
    return result;
}

double HedgingSimulator::RunSimulation() const {
    double T = to_hedge_->GetMaturity();
    double S0 = simulation_model_->GetStockPrice();
    std::vector<double> price_path = simulation_model_->GeneratePricePath(T, n_steps_);
 
    double dt = T / n_steps_;
    double charge = ChooseCharge(S0);
    double stock_quantity = SelectStockQuantity(0, S0);
    double bank_balance = charge - stock_quantity * S0;

    for (size_t i = 0; i < n_steps_ - 1; ++i) {
        double balance_with_interest = bank_balance * exp(simulation_model_->GetRiskFreeRate() * dt);
        double S = price_path[i];
        double date = dt * (i + 1);
        double new_stock_quantity = SelectStockQuantity(date, S);
        double costs = (new_stock_quantity - stock_quantity) * S;
        bank_balance = balance_with_interest - costs;
        stock_quantity = new_stock_quantity;
    }

    double balance_with_interest = bank_balance * exp(simulation_model_->GetRiskFreeRate() * dt);
    double S = price_path[n_steps_ - 1];
    double stock_value = stock_quantity * S;
    double payout = to_hedge_->Payoff(S);

    return balance_with_interest + stock_value - payout;
}
 
double HedgingSimulator::ChooseCharge(double stock_price) const {
    BlackScholesModel pricing_model = *pricing_model_;
    pricing_model.SetStockPrice(stock_price);
    return to_hedge_->Price(pricing_model);
}

double HedgingSimulator::SelectStockQuantity(double date, double stock_price) const {
    BlackScholesModel pricing_model = *pricing_model_;
    pricing_model.SetStockPrice(stock_price);
    pricing_model.SetDate(date);
    return to_hedge_->Delta(pricing_model);
}

void TestHedging() {
	std::ifstream file_input("data/delta_input.txt");
    std::ofstream file_output;
    double drift, stock_price, volatility, risk_free_rate, date;
    double maturity;
    size_t n_scenarios;
    
    if(file_input.is_open()) {
        double a[7];
        size_t i = 0;
        while (file_input >> a[i])
            i++;
        file_input.close();

        risk_free_rate = a[0] / 100;
		stock_price = a[1];
		drift = a[2];
		volatility = a[3] / 100;
        date = a[4];
		maturity = a[5];
		n_scenarios = a[6];

        file_output.open("data/delta_output.txt");
		
        size_t n_steps = 10;
        BlackScholesModel model(drift, stock_price, volatility, risk_free_rate, date);
		HedgingSimulator simulator(maturity, model, n_steps);
        
        std::vector<double> balance;
        balance.resize(n_scenarios);
		
        balance = simulator.RunSimulations(n_scenarios);
        for (size_t i = 0; i < n_scenarios; i++)
            file_output << i << " " << balance[i] << std::endl;

        file_output.close();
        
        file_output.open("data/delta_table_simulation.txt");
        file_output << stock_price << " " << risk_free_rate * 100 << " " << volatility * 100 << " " << drift << " " << date;
        file_output.close();

		file_output.open("data/delta_table_pricing.txt");
        file_output << stock_price << " " << risk_free_rate * 100 << " " << volatility * 100 << " " << drift << " " << date;
        file_output.close();

		file_output.open("data/delta_table_option.txt");
        file_output << maturity << " " << n_steps;
        file_output.close();

        std::cout << "Program executed well!" << std::endl;
    }
    else {
        std::cout << "Unable to open file!" << std::endl;
        std::cout << "Error during program execution!" << std::endl;
    }
}