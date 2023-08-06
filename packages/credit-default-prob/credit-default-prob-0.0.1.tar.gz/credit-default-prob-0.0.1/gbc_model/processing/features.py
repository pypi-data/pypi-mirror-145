from typing import List

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class BinaryAssign(BaseEstimator, TransformerMixin):
    def __init__(self, variables: List[str]):

        if not isinstance(variables, list):
            raise ValueError("variables should be a list")

        self.variables = variables

    def fit(self, X: pd.DataFrame, y: pd.Series = None):

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        X = X.copy()

        for feature in self.variables:
            X[feature] = np.where(
                X[feature] == 1.0,
                "1",
                (
                    np.where(
                        X[feature] == 2.0,
                        "2",
                        (
                            np.where(
                                X[feature] == "Y",
                                "Y",
                                (
                                    np.where(
                                        X[feature] == "N",
                                        "N",
                                        (
                                            np.where(
                                                X[feature] == 1,
                                                "1",
                                                (
                                                    np.where(
                                                        X[feature] == 2,
                                                        "2",
                                                        (
                                                            np.where(
                                                                X[feature] == 0,
                                                                "0",
                                                                None,
                                                            )
                                                        ),
                                                    )
                                                ),
                                            )
                                        ),
                                    )
                                ),
                            )
                        ),
                    )
                ),
            )
        return X


class SubsNum(BaseEstimator, TransformerMixin):
    def __init__(self, variables: List[str]):

        if not isinstance(variables, list):
            raise ValueError("variables should be a list")

        self.variables = variables

    def fit(self, X: pd.DataFrame, y: pd.DataFrame = None):

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        X = X.copy()

        for feature in self.variables:
            X[feature] = (
                X[feature]
                .astype(str)
                .str.replace("$", "", regex=True)
                .str.replace(",", "", regex=True)
                .astype(float)
            )

        return X


class SpecialCh(BaseEstimator, TransformerMixin):
    def __init__(self, variables: List[str], alpha: list):

        if not isinstance(variables, list):
            raise ValueError("variables should be a list")

        self.variables = variables
        self.alpha = alpha

    def fit(self, X: pd.DataFrame, y: pd.DataFrame = None):

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        X = X.copy()

        for feature in self.variables:
            for i in self.alpha:
                X[feature] = X[feature].astype(str).str.replace(i, "", regex=True)

        return X


class FunDec(BaseEstimator, TransformerMixin):
    def __init__(self, variables: List[str]):

        if not isinstance(variables, list):
            raise ValueError("variables should be a list")

        self.variables = variables

    def fit(self, X: pd.DataFrame, y: pd.Series = None):

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        X = X.copy()

        for feature in self.variables:

            X[feature] = X[feature].astype(int)

            X.loc[X[feature] <= 1989, feature] = 0
            X.loc[(X[feature] >= 1990) & (X[feature] <= 1999), feature] = 1
            X.loc[(X[feature] >= 2000) & (X[feature] <= 2009), feature] = 2
            X.loc[X[feature] >= 2010, feature] = 3

        return X


class CutDec(BaseEstimator, TransformerMixin):
    def __init__(self, variables: List[str]):

        if not isinstance(variables, list):
            raise ValueError("variables should be a list")

        self.variables = variables

    def fit(self, X: pd.DataFrame, y: pd.Series = None):

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        X = X.copy()

        for feature in self.variables:

            X[feature] = X[feature].astype(str).apply(lambda x: x[:2])

        return X


class NPtoDF(BaseEstimator, TransformerMixin):
    def __init__(self, variables: List[str]):

        if not isinstance(variables, list):
            raise ValueError("variables should be a list")

        self.variables = variables

    def fit(self, X: pd.DataFrame, y: pd.Series = None):

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        X = X.copy()

        X = pd.DataFrame(X, columns=self.variables)

        return X
