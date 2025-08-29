import { useEffect, useState } from 'react';
import { query, createThread } from '../api';
import '../App.css';

type Message = { role: 'user' | 'assistant'; text: string };

export const CopilotSidebar = () => {
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
					// Non-blocking: the app can still function without pre-created thread
					console.error('Failed to create thread on session start', err);
				}
			})();
		}
	}, []);

	const handleSend = async () => {
		if (!input.trim()) return;
		const text = input.trim();
		setMessages(prev => [...prev, { role: 'user', text }]);
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
		<aside className="copilot-aside">
			<div className="copilot-header">
				<div className="copilot-logo">CP</div>
				<div className="copilot-title">
					<div>Copilot</div>
					<div className="muted">AI assistant</div>
				</div>
			</div>

			<div className="copilot-messages" role="log" aria-live="polite">
				{messages.map((m, i) => (
					<div key={i} className={`copilot-msg ${m.role}`}>
						<div style={{ whiteSpace: 'pre-wrap' }}>{m.text}</div>
					</div>
				))}
			</div>

			<div className="copilot-input">
				<textarea
					className="copilot-textarea"
					value={input}
					onChange={(e) => setInput(e.target.value)}
					rows={3}
					placeholder="Ask the Copilot..."
					aria-label="Copilot input"
				/>

				<div className="copilot-controls">
					<button className="cta-primary" onClick={handleSend} disabled={loading || !input.trim()}>
						{loading ? 'Thinking…' : 'Send'}
					</button>
					<button className="cta-secondary" onClick={() => setMessages([])}>Clear</button>
				</div>
			</div>
		</aside>
	);
};
