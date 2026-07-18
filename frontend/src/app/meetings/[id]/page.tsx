'use client';

import { useState, useCallback } from 'react';
import { use } from 'react';
import { useQuery } from '@tanstack/react-query';
import Link from 'next/link';
import { ChevronLeft, Calendar, Clock, Users, Download } from 'lucide-react';
import Sidebar from '@/components/layout/Sidebar';
import Topbar from '@/components/layout/Topbar';
import TranscriptViewer from '@/components/transcript/TranscriptViewer';
import SummaryPanel from '@/components/summary/SummaryPanel';
import ActionItemsPanel from '@/components/summary/ActionItemsPanel';
import MediaPlayer from '@/components/player/MediaPlayer';
import CreateMeetingModal from '@/components/meetings/CreateMeetingModal';
import { meetingsApi, transcriptApi, summaryApi } from '@/lib/api';
import { Meeting } from '@/types';
import { formatDate, formatDuration, getInitials } from '@/lib/utils';
import toast from 'react-hot-toast';

type Tab = 'thread' | 'video' | 'soundbites';

interface PageProps {
  params: Promise<{ id: string }>;
}

export default function MeetingDetailPage({ params }: PageProps) {
  const { id } = use(params);

  const [activeTab, setActiveTab] = useState<Tab>('thread');
  const [currentTime, setCurrentTime] = useState(0);
  const [transcriptSearch, setTranscriptSearch] = useState('');
  const [showEditModal, setShowEditModal] = useState(false);

  // Data fetching
  const { data: meeting, isLoading: meetingLoading } = useQuery({
    queryKey: ['meeting', id],
    queryFn: () => meetingsApi.get(id),
  });

  const { data: transcript = [], isLoading: transcriptLoading } = useQuery({
    queryKey: ['transcript', id],
    queryFn: () => transcriptApi.get(id),
  });

  const { data: summary, isLoading: summaryLoading } = useQuery({
    queryKey: ['summary', id],
    queryFn: () => summaryApi.get(id),
  });

  const handleSeek = useCallback((time: number) => {
    setCurrentTime(time);
  }, []);

  const handleExport = () => {
    if (!meeting || !transcript.length) return;
    const lines = transcript
      .map((l) => `[${formatTimestamp(l.start_time)}] ${l.speaker_name}: ${l.text}`)
      .join('\n');
    const content = `# ${meeting.title}\nDate: ${formatDate(meeting.date)}\nDuration: ${formatDuration(meeting.duration)}\n\n## Transcript\n\n${lines}`;
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${meeting.title.replace(/\s+/g, '_')}_transcript.md`;
    a.click();
    URL.revokeObjectURL(url);
    toast.success('Transcript exported!');
  };

  function formatTimestamp(s: number) {
    const m = Math.floor(s / 60);
    const sec = Math.floor(s % 60);
    return `${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`;
  }

  if (meetingLoading) return <LoadingState />;
  if (!meeting) return <NotFoundState />;

  return (
    <div className="app-shell">
      <Sidebar />
      <div className="main-content">
        <Topbar />
        <main className="page-content" style={{ paddingTop: '20px' }}>
          {/* Back nav */}
          <Link
            href="/meetings"
            className="flex items-center gap-2 text-muted text-sm"
            style={{ marginBottom: '16px', display: 'inline-flex', alignItems: 'center', gap: '6px', color: 'var(--text-muted)', fontSize: '13px', transition: 'color 0.15s' }}
          >
            <ChevronLeft size={16} />
            Back to Notebook
          </Link>

          {/* Header */}
          <div className="meeting-detail-header">
            <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '16px' }}>
              <h1 className="meeting-detail-title">{meeting.title}</h1>
              <div style={{ display: 'flex', gap: '8px', flexShrink: 0 }}>
                <button
                  className="btn btn-secondary btn-sm"
                  onClick={handleExport}
                  title="Export transcript as Markdown"
                >
                  <Download size={14} />
                  Export
                </button>
                <button
                  className="btn btn-primary btn-sm"
                  onClick={() => setShowEditModal(true)}
                >
                  Edit
                </button>
              </div>
            </div>

            <div className="meeting-detail-meta">
              <span className="meeting-meta-item">
                <Calendar size={13} />
                {formatDate(meeting.date)}
              </span>
              <span className="meeting-meta-item">
                <Clock size={13} />
                {formatDuration(meeting.duration)}
              </span>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Users size={13} style={{ color: 'var(--text-muted)' }} />
                <div className="participants-row">
                  {meeting.participants.slice(0, 5).map((p) => (
                    <div
                      key={p.id}
                      className="avatar avatar-sm"
                      style={{ backgroundColor: p.avatar_color }}
                      title={p.name}
                    >
                      {getInitials(p.name)}
                    </div>
                  ))}
                  {meeting.participants.length > 5 && (
                    <div className="participants-overflow">+{meeting.participants.length - 5}</div>
                  )}
                </div>
              </div>
              <span className="badge badge-purple">Processed</span>
            </div>
          </div>

          {/* Tab Bar */}
          <div className="tab-bar" style={{ marginTop: '20px' }}>
            {(['thread', 'video', 'soundbites'] as Tab[]).map((tab) => (
              <button
                key={tab}
                id={`tab-${tab}`}
                className={`tab-item ${activeTab === tab ? 'active' : ''}`}
                onClick={() => setActiveTab(tab)}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </div>

          {/* Content */}
          {activeTab === 'thread' ? (
            <div className="detail-layout">
              {/* Left: Transcript */}
              <div>
                {transcriptLoading ? (
                  <div className="transcript-panel">
                    <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
                      Loading transcript...
                    </div>
                  </div>
                ) : (
                  <TranscriptViewer
                    lines={transcript}
                    currentTime={currentTime}
                    searchQuery={transcriptSearch}
                    onSeek={handleSeek}
                    onSearchChange={setTranscriptSearch}
                  />
                )}
              </div>

              {/* Right: Summary + Player */}
              <div className="summary-panel">
                <MediaPlayer
                  duration={meeting.duration}
                  currentTime={currentTime}
                  onSeek={handleSeek}
                  onTimeUpdate={setCurrentTime}
                  transcript={transcript}
                />

                {summaryLoading ? (
                  <SummarySkeleton />
                ) : summary ? (
                  <>
                    <SummaryPanel summary={summary} onSeek={handleSeek} />
                    <ActionItemsPanel meetingId={id} />
                  </>
                ) : (
                  <div className="card" style={{ textAlign: 'center', color: 'var(--text-muted)', fontSize: '13px' }}>
                    No summary available
                  </div>
                )}
              </div>
            </div>
          ) : (
            <ComingSoon tab={activeTab} />
          )}
        </main>
      </div>

      {showEditModal && (
        <CreateMeetingModal
          editMeeting={meeting}
          onClose={() => setShowEditModal(false)}
        />
      )}
    </div>
  );
}

function LoadingState() {
  return (
    <div className="app-shell">
      <Sidebar />
      <div className="main-content">
        <Topbar />
        <main className="page-content">
          <div className="skeleton" style={{ height: '32px', width: '60%', marginBottom: '16px' }} />
          <div className="skeleton" style={{ height: '20px', width: '40%', marginBottom: '24px' }} />
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 380px', gap: '24px' }}>
            <div className="skeleton" style={{ height: '500px', borderRadius: '14px' }} />
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div className="skeleton" style={{ height: '130px', borderRadius: '14px' }} />
              <div className="skeleton" style={{ height: '200px', borderRadius: '14px' }} />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

function NotFoundState() {
  return (
    <div className="app-shell">
      <Sidebar />
      <div className="main-content">
        <div className="empty-state" style={{ flex: 1 }}>
          <h2 className="empty-state-title">Meeting Not Found</h2>
          <Link href="/meetings" className="btn btn-primary">
            Back to Notebook
          </Link>
        </div>
      </div>
    </div>
  );
}

function SummarySkeleton() {
  return (
    <>
      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        <div className="skeleton" style={{ height: '16px', width: '40%' }} />
        <div className="skeleton" style={{ height: '80px' }} />
      </div>
      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        <div className="skeleton" style={{ height: '16px', width: '30%' }} />
        <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
          {[70, 90, 60, 80].map((w, i) => (
            <div key={i} className="skeleton" style={{ height: '26px', width: `${w}px`, borderRadius: '999px' }} />
          ))}
        </div>
      </div>
    </>
  );
}

function ComingSoon({ tab }: { tab: string }) {
  return (
    <div className="coming-soon">
      <div style={{ fontSize: '48px', marginBottom: '8px' }}>
        {tab === 'video' ? '🎬' : '🎵'}
      </div>
      <h2>{tab.charAt(0).toUpperCase() + tab.slice(1)}</h2>
      <p>This feature is coming soon. Stay tuned!</p>
    </div>
  );
}
