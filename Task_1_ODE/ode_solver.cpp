#include "ode_solver.h"

ODE_Solver::ODE_Solver() {
    this->h_ = 0.1;
    this->n_ = 10;
    this->x_arr_.resize(n_ + 1);
    this->y_arr_.resize(n_ + 1);
    x_arr_[0] = 0.0;
    for (size_t i = 0; i < this->n_; ++i) {
        x_arr_[i + 1] = x_arr_[i] + h_;
    }
    std::fill(y_arr_.begin(), y_arr_.end(), 0);
}

ODE_Solver::ODE_Solver(const double x_0, const double h, const size_t n) {
    this->h_ = h;
    this->n_ = n;
    this->x_arr_.resize(n_ + 1);
    this->y_arr_.resize(n_ + 1);
    x_arr_[0] = x_0;
    for (size_t i = 0; i < this->n_; ++i) {
        x_arr_[i + 1] = x_arr_[i] + h_;
    }
    std::fill(y_arr_.begin(), y_arr_.end(), 0);
}

ODE_Solver::~ODE_Solver() {}

void ODE_Solver::eulerSolve(const double y_0) {
    y_arr_[0] = y_0;
    for (size_t i = 0; i < this->n_; ++i) {
        y_arr_[i + 1] = y_arr_[i] + h_ * f(x_arr_[i], y_arr_[i]);
    }
}

void ODE_Solver::hoineSolve(const double y_0) {
    y_arr_[0] = y_0;
    for (size_t i = 0; i < this->n_; ++i) {
        double y_pred = y_arr_[i] + h_ * f(x_arr_[i], y_arr_[i]);
        y_arr_[i + 1] = y_arr_[i] + 0.5 * h_ * (f(x_arr_[i], y_arr_[i]) + f(x_arr_[i + 1], y_pred));
    }
}

void ODE_Solver::rungeSolve(const double y_0) {
    y_arr_[0] = y_0;
    for (size_t i = 0; i < this->n_; ++i) {
        double k_1 = f(x_arr_[i], y_arr_[i]); 
        double k_2 = f(x_arr_[i] + 0.5 * h_, y_arr_[i] + 0.5 * h_ * k_1);
        double k_3 = f(x_arr_[i] + 0.5 * h_, y_arr_[i] + 0.5 * h_ * k_2);
        double k_4 = f(x_arr_[i] + h_, y_arr_[i] + h_ * k_3);
        y_arr_[i + 1] = y_arr_[i] + (1 / 6.0) * h_ * (k_1 + 2 * k_2 + 2 * k_3 + k_4);
    }
}

void ODE_Solver::reset() {
    std::fill(y_arr_.begin(), y_arr_.end(), 0);
}

void ODE_Solver::printSolution() {
    for (size_t i = 0; i < this->n_ + 1; ++i) {
        std::cout << x_arr_[i] << ": " << y_arr_[i] << std::endl; 
    }
}

void ODE_Solver::printExactSolution() {
    for (size_t i = 0; i < this->n_ + 1; ++i) {
        std::cout << x_arr_[i] << ": " << exactSolution(x_arr_[i]) << std::endl; 
    }
}

void ODE_Solver::writeExactFile(const std::string& filename) {
    std::ofstream file;
	file.open(filename);
	if (!file.is_open()) {
		throw "Error: file open failed";
	}

    for (size_t i = 0; i < this->n_; ++i) {
        file << x_arr_[i] << " " << exactSolution(x_arr_[i]) << std::endl; 
    }
    file << x_arr_[n_] << " " << exactSolution(x_arr_[n_]);
    reset();

    file.close();
}


void ODE_Solver::writeEulerFile(const double y_0, const std::string& filename) {
    std::ofstream file;
	file.open(filename);
	if (!file.is_open()) {
		throw "Error: file open failed";
	}

    eulerSolve(y_0);
    for (size_t i = 0; i < this->n_; ++i) {
        file << x_arr_[i] << " " << y_arr_[i] << std::endl; 
    }
    file << x_arr_[n_] << " " << y_arr_[n_];
    reset();

    file.close();
}

void ODE_Solver::writeHoineFile(const double y_0, const std::string& filename) {
    std::ofstream file;
	file.open(filename);
	if (!file.is_open()) {
		throw "Error: file open failed";
	}

    hoineSolve(y_0);
    for (size_t i = 0; i < this->n_; ++i) {
        file << x_arr_[i] << " " << y_arr_[i] << std::endl; 
    }
    file << x_arr_[n_] << " " << y_arr_[n_];
    reset();

    file.close();
}

void ODE_Solver::writeRungeFile(const double y_0, const std::string& filename) {
    std::ofstream file;
	file.open(filename);
	if (!file.is_open()) {
		throw "Error: file open failed";
	}

    rungeSolve(y_0);
    for (size_t i = 0; i < this->n_; ++i) {
        file << x_arr_[i] << " " << y_arr_[i] << std::endl; 
    }
    file << x_arr_[n_] << " " << y_arr_[n_];
    reset();

    file.close();
}