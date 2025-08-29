import { useEffect, useState, useRef } from 'react';
import { query, createThread } from '../api';

type Message = { role: 'user' | 'assistant'; text: string };

const CopilotSidebar = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [threadId, setThreadId] = useState<string | null>(() => {
    try {
      return localStorage.getItem('copilot_thread_id');
    } catch (e) {
      return null;
    }
  });
  const [loading, setLoading] = useState(false);

  // Resizable sidebar state (persisted)
  const asideRef = useRef<HTMLDivElement | null>(null);
  const initialWidth = (() => {
    try {
      const v = Number(localStorage.getItem('copilot_sidebar_width'));
      return Number.isFinite(v) && v >= 220 ? v : 360;
    } catch (e) {
      return 360;
    }
  })();
  const [width, setWidth] = useState<number>(initialWidth);

  useEffect(() => {
    // Keep width persisted if changed programmatically elsewhere
    try {
      localStorage.setItem('copilot_sidebar_width', String(width));
    } catch {
      /* ignore */
    }
  }, [width]);

  useEffect(() => {
    if (threadId) {
      try {
        localStorage.setItem('copilot_thread_id', threadId);
      } catch (e) {
        /* ignore */
      }
    }
  }, [threadId]);

  useEffect(() => {
    // If no thread_id in localStorage, create one for this session
    if (!threadId) {
      (async () => {
        try {
          const res: any = await createThread();
          if (res && typeof res.thread_id === 'string') setThreadId(res.thread_id);
        } catch (err) {
          console.error('Failed to create thread on session start', err);
        }
      })();
    }
  }, []);

  // Drag handling: pointer events used so it works with mouse/touch
  const startDrag = (e: React.PointerEvent) => {
    e.preventDefault();
    const rect = asideRef.current?.getBoundingClientRect();
    if (!rect) return;

    const onPointerMove = (ev: PointerEvent) => {
      const clientX = ev.clientX;
      const newWidth = Math.round(rect.right - clientX);
      const minWidth = 220;
      const maxWidth = Math.max(minWidth, window.innerWidth - 200);
      const clamped = Math.max(minWidth, Math.min(maxWidth, newWidth));
      setWidth(clamped);
      try {
        localStorage.setItem('copilot_sidebar_width', String(clamped));
      } catch {
        /* ignore */
      }
    };

    const onPointerUp = () => {
      document.removeEventListener('pointermove', onPointerMove as any);
      document.removeEventListener('pointerup', onPointerUp as any);
      document.body.style.userSelect = '';
    };

    document.addEventListener('pointermove', onPointerMove as any);
    document.addEventListener('pointerup', onPointerUp as any);
    document.body.style.userSelect = 'none';
  };

  // Helper to extract readable answer (avoid showing raw JSON in chat)
  const parseAssistantText = (response: any): string => {
    if (response == null) return 'No answer';
    if (typeof response === 'string') {
      const s = response.trim();
      if ((s.startsWith('{') && s.endsWith('}')) || (s.startsWith('[') && s.endsWith(']'))) {
        try {
          const p = JSON.parse(s);
          if (p && typeof p === 'object') {
            if (typeof p.answer === 'string') return p.answer;
            if (typeof p.message === 'string') return p.message;
            if (p?.data && typeof p.data.answer === 'string') return p.data.answer;
            for (const k of Object.keys(p)) {
              if (typeof p[k] === 'string') return p[k];
            }
            return JSON.stringify(p);
          }
        } catch {
          return s;
        }
      }
      return s;
    }
    if (typeof response === 'object') {
      if (typeof response.answer === 'string') return response.answer;
      if (typeof response.message === 'string') return response.message;
      if (response?.data && typeof response.data.answer === 'string') return response.data.answer;
      for (const k of Object.keys(response)) {
        if (typeof response[k] === 'string') return response[k];
      }
      return JSON.stringify(response);
    }
    return String(response);
  };

  const handleSend = async () => {
    if (!input.trim()) return;
    const text = input.trim();
    setMessages(prev => [...prev, { role: 'user', text }]);
    setInput('');
    setLoading(true);

    const payload = { query: text, thread_id: threadId ?? undefined } as any;

    // optimistic assistant placeholder
    setMessages(prev => [...prev, { role: 'assistant', text: 'Thinking...' }]);

    try {
      const res: any = await query(payload);
      const assistantText = parseAssistantText(res) || 'No answer';

      setMessages(prev => {
        const last = prev[prev.length - 1];
        if (last && last.role === 'assistant') {
          const copy = [...prev];
          copy[copy.length - 1] = { role: 'assistant', text: assistantText };
          return copy;
        }
        return [...prev, { role: 'assistant', text: assistantText }];
      });

      if (res && typeof res.thread_id === 'string') {
        setThreadId(res.thread_id);
      }
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', text: `Error: ${String(err)}` }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <aside
      ref={asideRef}
      style={{ width: `${width}px` }}
      className="relative bg-white border-l border-gray-200 p-4 h-[calc(100vh-4rem)] sticky top-16 flex flex-col"
    >
      {/* left-edge drag handle (visible on large screens) */}
      <div
        onPointerDown={startDrag}
        className="hidden lg:flex absolute -left-3 top-0 bottom-0 items-center justify-center w-6 cursor-col-resize z-40"
        aria-hidden="true"
      >
        <div className="h-12 w-[2px] bg-gray-300 rounded"></div>
      </div>

      <div className="flex items-center gap-3 mb-3">
        <div className="w-11 h-11 rounded-md bg-gradient-to-r from-blue-600 to-blue-500 text-white font-bold flex items-center justify-center">CP</div>
        <div className="font-semibold">
          <div>Copilot</div>
          <div className="text-sm text-gray-500">AI assistant</div>
        </div>
      </div>

      <div className="flex-1 overflow-auto space-y-2" role="log" aria-live="polite">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`max-w-[85%] p-2 rounded-md ${m.role === 'user' ? 'bg-gray-100 self-end text-gray-900' : 'bg-blue-50 self-start text-gray-900'}`}
            style={{ whiteSpace: 'pre-wrap' }}
          >
            {m.text}
          </div>
        ))}
      </div>

      <div className="mt-3">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              if (!loading && input.trim()) {
                handleSend();
              }
            }
          }}
          rows={3}
          placeholder="Ask the Copilot..."
          aria-label="Copilot input"
          className="w-full border rounded-md p-2 border-gray-200"
        />

        <div className="flex gap-2 mt-2">
          <button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="bg-blue-600 text-white px-3 py-2 rounded-md disabled:opacity-50"
          >
            {loading ? 'Thinking…' : 'Send'}
          </button>
          <button onClick={() => setMessages([])} className="bg-white border border-gray-200 px-3 py-2 rounded-md">
            Clear
          </button>
        </div>
      </div>
    </aside>
  );
};

export default CopilotSidebar;