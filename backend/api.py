import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.schemas import (
    CreditInput,
    CreditResult,
    HealthResult,
    ProbabilityResult,
)


# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = (
    BASE_DIR
    / "artifacts"
    / "credit_risk_pipeline.joblib"
)


# -------------------------------------------------------------------
# Model container
# -------------------------------------------------------------------

model: Any | None = None


# -------------------------------------------------------------------
# Startup / shutdown
# -------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model

    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)

        print(
            f"Loaded credit-risk model from:\n{MODEL_PATH}"
        )
    else:
        model = None

        print(
            "WARNING: model artifact was not found.\n"
            "Run:\n"
            "python -m backend.model"
        )

    yield

    model = None


# -------------------------------------------------------------------
# FastAPI application
# -------------------------------------------------------------------

app = FastAPI(
    title="Credit Score Simulator API",
    description=(
        "Educational credit-risk simulator based on "
        "the UCI German Credit dataset."
    ),
    version="0.1.0",
    lifespan=lifespan,
)


# -------------------------------------------------------------------
# CORS
# -------------------------------------------------------------------

default_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

configured_origins = os.getenv(
    "FRONTEND_ORIGINS",
)

if configured_origins:
    allowed_origins = [
        origin.strip()
        for origin in configured_origins.split(",")
        if origin.strip()
    ]
else:
    allowed_origins = default_origins


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Credit Score Simulator API",
        "status": "running",
        "docs": "/docs",
    }


@app.get(
    "/health",
    response_model=HealthResult,
)
def health():
    return HealthResult(
        status="healthy",
        model_loaded=model is not None,
    )


@app.post(
    "/predict",
    response_model=CreditResult,
)
def predict_credit(
    data: CreditInput,
) -> CreditResult:
    """Predict credit risk for one validated applicant."""

    if model is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "Credit-risk model is not loaded. "
                "Train the model first using "
                "'python -m backend.model'."
            ),
        )

    try:
        input_frame = pd.DataFrame(
            [
                data.model_dump()
            ]
        )

        prediction = int(
            model.predict(
                input_frame
            )[0]
        )

        raw_probabilities = model.predict_proba(
            input_frame
        )[0]

        classifier = model.named_steps[
            "classifier"
        ]

        classes = list(
            classifier.classes_
        )

        good_index = classes.index(0)
        bad_index = classes.index(1)

        good_probability = float(
            raw_probabilities[
                good_index
            ]
        )

        bad_probability = float(
            raw_probabilities[
                bad_index
            ]
        )

        # Educational transformation only.
        #
        # 0% predicted bad-risk -> approximately 850
        # 100% predicted bad-risk -> approximately 300
        #
        # This is NOT a real bureau or FICO score.
        simulated_score = round(
            850
            - (
                bad_probability
                * 550
            )
        )

        simulated_score = max(
            300,
            min(
                850,
                simulated_score,
            ),
        )

        risk_label = (
            "good"
            if prediction == 0
            else "high-risk"
        )

        return CreditResult(
            prediction=risk_label,
            probabilities=ProbabilityResult(
                good_credit=round(
                    good_probability
                    * 100,
                    1,
                ),
                bad_credit=round(
                    bad_probability
                    * 100,
                    1,
                ),
            ),
            simulated_credit_score=(
                simulated_score
            ),
            score_disclaimer=(
                "Educational simulated score only. "
                "It is not a FICO score or a score "
                "issued by any credit bureau."
            ),
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Prediction failed: "
                f"{type(exc).__name__}: "
                f"{exc}"
            ),
        ) from exc