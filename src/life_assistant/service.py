from __future__ import annotations

from dataclasses import asdict
from threading import Lock

from .engine import RecognitionEngine, SuggestionEngine
from .models import FavoriteSuggestion, RecognitionRecord


class AssistantService:
    def __init__(self) -> None:
        self._recognizer = RecognitionEngine()
        self._suggestions = SuggestionEngine()
        self._records: dict[int, RecognitionRecord] = {}
        self._favorites: dict[int, FavoriteSuggestion] = {}
        self._record_seq = 1
        self._favorite_seq = 1
        self._lock = Lock()

    def recognize(self, user_id: str, image_ref: str, voice_note: str | None = None) -> dict:
        with self._lock:
            result = self._recognizer.recognize(image_ref=image_ref, voice_note=voice_note)
            suggestions = self._suggestions.generate(result.object_name, result.object_category)
            record = RecognitionRecord(
                id=self._record_seq,
                user_id=user_id,
                image_ref=image_ref,
                object_name=result.object_name,
                object_category=result.object_category,
                confidence_score=result.confidence_score,
                suggestions=suggestions,
                voice_note=voice_note,
            )
            self._records[record.id] = record
            self._record_seq += 1
            return self._serialize_record(record)

    def get_history(self, user_id: str) -> list[dict]:
        with self._lock:
            history = [r for r in self._records.values() if r.user_id == user_id]
        history.sort(key=lambda r: r.created_at, reverse=True)
        return [self._serialize_record(item) for item in history]

    def create_favorite(self, user_id: str, recognition_id: int, custom_tag: str) -> dict:
        with self._lock:
            if recognition_id not in self._records:
                raise KeyError("recognition_not_found")

            favorite = FavoriteSuggestion(
                id=self._favorite_seq,
                user_id=user_id,
                recognition_id=recognition_id,
                custom_tag=custom_tag,
            )
            self._favorites[favorite.id] = favorite
            self._favorite_seq += 1
            return self._serialize_favorite(favorite)

    def rename_favorite(self, user_id: str, favorite_id: int, custom_tag: str) -> dict:
        with self._lock:
            favorite = self._favorites.get(favorite_id)
            if not favorite or favorite.user_id != user_id:
                raise KeyError("favorite_not_found")
            favorite.custom_tag = custom_tag
            return self._serialize_favorite(favorite)

    def get_favorites(self, user_id: str) -> list[dict]:
        result = [f for f in self._favorites.values() if f.user_id == user_id]
        result.sort(key=lambda f: f.created_at, reverse=True)
        return [self._serialize_favorite(item) for item in result]

    def build_share_card(self, recognition_id: int) -> dict:
        record = self._records.get(recognition_id)
        if not record:
            raise KeyError("recognition_not_found")

        top_suggestions = record.suggestions[:3]
        content = (
            f"识别到：{record.object_name}（{record.object_category}）\n"
            f"可信度：{record.confidence_score:.0%}\n"
            f"建议：\n- " + "\n- ".join(top_suggestions)
        )
        return {
            "recognition_id": record.id,
            "title": f"我刚识别了 {record.object_name}",
            "object_name": record.object_name,
            "category": record.object_category,
            "confidence_score": record.confidence_score,
            "suggestions": top_suggestions,
            "share_text": content,
        }

    @staticmethod
    def _serialize_record(record: RecognitionRecord) -> dict:
        payload = asdict(record)
        payload["created_at"] = record.created_at.isoformat() + "Z"
        return payload

    @staticmethod
    def _serialize_favorite(favorite: FavoriteSuggestion) -> dict:
        payload = asdict(favorite)
        payload["created_at"] = favorite.created_at.isoformat() + "Z"
        return payload
