from inspect import signature
import numpy as np
from numpy import inf
import pandas as pd

from math import log
from scipy.optimize import nnls, lsq_linear
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression as _LinearRegression
from sklearn.linear_model import ElasticNet as _ElasticNet
from sklearn.linear_model import Ridge as _Ridge
from sklearn.linear_model import Lasso as _Lasso

from statsmodels.stats.outliers_influence import variance_inflation_factor

def _clean_X(X):
    if not isinstance( X, pd.DataFrame):
        X = pd.DataFrame(X)

    return X

def vif(X):

    '''
    The higher the value, the greater the correlation of the
    variable with other variables. Values of more than 4 or 5
    are sometimes regarded as being moderate to high, with
    values of 10 or more being regarded as very high.
    '''
    if X.shape[1] > 1:
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame()

        vif_data = pd.DataFrame()
        vif_data["feature"] = X.columns
        vif_data["VIF"] = [variance_inflation_factor(X.values, i)
                              for i in range(len(X.columns))]

        vif_data.loc[ vif_data['VIF'] <= 4, 'record'] = "low"
        vif_data.loc[ (vif_data['VIF'] > 4)&(vif_data['VIF'] < 10), 'record'] = "moderate"
        vif_data.loc[ vif_data['VIF'] >= 10, 'record'] = "high"
    else:
        vif_data = pd.DataFrame()
        vif_data['feature'] = X.columns
        vif_data['VIF'] = [0]
        vif_data['record'] = None

    return vif_data

class NonNegativeLeastSquares():
    def __init__(self):
        self.__doc__ = nnls.__doc__


    def fit(self, X, y, drop_cols=True):
        nnls.__doc__
        X = _clean_X(X)
        self.coef_, cost = nnls(X, y)

        if drop_cols:
            self.X = X.iloc[:, self.coef_>0 ]
        else:
            self.X = X

        self.num_params = self.X.shape[1]

        if drop_cols:
            # required for Drop1
            self.coef_= [i for i in self.coef_ if i != 0 ]


        self.vif = vif(self.X)

    def predict(self, X):
        return np.dot(X[self.X.columns], self.coef_ )

class BoundedLinearRegression():
    def __init__(self):
        self.__doc__ = nnls.__doc__

    def fit(self, X, y, bounds=(-inf, inf), method='trf',
        tol=1e-10, lsq_solver=None, lsmr_tol=None, max_iter=None,
        verbose=0
    ):
        lsq_linear.__doc__
        X = _clean_X(X)
        self.coef_, cost = lsq_linear(X, y, bounds=bounds, method=method,
        tol=tol, lsq_solver=lsq_solver, lsmr_tol=lsmr_tol, max_iter=max_iter,
        verbose=verbose)
        self.X = X.iloc[:, self.coefs_!=0 ]
        self.coef_= [i for i in self.coef_ if i != 0 ]
        self.num_params = self.X.shape[1]
        self.vif = vif(self.X)

    def predict(self, X):
        return np.dot(X[self.X.columns], self.coef_ )



class LinearRegression(_LinearRegression):

    def __init__(self, fit_intercept=True, normalize=False, copy_X=True, n_jobs=None, positive=False):
        super().__init__(fit_intercept=fit_intercept, normalize=normalize, copy_X=copy_X, n_jobs=n_jobs, positive=positive)
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params

    def predict(self, X):
        super().predict.__doc__
        return super().predict(X[self.X.columns.tolist()])

    def fit(self, X, y, sample_weight=None):
        super().fit.__doc__
        super().fit(X, y, sample_weight=sample_weight)
        self._calculate_aic(X, y)
        self.X = X
        self.vif = vif(self.X)

