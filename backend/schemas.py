# ---------------------------------------------------------
# Pydantic V2 data validation schemas for Credit Score Simulator
# ---------------------------------------------------------

from typing import Literal

from pydantic import BaseModel, Field


# ---------------------------------------------------------
# Literal type aliases matching shared/types.ts & German Credit dataset
# ---------------------------------------------------------

CheckingStatus = Literal["lt-0", "0-to-200", "ge-200", "none"]

CreditHistory = Literal[
    "no-credits",
    "all-paid",
    "existing-paid",
    "delayed",
    "critical",
]

Purpose = Literal[
    "new-car",
    "used-car",
    "furniture-equipment",
    "radio-tv",
    "domestic-appliances",
    "repairs",
    "education",
    "vacation",
    "retraining",
    "business",
    "other",
]

Savings = Literal["lt-100", "100-to-500", "500-to-1000", "ge-1000", "unknown"]

Employment = Literal[
    "unemployed",
    "lt-1",
    "1-to-4",
    "4-to-7",
    "ge-7",
]

PersonalStatus = Literal[
    "male-divorced-separated",
    "female-divorced-separated-married",
    "male-single",
    "male-married-widowed",
    "female-single",
]

OtherDebtors = Literal["none", "co-applicant", "guarantor"]

Property = Literal["real-estate", "savings-life-insurance", "car-or-other", "unknown"]

OtherInstallmentPlans = Literal["bank", "stores", "none"]

Housing = Literal["rent", "own", "free"]

Job = Literal[
    "unemployed-unskilled-nonresident",
    "unskilled-resident",
    "skilled-employee",
    "management-self-employed",
]

Telephone = Literal["none", "yes"]

ForeignWorker = Literal["yes", "no"]


# ---------------------------------------------------------
# Pydantic models for API request/response bodies
# ---------------------------------------------------------


class CreditInput(BaseModel):
    """Validated input payload for a single credit-risk prediction."""

    checking_status: CheckingStatus

    duration_months: int = Field(ge=1, le=72, description="Loan duration in months")

    credit_history: CreditHistory

    purpose: Purpose

    credit_amount: float = Field(
        ge=250, le=25000, description="Credit amount in DM (German dataset units)"
    )

    savings: Savings

    employment: Employment

    installment_rate: Literal[1, 2, 3, 4] = Field(
        ge=1, le=4, description="Installment rate as percent of disposable income"
    )

    personal_status: PersonalStatus

    other_debtors: OtherDebtors

    residence_years: Literal[1, 2, 3, 4] = Field(
        ge=1, le=4, description="Years at current residence"
    )

    property: Property

    age: int = Field(ge=18, le=100, description="Applicant age in years")

    other_installment_plans: OtherInstallmentPlans

    housing: Housing

    existing_credits: int = Field(
        ge=1, le=10, description="Number of existing credits / loans"
    )

    job: Job

    dependents: Literal[1, 2] = Field(
        ge=0, le=9, description="Number of people dependent on applicant's income"
    )

    telephone: Telephone

    foreign_worker: ForeignWorker


class ProbabilityResult(BaseModel):
    """Probability breakdown for good vs. high-risk credit (displayed as %)."""

    good_credit: float = Field(ge=0, le=100, description="Probability [0-100]% of good credit")

    bad_credit: float = Field(ge=0, le=100, description="Probability [0-100]% of high-risk credit")


class CreditResult(BaseModel):
    """Full prediction response returned to the frontend."""

    prediction: Literal["good", "high-risk"]

    probabilities: ProbabilityResult

    simulated_credit_score: int = Field(
        ge=300,
        le=850,
        description="Simulated credit score (300-850). Educational purposes only.",
    )

    score_disclaimer: str = Field(
        description=(
            "Educational simulated score only. "
            "It is not a FICO score or a score issued by any credit bureau."
        )
    )


class HealthResult(BaseModel):
    """Minimal health-check response for the API root."""

    status: str

    model_loaded: bool