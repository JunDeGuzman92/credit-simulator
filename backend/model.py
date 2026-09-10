import json
from pathlib import Path

import joblib
import lightgbm as lgb
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "german.data"

ARTIFACTS_DIR = BASE_DIR / "artifacts"

MODEL_PATH = ARTIFACTS_DIR / "credit_risk_pipeline.joblib"

METADATA_PATH = ARTIFACTS_DIR / "model_metadata.json"


# -------------------------------------------------------------------
# Raw German Credit dataset schema
# -------------------------------------------------------------------

RAW_COLUMNS = [
    "checking_status",
    "duration_months",
    "credit_history",
    "purpose",
    "credit_amount",
    "savings",
    "employment",
    "installment_rate",
    "personal_status",
    "other_debtors",
    "residence_years",
    "property",
    "age",
    "other_installment_plans",
    "housing",
    "existing_credits",
    "job",
    "dependents",
    "telephone",
    "foreign_worker",
    "target",
]


# -------------------------------------------------------------------
# UCI code mappings
# -------------------------------------------------------------------

CATEGORY_MAPPINGS = {
    "checking_status": {
        "A11": "lt-0",
        "A12": "0-to-200",
        "A13": "ge-200",
        "A14": "none",
    },
    "credit_history": {
        "A30": "no-credits",
        "A31": "all-paid",
        "A32": "existing-paid",
        "A33": "delayed",
        "A34": "critical",
    },
    "purpose": {
        "A40": "new-car",
        "A41": "used-car",
        "A42": "furniture-equipment",
        "A43": "radio-tv",
        "A44": "domestic-appliances",
        "A45": "repairs",
        "A46": "education",
        "A47": "vacation",
        "A48": "retraining",
        "A49": "business",
        "A410": "other",
    },
    "savings": {
        "A61": "lt-100",
        "A62": "100-to-500",
        "A63": "500-to-1000",
        "A64": "ge-1000",
        "A65": "unknown",
    },
    "employment": {
        "A71": "unemployed",
        "A72": "lt-1",
        "A73": "1-to-4",
        "A74": "4-to-7",
        "A75": "ge-7",
    },
    "personal_status": {
        "A91": "male-divorced-separated",
        "A92": "female-divorced-separated-married",
        "A93": "male-single",
        "A94": "male-married-widowed",
        "A95": "female-single",
    },
    "other_debtors": {
        "A101": "none",
        "A102": "co-applicant",
        "A103": "guarantor",
    },
    "property": {
        "A121": "real-estate",
        "A122": "savings-life-insurance",
        "A123": "car-or-other",
        "A124": "unknown",
    },
    "other_installment_plans": {
        "A141": "bank",
        "A142": "stores",
        "A143": "none",
    },
    "housing": {
        "A151": "rent",
        "A152": "own",
        "A153": "free",
    },
    "job": {
        "A171": "unemployed-unskilled-nonresident",
        "A172": "unskilled-resident",
        "A173": "skilled-employee",
        "A174": "management-self-employed",
    },
    "telephone": {
        "A191": "none",
        "A192": "yes",
    },
    "foreign_worker": {
        "A201": "yes",
        "A202": "no",
    },
}


CATEGORICAL_COLUMNS = [
    "checking_status",
    "credit_history",
    "purpose",
    "savings",
    "employment",
    "personal_status",
    "other_debtors",
    "property",
    "other_installment_plans",
    "housing",
    "job",
    "telephone",
    "foreign_worker",
]


NUMERIC_COLUMNS = [
    "duration_months",
    "credit_amount",
    "installment_rate",
    "residence_years",
    "age",
    "existing_credits",
    "dependents",
]


FEATURE_COLUMNS = CATEGORICAL_COLUMNS + NUMERIC_COLUMNS


# -------------------------------------------------------------------
# Data loading
# -------------------------------------------------------------------