class ElasticNet(_ElasticNet):

    def __init__(self, alpha=1.0, l1_ratio=0.5, fit_intercept=True, normalize=False, precompute=False, max_iter=1000, copy_X=True, tol=0.0001, warm_start=False, positive=False, random_state=None, selection='cyclic'):
        super().__init__(alpha=alpha, l1_ratio=l1_ratio, fit_intercept=fit_intercept, normalize=normalize, precompute=precompute, max_iter=max_iter, copy_X=copy_X, tol=tol, warm_start=warm_start, positive=positive, random_state=random_state, selection=selection)
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params

    def predict(self, X):
        super().predict.__doc__
        return super().predict(X[self.X.columns.tolist()])

    def fit(self, X, y, sample_weight=None, check_input=True):
        super().fit.__doc__
        super().fit(X, y, sample_weight=sample_weight, check_input=check_input)
        self._calculate_aic(X, y)
        self.X = X
        self.vif = vif(self.X)

class Ridge(_Ridge):

    def __init__(self, alpha=1.0, fit_intercept=True, normalize=False, copy_X=True, max_iter=None, tol=0.001, solver='auto', random_state=None):
        super().__init__(alpha=alpha, fit_intercept=fit_intercept, normalize=normalize, copy_X=copy_X, max_iter=max_iter, tol=tol, solver=solver, random_state=random_state)
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params

    def predict(self, X):
        return super().predict(X[self.X.columns.tolist()])

    def fit(self, X, y, sample_weight=None):
        super().fit(X, y, sample_weight=sample_weight)
        self._calculate_aic(X, y)
        self.X = X
        self.vif = vif(self.X)


class Lasso(_Lasso):

    def __init__(self, alpha=1.0, fit_intercept=True, normalize=False, precompute=False, copy_X=True, max_iter=1000, tol=0.0001, warm_start=False, positive=False, random_state=None, selection='cyclic'):
        super().__init__(alpha=alpha, fit_intercept=fit_intercept, normalize=normalize, precompute=precompute, copy_X=copy_X, max_iter=max_iter, tol=tol, warm_start=warm_start, positive=positive, random_state=random_state, selection=selection
)
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params

    def predict(self, X):
        return super().predict(X[self.X.columns.tolist()])

    def fit(self, X, y, sample_weight=None, check_input=True):
        super().fit(X, y, sample_weight=sample_weight, check_input=check_input)
        self._calculate_aic(X, y)
        self.X = X
        self.vif = vif(self.X)

class Add1NonNegativeLeastSquares(NonNegativeLeastSquares):
    def __init__(self):
        super().__init__()
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params

    def predict(self, X):
        super().predict.__doc__
        return super().predict(X[self.X.columns.tolist()])

    def fit(self, X, y, max_n=None):
        super().fit.__doc__
        super().fit(X, y, False)
        self._calculate_aic(X, y)
        self.X = X
        current_index = []
        aic_dict = {}

        while True:

            for i in range(0, X.shape[1] ):
                if not i in current_index or current_index == []:
                    new_index = current_index+[i]

                    if isinstance(X, pd.DataFrame):
                        newX = X.iloc[:, new_index ]
                    else:
                        newX = X[:, new_index ]

                    super().fit(newX, y, False)
                    self._calculate_aic(newX, y)


                    aic_dict[ i ] = {'new_index': new_index, 'aic':self.aic, 'X': newX, 'model': super()}

            best_label, best_dict = [
                (k,v) for k, v in aic_dict.items()
                if v['aic'] == min( [j['aic'] for j in aic_dict.values()] )
            ][0]

            self.aic = best_dict['aic']
            self.X = best_dict['X']
            new_index = best_dict['new_index']

            super().fit(self.X, y, False)

            if best_label =='current' or (max_n != None and self.X.shape[1] >= max_n):
                break
            else:
                aic_dict = {}
                aic_dict['current'] = {'aic':self.aic, 'new_index': new_index, 'X': self.X, 'model': super()}
                current_index = new_index

                if len(current_index)==X.shape[1]:

                    super().fit(self.X, y, True)
                    self.aic = best_dict['aic']
                    self.X = best_dict['X']
                    break

        self.vif = vif(self.X)

