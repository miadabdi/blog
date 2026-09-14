/**
 * API client: same-origin /api base (vite proxy in dev, nginx in prod).
 * Unwraps the backend response envelope, injects the bearer token,
 * and redirects to /login on 401.
 */

const TOKEN_KEY = 'blog_token';

export class ApiError extends Error {
  constructor(
    readonly status: number,
    readonly code: string,
    message: string,
    readonly detail?: unknown,
  ) {
    super(message);
  }
}

export const getToken = () => localStorage.getItem(TOKEN_KEY);
export const setToken = (t: string) => localStorage.setItem(TOKEN_KEY, t);
export const clearToken = () => localStorage.removeItem(TOKEN_KEY);

/** Canonical browser-usable URL for a stored object. */
export const fileUrl = (bucket: string, name: string) =>
  `/api/file/object/${bucket}/${name}`;

export async function api<T>(path: string, opts: RequestInit = {}): Promise<T> {
  const headers = new Headers(opts.headers);
  const token = getToken();
  if (token) headers.set('Authorization', `Bearer ${token}`);
  if (opts.body && !(opts.body instanceof FormData) && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  const res = await fetch(`/api${path}`, { ...opts, headers });

  // ponytail: no refresh endpoint exists — 401 means re-login
  if (res.status === 401 && location.pathname !== '/login') {
    clearToken();
    location.href = '/login';
  }

  const body: unknown = (res.headers.get('content-type') ?? '').includes('application/json')
    ? await res.json()
    : await res.text();

  if (!res.ok) {
    const e =
      typeof body === 'object' && body !== null
        ? (body as Record<string, unknown>)
        : { message: String(body) };
    const asText = (v: unknown, fallback: string) =>
      typeof v === 'string' && v ? v : v == null ? fallback : JSON.stringify(v);
    throw new ApiError(
      res.status,
      asText(e.code, 'ERROR'),
      asText(e.message, asText(e.detail, 'Request failed')),
      e.detail,
    );
  }

  // unwrap the {code, data, ...} envelope when present; plain bodies pass through
  if (typeof body === 'object' && body !== null && 'data' in body && 'code' in body) {
    return (body as { data: T }).data;
  }
  return body as T;
}

export async function login(email: string, password: string): Promise<void> {
  const t = await api<{ access_token: string }>('/auth/signin', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ username: email, password }),
  });
  setToken(t.access_token);
}
