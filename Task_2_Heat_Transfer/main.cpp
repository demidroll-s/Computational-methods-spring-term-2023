#include "heat_transfer_equation_solver.h"
#include "linear_solver.h"

int main() {
    double h = 0.005;
    double tau = 1e-3;
    size_t size_x = 200;
    size_t size_time = static_cast<size_t>(1e3);
    HeatTransferEquation_Solver solver(h, tau, size_x, size_time);
    
    solver.ImplicitSchemeSolution("data/implicit_solution.txt");

    return 0;
}