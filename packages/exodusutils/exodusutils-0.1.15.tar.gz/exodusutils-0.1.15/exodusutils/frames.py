from typing import List, Optional

import numpy as np
import pandas as pd
from pydantic import BaseModel

from exodusutils import internal
from exodusutils.exceptions.exceptions import ExodusMethodNotAllowed


class TrainFrames(BaseModel):
    """
    A collection of dataframes. The validation frame and test frame are optional.
    """

    train: pd.DataFrame
    validation: Optional[pd.DataFrame]
    test: Optional[pd.DataFrame]

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def iid_without_test(cls, df: pd.DataFrame, validation_percentage: float):
        """
        Create `TrainFrames` for an IID model algoritghm.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe to split into train and test.
        validation_percentage : float
            validation percentage

        Returns
        -------
        TrainFrames, without test frame. Useful when training the final model.
        """
        train, validation = internal.train_validation_split(df, validation_percentage)
        return cls(train=train, validation=validation, test=None)


class CVFrames(BaseModel):
    """
    A list of `TrainFrames`. User should not initialize this class directly, instead they should \
use the classmethod `iid`.
    """

    frames: List[TrainFrames]

    @classmethod
    def iid(
        cls,
        df: pd.DataFrame,
        nfolds: int,
        validation_percentage: float,
        fold_assignment_column_name: Optional[str] = None,
    ):
        """
        Create CV frames for an IID experiment.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe to split to CV frames.
        nfolds : int
            nfolds
        validation_percentage : float
            validation percentage
        fold_assignment_column_name : Optional[str]
            If defined, fold will be cut according to it.

        Returns
        -------
        CVFrames
        """
        frames = []

        if fold_assignment_column_name is None:
            name: str = "FOLD_COLUMN"
            df = internal.append_fold_column(df, name, nfolds)
        else:
            if fold_assignment_column_name not in df.columns:
                raise ExodusMethodNotAllowed(
                    f"Fold column {fold_assignment_column_name} not found in dataframe"
                )
            name = fold_assignment_column_name

        for fold in range(nfolds):
            train, validation = df.pipe(
                internal.select_and_drop_fold_column, name, fold, test=False
            ).pipe(internal.train_validation_split, validation_percentage)
            test = internal.select_and_drop_fold_column(df, name, fold, test=True)
            frames.append(TrainFrames(train=train, validation=validation, test=test))
        return cls(frames=frames)