class Add1LinearRegression(_LinearRegression):
    def __init__(self, fit_intercept=True, normalize=False, copy_X=True, n_jobs=None, positive=False):
        super().__init__(fit_intercept=fit_intercept, normalize=normalize, copy_X=copy_X, n_jobs=n_jobs, positive=positive
)
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params

    def predict(self, X):
        super().predict.__doc__
        return super().predict(X[self.X.columns.tolist()])

    def fit(self, X, y, max_n=None, sample_weight=None):
        super().fit.__doc__
        super().fit(X, y, sample_weight=sample_weight)
        self._calculate_aic(X, y)
        self.X = X
        current_index = []
        aic_dict = {}

        while True:

            for i in range(0, X.shape[1] ):
                if not i in current_index or current_index == []:
                    new_index = current_index+[i]

                    if isinstance(X, pd.DataFrame):
                        newX = X.iloc[:, new_index ]
                    else:
                        newX = X[:, new_index ]

                    super().fit(newX, y)
                    self._calculate_aic(newX, y)


                    aic_dict[ i ] = {'new_index': new_index, 'aic':self.aic, 'X': newX, 'model': super()}

            best_label, best_dict = [
                (k,v) for k, v in aic_dict.items()
                if v['aic'] == min( [j['aic'] for j in aic_dict.values()] )
            ][0]

            self.aic = best_dict['aic']
            self.X = best_dict['X']
            new_index = best_dict['new_index']

            super().fit(self.X, y, sample_weight=sample_weight)

            if best_label =='current' or (max_n != None and self.X.shape[1] >= max_n):
                break
            else:
                aic_dict = {}
                aic_dict['current'] = {'aic':self.aic, 'new_index': new_index, 'X': self.X, 'model': super()}
                current_index = new_index

                if len(current_index)==X.shape[1]:

                    super().fit(self.X, y)
                    self.aic = best_dict['aic']
                    self.X = best_dict['X']
                    break

        self.vif = vif(self.X)

class Add1ElasticNet(_ElasticNet):
    def __init__(self, alpha=1.0, l1_ratio=0.5, fit_intercept=True, normalize=False, precompute=False, max_iter=1000, copy_X=True, tol=0.0001, warm_start=False, positive=False, random_state=None, selection='cyclic'):
        super().__init__(alpha=alpha, l1_ratio=l1_ratio, fit_intercept=fit_intercept, normalize=normalize, precompute=precompute, max_iter=max_iter, copy_X=copy_X, tol=tol, warm_start=warm_start, positive=positive, random_state=random_state, selection=selection)
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params

    def predict(self, X):
        super().predict.__doc__
        return super().predict(X[self.X.columns.tolist()])

    def fit(self, X, y, max_n=None, sample_weight=None, check_input=True):
        super().fit.__doc__
        super().fit(X, y, sample_weight=sample_weight, check_input=check_input)
        self._calculate_aic(X, y)
        self.X = X
        current_index = []
        aic_dict = {}

        while True:

            for i in range(0, X.shape[1] ):
                if not i in current_index or current_index == []:
                    new_index = current_index+[i]

                    if isinstance(X, pd.DataFrame):
                        newX = X.iloc[:, new_index ]
                    else:
                        newX = X[:, new_index ]

                    super().fit(newX, y, sample_weight=sample_weight, check_input=check_input)
                    self._calculate_aic(newX, y)


                    aic_dict[ i ] = {'new_index': new_index, 'aic':self.aic, 'X': newX, 'model': super()}

            best_label, best_dict = [
                (k,v) for k, v in aic_dict.items()
                if v['aic'] == min( [j['aic'] for j in aic_dict.values()] )
            ][0]

            self.aic = best_dict['aic']
            self.X = best_dict['X']
            new_index = best_dict['new_index']

            super().fit(self.X, y, sample_weight=sample_weight, check_input=check_input)

            if best_label =='current' or (max_n != None and self.X.shape[1] >= max_n):
                break
            else:
                aic_dict = {}
                aic_dict['current'] = {'aic':self.aic, 'new_index': new_index, 'X': self.X, 'model': super()}
                current_index = new_index

                if len(current_index)==X.shape[1]:

                    super().fit(self.X, y, sample_weight=sample_weight, check_input=check_input)
                    self.aic = best_dict['aic']
                    self.X = best_dict['X']
                    break

        self.vif = vif(self.X)

