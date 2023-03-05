#include "linear_solver.h"

LinearSolver::LinearSolver(const size_t n, 
    const std::vector<double>& a, const std::vector<double>& b, 
    const std::vector<double>& c, const std::vector<double>& f) {
    
    n_ = n;

    a_ = a;
    b_ = b;
    c_ = c;
    f_ = f;

    sol_.resize(n_);
    std::fill(sol_.begin(), sol_.end(), 0.0);
}

void LinearSolver::Solve() {
    std::vector<double> alpha = {};
    std::vector<double> beta = {};

    alpha.resize(n_);
    beta.resize(n_);

    std::fill(alpha.begin(), alpha.end(), 0.0);
    std::fill(beta.begin(), beta.end(), 0.0);

    ///Direct course of the run
    alpha[0] = b_[0] / c_[0];
    beta[0] = f_[0] / c_[0];

    for (size_t i = 1; i < n_ - 1; ++i) {
        alpha[i] = b_[i] / (c_[i] - a_[i] * alpha[i - 1]);
        beta[i] = (f_[i] + a_[i] * beta[i - 1]) / (c_[i] - a_[i] * alpha[i - 1]);
    }

    beta[n_ - 1] = (f_[n_ - 1] + a_[n_ - 1] * beta[n_ - 2]) / (c_[n_ - 1] - a_[n_ - 1] * alpha[n_ - 2]);
    
    ///Reverse course of run
    sol_[n_ - 1] = beta[n_ - 1];

    for (size_t i = n_ - 1; i > 0; --i) {
        sol_[i - 1] = alpha[i - 1] * sol_[i] + beta[i - 1];
    }
}