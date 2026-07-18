'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles } from 'lucide-react';
import { getInitials } from '@/lib/utils';

type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
};

const INITIAL_MESSAGE: Message = {
  id: 'msg-1',
  role: 'assistant',
  content: "Hi! I'm Fred, your AI meeting assistant. Ask me anything about your meetings, action items, or insights. (Note: This is a simulated demo environment!)"
};

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([INITIAL_MESSAGE]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    // Simulate AI response delay
    setTimeout(() => {
      let aiContent = "I'm currently running in a simulated environment without live API access. However, in production, I would analyze your meetings and provide detailed answers, summaries, or draft emails based on this request!";
      
      const lowerInput = userMessage.content.toLowerCase();
      if (lowerInput.includes('summary')) {
        aiContent = "Based on recent meetings, the team is heavily focused on Q3 Roadmap Planning and improving mobile performance. Would you like a detailed breakdown of the action items?";
      } else if (lowerInput.includes('action')) {
        aiContent = "You have 3 pending action items across your meetings, mostly related to UX research and mobile engineering plans.";
      } else if (lowerInput.includes('hello') || lowerInput.includes('hi')) {
        aiContent = "Hello there! How can I help you today?";
      }

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: aiContent
      };

      setMessages(prev => [...prev, aiMessage]);
      setIsTyping(false);
    }, 1500);
  };

  return (
    <div className="chat-interface" style={{ display: 'flex', flexDirection: 'column', height: '100%', backgroundColor: 'var(--color-bg-secondary)', borderRadius: '12px', border: '1px solid var(--color-border)', overflow: 'hidden' }}>
      
      {/* Chat Header */}
      <div style={{ padding: '16px 20px', borderBottom: '1px solid var(--color-border)', display: 'flex', alignItems: 'center', gap: '12px', backgroundColor: 'var(--color-bg-elevated)' }}>
        <div style={{ width: '32px', height: '32px', borderRadius: '8px', backgroundColor: 'var(--color-accent-purple)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Sparkles size={16} color="white" />
        </div>
        <div>
          <h2 style={{ fontSize: '15px', fontWeight: 600, margin: 0, fontFamily: 'var(--font-heading)' }}>AskFred</h2>
          <p style={{ fontSize: '12px', color: 'var(--color-text-secondary)', margin: 0 }}>AI Meeting Assistant</p>
        </div>
      </div>

      {/* Messages Area */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '20px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
        {messages.map((msg) => (
          <div key={msg.id} style={{ display: 'flex', gap: '16px', flexDirection: msg.role === 'user' ? 'row-reverse' : 'row' }}>
            <div style={{ flexShrink: 0 }}>
              {msg.role === 'assistant' ? (
                <div style={{ width: '28px', height: '28px', borderRadius: '6px', backgroundColor: 'var(--color-accent-purple)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Bot size={14} color="white" />
                </div>
              ) : (
                <div style={{ width: '28px', height: '28px', borderRadius: '50%', backgroundColor: '#059669', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '10px', fontWeight: 'bold' }}>
                  {getInitials('Demo User')}
                </div>
              )}
            </div>
            
            <div style={{ 
              maxWidth: '75%', 
              padding: '12px 16px', 
              borderRadius: '12px',
              backgroundColor: msg.role === 'user' ? 'var(--color-accent-purple)' : 'var(--color-bg-elevated)',
              border: msg.role === 'user' ? 'none' : '1px solid var(--color-border)',
              color: msg.role === 'user' ? 'white' : 'var(--color-text-primary)',
              fontSize: '14px',
              lineHeight: 1.5,
              borderTopRightRadius: msg.role === 'user' ? '4px' : '12px',
              borderTopLeftRadius: msg.role === 'assistant' ? '4px' : '12px'
            }}>
              {msg.content}
            </div>
          </div>
        ))}

        {isTyping && (
          <div style={{ display: 'flex', gap: '16px', flexDirection: 'row' }}>
            <div style={{ width: '28px', height: '28px', borderRadius: '6px', backgroundColor: 'var(--color-accent-purple)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
              <Bot size={14} color="white" />
            </div>
            <div style={{ 
              padding: '12px 16px', 
              borderRadius: '12px',
              backgroundColor: 'var(--color-bg-elevated)',
              border: '1px solid var(--color-border)',
              borderTopLeftRadius: '4px',
              display: 'flex',
              alignItems: 'center',
              gap: '4px'
            }}>
              <span className="typing-dot" style={{ width: '6px', height: '6px', backgroundColor: 'var(--color-text-secondary)', borderRadius: '50%', animation: 'pulse 1.5s infinite' }}></span>
              <span className="typing-dot" style={{ width: '6px', height: '6px', backgroundColor: 'var(--color-text-secondary)', borderRadius: '50%', animation: 'pulse 1.5s infinite 0.2s' }}></span>
              <span className="typing-dot" style={{ width: '6px', height: '6px', backgroundColor: 'var(--color-text-secondary)', borderRadius: '50%', animation: 'pulse 1.5s infinite 0.4s' }}></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div style={{ padding: '16px', borderTop: '1px solid var(--color-border)', backgroundColor: 'var(--color-bg-primary)' }}>
        <div style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask Fred anything..."
            style={{ 
              width: '100%', 
              padding: '14px 48px 14px 16px', 
              borderRadius: '8px', 
              border: '1px solid var(--color-border)', 
              backgroundColor: 'var(--color-bg-elevated)', 
              color: 'var(--color-text-primary)',
              fontSize: '14px',
              outline: 'none'
            }}
          />
          <button 
            onClick={handleSend}
            disabled={!input.trim() || isTyping}
            style={{ 
              position: 'absolute', 
              right: '8px', 
              width: '32px', 
              height: '32px', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              backgroundColor: input.trim() ? 'var(--color-accent-purple)' : 'transparent',
              color: input.trim() ? 'white' : 'var(--color-text-secondary)',
              border: 'none',
              borderRadius: '6px',
              cursor: input.trim() ? 'pointer' : 'default',
              transition: 'all 0.2s'
            }}
          >
            <Send size={16} />
          </button>
        </div>
        <div style={{ textAlign: 'center', marginTop: '8px', fontSize: '11px', color: 'var(--color-text-secondary)' }}>
          Fred can make mistakes. Consider verifying important information.
        </div>
      </div>
      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 0.4; transform: scale(0.8); }
          50% { opacity: 1; transform: scale(1.2); }
        }
      `}</style>
    </div>
  );
}
