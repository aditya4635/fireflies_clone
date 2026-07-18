'use client';

import { useRef, useState, useEffect, useCallback } from 'react';
import { Play, Pause, SkipBack, SkipForward, Volume2 } from 'lucide-react';
import { formatTimestamp } from '@/lib/utils';

interface MediaPlayerProps {
  duration: number;
  currentTime: number;
  onSeek: (time: number) => void;
  onTimeUpdate?: (time: number) => void;
}

const SPEEDS = [0.5, 0.75, 1, 1.25, 1.5, 2];
const BAR_COUNT = 60;

export default function MediaPlayer({ duration, currentTime, onSeek, onTimeUpdate }: MediaPlayerProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(1);
  const [internalTime, setInternalTime] = useState(currentTime);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  // Sync external seeks into internal state
  useEffect(() => {
    setInternalTime(currentTime);
  }, [currentTime]);

  // Fake playback timer
  useEffect(() => {
    if (isPlaying) {
      intervalRef.current = setInterval(() => {
        setInternalTime((prev) => {
          const next = Math.min(prev + 0.25 * speed, duration);
          onTimeUpdate?.(next);
          if (next >= duration) {
            setIsPlaying(false);
          }
          return next;
        });
      }, 250);
    } else {
      if (intervalRef.current) clearInterval(intervalRef.current);
    }
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [isPlaying, speed, duration, onTimeUpdate]);

  const handleSeekBar = (e: React.ChangeEvent<HTMLInputElement>) => {
    const t = parseFloat(e.target.value);
    setInternalTime(t);
    onSeek(t);
  };

  const skip = (delta: number) => {
    const t = Math.max(0, Math.min(internalTime + delta, duration));
    setInternalTime(t);
    onSeek(t);
  };

  const cycleSpeed = () => {
    const idx = SPEEDS.indexOf(speed);
    setSpeed(SPEEDS[(idx + 1) % SPEEDS.length]);
  };

  const progress = duration > 0 ? internalTime / duration : 0;

  return (
    <div className="player-card">
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
        <Volume2 size={14} style={{ color: 'var(--accent-light)' }} />
        <span style={{ fontSize: '12px', fontWeight: 700, color: 'var(--text-secondary)', fontFamily: 'var(--font-heading)' }}>
          Audio Player
        </span>
        <span className="badge badge-purple" style={{ marginLeft: 'auto' }}>
          Preview
        </span>
      </div>

      {/* Waveform visualizer */}
      <div className="player-waveform">
        {Array.from({ length: BAR_COUNT }).map((_, i) => {
          const relPos = i / BAR_COUNT;
          const isPast = relPos <= progress;
          const height = 20 + Math.sin(i * 0.4) * 12 + Math.sin(i * 0.9) * 8;
          return (
            <div
              key={i}
              className="waveform-bar"
              style={{
                height: `${height}px`,
                background: isPast ? 'var(--accent)' : 'var(--border)',
                animationDelay: `${(i * 0.05) % 1.2}s`,
                animationPlayState: isPlaying ? 'running' : 'paused',
                opacity: isPast ? 0.9 : 0.4,
              }}
            />
          );
        })}
      </div>

      {/* Controls */}
      <div className="player-controls">
        <button className="icon-btn" onClick={() => skip(-10)} title="Back 10s" aria-label="Skip back 10 seconds">
          <SkipBack size={16} />
        </button>

        <button
          className="player-play-btn"
          onClick={() => setIsPlaying((p) => !p)}
          aria-label={isPlaying ? 'Pause' : 'Play'}
        >
          {isPlaying ? <Pause size={18} fill="white" /> : <Play size={18} fill="white" />}
        </button>

        <button className="icon-btn" onClick={() => skip(10)} title="Forward 10s" aria-label="Skip forward 10 seconds">
          <SkipForward size={16} />
        </button>

        <div className="player-seek">
          <input
            type="range"
            className="player-progress"
            min={0}
            max={duration}
            step={0.1}
            value={internalTime}
            onChange={handleSeekBar}
            aria-label="Seek position"
          />
          <div className="player-time">
            <span>{formatTimestamp(internalTime)}</span>
            <span>{formatTimestamp(duration)}</span>
          </div>
        </div>

        <select
          className="player-speed"
          value={speed}
          onChange={(e) => setSpeed(parseFloat(e.target.value))}
          aria-label="Playback speed"
        >
          {SPEEDS.map((s) => (
            <option key={s} value={s}>{s}x</option>
          ))}
        </select>
      </div>
    </div>
  );
}
