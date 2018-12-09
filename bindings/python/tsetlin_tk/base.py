import json


from . import libtsetlin


def _validate_params(params):
    rv = dict(params)

    for k, v in params.items():
        if k == "s":
            v = float(v)
            assert(v > 0.)
        elif k == "boost_true_positive_feedback":
            v = int(v)
            assert(v in [0, 1])
        elif k == "n_jobs":
            v = int(v)
            assert(v == -1 or v > 0)
        elif k == "number_of_pos_neg_clauses_per_class":
            v = int(v)
            assert(v > 0)
        elif k == "number_of_states":
            v = int(v)
            assert(v > 0)
        elif k == "random_state":
            if v is not None:
                v = int(v)
        elif k == "threshold":
            v = int(v)
            assert(v > 0)
        elif k == "verbose":
            v = bool(v)

        rv[k] = v

    return rv


def _params_as_json_bytes(params):
    return json.dumps(params).encode('UTF-8')


def _fit_tsetlin_classifier(X, y, params, n_iter):
    """
    "number_of_labels" and "number_of_features" will be derived from X and y
    """
    js_state = libtsetlin.classifier_fit(_params_as_json_bytes(params))

    return "{}"