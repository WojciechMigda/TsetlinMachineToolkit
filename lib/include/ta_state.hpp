#pragma once

#ifndef LIB_INCLUDE_TA_STATE_HPP_
#define LIB_INCLUDE_TA_STATE_HPP_

#include "tsetlini_types.hpp"
#include "mt.hpp"

#include <variant>
#include <type_traits>


namespace Tsetlini
{


template<typename, typename = std::void_t<>>
struct is_TA_state
    : std::false_type
{
};


template<typename T>
struct is_TA_state<T, std::void_t<
        typename T::value_type,
        decltype(T::initialize(
            std::declval<typename T::value_type &>(),
            std::declval<std::string const &>(),
            std::declval<int>(),
            std::declval<int>(),
            std::declval<IRNG &>()))
    >>
    : std::true_type
{
};


struct TAStateBase
{
    using matrix_variant_type = std::variant<
        numeric_matrix_int32
        , numeric_matrix_int16
        , numeric_matrix_int8
    >;
};


struct TAState : public TAStateBase
{
    using value_type = matrix_variant_type;

    static void initialize(
        value_type & state,
        std::string const & counting_type,
        int number_of_clauses,
        int number_of_features,
        IRNG & igen);
};


struct TAStateWithSignum : public TAStateBase
{
    struct value_type
    {
        matrix_variant_type matrix;
        bit_matrix_uint64 signum;
    };

    static void initialize(
        value_type & state,
        std::string const & counting_type,
        int number_of_clauses,
        int number_of_features,
        IRNG & igen);
};


}  // namespace Tsetlini


#endif /* LIB_INCLUDE_TA_STATE_HPP_ */
