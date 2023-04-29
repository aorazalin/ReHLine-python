import warnings
import sys
from benchopt import BaseSolver, safe_import_context
sys.path.insert(0, '../') # the code for ReHLine is in this directory
import numpy as np

with safe_import_context() as import_ctx:
    from _rehline import ReHLine

class Solver(BaseSolver):
    name = 'rehline'

    install_cmd = 'pip'
    requirements = ['scikit-learn']

    def set_objective(self, X, y, Z, C, rho):
        self.X, self.y, self.Z, self.C, self.rho = X, y, Z, C, rho
        n, d = X.shape

        A = np.repeat([self.Z @ self.X], repeats=[2], axis=0) / n
        A[1] = -A[1]
        b = np.array([self.rho, self.rho])

        self.clf = ReHLine(C=self.C/n, verbose=False, tol=1e-12)
        self.clf.make_ReLHLoss(X=X, y=y, loss={'name':'SVM'})
        self.clf.A = A
        self.clf.b = b

    def run(self, n_iter):
        self.clf.max_iter = n_iter
        self.clf.fit(self.X)

    def get_result(self):
        return self.clf.coef_