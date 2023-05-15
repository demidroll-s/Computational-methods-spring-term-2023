#include "multilevel_monte_carlo.h"

MultilevelMonteCarloPricer::MultilevelMonteCarloPricer(size_t l_min, size_t l_max, 
    size_t n_scenarios_initial, double accuracy) {
    /* Check arguments */
    if (l_min < 2)
        throw std::invalid_argument("Minimum level of refinement l_min should not be less than 2");
    if (l_max < l_min)
        throw std::invalid_argument("Maximum level of refinement l_max should not be less than minimum level of refinement l_min");
    if (accuracy <= 0.0)
        throw std::invalid_argument("Desired accuacy eps should be higher than 0.0");

    this->l_min_ = l_min;
    this->l_max_ = l_max;
    this->n_scenarios_initial_ = n_scenarios_initial;
    this->accuracy_ = accuracy;
}

size_t MultilevelMonteCarloPricer::GetMinLevelRefinement() const {
    return l_min_;
}

size_t MultilevelMonteCarloPricer::GetMaxLevelRefinement() const {
    return l_max_;
}

size_t MultilevelMonteCarloPricer::GetNumberScenariosInitial() const {
    return n_scenarios_initial_;
}

double MultilevelMonteCarloPricer::GetAccuracy() const {
    return accuracy_;
}

double MultilevelMonteCarloPricer::Routine(double alpha_0, double beta_0, double gamma_0,
    std::vector<size_t>& Nl, std::vector<double>& Cl) {
    
    std::vector<double> sums(7, 0.0);
    std::vector<std::vector<double>> suml;
    suml.resize(3);
    for (size_t n = 0; n < 3; ++n) {
        suml[n].resize(21);
        std::fill(suml[n].begin(), suml[n].end(), 0.0);
    }


    std::vector<double> ml(21, 0.0);
    std::vector<double> Vl(21, 0.0);
    std::vector<double> NlCl(21, 0.0);

    std::vector<double> x(21, 0.0);
    std::vector<double> y(21, 0.0);

    std::vector<size_t> dNl(21, 0);

    double sum = 0.0;

    double alpha = std::max(0.0, alpha_0);
    double beta  = std::max(0.0, beta_0);
    double gamma = std::max(0.0, gamma_0);
    // MSE split between bias^2 and variance
    double theta = 0.25; 

    size_t L = l_min_;
    bool convergence_flag = false;

    for (size_t l = 0; l <= l_max_; ++l) {
        Nl[l] = 0;
        Cl[l] = static_cast<double>(pow(2.0, (double) l * gamma));
        NlCl[l] = 0.0;

        for(size_t n = 0; n < 3; ++n)
            suml[n][l] = 0.0;
    }

    for (size_t l = 0; l <= l_min_; ++l)
        dNl[l] = n_scenarios_initial_;

    while (!convergence_flag) {
        //Update sample sums
        for (size_t l = 0; l <= L; ++l) {
            if (dNl[l] > 0) {
                for(size_t n = 0; n < 7; ++n)
                    sums[n] = 0.0;
                
                RoutineLower(l, dNl[l], sums);
                
                suml[0][l] += static_cast<double>(dNl[l]);
                suml[1][l] += sums[1];
                suml[2][l] += sums[2];
                NlCl[l] += sums[0];  // sum total cost
            }
        }

        // Compute absolute average, variance and cost,
        // correct for possible under-sampling,
        // and set optimal number of new samples

        sum = 0.0;

        for (size_t l = 0; l <= L; ++l) {
            ml[l] = abs(suml[1][l] / suml[0][l]);
            Vl[l] = std::max(suml[2][l] / suml[0][l] - ml[l] * ml[l], 0.0);
            if (gamma_0 <= 0.0)
                Cl[l] = NlCl[l] / suml[0][l];

            if (l > 1) {
                ml[l] = std::max(ml[l],  0.5 * ml[l-1] / powf(2.0, alpha));
                Vl[l] = std::max(Vl[l],  0.5 * Vl[l-1] / powf(2.0, beta));
            }

            sum += sqrt(Vl[l] * Cl[l]);
        }

        for (size_t l = 0; l <= L; ++l) {
            dNl[l] = static_cast<size_t>(ceil(std::max(0.0, sqrt(Vl[l] / Cl[l]) 
                * sum /((1.0 - theta) * accuracy_ * accuracy_) - suml[0][l])));
        }
 
        // Use linear regression to estimate 
        // alpha, beta, gamma if not given
        if (alpha_0 <= 0.0) {
            for (size_t l = 1; l <= L; ++l) {
                x[l-1] = l;
                y[l-1] = -log2(ml[l]);
            }
            Regression(L, x, y, alpha, sum);
            alpha = std::max(alpha, 0.5);
        }

        if (beta_0 <= 0.0) {
            for (size_t l = 1; l <= L; ++l) {
                x[l-1] = l;
                y[l-1] = -log2(Vl[l]);
            }
            Regression(L, x, y, beta, sum);
            beta = std::max(beta, 0.5);
        }

        if (gamma_0 <= 0.0) {
            for (size_t l = 1; l <= L; ++l) {
                x[l-1] = l;
                y[l-1] = -log2(Cl[l]);
            }
            Regression(L, x, y, beta, sum);
            gamma = std::max(gamma, 0.5);
        }

        sum = 0.0;
        for (size_t l = 0; l <= L; ++l)
            sum += std::max(0.0, static_cast<double>(dNl[l]) - 0.01 * suml[0][l]);

        if (sum == 0) {
            convergence_flag = true;
            double rem = ml[L] / (pow(2.0, alpha) - 1.0);

            if (rem > sqrt(theta)* accuracy_) {
                if (L == l_max_)
                    std::cout << "Failed to achieve weak convergence!" << std::endl;
                else {
                    convergence_flag = false;
                    L++;
                    Vl[L] = Vl[L-1] / pow(2.0, beta);
                    Cl[L] = Cl[L-1] * pow(2.0, gamma);

                    sum = 0.0;
                    for (size_t l = 0; l <= L; l++)
                        sum += sqrt(Vl[l] * Cl[l]);
                    for (size_t l = 0; l <= L; l++)
                        dNl[l] = static_cast<size_t>(ceil(std::max(0.0, sqrtf(Vl[l] / Cl[l]) 
                            * sum / ((1.0 - theta) * accuracy_ * accuracy_) - suml[0][l])));
                }
            }
        }
    }
    
    // Finally, evaluate multilevel estimator and set output
    double P = 0.0;
    for (size_t l = 0; l <= L; ++l) {
        P += suml[1][l] / suml[0][l];
        Nl[l] = suml[0][l];
        Cl[l] = NlCl[l] / Nl[l];
    }

    return P;
}