'use client';

import { useState } from 'react';
import { ChevronDown, ChevronUp, Lightbulb, Hash, BookMarked, Smile } from 'lucide-react';
import { Summary } from '@/types';
import { formatTimestamp } from '@/lib/utils';

interface SummaryPanelProps {
  summary: Summary;
  onSeek: (time: number) => void;
}

function Section({
  title,
  icon: Icon,
  children,
  defaultOpen = true,
}: {
  title: string;
  icon: React.ElementType;
  children: React.ReactNode;
  defaultOpen?: boolean;
}) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="summary-section">
      <div className="summary-section-header" onClick={() => setOpen((o) => !o)}>
        <div className="summary-section-title">
          <Icon size={14} style={{ color: 'var(--accent-light)' }} />
          {title}
        </div>
        {open ? <ChevronUp size={14} style={{ color: 'var(--text-muted)' }} /> : <ChevronDown size={14} style={{ color: 'var(--text-muted)' }} />}
      </div>
      {open && <div className="summary-section-body">{children}</div>}
    </div>
  );
}

export default function SummaryPanel({ summary, onSeek }: SummaryPanelProps) {
  const sentimentIcon = {
    positive: '😊',
    neutral: '😐',
    negative: '😞',
  }[summary.sentiment] ?? '😐';

  const sentimentClass = `sentiment-${summary.sentiment}`;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      {/* Overview */}
      <Section title="Overview" icon={Lightbulb}>
        <p className="summary-overview">{summary.overview}</p>
        <div style={{ marginTop: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Sentiment:</span>
          <span className={`badge ${sentimentClass === 'sentiment-positive' ? 'badge-green' : sentimentClass === 'sentiment-negative' ? 'badge-red' : 'badge-gray'}`}>
            {sentimentIcon} {summary.sentiment}
          </span>
        </div>
      </Section>

      {/* Key Topics */}
      <Section title="Key Topics" icon={Hash}>
        <div className="topics-list">
          {summary.key_topics.map((topic) => (
            <span key={topic} className="topic-chip">{topic}</span>
          ))}
        </div>
      </Section>

      {/* Chapters */}
      <Section title="Chapters" icon={BookMarked}>
        <div className="chapters-list">
          {summary.chapters.map((chapter, i) => (
            <div
              key={i}
              className="chapter-item"
              onClick={() => onSeek(chapter.start_time)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => e.key === 'Enter' && onSeek(chapter.start_time)}
              aria-label={`Jump to chapter: ${chapter.title}`}
            >
              <span className="chapter-time">{formatTimestamp(chapter.start_time)}</span>
              <div className="chapter-info">
                <div className="chapter-title">{chapter.title}</div>
                <div className="chapter-summary">{chapter.summary}</div>
              </div>
            </div>
          ))}
        </div>
      </Section>
    </div>
  );
}
