'use client';

import { useState, useEffect, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { Search, BookOpen, FileText, ArrowRight } from 'lucide-react';
import Sidebar from '@/components/layout/Sidebar';
import Topbar from '@/components/layout/Topbar';
import { searchApi } from '@/lib/api';
import { SearchResult } from '@/types';
import { useDebounce } from '@/hooks/useDebounce';
import { formatTimestamp, truncate } from '@/lib/utils';
import Link from 'next/link';

function SearchContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const initialQuery = searchParams.get('q') ?? '';

  const [query, setQuery] = useState(initialQuery);
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);

  const debouncedQuery = useDebounce(query, 300);

  useEffect(() => {
    if (!debouncedQuery.trim()) {
      setResults([]);
      return;
    }
    setLoading(true);
    searchApi
      .global(debouncedQuery)
      .then(setResults)
      .catch(() => setResults([]))
      .finally(() => setLoading(false));
  }, [debouncedQuery]);

  const meetingResults = results.filter((r) => r.type === 'meeting');
  const transcriptResults = results.filter((r) => r.type === 'transcript');

  return (
    <div className="app-shell">
      <Sidebar />
      <div className="main-content">
        <Topbar />
        <main className="page-content">
          <div style={{ maxWidth: '720px', margin: '0 auto' }}>
            <h1 style={{ fontFamily: 'var(--font-heading)', fontSize: '22px', fontWeight: 700, marginBottom: '20px' }}>
              Global Search
            </h1>

            {/* Search input */}
            <div className="search-wrapper" style={{ maxWidth: '100%', marginBottom: '28px' }}>
              <Search size={16} className="search-wrapper-icon" />
              <input
                id="global-search-input"
                className="form-input"
                type="text"
                placeholder="Search across all meetings and transcripts..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                autoFocus
                style={{ paddingLeft: '42px', fontSize: '15px', height: '48px', borderRadius: 'var(--radius)' }}
              />
            </div>

            {/* Results */}
            {loading ? (
              <div style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '40px' }}>
                Searching...
              </div>
            ) : !query.trim() ? (
              <div className="empty-state" style={{ padding: '40px' }}>
                <div className="empty-state-icon">
                  <Search size={24} />
                </div>
                <p className="empty-state-desc">Type to search across all meetings and transcripts</p>
              </div>
            ) : results.length === 0 ? (
              <div className="empty-state" style={{ padding: '40px' }}>
                <div className="empty-state-icon">
                  <Search size={24} />
                </div>
                <h2 className="empty-state-title">No results for "{query}"</h2>
                <p className="empty-state-desc">Try different keywords or check the spelling.</p>
              </div>
            ) : (
              <>
                {meetingResults.length > 0 && (
                  <ResultGroup
                    title="Meetings"
                    icon={<BookOpen size={14} />}
                    results={meetingResults}
                    query={query}
                  />
                )}
                {transcriptResults.length > 0 && (
                  <ResultGroup
                    title="Transcript Matches"
                    icon={<FileText size={14} />}
                    results={transcriptResults}
                    query={query}
                  />
                )}
                <p style={{ textAlign: 'center', fontSize: '12px', color: 'var(--text-muted)', marginTop: '20px' }}>
                  {results.length} result{results.length !== 1 ? 's' : ''} found
                </p>
              </>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}

function ResultGroup({
  title,
  icon,
  results,
  query,
}: {
  title: string;
  icon: React.ReactNode;
  results: SearchResult[];
  query: string;
}) {
  return (
    <div style={{ marginBottom: '28px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px', color: 'var(--text-secondary)', fontWeight: 700, fontSize: '12px', letterSpacing: '0.06em', textTransform: 'uppercase' }}>
        {icon}
        {title}
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {results.map((result, i) => (
          <Link
            key={i}
            href={`/meetings/${result.meeting_id}${result.timestamp ? `#t=${result.timestamp}` : ''}`}
            style={{ display: 'block' }}
          >
            <div className="card card-hover" style={{ cursor: 'pointer' }}>
              <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '12px' }}>
                <div style={{ flex: 1 }}>
                  <div style={{ fontFamily: 'var(--font-heading)', fontWeight: 600, fontSize: '14px', marginBottom: '4px' }}>
                    {result.meeting_title}
                  </div>
                  {result.snippet !== result.meeting_title && (
                    <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: 1.55 }}>
                      {truncate(result.snippet, 200)}
                    </p>
                  )}
                  {result.timestamp !== null && result.timestamp !== undefined && (
                    <span className="badge badge-purple" style={{ marginTop: '8px', display: 'inline-flex' }}>
                      @ {formatTimestamp(result.timestamp)}
                    </span>
                  )}
                </div>
                <ArrowRight size={14} style={{ color: 'var(--text-muted)', flexShrink: 0, marginTop: '2px' }} />
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

export default function SearchPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <SearchContent />
    </Suspense>
  );
}
