import pytest

from life_assistant.service import AssistantService


def test_recognition_and_suggestions() -> None:
    svc = AssistantService()
    record = svc.recognize(user_id="u1", image_ref="my_tomato_photo.jpg")

    assert record["object_name"] == "西红柿"
    assert record["object_category"] == "食材"
    assert len(record["suggestions"]) >= 3


def test_favorite_and_rename() -> None:
    svc = AssistantService()
    record = svc.recognize(user_id="u1", image_ref="rose.png")

    favorite = svc.create_favorite("u1", record["id"], "阳台植物")
    renamed = svc.rename_favorite("u1", favorite["id"], "卧室植物")

    assert renamed["custom_tag"] == "卧室植物"


def test_rename_favorite_rejects_other_users() -> None:
    svc = AssistantService()
    record = svc.recognize(user_id="owner", image_ref="rose.png")
    favorite = svc.create_favorite("owner", record["id"], "阳台植物")

    with pytest.raises(KeyError):
        svc.rename_favorite("intruder", favorite["id"], "恶意篡改")


def test_share_card_contains_core_fields() -> None:
    svc = AssistantService()
    record = svc.recognize(user_id="u1", image_ref="detergent-bottle.jpeg")
    card = svc.build_share_card(record["id"])

    assert card["object_name"] == "洗洁精"
    assert card["category"] == "日常用品"
    assert len(card["suggestions"]) == 3
    assert "可信度" in card["share_text"]


def test_get_history_is_thread_safe() -> None:
    from threading import Thread

    svc = AssistantService()
    errors: list[Exception] = []

    def writer() -> None:
        try:
            for i in range(200):
                svc.recognize(user_id="u1", image_ref=f"image-{i}.jpg")
        except Exception as exc:  # pragma: no cover - this should not execute
            errors.append(exc)

    def reader() -> None:
        try:
            for _ in range(200):
                svc.get_history("u1")
        except Exception as exc:  # pragma: no cover - this should not execute
            errors.append(exc)

    threads = [Thread(target=writer), Thread(target=reader), Thread(target=reader)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert not errors
