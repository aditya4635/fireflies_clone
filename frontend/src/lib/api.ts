/**
 * Typed API client wrapping fetch against the Next.js rewrite proxy.
 * All backend calls go through /api/v1/* which is proxied to FastAPI.
 */
import {
  Meeting,
  MeetingListResponse,
  MeetingCreate,
  MeetingUpdate,
  TranscriptLine,
  Summary,
  ActionItem,
  ActionItemCreate,
  ActionItemUpdate,
  SearchResult,
} from '@/types';

const BASE = '/api/v1';

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${url}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail ?? `Request failed: ${res.status}`);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

// ---------------------------------------------------------------------------
// Meetings
// ---------------------------------------------------------------------------
export const meetingsApi = {
  list: (params?: { search?: string; topic?: string; page?: number; page_size?: number }) => {
    const qs = new URLSearchParams();
    if (params?.search) qs.set('search', params.search);
    if (params?.topic) qs.set('topic', params.topic);
    if (params?.page) qs.set('page', String(params.page));
    if (params?.page_size) qs.set('page_size', String(params.page_size));
    return request<MeetingListResponse>(`/meetings?${qs}`);
  },
  get: (id: string) => request<Meeting>(`/meetings/${id}`),
  create: (data: MeetingCreate) =>
    request<Meeting>('/meetings', { method: 'POST', body: JSON.stringify(data) }),
  update: (id: string, data: MeetingUpdate) =>
    request<Meeting>(`/meetings/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  delete: (id: string) => request<void>(`/meetings/${id}`, { method: 'DELETE' }),
};

// ---------------------------------------------------------------------------
// Transcripts
// ---------------------------------------------------------------------------
export const transcriptApi = {
  get: (meetingId: string) =>
    request<TranscriptLine[]>(`/meetings/${meetingId}/transcript`),
  search: (meetingId: string, q: string) =>
    request<TranscriptLine[]>(`/meetings/${meetingId}/transcript/search?q=${encodeURIComponent(q)}`),
  paste: (meetingId: string, text: string) =>
    request<{ lines_imported: number; message: string }>(
      `/meetings/${meetingId}/transcript/paste`,
      { method: 'POST', body: JSON.stringify({ text }) }
    ),
  upload: (meetingId: string, file: File) => {
    const form = new FormData();
    form.append('file', file);
    return fetch(`${BASE}/meetings/${meetingId}/transcript/upload`, {
      method: 'POST',
      body: form,
    }).then((r) => r.json());
  },
};

// ---------------------------------------------------------------------------
// Summaries
// ---------------------------------------------------------------------------
export const summaryApi = {
  get: (meetingId: string) => request<Summary>(`/meetings/${meetingId}/summary`),
  update: (meetingId: string, data: Partial<Summary>) =>
    request<Summary>(`/meetings/${meetingId}/summary`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
};

// ---------------------------------------------------------------------------
// Action Items
// ---------------------------------------------------------------------------
export const actionItemsApi = {
  list: (meetingId: string) =>
    request<ActionItem[]>(`/meetings/${meetingId}/action-items`),
  create: (meetingId: string, data: ActionItemCreate) =>
    request<ActionItem>(`/meetings/${meetingId}/action-items`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  update: (id: string, data: ActionItemUpdate) =>
    request<ActionItem>(`/action-items/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
  delete: (id: string) => request<void>(`/action-items/${id}`, { method: 'DELETE' }),
};

// ---------------------------------------------------------------------------
// Global Search
// ---------------------------------------------------------------------------
export const searchApi = {
  global: (q: string) =>
    request<SearchResult[]>(`/search?q=${encodeURIComponent(q)}`),
};
