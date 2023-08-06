import os
import sys
fp = os.path.dirname(os.path.abspath( __file__ ))
fpp = os.path.join(fp, 'src')
sys.path.insert(0 , fpp)

from sklearn_linear_model_modification import *
from sklearn.datasets import load_boston

def load_Xy():
    data = load_boston()
    X = pd.DataFrame( data['data'], columns=data['feature_names'] )
    y = data['target']
    return X, y


def test_mod():
    X, y = load_Xy()

    lmod = Ridge()
    lmod.fit(X, y)
    lmod.predict(X)

    lmod = Lasso()
    lmod.fit(X, y)
    lmod.predict(X)

    lmod = ElasticNet()
    lmod.fit(X, y)
    lmod.predict(X)

    lmod = LinearRegression()
    lmod.fit(X, y)
    lmod.predict(X)

    lmod = NonNegativeLeastSquares()
    lmod.fit(X, y)
    lmod.predict(X)
    assert True


def test_add1():
    X, y = load_Xy()


    lmod = Add1Ridge()
    lmod.fit(X, y)
    lmod.predict(X)
    print(type(lmod.coef_))
    
    lmod = Add1Lasso()
    lmod.fit(X, y)
    lmod.predict(X)

    lmod = Add1ElasticNet()
    lmod.fit(X, y)
    lmod.predict(X)

    lmod = Add1LinearRegression()
    lmod.fit(X, y)
    lmod.predict(X)

    lmod = Add1NonNegativeLeastSquares()
    lmod.fit(X, y)
    lmod.predict(X)
    assert True

def test_drop1():
    X, y = load_Xy()

    lmod = Drop1Ridge()
    lmod.fit(X, y)
    lmod.predict(X)

    lmod = Drop1Lasso()
    lmod.fit(X, y)
    lmod.predict(X)

    lmod = Drop1ElasticNet()
    lmod.fit(X, y)
    lmod.predict(X)

    lmod = Drop1LinearRegression()
    lmod.fit(X, y)
    lmod.predict(X)

    lmod = Drop1NonNegativeLeastSquares()
    lmod.fit(X, y)
    lmod.predict(X)
    assert True
