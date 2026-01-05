import type { Event2, ShowDetails } from "../context/BookingContext";

const API_BASE_URL = "http://localhost:8000/api/v1";

type RequestOptions = {
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  body?: unknown;
  token?: string | null;
  headers?: Record<string, string>;
};

async function apiRequest<T>(
  path: string,
  { method = "GET", body, token, headers = {} }: RequestOptions = {}
): Promise<T> {
  const normalizedPath = path.replace(/^\/+/, "");
  const url = `${API_BASE_URL}/${normalizedPath}`;
  const requestHeaders: Record<string, string> = {
    Accept: "application/json",
    ...headers,
  };

  if (body !== undefined) {
    requestHeaders["Content-Type"] = "application/json";
  }

  if (token) {
    requestHeaders.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(url, {
    method,
    headers: requestHeaders,
    body: body === undefined ? undefined : JSON.stringify(body),
  });

  if (!response.ok) {
    const errorText = await response.text().catch(() => "");
    throw new Error(
      errorText || `Request failed with status ${response.status}`
    );
  }

  return (await response.json()) as T;
}

export async function fetchShows({
  category,
  city,
  token,
}: {
  category: string;
  city: string;
  token?: string | null;
}): Promise<Event2[]> {
  const params = new URLSearchParams({ category, city });
  return apiRequest<Event2[]>(`/show?${params.toString()}`, { token });
}

export async function fetchShowDetails({
  showId,
  token,
}: {
  showId: string | number;
  token?: string | null;
}): Promise<ShowDetails> {
  return apiRequest<ShowDetails>(`/show/${showId}`, { token });
}
