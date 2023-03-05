#pragma once

#include <iostream>
#include <vector>
#include <algorithm>

class LinearSolver {
public:
    ///Constructors and destructors
    LinearSolver(const size_t n, 
    const std::vector<double>& a, const std::vector<double>& b, 
    const std::vector<double>& c, const std::vector<double>& f);

    ///Getting method
    std::vector<double>& GetSolution() { return sol_; }
    
    ///Solve method
    void Solve();

private:
    size_t n_; ///size of linear system
    std::vector<double> a_; ///lower diagonal
    std::vector<double> b_; ///upper diagonal
    std::vector<double> c_; ///main diagonal
    std::vector<double> f_; ///rhs

    std::vector<double> sol_;
};