class Add1Ridge(_Ridge):
    def __init__(self, alpha=1.0, fit_intercept=True, normalize=False, copy_X=True, max_iter=None, tol=0.001, solver='auto', random_state=None):
        super().__init__(alpha=alpha, fit_intercept=fit_intercept, normalize=normalize, copy_X=copy_X, max_iter=max_iter, tol=tol, solver=solver, random_state=random_state)
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params

    def predict(self, X):
        super().predict.__doc__
        return super().predict(X[self.X.columns.tolist()])

    def fit(self, X, y, max_n=None, sample_weight=None):
        super().fit.__doc__
        super().fit(X, y, sample_weight=sample_weight)
        self._calculate_aic(X, y)
        self.X = X
        current_index = []
        aic_dict = {}

        while True:

            for i in range(0, X.shape[1] ):
                if not i in current_index or current_index == []:
                    new_index = current_index+[i]

                    if isinstance(X, pd.DataFrame):
                        newX = X.iloc[:, new_index ]
                    else:
                        newX = X[:, new_index ]

                    super().fit(newX, y, sample_weight=sample_weight)
                    self._calculate_aic(newX, y)


                    aic_dict[ i ] = {'new_index': new_index, 'aic':self.aic, 'X': newX, 'model': super()}

            best_label, best_dict = [
                (k,v) for k, v in aic_dict.items()
                if v['aic'] == min( [j['aic'] for j in aic_dict.values()] )
            ][0]

            self.aic = best_dict['aic']
            self.X = best_dict['X']
            new_index = best_dict['new_index']

            super().fit(self.X, y, sample_weight=sample_weight)

            if best_label =='current' or (max_n != None and self.X.shape[1] >= max_n):
                break
            else:
                aic_dict = {}
                aic_dict['current'] = {'aic':self.aic, 'new_index': new_index, 'X': self.X, 'model': super()}
                current_index = new_index

                if len(current_index)==X.shape[1]:

                    super().fit(self.X, y, sample_weight=sample_weight)
                    self.aic = best_dict['aic']
                    self.X = best_dict['X']
                    break

        self.vif = vif(self.X)

class Add1Lasso(_Lasso):
    def __init__(self, alpha=1.0, fit_intercept=True, normalize=False, precompute=False, copy_X=True, max_iter=1000, tol=0.0001, warm_start=False, positive=False, random_state=None, selection='cyclic'):
        super().__init__(alpha=alpha, fit_intercept=fit_intercept, normalize=normalize, precompute=precompute, copy_X=copy_X, max_iter=max_iter, tol=tol, warm_start=warm_start, positive=positive, random_state=random_state, selection=selection)
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params

    def predict(self, X):
        super().predict.__doc__
        return super().predict(X[self.X.columns.tolist()])

    def fit(self, X, y, max_n=None, sample_weight=None, check_input=True):
        super().fit.__doc__
        super().fit(X, y, sample_weight=sample_weight, check_input=check_input)
        self._calculate_aic(X, y)
        self.X = X
        current_index = []
        aic_dict = {}

        while True:

            for i in range(0, X.shape[1] ):
                if not i in current_index or current_index == []:
                    new_index = current_index+[i]

                    if isinstance(X, pd.DataFrame):
                        newX = X.iloc[:, new_index ]
                    else:
                        newX = X[:, new_index ]

                    super().fit(newX, y)
                    self._calculate_aic(newX, y)


                    aic_dict[ i ] = {'new_index': new_index, 'aic':self.aic, 'X': newX, 'model': super()}

            best_label, best_dict = [
                (k,v) for k, v in aic_dict.items()
                if v['aic'] == min( [j['aic'] for j in aic_dict.values()] )
            ][0]

            self.aic = best_dict['aic']
            self.X = best_dict['X']
            new_index = best_dict['new_index']

            super().fit(self.X, y, sample_weight=sample_weight, check_input=check_input)

            if best_label =='current' or (max_n != None and self.X.shape[1] >= max_n):
                break
            else:
                aic_dict = {}
                aic_dict['current'] = {'aic':self.aic, 'new_index': new_index, 'X': self.X, 'model': super()}
                current_index = new_index

                if len(current_index)==X.shape[1]:

                    super().fit(self.X, y, sample_weight=sample_weight, check_input=check_input)
                    self.aic = best_dict['aic']
                    self.X = best_dict['X']
                    break

        self.vif = vif(self.X)

