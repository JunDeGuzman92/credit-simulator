// ---------------------------------------------------------
// German Credit categorical types
// ---------------------------------------------------------

export type CheckingStatus =
  | "lt-0"
  | "0-to-200"
  | "ge-200"
  | "none";

export type CreditHistory =
  | "no-credits"
  | "all-paid"
  | "existing-paid"
  | "delayed"
  | "critical";

export type Purpose =
  | "new-car"
  | "used-car"
  | "furniture-equipment"
  | "radio-tv"
  | "domestic-appliances"
  | "repairs"
  | "education"
  | "vacation"
  | "retraining"
  | "business"
  | "other";

export type Savings =
  | "lt-100"
  | "100-to-500"
  | "500-to-1000"
  | "ge-1000"
  | "unknown";

export type Employment =
  | "unemployed"
  | "lt-1"
  | "1-to-4"
  | "4-to-7"
  | "ge-7";

export type PersonalStatus =
  | "male-divorced-separated"
  | "female-divorced-separated-married"
  | "male-single"
  | "male-married-widowed"
  | "female-single";

export type OtherDebtors =
  | "none"
  | "co-applicant"
  | "guarantor";

export type Property =
  | "real-estate"
  | "savings-life-insurance"
  | "car-or-other"
  | "unknown";

export type OtherInstallmentPlans =
  | "bank"
  | "stores"
  | "none";

export type Housing =
  | "rent"
  | "own"
  | "free";

export type Job =
  | "unemployed-unskilled-nonresident"
  | "unskilled-resident"
  | "skilled-employee"
  | "management-self-employed";

export type Telephone =
  | "none"
  | "yes";

export type ForeignWorker =
  | "yes"
  | "no";


// ---------------------------------------------------------
// API request
// ---------------------------------------------------------

export interface CreditInput {
  checking_status: CheckingStatus;

  duration_months: number;

  credit_history: CreditHistory;

  purpose: Purpose;

  credit_amount: number;

  savings: Savings;

  employment: Employment;

  installment_rate: 1 | 2 | 3 | 4;

  personal_status: PersonalStatus;

  other_debtors: OtherDebtors;

  residence_years: 1 | 2 | 3 | 4;

  property: Property;

  age: number;

  other_installment_plans: OtherInstallmentPlans;

  housing: Housing;

  existing_credits: number;

  job: Job;

  dependents: 1 | 2;

  telephone: Telephone;

  foreign_worker: ForeignWorker;
}


// ---------------------------------------------------------
// Prediction response
// ---------------------------------------------------------

export type CreditRiskPrediction =
  | "good"
  | "high-risk";

export interface CreditProbabilities {
  good_credit: number;
  bad_credit: number;
}

export interface CreditResult {
  prediction: CreditRiskPrediction;

  probabilities: CreditProbabilities;

  simulated_credit_score: number;

  score_disclaimer: string;
}


// ---------------------------------------------------------
// Health endpoint response
// ---------------------------------------------------------

export interface HealthResult {
  status: string;
  model_loaded: boolean;
}


// ---------------------------------------------------------
// API error shape
// ---------------------------------------------------------

export interface ApiError {
  detail: string;
}