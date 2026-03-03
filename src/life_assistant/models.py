from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass(slots=True)
class RecognitionRecord:
    id: int
    user_id: str
    image_ref: str
    object_name: str
    object_category: str
    confidence_score: float
    suggestions: List[str]
    voice_note: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class FavoriteSuggestion:
    id: int
    user_id: str
    recognition_id: int
    custom_tag: str
    created_at: datetime = field(default_factory=datetime.utcnow)
