import statsmodels.api as sm


def ols(X, y, constant=True):
    features = X.copy()

    if constant:
        features = sm.add_constant(features)

    model = sm.OLS(y, features)

    result = model.fit()
    print(result.summary())

    return result, model
