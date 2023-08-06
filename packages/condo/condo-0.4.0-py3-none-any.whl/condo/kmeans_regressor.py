

class CatRegressor:
    def __init__(self, kmeaners, mus_dicts, vars_dicts):
        self.kmeaners_ = kmeaners
        self.mus_dicts_ = mus_dicts
        self.vars_dicts = vars_dicts

    def fit(self, X, y):
        assert False

    def predict(self, X):
        Xcat = X.copy()
        num_confounders = len(self.kmeaners_)


