'use client';

import { useEffect, useRef, useState } from 'react';
import { Search, X } from 'lucide-react';
import { TranscriptLine } from '@/types';
import { formatTimestamp, getInitials, highlightText } from '@/lib/utils';

interface TranscriptViewerProps {
  lines: TranscriptLine[];
  currentTime: number;
  searchQuery: string;
  onSeek: (time: number) => void;
  onSearchChange: (q: string) => void;
}

// Assign consistent colors to speakers
function getSpeakerColor(name: string, index: number): string {
  const COLORS = ['#7C3AED', '#059669', '#2563EB', '#D97706', '#DB2777', '#0891B2'];
  return COLORS[index % COLORS.length];
}

export default function TranscriptViewer({
  lines,
  currentTime,
  searchQuery,
  onSeek,
  onSearchChange,
}: TranscriptViewerProps) {
  const activeRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [speakerColorMap, setSpeakerColorMap] = useState<Record<string, string>>({});

  // Build speaker → color map on first render
  useEffect(() => {
    const map: Record<string, string> = {};
    let idx = 0;
    for (const line of lines) {
      if (!(line.speaker_name in map)) {
        map[line.speaker_name] = getSpeakerColor(line.speaker_name, idx++);
      }
    }
    setSpeakerColorMap(map);
  }, [lines]);

  // Auto-scroll active line into view
  useEffect(() => {
    if (activeRef.current && containerRef.current) {
      const container = containerRef.current;
      const el = activeRef.current;
      const { top, bottom } = el.getBoundingClientRect();
      const { top: cTop, bottom: cBottom } = container.getBoundingClientRect();
      if (top < cTop + 60 || bottom > cBottom - 60) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
  }, [currentTime]);

  const activeLine = lines.findLast(
    (l) => l.start_time <= currentTime && currentTime <= l.end_time
  );

  const filteredLines = searchQuery
    ? lines.filter((l) => l.text.toLowerCase().includes(searchQuery.toLowerCase()))
    : lines;

  const displayLines = searchQuery ? filteredLines : lines;

  return (
    <div className="transcript-panel">
      {/* Search bar */}
      <div className="transcript-search-bar">
        <div className="search-wrapper" style={{ maxWidth: '100%' }}>
          <Search size={13} className="search-wrapper-icon" />
          <input
            id="transcript-search"
            className="form-input"
            type="text"
            placeholder="Search transcript..."
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            aria-label="Search within transcript"
          />
          {searchQuery && (
            <button
              className="icon-btn btn-sm"
              onClick={() => onSearchChange('')}
              style={{ position: 'absolute', right: '6px', top: '50%', transform: 'translateY(-50%)' }}
              aria-label="Clear search"
            >
              <X size={14} />
            </button>
          )}
        </div>
        {searchQuery && (
          <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '6px' }}>
            {filteredLines.length} result{filteredLines.length !== 1 ? 's' : ''} found
          </p>
        )}
      </div>

      {/* Lines */}
      <div className="transcript-lines" ref={containerRef}>
        {displayLines.length === 0 ? (
          <div style={{ padding: '40px 20px', textAlign: 'center', color: 'var(--text-muted)', fontSize: '13px' }}>
            No transcript lines found.
          </div>
        ) : (
          displayLines.map((line) => {
            const isActive = line.id === activeLine?.id;
            const isMatch = searchQuery && line.text.toLowerCase().includes(searchQuery.toLowerCase());

            return (
              <div
                key={line.id}
                ref={isActive ? activeRef : undefined}
                className={`transcript-line ${isActive ? 'active' : ''} ${isMatch ? 'search-match' : ''}`}
                onClick={() => onSeek(line.start_time)}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => e.key === 'Enter' && onSeek(line.start_time)}
                aria-label={`Jump to ${formatTimestamp(line.start_time)}: ${line.speaker_name}`}
              >
                <div className="transcript-line-left">
                  <div
                    className="avatar avatar-sm"
                    style={{ backgroundColor: speakerColorMap[line.speaker_name] ?? '#7C3AED' }}
                    title={line.speaker_name}
                  >
                    {getInitials(line.speaker_name)}
                  </div>
                  <span className="transcript-timestamp">{formatTimestamp(line.start_time)}</span>
                </div>

                <div className="transcript-line-content">
                  <div
                    className="transcript-speaker"
                    style={{ color: speakerColorMap[line.speaker_name] ?? 'var(--accent-light)' }}
                  >
                    {line.speaker_name}
                  </div>
                  <div
                    className="transcript-text"
                    dangerouslySetInnerHTML={{
                      __html: searchQuery
                        ? highlightText(line.text, searchQuery)
                        : line.text,
                    }}
                  />
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
