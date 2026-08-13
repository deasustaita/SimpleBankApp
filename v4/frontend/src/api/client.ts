// src/api/client.ts
// constants across apis

const BASE_URL = "http://localhost:8000/api/v1";

export async function apiRequest<t>(endpoint:string) {
    const response = await fetch(`${BASE_URL}${endpoint}`)

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error (errorData.detail || 'Something went wrong');
    }

    return response.json();
}