# coding: utf-8
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.utils.multiclass import unique_labels

from .base import (
    _validate_params, _fit_tsetlin_classifier)


class TsetlinMachineClassifier(BaseEstimator, ClassifierMixin):
    """Tsetlin Machine Multiclass classifier.

    This estimator implements Tsetlin Machine multiclass classifier
    following the example code from https://github.com/cair/TsetlinMachineCython
    with several speed and logic improvements.

    Parameters
    ----------
    number_of_pos_neg_clauses_per_class : int, default=5
        Number of positive / negative clauses per class. E.g. for N classes this
        will lead to the model having
        2 * number_of_pos_neg_clauses_per_class * N clauses.
    number_of_states: int, default=100
        Number of integral states associated with a single Tsetlin automaton.
    s: float, default=2.0
        TODO.
    threshold: int, default=15
        Threshold value for Tsetlin automata.
    boost_true_positive_feedback: int, default=0
        TODO.
    n_jobs: int, default=-1
        The number of CPUs to use for computation.
        ``-1`` means using all processors.
    verbose: bool, default=False
        Flag to disable/enable verbose output
    random_state: int, default=None
        The seed of the pseudo random number generator to use.
        If None, the random number generator is the RandomState
        instance used by `np.random`.

    Attributes
    ----------
    X_ : ndarray, shape (n_samples, n_features)
        The input passed during :meth:`fit`.
    y_ : ndarray, shape (n_samples,)
        The labels passed during :meth:`fit`.
    classes_ : ndarray, shape (n_classes,)
        The classes seen at :meth:`fit`.
    """
    def __init__(self,
                 number_of_pos_neg_clauses_per_class=5,
                 number_of_states=100,
                 s=2.0,
                 threshold=15,
                 boost_true_positive_feedback=0,
                 n_jobs=-1,
                 verbose=False,
                 random_state=None):
        self.number_of_pos_neg_clauses_per_class = number_of_pos_neg_clauses_per_class
        self.number_of_states = number_of_states
        self.s = s
        self.threshold = threshold
        self.boost_true_positive_feedback = boost_true_positive_feedback
        self.n_jobs = n_jobs
        self.verbose = verbose
        self.random_state = random_state


    def fit(self, X, y, n_iter=500):
        """A reference implementation of a fitting function for a classifier.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The training input samples.
        y : array-like, shape (n_samples,)
            The target values. An array of int.

        Returns
        -------
        self : object
            Returns self.
        """

        self.set_params(**_validate_params(self.get_params()))
        n_iter = int(n_iter)
        assert(n_iter > 0)

        # Check that X and y have correct shape
        X, y = check_X_y(X, y)

        self.n_features_ = X.shape[1]

        # Store the classes seen during fit
        # I will need this for partial_fit to verify absence of unseen labels
        # for y=[1, 4, 7, 99, 7] this produces a tuple
        # (array([ 1,  4,  7, 99]), array([0, 1, 2, 3, 2]))
        self.classes_, y = np.unique(y, return_inverse=True)

        if len(self.classes_) < 2:
            raise ValueError("This estimator needs samples of at least 2 classes"
                             " in the data, but the data contains only one"
                             " class: {}".format(self.classes_[0]))

        self.model_ = _fit_tsetlin_classifier(
            X, y, self.get_params(), n_iter)

        return self


    def predict(self, X):
        """A reference implementation of a prediction for a classifier.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        y : ndarray, shape (n_samples,)
            The label for each sample is the label of the closest sample
            seen during fit.
        """
        # Check is fit had been called
        check_is_fitted(self, ['model_'])

        # Input validation
        X = check_array(X)

        return np.ones(X.shape[0])


    def predict_proba(self, X):
        return np.zeros((X.shape[0], self.classes_.size))


    def partial_fit(self, X, y):
        """Fit using existing state of the classifier for online-learning.
        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            Subset of the training data
        y : numpy array, shape (n_samples,)
            Subset of the target values

        Returns
        -------
        self : returns an instance of self.
        """
        return self