#include "estimator_state_cache.hpp"
#include "tsetlini_params.hpp"
#include "params_companion.hpp"
#include "mt.hpp"


namespace Tsetlini
{


void ClassifierStateCache::reset(
    ClassifierStateCache::value_type & cache,
    params_t const & params,
    FRNG & fgen,
    IRNG const & igen)
{
    cache.clause_output.clear();
    cache.clause_output.resize(Params::number_of_classifier_clauses(params) / 2);
    cache.label_sum.clear();
    cache.label_sum.resize(Params::number_of_labels(params));
    cache.feedback_to_clauses.clear();
    cache.feedback_to_clauses.resize(Params::number_of_classifier_clauses(params) / 2);

    // initialize frand cache
    cache.fcache = ClassifierStateCache::frand_cache_type(fgen, 2 * Params::number_of_features(params), igen.peek());
}


bool ClassifierStateCache::are_equal(value_type const & lhs, value_type const & rhs)
{
    return
        lhs.feedback_to_clauses.size() == rhs.feedback_to_clauses.size()
        and lhs.clause_output.size() == rhs.clause_output.size()
        and lhs.label_sum.size() == rhs.label_sum.size();
}


void RegressorStateCache::reset(
    RegressorStateCache::value_type & cache,
    params_t const & params,
    FRNG & fgen,
    IRNG const & igen)
{
    cache.clause_output.clear();
    cache.clause_output.resize(Params::number_of_regressor_clauses(params) / 2);
    cache.feedback_to_clauses.clear();
    cache.feedback_to_clauses.resize(Params::number_of_regressor_clauses(params) / 2);

    // initialize frand cache
    cache.fcache = RegressorStateCache::frand_cache_type(fgen, 2 * Params::number_of_features(params), igen.peek());
}


bool RegressorStateCache::are_equal(value_type const & lhs, value_type const & rhs)
{
    return
        lhs.feedback_to_clauses.size() == rhs.feedback_to_clauses.size()
        and lhs.clause_output.size() == rhs.clause_output.size();
}


}  // namespace Tsetlini