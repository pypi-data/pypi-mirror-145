# !/usr/bin/env python
# Created by "Thieu" at 09:29, 23/09/2020 ----------%
#       Email: nguyenthieu2102@gmail.com            %
#       Github: https://github.com/thieu1995        %
# --------------------------------------------------%

from permetrics.evaluator import Evaluator
import numpy as np


class ClassificationMetric(Evaluator):
    """
    This is class contains all classification metrics (for both binary and multiple classification problem)

    Notes
    ~~~~~
    + Extension of: https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics
    """

    def __init__(self, y_true=None, y_pred=None, decimal=5, **kwargs):
        """
        Args:
            y_true (tuple, list, np.ndarray): The ground truth values
            y_pred (tuple, list, np.ndarray): The prediction values
            decimal (int): The number of fractional parts after the decimal point
            **kwargs ():
        """
        super().__init__(y_true, y_pred, decimal, **kwargs)
        if kwargs is None: kwargs = {}
        self.set_keyword_arguments(kwargs)

    def mean_log_likelihood(self, y_true=None, y_pred=None, multi_output="raw_values", decimal=None, non_zero=True, positive=True):
        """
        Mean Log Likelihood (MLL): Best possible score is ..., the higher value is better. Range = (-inf, +inf)

        Link: https://github.com/benhamner/Metrics/blob/master/Python/ml_metrics/elementwise.py#L235

        Args:
            y_true (tuple, list, np.ndarray): The ground truth values
            y_pred (tuple, list, np.ndarray): The prediction values
            multi_output: Can be "raw_values" or list weights of variables such as [0.5, 0.2, 0.3] for 3 columns, (Optional, default = "raw_values")
            decimal (int): The number of fractional parts after the decimal point (Optional, default = 5)
            non_zero (bool): Remove all rows contain 0 value in y_pred (some methods have denominator is y_pred) (Optional, default = True)
            positive (bool): Calculate metric based on positive values only or not (Optional, default = True)

        Returns:
            result (float, int, np.ndarray): MLL metric
        """
        y_true, y_pred, one_dim, decimal = self.get_processed_data(y_true, y_pred, decimal)
        if non_zero:
            y_true, y_pred = self.get_non_zero_data(y_true, y_pred, one_dim, 1)
        else:
            y_pred[y_pred == 0] = self.EPSILON
        y_true, y_pred = self.get_positive_data(y_true, y_pred, one_dim, 2)
        if one_dim:
            return np.round(np.mean(-(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))), decimal)
        else:
            result = np.mean(-(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred)), axis=0)
            return self.get_multi_output_result(result, multi_output, decimal)

    def single_log_likelihood(self, y_true=None, y_pred=None, decimal=None, non_zero=True, positive=True):
        """
        Log Likelihood (LL): Best possible score is ..., the higher value is better. Range = (-inf, +inf)

        Note: Computes the log likelihood between two numbers, or for element between a pair of list, tuple or numpy arrays.

        Args:
            y_true (tuple, list, np.ndarray): The ground truth values
            y_pred (tuple, list, np.ndarray): The prediction values
            multi_output: Can be "raw_values" or list weights of variables such as [0.5, 0.2, 0.3] for 3 columns, (Optional, default = "raw_values")
            decimal (int): The number of fractional parts after the decimal point (Optional, default = 5)
            non_zero (bool): Remove all rows contain 0 value in y_pred (some methods have denominator is y_pred) (Optional, default = True)
            positive (bool): Calculate metric based on positive values only or not (Optional, default = True)

        Returns:
            result (float, int, np.ndarray): LL metric
        """
        y_true, y_pred, one_dim, decimal = self.get_processed_data(y_true, y_pred, decimal)
        if non_zero:
            y_true, y_pred = self.get_non_zero_data(y_true, y_pred, one_dim, 1)
        else:
            y_pred[y_pred == 0] = self.EPSILON
        y_true, y_pred = self.get_positive_data(y_true, y_pred, one_dim, 2)
        return np.round(-(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred)), decimal)

    MLL = mll = mean_log_likelihood
    LL = ll = single_log_likelihood
