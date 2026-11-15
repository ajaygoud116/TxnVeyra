export type HealthResponse = {
  status: string;
  service: string;
  database: string;
};

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";

export async function getHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE}/api/v1/health`);
  if (!response.ok) {
    throw new Error(`API health request failed (${response.status})`);
  }
  return response.json() as Promise<HealthResponse>;
}