def _drop_column_by_index(X, i):
    '''
    X : pd.DataFrame, numpy array
    i:number
    '''

    if isinstance(X, pd.DataFrame):

        col = X.columns[i]
        new_X = X.loc[:, [i for i in X.columns if i != col ]]
    else:
        new_X = np.delete(X, i, 1)



    return new_X


class Drop1ElasticNet(_ElasticNet):

    def __init__(self, alpha=1.0, l1_ratio=0.5, fit_intercept=True, normalize=False, precompute=False, max_iter=1000, copy_X=True, tol=0.0001, warm_start=False, positive=False, random_state=None, selection='cyclic'):
        super().__init__(alpha=alpha, l1_ratio=l1_ratio, fit_intercept=fit_intercept, normalize=normalize, precompute=precompute, max_iter=max_iter, copy_X=copy_X, tol=tol, warm_start=warm_start, positive=positive, random_state=random_state, selection=selection)
        self.__doc__ = super().__doc__


    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params

    def predict(self, X):
        super().predict.__doc__
        return super().predict(X[self.X.columns.tolist()])

    def fit(self, X, y, sample_weight=None, check_input=True):
        super().fit.__doc__
        super().fit(X, y, sample_weight=sample_weight, check_input=check_input)
        self._calculate_aic(X, y)
        self.X = X

        while True:

            aic_dict = {}
            aic_dict['current'] = {'aic':self.aic, 'X': self.X, 'model': super()}
            start_X = self.X.copy(deep=True)
            for i in range(0, self.num_params-1):
                newX = _drop_column_by_index(start_X, i)
                super().fit(newX, y)
                self._calculate_aic(newX, y)
                aic_dict[i] = {'aic':self.aic, 'X': newX, 'model': super() }

            best_label, best_dict = [
                (k,v) for k, v in aic_dict.items()
                if v['aic'] == min( [j['aic'] for j in aic_dict.values()] )
            ][0]

            self.aic = best_dict['aic']
            self.X = best_dict['X']
            super().fit(self.X, y)

            if best_label =='current':
                break

        self.vif = vif(self.X)

class Drop1NonNegativeLeastSquares(NonNegativeLeastSquares):
    def __init__(self):
        super().__init__()
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params

    def predict(self, X):
        super().predict.__doc__
        return super().predict(X[self.X.columns.tolist()])

    def fit(self, X, y):

        super().fit(X, y, False)
        self._calculate_aic(X, y)
        self.X = X


        while True:

            aic_dict = {}
            aic_dict['current'] = {'aic':self.aic, 'X': self.X, 'model': super()}

            start_X = self.X.copy(deep=True)
            for i in range(0, self.num_params-1):
                newX = _drop_column_by_index(start_X, i)
                super().fit(newX, y, False)
                self._calculate_aic(newX, y)
                aic_dict[i] = {'aic':self.aic, 'X': newX, 'model': super() }

            best_label, best_dict = [
                (k,v) for k, v in aic_dict.items()
                if v['aic'] == min( [j['aic'] for j in aic_dict.values()] )
            ][0]

            self.aic = best_dict['aic']
            self.X = best_dict['X']
            super().fit(self.X, y, False)

            if best_label =='current':
                super().fit(self.X, y, True)
                break

        self.vif = vif(self.X)

