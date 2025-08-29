import React, { useEffect, useState } from 'react';
import { query, createThread } from '../api';

type Message = { role: 'user' | 'assistant'; text: string };

export const CopilotSidebar: React.FC = () => {
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

	useEffect(() => {
		if (threadId) {
			try { localStorage.setItem('copilot_thread_id', threadId); } catch (e) { /* ignore */ }
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
					// Non-blocking: the app can still function without pre-created thread
					console.error('Failed to create thread on session start', err);
				}
			})();
		}
	}, []);

	const handleSend = async () => {
		if (!input.trim()) return;
		const text = input.trim();
		setMessages(prev => [...prev, { role: 'user', text }] );
		setInput('');
		setLoading(true);

		const payload = { query: text, thread_id: threadId ?? undefined };

		// show a placeholder assistant message while we wait for the non-streaming response
		setMessages(prev => [...prev, { role: 'assistant', text: 'Thinking...' }]);

		try {
			const res = await query(payload);
			const assistantText = (res && (res.answer ?? JSON.stringify(res))) || 'No answer';

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
		<aside style={{ width: 360, borderLeft: '1px solid #ddd', padding: 12, height: '100vh', boxSizing: 'border-box', overflow: 'auto' }}>
			<h3>Copilot</h3>
			<div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginBottom: 12 }}>
				{messages.map((m, i) => (
					<div key={i} style={{ background: m.role === 'user' ? '#f3f3f3' : '#e8f0ff', padding: 8, borderRadius: 6 }}>
						<div style={{ whiteSpace: 'pre-wrap' }}>{m.text}</div>
					</div>
				))}
			</div>

			<textarea value={input} onChange={(e) => setInput(e.target.value)} rows={3} placeholder="Ask the Copilot..." style={{ width: '100%' }} />
			<div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
				<button onClick={handleSend} disabled={loading || !input.trim()}>{loading ? 'Thinking…' : 'Send'}</button>
				<button onClick={() => setMessages([])}>Clear</button>
			</div>
		</aside>
	);
};
