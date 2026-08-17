// src/api/client.ts
// constants across apis

const BASE_URL = "http://localhost:8000/api/v1";

export async function apiRequest<T>(endpoint:string, options: RequestInit = {}): Promise<T> {
    const token = localStorage.getItem('sb_access_token');

    const response = await fetch(`${BASE_URL}${endpoint}`, {
    headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...options.headers,
    },
    ...options,
    });


    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error (errorData.detail || 'Something went wrong');
    }

    return response.json();
}