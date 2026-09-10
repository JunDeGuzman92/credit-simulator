'use client';

import { useState } from 'react';
import type { CreditInput, CreditResult } from '../../shared/types';
import { predictCredit } from '../lib/api';

interface FormField {
  name: keyof CreditInput;
  label: string;
  type: 'select' | 'number';
  options?: string[];
  min?: number;
  max?: number;
  step?: number;
  placeholder?: string;
}

const formFields: FormField[] = [
  { name: 'checking_status', label: 'Checking Account Status', type: 'select', options: ['lt-0', '0-to-200', 'ge-200', 'none'] },
  { name: 'duration_months', label: 'Loan Duration (months)', type: 'number', min: 1, max: 72, step: 1 },
  { name: 'credit_history', label: 'Credit History', type: 'select', options: ['no-credits', 'all-paid', 'existing-paid', 'delayed', 'critical'] },
  { name: 'purpose', label: 'Purpose', type: 'select', options: ['new-car', 'used-car', 'furniture-equipment', 'radio-tv', 'domestic-appliances', 'repairs', 'education', 'vacation', 'retraining', 'business', 'other'] },
  { name: 'credit_amount', label: 'Credit Amount (DM)', type: 'number', min: 250, max: 25000, step: 100 },
  { name: 'savings', label: 'Savings', type: 'select', options: ['lt-100', '100-to-500', '500-to-1000', 'ge-1000', 'unknown'] },
  { name: 'employment', label: 'Employment', type: 'select', options: ['unemployed', 'lt-1', '1-to-4', '4-to-7', 'ge-7'] },
  { name: 'installment_rate', label: 'Installment Rate (%)', type: 'select', options: ['1', '2', '3', '4'] },
  { name: 'personal_status', label: 'Personal Status', type: 'select', options: ['male-divorced-separated', 'female-divorced-separated-married', 'male-single', 'male-married-widowed', 'female-single'] },
  { name: 'other_debtors', label: 'Other Debtors', type: 'select', options: ['none', 'co-applicant', 'guarantor'] },
  { name: 'residence_years', label: 'Residence Years', type: 'select', options: ['1', '2', '3', '4'] },
  { name: 'property', label: 'Property', type: 'select', options: ['real-estate', 'savings-life-insurance', 'car-or-other', 'unknown'] },
  { name: 'age', label: 'Age', type: 'number', min: 18, max: 100, step: 1 },
  { name: 'other_installment_plans', label: 'Other Installment Plans', type: 'select', options: ['bank', 'stores', 'none'] },
  { name: 'housing', label: 'Housing', type: 'select', options: ['rent', 'own', 'free'] },
  { name: 'existing_credits', label: 'Existing Credits', type: 'number', min: 1, max: 10, step: 1 },
  { name: 'job', label: 'Job', type: 'select', options: ['unemployed-unskilled-nonresident', 'unskilled-resident', 'skilled-employee', 'management-self-employed'] },
  { name: 'dependents', label: 'Dependents', type: 'select', options: ['1', '2'] },
  { name: 'telephone', label: 'Telephone', type: 'select', options: ['none', 'yes'] },
  { name: 'foreign_worker', label: 'Foreign Worker', type: 'select', options: ['yes', 'no'] },
];

export function CreditScoreForm() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<CreditResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [input, setInput] = useState<CreditInput>({
    checking_status: '0-to-200',
    duration_months: 24,
    credit_history: 'existing-paid',
    purpose: 'radio-tv',
    credit_amount: 3500,
    savings: '100-to-500',
    employment: '1-to-4',
    installment_rate: 2,
    personal_status: 'male-single',
    other_debtors: 'none',
    residence_years: 3,
    property: 'real-estate',
    age: 32,
    other_installment_plans: 'none',
    housing: 'own',
    existing_credits: 1,
    job: 'skilled-employee',
    dependents: 1,
    telephone: 'yes',
    foreign_worker: 'yes',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await predictCredit(input);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Prediction failed');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (
    name: keyof CreditInput,
    value: string | number
  ) => {
    setInput((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-2xl shadow-xl p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Credit Score Simulator
        </h2>
        <p className="text-gray-600 mb-8">
          Fill out the form below to simulate a credit risk assessment based on the German Credit dataset.
        </p>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {formFields.map((field) => (
              <div key={field.name} className="space-y-2">
                <label
                  htmlFor={field.name}
                  className="block text-sm font-medium text-gray-700"
                >
                  {field.label}
                </label>

                {field.type === 'select' ? (
                  <select
                    id={field.name}
                    name={field.name}
                    value={input[field.name] as string}
                    onChange={(e) => handleInputChange(field.name, e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  >
                    <option value="">Select {field.label}</option>
                    {field.options?.map((option) => (
                      <option key={option} value={option}>
                        {option.replace(/-/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase())}
                      </option>
                    ))}
                  </select>
                ) : (
                  <input
                    id={field.name}
                    name={field.name}
                    type="number"
                    value={input[field.name] as number}
                    onChange={(e) => handleInputChange(field.name, Number(e.target.value))}
                    min={field.min}
                    max={field.max}
                    step={field.step}
                    placeholder={field.placeholder}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    required
                  />
                )}
              </div>
            ))}
          </div>

          <button
            type="submit"
            disabled={loading}
            className={`w-full py-3 px-6 font-medium rounded-lg text-white transition-colors ${
              loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
            }`}
          >
            {loading ? 'Calculating...' : 'Predict Credit Score'}
          </button>
        </form>

        {error && (
          <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-800 font-medium">Error: {error}</p>
          </div>
        )}

        {result && (
          <div className="mt-8 p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-200">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Prediction Results</h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white p-4 rounded-lg shadow-sm">
                <p className="text-3xl font-bold text-blue-600">
                  {result.simulated_credit_score}
                </p>
                <p className="text-sm text-gray-600 mt-1">Simulated Credit Score</p>
                <p className={`text-sm font-medium mt-2 ${
                  result.prediction === 'good' ? 'text-green-600' : 'text-red-600'
                }`}>
                  {result.prediction === 'good' ? 'Good Credit' : 'High Risk'}
                </p>
              </div>

              <div className="bg-white p-4 rounded-lg shadow-sm">
                <p className="text-sm font-medium text-gray-700 mb-2">Probability Breakdown</p>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Good Credit:</span>
                    <span className="text-sm font-medium text-green-600">
                      {result.probabilities.good_credit}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">High Risk:</span>
                    <span className="text-sm font-medium text-red-600">
                      {result.probabilities.bad_credit}%
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-xs text-yellow-800">
                <strong>Disclaimer:</strong> {result.score_disclaimer}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}