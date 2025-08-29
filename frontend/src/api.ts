export interface QueryPayload {
  query: string;
  pseudo_user_id?: string;
  thread_id?: string;
}

export async function query(payload: QueryPayload) {
  const base = (import.meta.env.VITE_API_BASE_URL as string) || '';
  const res = await fetch(`${base}/api/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function streamQuery(payload: QueryPayload, onChunk: (chunk: string) => void) {
  const base = (import.meta.env.VITE_API_BASE_URL as string) || '';
  const res = await fetch(`${base}/api/query/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.body) throw new Error('No stream available');

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let done = false;
  while (!done) {
    const { value, done: rDone } = await reader.read();
    done = rDone;
    if (value) {
      const chunk = decoder.decode(value, { stream: true });
      onChunk(chunk);
    }
  }
  return;
}

export async function createThread(pseudo_user_id?: string) {
  const base = (import.meta.env.VITE_API_BASE_URL as string) || '';
  const res = await fetch(`${base}/api/threads`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ pseudo_user_id }),
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}
