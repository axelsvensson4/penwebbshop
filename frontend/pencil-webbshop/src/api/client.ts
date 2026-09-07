export type QueryParams = Record<string, string | number | boolean | null | undefined>

const DEFAULT_API_BASE_URL = 'http://localhost:8000/api'
let authToken: string | null = null

export function setAuthToken (token: string | null) {
  authToken = token
}

export class ApiError extends Error {
  constructor (
    message: string,
    public readonly status: number,
    public readonly payload?: unknown,
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

function getApiBaseUrl () {
  return import.meta.env.VITE_API_BASE_URL ?? DEFAULT_API_BASE_URL
}

function buildUrl (path: string, params?: QueryParams) {
  const url = new URL(`${getApiBaseUrl()}${path}`)

  for (const [key, value] of Object.entries(params ?? {})) {
    if (value !== null && value !== undefined && value !== '') {
      url.searchParams.set(key, String(value))
    }
  }

  return url.toString()
}

async function request<T> (path: string, init?: RequestInit, params?: QueryParams): Promise<T> {
  const isFormData = init?.body instanceof FormData
  const headers = {
    Accept: 'application/json',
    ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
    ...(isFormData ? {} : { 'Content-Type': 'application/json' }),
    ...init?.headers,
  }
  const response = await fetch(buildUrl(path, params), {
    ...init,
    headers,
    credentials: 'include',
  })

  if (response.status === 204) {
    return undefined as T
  }

  const payload = await response.json().catch(() => undefined)

  if (!response.ok) {
    const detail = typeof payload === 'object' && payload && 'detail' in payload
      ? String((payload as { detail: unknown }).detail)
      : 'API request failed'

    throw new ApiError(detail, response.status, payload)
  }

  return payload as T
}

export const apiClient = {
  get<T> (path: string, params?: QueryParams) {
    return request<T>(path, { method: 'GET' }, params)
  },
  post<T> (path: string, body: unknown) {
    return request<T>(path, { method: 'POST', body: JSON.stringify(body) })
  },
  patch<T> (path: string, body: unknown) {
    return request<T>(path, { method: 'PATCH', body: JSON.stringify(body) })
  },
  put<T> (path: string, body: unknown) {
    return request<T>(path, { method: 'PUT', body: JSON.stringify(body) })
  },
  delete<T> (path: string) {
    return request<T>(path, { method: 'DELETE' })
  },
  form<T> (path: string, body: FormData) {
    return request<T>(path, { method: 'POST', body })
  },
  file<T> (path: string, body: File) {
    return request<T>(path, {
      method: 'POST',
      body,
      headers: { 'Content-Type': body.type },
    })
  },
}
