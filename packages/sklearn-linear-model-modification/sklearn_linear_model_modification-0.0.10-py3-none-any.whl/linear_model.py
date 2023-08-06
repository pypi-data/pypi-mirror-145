import numpy as np
import pandas as pd

from math import log
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression as _LinearRegression
from sklearn.linear_model import ElasticNet as _ElasticNet
from sklearn.linear_model import Ridge as _Ridge
from sklearn.linear_model import Lasso as _Lasso

from statsmodels.stats.outliers_influence import variance_inflation_factor

def vif(X):

    '''
    The higher the value, the greater the correlation of the
    variable with other variables. Values of more than 4 or 5
    are sometimes regarded as being moderate to high, with
    values of 10 or more being regarded as very high.
    '''

    if not isinstance(X, pd.DataFrame):
        X = pd.DataFrame()

    vif_data = pd.DataFrame()
    vif_data["feature"] = X.columns
    vif_data["VIF"] = [variance_inflation_factor(X.values, i)
                          for i in range(len(X.columns))]

    vif_data.loc[ vif_data['VIF'] <= 4, 'record'] = "low"
    vif_data.loc[ (vif_data['VIF'] > 4)&(vif_data['VIF'] < 10), 'record'] = "moderate"
    vif_data.loc[ vif_data['VIF'] >= 10, 'record'] = "high"
    return vif_data

class LinearRegression(_LinearRegression):

    def __init__(self):
        super().__init__()
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params

    def fit(self, X, y):
        super().fit(X, y)
        self._calculate_aic(X, y)
        self.X = X
        self.vif = vif(self.X)

class ElasticNet(_ElasticNet):

    def __init__(self):
        super().__init__()
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params

    def fit(self, X, y):
        super().fit(X, y)
        self._calculate_aic(X, y)
        self.X = X
        self.vif = vif(self.X)

class Ridge(_Ridge):

    def __init__(self):
        super().__init__()
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params

    def fit(self, X, y):
        super().fit(X, y)
        self._calculate_aic(X, y)
        self.X = X
        self.vif = vif(self.X)


class Lasso(_Lasso):

    def __init__(self):
        super().__init__()
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params

    def fit(self, X, y):
        super().fit(X, y)
        self._calculate_aic(X, y)
        self.X = X
        self.vif = vif(self.X)

class Add1LinearRegression(_LinearRegression):
    def __init__(self):
        super().__init__()
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params


    def fit(self, X, y):

        super().fit(X, y)
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

            super().fit(self.X, y)

            if best_label =='current':
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
    def __init__(self):
        super().__init__()
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params


    def fit(self, X, y):

        super().fit(X, y)
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

            super().fit(self.X, y)

            if best_label =='current':
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

class Add1Ridge(_Ridge):
    def __init__(self):
        super().__init__()
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params


    def fit(self, X, y):

        super().fit(X, y)
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

            super().fit(self.X, y)

            if best_label =='current':
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

class Add1Lasso(_Lasso):
    def __init__(self):
        super().__init__()
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params


    def fit(self, X, y):

        super().fit(X, y)
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

            super().fit(self.X, y)

            if best_label =='current':
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

def _drop_column_by_index(X, i):
    '''
    X : pd.DataFrame, numpy array
    i:number
    '''
    if isinstance(X, pd.DataFrame):
        X = X.drop(X.columns[i], axis=1).copy()
    else:
        X = np.delete(X, i, 1)

    return X


class Drop1ElasticNet(_ElasticNet):
    def __init__(self):
        super().__init__()
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params


    def fit(self, X, y):

        super().fit(X, y)
        self._calculate_aic(X, y)
        self.X = X


        while True:

            aic_dict = {}
            aic_dict['current'] = {'aic':self.aic, 'X': self.X, 'model': super()}

            for i in range(0, self.num_params-1):
                newX = _drop_column_by_index(self.X, i)
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

class Drop1LinearRegression(_LinearRegression):
    def __init__(self):
        super().__init__()
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params


    def fit(self, X, y):

        super().fit(X, y)
        self._calculate_aic(X, y)
        self.X = X


        while True:

            aic_dict = {}
            aic_dict['current'] = {'aic':self.aic, 'X': self.X, 'model': super()}

            for i in range(0, self.num_params-1):
                newX = _drop_column_by_index(self.X, i)
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

class Drop1Lasso(_Lasso):
    def __init__(self):
        super().__init__()
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params


    def fit(self, X, y):

        super().fit(X, y)
        self._calculate_aic(X, y)
        self.X = X


        while True:

            aic_dict = {}
            aic_dict['current'] = {'aic':self.aic, 'X': self.X, 'model': super()}

            for i in range(0, self.num_params-1):
                newX = _drop_column_by_index(self.X, i)
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
    def __init__(self):
        super().__init__()
        self.__doc__ = super().__doc__

    def _calculate_aic(self, X, y):
        n = len(y)
        yhat = super().predict(X)
        self.mse = mean_squared_error(y, yhat)
        self.num_params = len(self.coef_) + 1
        self.aic = n * log(self.mse) + 2 * self.num_params


    def fit(self, X, y):

        super().fit(X, y)
        self._calculate_aic(X, y)
        self.X = X


        while True:

            aic_dict = {}
            aic_dict['current'] = {'aic':self.aic, 'X': self.X, 'model': super()}

            for i in range(0, self.num_params-1):
                newX = _drop_column_by_index(self.X, i)
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
