from typing import Any, Dict

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from akerbp.mlpet import Dataset
from akerbp.mlpet.utilities import feature_target_split


class FeatureSelector(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X: pd.DataFrame, y: pd.DataFrame = None) -> "FeatureSelector":
        return self

    def transform(self, X: pd.DataFrame, y: pd.DataFrame = None) -> pd.DataFrame:
        return X[self.columns]


class MLPetTransformer(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        ds: Dataset,
        train_kwargs: Dict[str, Dict[str, Any]] = None,
        test_kwargs: Dict[str, Dict[str, Any]] = None,
        verbose=False,
    ):
        self.ds = ds
        self.train_kwargs = train_kwargs
        self.test_kwargs = test_kwargs
        self.verbose = verbose

    def fit(self, X: pd.DataFrame, y: pd.DataFrame) -> "MLPetTransformer":
        """
        Purely an implementational function to adhere to the sklearn API. See
        docstring for fit_transform.

        Args:
            X (pd.DataFrame): feature set
            y (pd.DataFrame): label set
        """
        return self

    def fit_transform(
        self, X: pd.DataFrame = None, y: pd.DataFrame = None
    ) -> pd.DataFrame:
        """
        Performs the requested train preprocessing pipeline either via the kwargs
        passed at class instantiation or via the pipeline defined in the class
        connected Dataset's settings file.

        Args:
            X (pd.DataFrame - optional): feature set to be preprocessed.
                Defaults to None. If X=None, the transformers attempts to
                retrieve X from the df_original saved to the dataset class
            y (pd.DataFrame - optional): Preprocessing of the label column is
                **NOT** supported. This is by default set to None

        Returns:
            X (pd.DataFrame - optional): Preprocessed feature set
            y (pd.DataFrame - optional): Preprocessed label set
        """
        # Combine the sets for preprocessing
        if X is not None:
            df = X
        elif hasattr(self.ds, "df_original"):
            df = self.ds.df_original.copy()
        else:
            raise ValueError("No dataframe was provided to the transformer!")

        # Perform preprocessing
        if self.train_kwargs is not None:
            df = self.ds.preprocess(df, verbose=self.verbose, **self.train_kwargs)
        elif hasattr(self.ds, "preprocessing_pipeline"):
            df = self.ds.preprocess(
                df,
                verbose=self.verbose,
            )
        else:
            ValueError("No preprocessing kwargs were provided to the transformer!")

        # Retrieve X
        if self.ds.label_column in df:
            X, _ = feature_target_split(df, self.ds.label_column)
        else:
            X = df

        return X

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Perform the requested test preprocessing pipeline either via the kwargs
        passed at class instantiation or via the pipeline defined in the class
        connected Dataset's settings file.

        Args:
            X (pd.DataFrame): The test set to be preprocessed

        Returns:
            pd.DataFrame: The preprocessed test set
        """
        # Perform preprocessing
        if self.test_kwargs is not None:
            X = self.ds.preprocess(X, verbose=self.verbose, **self.test_kwargs)
        elif hasattr(self.ds, "preprocessing_pipeline"):
            X = self.ds.preprocess(X, verbose=self.verbose)
        else:
            ValueError("No preprocessing kwargs were provided to the transformer!")
        return X