class Drop1LinearRegression(_LinearRegression):
    def __init__(self, fit_intercept=True, normalize=False, copy_X=True, n_jobs=None, positive=False):
        super().__init__(fit_intercept=fit_intercept, normalize=normalize, copy_X=copy_X, n_jobs=n_jobs, positive=positive)
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params

    def predict(self, X):
        super().predict.__doc__
        return super().predict(X[self.X.columns.tolist()])

    def fit(self, X, y, sample_weight=None):

        super().fit(X, y, sample_weight=None)
        self._calculate_aic(X, y)
        self.X = X


        while True:

            aic_dict = {}
            aic_dict['current'] = {'aic':self.aic, 'X': self.X, 'model': super()}

            start_X = self.X.copy(deep=True)
            for i in range(0, self.num_params-1):
                newX = _drop_column_by_index(start_X, i)
                super().fit(newX, y, sample_weight=sample_weight)
                self._calculate_aic(newX, y)
                aic_dict[i] = {'aic':self.aic, 'X': newX, 'model': super() }

            best_label, best_dict = [
                (k,v) for k, v in aic_dict.items()
                if v['aic'] == min( [j['aic'] for j in aic_dict.values()] )
            ][0]

            self.aic = best_dict['aic']
            self.X = best_dict['X']
            super().fit(self.X, y, sample_weight=sample_weight)

            if best_label =='current':
                break

        self.vif = vif(self.X)

class Drop1Lasso(_Lasso):
    def __init__(self, alpha=1.0, fit_intercept=True, normalize=False, precompute=False, copy_X=True, max_iter=1000, tol=0.0001, warm_start=False, positive=False, random_state=None, selection='cyclic'):
        super().__init__(alpha=alpha, fit_intercept=fit_intercept, normalize=normalize, precompute=precompute, copy_X=copy_X, max_iter=max_iter, tol=tol, warm_start=warm_start, positive=positive, random_state=random_state, selection=selection)
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params

    def predict(self, X):
        super().predict.__doc__
        return super().predict(X[self.X.columns.tolist()])

    def fit(self, X, y, sample_weight=None, check_input=True):
        super().fit.__doc__
        super().fit(X, y, sample_weight=sample_weight, check_input=check_input)
        self._calculate_aic(X, y)
        self.X = X

        while True:

            aic_dict = {}
            aic_dict['current'] = {'aic':self.aic, 'X': self.X, 'model': super()}
            start_X = self.X.copy(deep=True)
            for i in range(0, self.num_params-1):
                newX = _drop_column_by_index(start_X, i)
                super().fit(newX, y)
                self._calculate_aic(newX, y)
                aic_dict[i] = {'aic':self.aic, 'X': newX, 'model': super() }

            best_label, best_dict = [
                (k,v) for k, v in aic_dict.items()
                if v['aic'] == min( [j['aic'] for j in aic_dict.values()] )
            ][0]

            self.aic = best_dict['aic']
            self.X = best_dict['X']
            super().fit(self.X, y)

            if best_label =='current':
                break

        self.vif = vif(self.X)

class Drop1Ridge(_Ridge):
    def __init__(self, alpha=1.0, fit_intercept=True, normalize=False, copy_X=True, max_iter=None, tol=0.001, solver='auto', random_state=None):
        super().__init__(alpha=alpha, fit_intercept=fit_intercept, normalize=normalize, copy_X=copy_X, max_iter=max_iter, tol=tol, solver=solver, random_state=random_state)
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params

    def predict(self, X):
        super().predict.__doc__
        return super().predict(X[self.X.columns.tolist()])

    def fit(self, X, y, sample_weight=None):
        super().fit.__doc__
        super().fit(X, y, sample_weight=sample_weight)
        self._calculate_aic(X, y)
        self.X = X


        while True:

            aic_dict = {}
            aic_dict['current'] = {'aic':self.aic, 'X': self.X, 'model': super()}
            start_X = self.X.copy(deep=True)
            for i in range(0, self.num_params-1):
                newX = _drop_column_by_index(start_X, i)
                super().fit(newX, y, sample_weight=sample_weight)
                self._calculate_aic(newX, y)
                aic_dict[i] = {'aic':self.aic, 'X': newX, 'model': super() }

            best_label, best_dict = [
                (k,v) for k, v in aic_dict.items()
                if v['aic'] == min( [j['aic'] for j in aic_dict.values()] )
            ][0]

            self.aic = best_dict['aic']
            self.X = best_dict['X']
            super().fit(self.X, y)

            if best_label =='current':
                break


        self.vif = vif(self.X)
