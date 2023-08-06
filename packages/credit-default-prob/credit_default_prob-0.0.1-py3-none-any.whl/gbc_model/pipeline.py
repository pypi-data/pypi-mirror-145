import string

from feature_engine.encoding import (
    CountFrequencyEncoder,
    OneHotEncoder,
    OrdinalEncoder,
    RareLabelEncoder,
)
from feature_engine.imputation import CategoricalImputer
from feature_engine.outliers import ArbitraryOutlierCapper
from feature_engine.selection import DropFeatures
from feature_engine.transformation import YeoJohnsonTransformer
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

from gbc_model.config.core import config
from gbc_model.processing import features as pp

a = string.ascii_letters + string.punctuation + string.whitespace
alpha = list(a)

pca = PCA()

sba_pipe_y = Pipeline(
    [
        (
            "frequent_imputation - target",
            CategoricalImputer(
                imputation_method="frequent",
                variables=config.model_config.target,
            ),
        ),
        (
            "Binary Imputation",
            OneHotEncoder(
                variables=config.model_config.target,
                drop_last=True,
            ),
        ),
    ]
)

sba_pipe_x = Pipeline(
    [
        (
            "frequent_imputation - features",
            CategoricalImputer(
                imputation_method="frequent",
                variables=config.model_config.cat_vars_with_na,
            ),
        ),
        (
            "BinaryAssign",
            pp.BinaryAssign(
                variables=config.model_config.binary_vars,
            ),
        ),
        (
            "missing_imputation - binary features (miss)",
            CategoricalImputer(
                imputation_method="missing",
                variables=config.model_config.binary_miss,
            ),
        ),
        (
            "frequent_imputation - binary features (freq)",
            CategoricalImputer(
                imputation_method="frequent",
                variables=config.model_config.binary_freq,
            ),
        ),
        (
            "Dollar Signs",
            pp.SubsNum(
                variables=config.model_config.num_vars,
            ),
        ),
        (
            "SpecialCh",
            pp.SpecialCh(
                variables=config.model_config.temp_vars,
                alpha=alpha,
            ),
        ),
        (
            "Decades",
            pp.FunDec(
                variables=config.model_config.temp_vars,
            ),
        ),
        (
            "Outliers",
            ArbitraryOutlierCapper(
                max_capping_dict=config.model_config.outliers,
                min_capping_dict=None,
            ),
        ),
        (
            "Yeo-Johnson",
            YeoJohnsonTransformer(
                variables=config.model_config.num_vars,
            ),
        ),
        (
            "Decimal Cut for Zip and NAICS",
            pp.CutDec(
                variables=config.model_config.zipnaics,
            ),
        ),
        (
            "Rare Label",
            RareLabelEncoder(
                tol=0.01,
                n_categories=1,
                variables=config.model_config.cat_vars,
            ),
        ),
        (
            "Ordinal Encoder for almost-Binary vars",
            OrdinalEncoder(
                encoding_method="arbitrary",
                variables=config.model_config.binary_vars,
            ),
        ),
        (
            "Frequency Encoder for Cat_vars",
            CountFrequencyEncoder(
                encoding_method="frequency",
                variables=config.model_config.cat_vars,
            ),
        ),
        ("MinMax Scaler for all variables", MinMaxScaler()),
        (
            "NPtoDF",
            pp.NPtoDF(
                variables=config.model_config.features,
            ),
        ),
        (
            "PCA - continuous variables",
            ColumnTransformer(
                [("pca", pca, config.model_config.num_vars)],
                remainder="passthrough",
            ),
        ),
        (
            "NPtoDF2",
            pp.NPtoDF(
                variables=config.model_config.features_with_pca,
            ),
        ),
        (
            "drop_features",
            DropFeatures(
                features_to_drop=config.model_config.pca_to_drop,
            ),
        ),
        (
            "GBC",
            GradientBoostingClassifier(
                max_depth=config.model_config.max_depth,
                n_estimators=config.model_config.n_estimators,
            ),
        ),
    ]
)
