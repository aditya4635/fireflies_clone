"""
Transcript service — handles parsing and importing transcript data.
Supports plain text, .vtt (WebVTT), and JSON formats.
"""
import uuid
import json
import re
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.transcript import TranscriptLine
from app.models.meeting import Meeting


class TranscriptService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_transcript(self, meeting_id: str) -> List[TranscriptLine]:
        stmt = (
            select(TranscriptLine)
            .where(TranscriptLine.meeting_id == meeting_id)
            .order_by(TranscriptLine.sequence_number)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def search_transcript(self, meeting_id: str, query: str) -> List[TranscriptLine]:
        stmt = (
            select(TranscriptLine)
            .where(
                TranscriptLine.meeting_id == meeting_id,
                TranscriptLine.text.ilike(f"%{query}%"),
            )
            .order_by(TranscriptLine.sequence_number)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def import_transcript_text(self, meeting_id: str, raw_text: str) -> int:
        """
        Parse a raw transcript text and persist as TranscriptLine rows.
        Expected format: 'Speaker Name: utterance text' per line.
        Assigns auto-incrementing timestamps (10s per line).
        """
        # Clear existing transcript for this meeting
        existing = await self.db.execute(
            select(TranscriptLine).where(TranscriptLine.meeting_id == meeting_id)
        )
        for line in existing.scalars().all():
            await self.db.delete(line)

        lines = [l.strip() for l in raw_text.strip().split("\n") if l.strip()]
        seq = 0
        count = 0
        for raw_line in lines:
            if ":" in raw_line:
                parts = raw_line.split(":", 1)
                speaker = parts[0].strip()
                text = parts[1].strip()
            else:
                speaker = "Speaker"
                text = raw_line

            start = seq * 10.0
            end = start + 9.5
            tl = TranscriptLine(
                id=str(uuid.uuid4()),
                meeting_id=meeting_id,
                speaker_name=speaker,
                start_time=start,
                end_time=end,
                text=text,
                sequence_number=seq,
            )
            self.db.add(tl)
            seq += 1
            count += 1

        await self.db.commit()
        return count

    async def import_vtt(self, meeting_id: str, vtt_content: str) -> int:
        """Parse WebVTT format transcript."""
        existing = await self.db.execute(
            select(TranscriptLine).where(TranscriptLine.meeting_id == meeting_id)
        )
        for line in existing.scalars().all():
            await self.db.delete(line)

        lines = vtt_content.strip().split("\n")
        seq = 0
        count = 0
        i = 0
        while i < len(lines):
            # Match timestamp line: 00:00:01.000 --> 00:00:05.000
            ts_match = re.match(
                r"(\d+:\d+:\d+\.\d+)\s+-->\s+(\d+:\d+:\d+\.\d+)",
                lines[i].strip()
            )
            if ts_match:
                start = self._vtt_ts_to_seconds(ts_match.group(1))
                end = self._vtt_ts_to_seconds(ts_match.group(2))
                i += 1
                text_lines = []
                while i < len(lines) and lines[i].strip():
                    text_lines.append(lines[i].strip())
                    i += 1
                full_text = " ".join(text_lines)
                speaker, text = self._extract_speaker(full_text)
                tl = TranscriptLine(
                    id=str(uuid.uuid4()),
                    meeting_id=meeting_id,
                    speaker_name=speaker,
                    start_time=start,
                    end_time=end,
                    text=text,
                    sequence_number=seq,
                )
                self.db.add(tl)
                seq += 1
                count += 1
            else:
                i += 1

        await self.db.commit()
        return count

    def _vtt_ts_to_seconds(self, ts: str) -> float:
        parts = ts.replace(",", ".").split(":")
        h, m, s = float(parts[0]), float(parts[1]), float(parts[2])
        return h * 3600 + m * 60 + s

    def _extract_speaker(self, text: str):
        if ":" in text:
            parts = text.split(":", 1)
            return parts[0].strip(), parts[1].strip()
        return "Speaker", text
