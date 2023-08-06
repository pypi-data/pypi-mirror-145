#pragma once
#include <functional>
#include <type_traits>
#include "Definitions.h"

namespace libcalculus {
    template<typename T>
    struct Traits {
    public:
        static constexpr REAL tol = [] {
            if constexpr (std::is_same<T, REAL>::value)
                return 1e-6;
            else if constexpr (std::is_same<T, COMPLEX>::value)
                return 1e-6;
        }();

        inline static bool close(T const a, T const b, REAL const tol=Traits<T>::tol) noexcept { return std::abs(a - b) < tol; }
    };

    template<typename Dom>
    class CComparison {
    public:
        std::string latex;
        std::function<bool(Dom)> eval = [](Dom z) { return true; };

        CComparison() {}
        CComparison(CComparison const &cc) : latex{cc.latex}, eval{cc.eval} {}
        CComparison(std::function<bool(Dom)> const &eval, std::string const &latex) : latex{latex}, eval{eval} {}

        // Unary operators
        CComparison operator~() const;

        // Binary operators
        CComparison operator|(CComparison const &rhs) const;
        CComparison operator&(CComparison const &rhs) const;

        // In-place binary operators
        CComparison &operator|=(CComparison const &rhs);
        CComparison &operator&=(CComparison const &rhs);
    };
}
