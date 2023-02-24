#include "ode_solver.h"

int main() {
    double x_0 = 0.0;
    double h = 0.1;
    size_t n = 10;
    ODE_Solver solver(x_0, h, n);

    double y_0 = 1.0;

    solver.writeExactFile("data/data_exact.txt");
    solver.writeEulerFile(y_0, "data/data_euler.txt");
    solver.writeHoineFile(y_0, "data/data_hoine.txt");
    solver.writeRungeFile(y_0, "data/data_runge.txt");
    
    return 0;
}