def load_dataset() -> pd.DataFrame:
    """Load and decode the German Credit dataset."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"German Credit dataset not found at:\n{DATA_PATH}\n\n"
            "Place the UCI german.data file inside backend/data/."
        )

    df = pd.read_csv(
        DATA_PATH,
        names=RAW_COLUMNS,
        sep=r"\s+",
    )

    if df.shape[1] != len(RAW_COLUMNS):
        raise ValueError(
            "Unexpected German Credit dataset structure. "
            f"Expected {len(RAW_COLUMNS)} columns, "
            f"received {df.shape[1]}."
        )

    for column, mapping in CATEGORY_MAPPINGS.items():
        df[column] = df[column].map(mapping)

        if df[column].isna().any():
            raise ValueError(
                f"Unknown category code detected in '{column}'."
            )

    # Original dataset:
    # 1 = good credit
    # 2 = bad credit
    #
    # Internal application convention:
    # 0 = good credit
    # 1 = bad/high-risk credit
    df["target"] = df["target"].map(
        {
            1: 0,
            2: 1,
        }
    )

    if df["target"].isna().any():
        raise ValueError(
            "Unexpected target values found in German Credit dataset."
        )

    return df


# -------------------------------------------------------------------
# Model pipeline
# -------------------------------------------------------------------

def build_pipeline() -> Pipeline:
    """Create preprocessing + LightGBM pipeline."""

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore",
                ),
                CATEGORICAL_COLUMNS,
            ),
            (
                "numeric",
                "passthrough",
                NUMERIC_COLUMNS,
            ),
        ],
        remainder="drop",
    )

    classifier = lgb.LGBMClassifier(
        objective="binary",
        n_estimators=100,
        learning_rate=0.05,
        num_leaves=15,
        random_state=42,
        n_jobs=-1,
        verbosity=-1,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ]
    )

    return pipeline


# -------------------------------------------------------------------
# Training
# -------------------------------------------------------------------

def train_and_save() -> Pipeline:
    """Train, evaluate and persist the complete ML pipeline."""

    print("Loading German Credit dataset...")

    df = load_dataset()

    X = df[FEATURE_COLUMNS].copy()
    y = df["target"].astype(int)

    print(f"Rows: {len(df)}")
    print(f"Features: {len(FEATURE_COLUMNS)}")
    print()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    pipeline = build_pipeline()

    print("Training LightGBM pipeline...")

    pipeline.fit(
        X_train,
        y_train,
    )

    predictions = pipeline.predict(X_test)

    probabilities = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": float(
            accuracy_score(
                y_test,
                predictions,
            )
        ),
        "precision": float(
            precision_score(
                y_test,
                predictions,
                zero_division=0,
            )
        ),
        "recall": float(
            recall_score(
                y_test,
                predictions,
                zero_division=0,
            )
        ),
        "f1": float(
            f1_score(
                y_test,
                predictions,
                zero_division=0,
            )
        ),
        "roc_auc": float(
            roc_auc_score(
                y_test,
                probabilities,
            )
        ),
        "confusion_matrix": confusion_matrix(
            y_test,
            predictions,
        ).tolist(),
        "classification_report": classification_report(
            y_test,
            predictions,
            target_names=[
                "good",
                "bad",
            ],
            output_dict=True,
            zero_division=0,
        ),
    }

    print()
    print("Evaluation")
    print("-" * 40)
    print(f"Accuracy : {metrics['accuracy']:.3f}")
    print(f"Precision: {metrics['precision']:.3f}")
    print(f"Recall   : {metrics['recall']:.3f}")
    print(f"F1       : {metrics['f1']:.3f}")
    print(f"ROC-AUC  : {metrics['roc_auc']:.3f}")
    print()

    ARTIFACTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        pipeline,
        MODEL_PATH,
    )

    metadata = {
        "model_type": "LightGBM binary classifier",
        "dataset": "UCI German Credit",
        "target_mapping": {
            "0": "good",
            "1": "bad",
        },
        "feature_columns": FEATURE_COLUMNS,
        "categorical_columns": CATEGORICAL_COLUMNS,
        "numeric_columns": NUMERIC_COLUMNS,
        "metrics": metrics,
    }

    with METADATA_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            metadata,
            file,
            indent=2,
        )

    print(f"Model saved to:\n{MODEL_PATH}")
    print()
    print(f"Metadata saved to:\n{METADATA_PATH}")

    return pipeline


# -------------------------------------------------------------------
# Entry point
# -------------------------------------------------------------------

if __name__ == "__main__":
    train_and_save()