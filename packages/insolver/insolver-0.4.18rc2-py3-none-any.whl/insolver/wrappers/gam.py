from functools import partial

from pandas import DataFrame, Series, concat
from numpy import sum, sqrt, repeat

from h2o.frame import H2OFrame
from h2o.estimators.gam import H2OGeneralizedAdditiveEstimator

from .base import InsolverBaseWrapper
from .extensions import InsolverH2OExtension, InsolverPDPExtension
from .extensions.h2oext import to_h2oframe


class InsolverGAMWrapper(InsolverBaseWrapper, InsolverH2OExtension, InsolverPDPExtension):
    """Insolver wrapper for Generalized Additive Models.

    Parameters:
        backend (str): Framework for building GAM, currently 'h2o' is supported.
        family (str, float, int, optional): Distribution for GAM. Supports any family from h2o as
        str. By default, Gaussian GAM is fitted.
        link (str, optional): Link function for GAM. If `None`, sets to default value for h2o.
        standardize (bool, optional): Whether to standardize data before fitting the model. Enabled by default.
        h2o_init_params (dict, optional): Parameters passed to `h2o.init()`, when `backend` == 'h2o'.
        load_path (str, optional): Path to GAM model to load from disk.
        **kwargs: Parameters for GAM estimator (for H2OGeneralizedAdditiveEstimator) except `family` and `link`.
        """
    def __init__(self, backend, family=None, link=None, standardize=True, h2o_init_params=None,
                 load_path=None, **kwargs):
        super(InsolverGAMWrapper, self).__init__(backend)
        self.algo, self._backends = 'gam', ['h2o']
        self._back_load_dict = {'h2o': partial(self._h2o_load, h2o_init_params=h2o_init_params)}
        self._back_save_dict = {'h2o': self._h2o_save}

        if backend not in self._backends:
            raise NotImplementedError(f'Error with the backend choice. Supported backends: {self._backends}')

        self.params, self.standardize = None, standardize
        if load_path is not None:
            self.load_model(load_path)
        else:
            family = family if family is not None else 'gaussian'
            link = link if link is not None else 'family_default' if backend == 'h2o' else 'auto'
            if backend == 'h2o':
                self._h2o_init(h2o_init_params)
                self.model = H2OGeneralizedAdditiveEstimator(family=family, link=link, standardize=self.standardize,
                                                             **kwargs)
        self._update_meta()

    def fit(self, X, y, sample_weight=None, X_valid=None, y_valid=None, sample_weight_valid=None, **kwargs):
        """Fit a Generalized Additive Model.

        Args:
            X (pd.DataFrame, pd.Series): Training data.
            y (pd.DataFrame, pd.Series): Training target values.
            sample_weight (pd.DataFrame, pd.Series, optional): Training sample weights.
            X_valid (pd.DataFrame, pd.Series, optional): Validation data (only h2o supported).
            y_valid (pd.DataFrame, pd.Series, optional): Validation target values (only h2o supported).
            sample_weight_valid (pd.DataFrame, pd.Series, optional): Validation sample weights.
            **kwargs: Other parameters passed to H2OGeneralizedAdditiveEstimator.
        """
        if (self.backend == 'h2o') & isinstance(self.model, H2OGeneralizedAdditiveEstimator):
            features, target, train_set, params = self._x_y_to_h2o_frame(X, y, sample_weight, {**kwargs}, X_valid,
                                                                         y_valid, sample_weight_valid)
            self.model.train(y=target, x=features, training_frame=train_set, **params)
        else:
            raise NotImplementedError(f'Error with the backend choice. Supported backends: {self._backends}')
        self._update_meta()

    def predict(self, X, sample_weight=None, **kwargs):
        """Predict using GAM with feature matrix X.

        Args:
            X (pd.DataFrame, pd.Series): Samples.
            sample_weight (pd.DataFrame, pd.Series, optional): Test sample weights.
            **kwargs: Other parameters passed to H2OGeneralizedAdditiveEstimator.predict().

        Returns:
            array: Returns predicted values.
        """
        if (self.backend == 'h2o') & isinstance(self.model, H2OGeneralizedAdditiveEstimator):
            if self.model.parms['offset_column']['actual_value'] is not None and sample_weight is None:
                offset_name = self.model.parms['offset_column']['actual_value']['column_name']
                sample_weight = Series(repeat(0, len(X)), name=offset_name, index=X.index)
            if sample_weight is not None:
                X = concat([X, sample_weight], axis=1)
            h2o_predict = X if isinstance(X, H2OFrame) else to_h2oframe(X)
            predictions = self.model.predict(h2o_predict, **kwargs).as_data_frame().values.reshape(-1)
        else:
            raise NotImplementedError(f'Error with the backend choice. Supported backends: {self._backends}')
        return predictions

    def coef_norm(self):
        """Output GAM coefficients for standardized data.

        Returns:
            dict: {`str`: `float`} Dictionary containing GAM coefficients for standardized data.
        """
        if self.standardize:
            if (self.backend == 'h2o') & isinstance(self.model, H2OGeneralizedAdditiveEstimator):
                coefs = self.model.coef_norm()
            else:
                raise NotImplementedError(f'Error with the backend choice. Supported backends: {self._backends}')
        else:
            raise Exception('Normalized coefficients unavailable since model fitted on non-standardized data.')
        return coefs

    def coef(self):
        """Output GAM coefficients for non-standardized data. Also calculated when GAM fitted on standardized data.

        Returns:
            dict: {`str`: `float`} Dictionary containing GAM coefficients for non-standardized data.
        """
        if (self.backend == 'h2o') & isinstance(self.model, H2OGeneralizedAdditiveEstimator):
            coefs = self.model.coef()
        else:
            raise NotImplementedError(f'Error with the backend choice. Supported backends: {self._backends}')
        return coefs
