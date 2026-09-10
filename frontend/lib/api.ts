/**
 * API client for communicating with the Credit Score Simulator backend
 */

import type {
  CreditInput,
  CreditResult,
  HealthResult,
} from '../../shared/types';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export class ApiRequestError extends Error {
  constructor(
    message: string,
    public status?: number,
    public detail?: string
  ) {
    super(message);
    this.name = 'ApiRequestError';
  }
}

/**
 * Check if the API and model are healthy
 */
export async function checkHealth(): Promise<HealthResult> {
  try {
    const response = await fetch(`${API_BASE}/health`);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new ApiRequestError(
        'Health check failed',
        response.status,
        errorData.detail || 'Unknown error'
      );
    }

    return response.json();
  } catch (error) {
    if (error instanceof ApiRequestError) throw error;
    throw new ApiRequestError(
      'Failed to connect to API',
      undefined,
      error instanceof Error ? error.message : 'Network error'
    );
  }
}

/**
 * Predict credit risk for a given input
 */
export async function predictCredit(
  data: CreditInput
): Promise<CreditResult> {
  try {
    const response = await fetch(`${API_BASE}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new ApiRequestError(
        'Prediction failed',
        response.status,
        errorData.detail || 'Unknown error'
      );
    }

    return response.json();
  } catch (error) {
    if (error instanceof ApiRequestError) throw error;
    throw new ApiRequestError(
      'Failed to connect to prediction endpoint',
      undefined,
      error instanceof Error ? error.message : 'Network error'
    );
  }
}

/**
 * Get API root status
 */
export async function getRootStatus(): Promise<{
  message: string;
  status: string;
  docs: string;
}> {
  const response = await fetch(`${API_BASE}/`);

  if (!response.ok) {
    throw new ApiRequestError('Failed to fetch root status');
  }

  return response.json();
}