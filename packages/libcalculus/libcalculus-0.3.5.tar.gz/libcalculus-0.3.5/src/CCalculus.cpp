#include "CCalculus.h"

namespace libcalculus {
    template<>
    CFunction<COMPLEX, COMPLEX> Derivative(CFunction<COMPLEX, COMPLEX> const &f, REAL const tol, REAL const radius) {
        auto df = [=](COMPLEX z) {
            COMPLEX prev_result, result = 0.;
            REAL dz = radius;
            size_t while_iters = 0;
            while (while_iters < 2 || !Traits<COMPLEX>::close(prev_result, result, tol)) {
                dz *= .5;
                prev_result = result;
                result = (f(z + dz) - f(z)) / dz;
                ++while_iters;
            }
            return result;
        };
        std::string latex = "\\frac{\\text{d}}{\\text{d}" LATEX_VAR "}\\left(";
        latex.append(f._latex);
        latex.append("\\right)");
        return CFunction<COMPLEX, COMPLEX>(df, latex, OP_TYPE::FUNC);
    }

    template<>
    CFunction<REAL, REAL> Derivative(CFunction<REAL, REAL> const &f, REAL const tol, REAL const radius) {
        auto df = [=](REAL x) {
            REAL prev_result, result = 0.;
            REAL dx = radius;
            size_t while_iters = 0;
            while (while_iters < 2 || !Traits<REAL>::close(prev_result, result, tol)) {
                dx *= .5;
                prev_result = result;
                result = (f(x + dx) - f(x)) / dx;
                ++while_iters;
            }
            return result;
        };
        std::string latex = "\\frac{\\text{d}}{\\text{d}" LATEX_VAR "}\\left(";
        latex.append(f._latex);
        latex.append("\\right)");
        return CFunction<REAL, REAL>(df, latex, OP_TYPE::FUNC);
    }

    template<>
    CFunction<REAL, COMPLEX> Derivative(CFunction<REAL, COMPLEX> const &f, REAL const tol, REAL const radius) {
        auto df = [=](REAL t) {
            COMPLEX prev_result, result = 0.;
            REAL dt = radius;
            size_t while_iters = 0;
            while (while_iters < 2 || !Traits<COMPLEX>::close(prev_result, result, tol)) {
                dt *= .5;
                prev_result = result;
                result = (f(t + dt) - f(t)) / dt;
                ++while_iters;
            }
            return result;
        };
        std::string latex = "\\frac{\\text{d}}{\\text{d}" LATEX_VAR "}\\left(";
        latex.append(f._latex);
        latex.append("\\right)");
        return CFunction<REAL, COMPLEX>(df, latex, OP_TYPE::FUNC);
    }

    template<>
    COMPLEX Integrate(CFunction<COMPLEX, COMPLEX> const &f,
                      CFunction<REAL, COMPLEX> const &contour, REAL const start, REAL const end, REAL const tol) {
         COMPLEX prev_result, result = 0.;
         size_t while_iters = 0, n = INTEGRATION_SUBDIV_FACTOR / tol;
         while (while_iters < 2 || !Traits<COMPLEX>::close(prev_result, result, tol)) {
             n *= 2;
             prev_result = result;
             result = 0.;
             COMPLEX z, prev_z = contour(start);

             for (size_t k = 1; k <= n; ++k) {
                 z = contour(start + (end - start) * k / n);
                 result += f(z) * (z - prev_z);
                 prev_z = z;
             }
             ++while_iters;
         }
         return result;
    }

    template<>
    REAL Integrate(CFunction<REAL, REAL> const &f, CFunction<REAL, REAL> const &contour, REAL const start, REAL const end, REAL const tol) {
        auto const reverse = start > end;
        return (reverse ? -1. : 1.) * boost::math::quadrature::gauss_kronrod<REAL, 61>::integrate(f, contour(reverse ? end : start), contour(reverse ? start : end), 15, tol);
    }
}
