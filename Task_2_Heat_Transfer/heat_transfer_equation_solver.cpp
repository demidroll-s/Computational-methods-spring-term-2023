#include "heat_transfer_equation_solver.h"

///Constructors and destructors
HeatTransferEquation_Solver::HeatTransferEquation_Solver() {
    this->h_ = 0.1;
    this->tau_ = 0.1;
    this->size_x_ = 10;
    this->size_time_ = 10;

    this->x_.resize(size_x_ + 1);
    this->u_0_.resize(size_x_ + 1);
    this->u_1_.resize(size_x_ + 1);
    this->time_.resize(size_time_ + 1);
    
    x_[0] = 0.0;
    for (size_t m = 0; m < size_x_; ++m) {
        x_[m + 1] = x_[m] + h_;
    }

    time_[0] = 0.0;
    for (size_t n = 0; n < size_time_; ++n) {
        time_[n + 1] = time_[n] + tau_;
    }

    std::fill(u_0_.begin(), u_0_.end(), 0.0);
    std::fill(u_1_.begin(), u_1_.end(), 0.0);
}

HeatTransferEquation_Solver::HeatTransferEquation_Solver(const double h, const double tau, 
    const size_t size_x, const size_t size_time) {
    this->h_ = h;
    this->tau_ = tau;
    this->size_x_ = size_x;
    this->size_time_ = size_time;

    this->x_.resize(size_x_ + 1);
    this->u_0_.resize(size_x_ + 1);
    this->u_1_.resize(size_x_ + 1);
    this->time_.resize(size_time_ + 1);
    
    x_[0] = 0.0;
    for (size_t m = 0; m < size_x_; ++m) {
        x_[m + 1] = x_[m] + h_;
    }

    time_[0] = 0.0;
    for (size_t n = 0; n < size_time_; ++n) {
        time_[n + 1] = time_[n] + tau_;
    }

    std::fill(u_0_.begin(), u_0_.end(), 0.0);
    std::fill(u_1_.begin(), u_1_.end(), 0.0);
}

HeatTransferEquation_Solver::~HeatTransferEquation_Solver() {}

///Computational methods to find soltution
void HeatTransferEquation_Solver::ExplicitScheme(size_t n) {
    u_1_[0] = 1.0;
    u_1_[size_x_] = (t_2_ - t_0_) / (t_1_ - t_0_);

    for (size_t m = 1; m < size_x_; ++m) {
        double sigma = tau_ / (h_ * h_);
        
        double left = 0.5 * (a_conductivity(x_[m - 1] , time_[n], u_0_[m - 1]) + a_conductivity(x_[m] , time_[n], u_0_[m]));
        double right = 0.5 * (a_conductivity(x_[m] , time_[n], u_0_[m]) + a_conductivity(x_[m + 1] , time_[n], u_0_[m + 1]));
        double center = left + right;
        
        u_1_[m] = u_0_[m] + sigma * (left * u_0_[m - 1] - center * u_0_[m] + right * u_0_[m + 1]);
        u_1_[m] += tau_ * q(x_[m], time_[n]);
    }
}

void HeatTransferEquation_Solver::ExplicitSchemeSolution(const std::string& filename) {
    std::ofstream file;
	file.open(filename);
	if (!file.is_open()) {
		throw "Error: file open failed";
	}
    
    double time = 0.0;

    u_0_[0] = 1.0;
    u_0_[size_x_] = (t_2_ - t_0_) / (t_1_ - t_0_);
    
    for (size_t m = 1; m < size_x_; ++m) {
        u_0_[m] = 0.0;
    }

    WriteExplicitLayer(file, time);

    for (size_t n = 0; n < size_time_; ++n) {
        time += tau_;

        std::cout << "----------------------------------" << std::endl;
        std::cout << "TIME = " << time << std::endl;
        std::cout << "----------------------------------" << std::endl;

        ExplicitScheme(n);
        Overwrite();
        WriteExplicitLayer(file, time);
    }

    file.close();
}

void HeatTransferEquation_Solver::ImplicitScheme(size_t n) {
    std::vector<double> a, b, c, f;
    
    a.resize(size_x_ + 1);
    b.resize(size_x_ + 1);
    c.resize(size_x_ + 1);
    f.resize(size_x_ + 1);

    std::fill(a.begin(), a.end(), 0.0);
    std::fill(b.begin(), b.end(), 0.0);
    std::fill(c.begin(), c.end(), 0.0);
    std::fill(f.begin(), f.end(), 0.0);

    c[0] = -1.0;
    f[0] = -1.0;

    for (size_t m = 1; m < size_x_; ++m) {
        double sigma = tau_ / (h_ * h_);
        
        double left = 0.5 * (a_conductivity(x_[m - 1] , time_[n], u_0_[m - 1]) + a_conductivity(x_[m] , time_[n], u_0_[m]));
        double right = 0.5 * (a_conductivity(x_[m] , time_[n], u_0_[m]) + a_conductivity(x_[m + 1] , time_[n], u_0_[m + 1]));
        double center = left + right;

        c[m] = 1 + sigma * center;
        a[m] = sigma * left;
        b[m] = sigma * right;
        f[m] = -u_0_[m];
    }

    c[size_x_] = -1.0;
    f[size_x_] = -(t_2_ - t_0_) / (t_1_ - t_0_);

    LinearSolver linear_solver(size_x_ + 1, a, b, c, f);
    linear_solver.Solve();
    std::vector<double> solution = linear_solver.GetSolution();

    for (size_t m = 0; m < size_x_ + 1; ++m) {
        u_1_[m] = solution[m];
    }
}

void HeatTransferEquation_Solver::ImplicitSchemeSolution(const std::string& filename) {
    std::ofstream file;
	file.open(filename);
	if (!file.is_open()) {
		throw "Error: file open failed";
	}
    
    double time = 0.0;

    u_0_[0] = 1.0;
    u_0_[size_x_] = (t_2_ - t_0_) / (t_1_ - t_0_);
    
    for (size_t m = 1; m < size_x_; ++m) {
        u_0_[m] = 0.0;
    }

    WriteExplicitLayer(file, time);

    for (size_t n = 0; n < size_time_; ++n) {
        time += tau_;

        std::cout << "----------------------------------" << std::endl;
        std::cout << "TIME = " << time << std::endl;
        std::cout << "----------------------------------" << std::endl;

        ImplicitScheme(n);
        Overwrite();
        WriteExplicitLayer(file, time);
    }

    file.close();
}

///Overwrite the solution on the explicit and implicit layer
void HeatTransferEquation_Solver::Overwrite() {
    for (size_t m = 0; m < size_x_ + 1; ++m) {
        u_0_[m] = u_1_[m];
    }
}

///IO manipulations
void HeatTransferEquation_Solver::WriteExplicitLayer(std::ofstream& file, const double time) {
    file << "----------------------------------" << std::endl;
    file << "TIME = " << time << std::endl;
    file << "----------------------------------" << std::endl;

    for (size_t m = 0; m < size_x_ + 1; ++m) {
        file << u_0_[m] << " ";
    }
    file << std::endl;
}