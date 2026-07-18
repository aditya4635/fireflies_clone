'use client';

import Sidebar from '@/components/layout/Sidebar';
import Topbar from '@/components/layout/Topbar';
import ChatInterface from '@/components/askfred/ChatInterface';
import { MessageSquare } from 'lucide-react';

export default function AskFredPage() {
  return (
    <div className="app-shell">
      <Sidebar />
      <div className="main-content">
        <Topbar />
        <main className="page-content" style={{ display: 'flex', flexDirection: 'column', padding: '20px', height: 'calc(100vh - 64px)' }}>
          <div style={{ marginBottom: '20px' }}>
            <h1 className="meeting-detail-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <MessageSquare size={24} style={{ color: 'var(--accent-purple)' }} />
              AskFred
            </h1>
            <p style={{ color: 'var(--text-muted)', fontSize: '14px', marginTop: '4px' }}>
              Chat with your AI meeting assistant to generate summaries, extract action items, and find insights across all your conversations.
            </p>
          </div>
          
          {/* Chat Interface Container */}
          <div style={{ flex: 1, minHeight: 0, maxWidth: '1000px', margin: '0 auto', width: '100%' }}>
            <ChatInterface />
          </div>
        </main>
      </div>
    </div>
  );
}
