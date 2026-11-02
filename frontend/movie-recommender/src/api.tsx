import * as z from "zod";

function getErrorMessage(status: number, data: unknown): string {
  if (
    typeof data === "object" &&
    data !== null &&
    "detail" in data &&
    typeof data.detail === "string"
  ) {
    return data.detail;
  } else {
    return `Request failed with status ${status}`;
  }
}

class ApiError extends Error {
  status: number;
  data: unknown;

  constructor(status: number, data: unknown) {
    super(getErrorMessage(status, data));
    this.status = status;
    this.data = data;
  }
}

export async function apiFetch(
  path: string,
  options: RequestInit = {},
): Promise<unknown> {
  const url = `/api${path}`;
  const token = localStorage.getItem("token");

  const res = await fetch(url, {
    ...options,
    ...(token && { Authorization: `Bearer ${token}` }),
  });
  if (!res.ok) {
    const data = await res.json().catch(() => null);
    throw new ApiError(res.status, data);
  }

  if (res.status === 204) {
    return undefined;
  }

  const data = await res.json();
  return data;
}

export async function fullFetch<T>(
  path: string,
  options: RequestInit = {},
  schema: z.ZodType<T>,
): Promise<T> {
  const data = await apiFetch(path, options);
  return schema.parse(data);
}
