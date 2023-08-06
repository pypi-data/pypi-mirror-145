from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from gbc_model.config.core import config


def drop_na_inputs(*, input_data: pd.DataFrame) -> pd.DataFrame:
    """Check model inputs for na values and filter."""
    validated_data = input_data.copy()
    new_vars_with_na = [
        var
        for var in config.model_config.features
        if var
        not in config.model_config.cat_vars_with_na
        + config.model_config.binary_miss
        + config.model_config.binary_freq
        and validated_data[var].isnull().sum() > 0
    ]
    validated_data.dropna(subset=new_vars_with_na, inplace=True)

    return validated_data


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""

    # convert syntax error field names (beginning with numbers)
    relevant_data = input_data[config.model_config.features].copy()
    validated_data = drop_na_inputs(input_data=relevant_data)
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultipleSBAInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class SBAInputSchema(BaseModel):
    City: Optional[str]
    Zip: Optional[int]
    Bank: Optional[str]
    NAICS: Optional[int]
    ApprovalFY: Optional[str]
    Term: Optional[int]
    NoEmp: Optional[int]
    NewExist: Optional[float]
    CreateJob: Optional[int]
    RetainedJob: Optional[int]
    UrbanRural: Optional[int]
    RevLineCr: Optional[str]
    LowDoc: Optional[str]
    DisbursementGross: Optional[str]
    GrAppv: Optional[str]
    SBA_Appv: Optional[str]


class MultipleSBAInputs(BaseModel):
    inputs: List[SBAInputSchema]
