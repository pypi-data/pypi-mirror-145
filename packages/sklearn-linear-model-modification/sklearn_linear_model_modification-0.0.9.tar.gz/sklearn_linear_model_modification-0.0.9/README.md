# SKLearn Linear Model Modification

This class should act exactly like sklearn linear model to solve regression problems with the benefit of being able to use drop1 and add1 based on AIC.


## Installation

Run the following to install:

```python
pip install sklearn_linear_model_modification
```

## Usage

```
import pandas as pd
from sklearn_linear_model_modification import LinearRegression, Add1LinearRegression, Drop1LinearRegression
from sklearn_linear_model_modification import Lasso, Add1Lasso, Drop1Lasso
from sklearn_linear_model_modification import ElasticNet, Add1ElasticNet, Drop1ElasticNet
from sklearn_linear_model_modification import Ridge, Add1Ridge, Drop1Ridge

def load_Xy():
    data = load_boston()
    X = pd.DataFrame( data['data'], columns=data['feature_names'] )
    y = data['target']
    return X, y



X, y = load_Xy()

lmod = Ridge()
lmod.fit(X, y)

lmod = Lasso()
lmod.fit(X, y)

lmod = ElasticNet()
lmod.fit(X, y)

lmod = LinearRegression()
lmod.fit(X, y)


lmod = Add1Ridge()
lmod.fit(X, y)

lmod = Add1Lasso()
lmod.fit(X, y)

lmod = Add1ElasticNet()
lmod.fit(X, y)

lmod = Add1LinearRegression()
lmod.fit(X, y)

lmod = Drop1Ridge()
lmod.fit(X, y)

lmod = Drop1Lasso()
lmod.fit(X, y)

lmod = Drop1ElasticNet()
lmod.fit(X, y)

lmod = Drop1LinearRegression()
lmod.fit(X, y)
```

## Development sklearn_linear_model_modification

To install sklearn_linear_model_modification, along with the tools you need to develop and run tests, run the following in your virtualend:
```bash
$ pip install -e .[dev]
```
