/**
 * TypeScript types mirroring the backend Pydantic schemas.
 * Single source of truth for all data shapes used across the frontend.
 */

export interface Participant {
  id: string;
  name: string;
  email: string | null;
  avatar_color: string;
}

export interface Meeting {
  id: string;
  title: string;
  date: string; // ISO string
  duration: number; // seconds
  bot_name: string;
  status: 'processing' | 'processed' | 'failed';
  source: string;
  created_at: string;
  updated_at: string;
  participants: Participant[];
}

export interface MeetingListResponse {
  items: Meeting[];
  total: number;
  page: number;
  page_size: number;
}

export interface MeetingCreate {
  title: string;
  date: string;
  duration: number;
  participants: Array<{ name: string; email?: string; avatar_color?: string }>;
  transcript_text?: string;
}

export interface MeetingUpdate {
  title?: string;
  date?: string;
  duration?: number;
  participants?: Array<{ name: string; email?: string; avatar_color?: string }>;
}

export interface TranscriptLine {
  id: string;
  meeting_id: string;
  participant_id: string | null;
  speaker_name: string;
  start_time: number; // seconds
  end_time: number;
  text: string;
  sequence_number: number;
  created_at: string;
}

export interface Chapter {
  title: string;
  start_time: number;
  summary: string;
}

export interface Summary {
  id: string;
  meeting_id: string;
  overview: string;
  key_topics: string[];
  chapters: Chapter[];
  sentiment: 'positive' | 'neutral' | 'negative';
  created_at: string;
  updated_at: string;
}

export interface ActionItem {
  id: string;
  meeting_id: string;
  assignee: string | null;
  text: string;
  due_date: string | null;
  completed: boolean;
  priority: 'high' | 'medium' | 'low';
  created_at: string;
  updated_at: string;
}

export interface ActionItemCreate {
  text: string;
  assignee?: string;
  due_date?: string;
  priority?: 'high' | 'medium' | 'low';
}

export interface ActionItemUpdate {
  text?: string;
  assignee?: string;
  due_date?: string;
  completed?: boolean;
  priority?: 'high' | 'medium' | 'low';
}

export interface SearchResult {
  type: 'meeting' | 'transcript';
  meeting_id: string;
  meeting_title: string;
  snippet: string;
  timestamp: number | null;
}
