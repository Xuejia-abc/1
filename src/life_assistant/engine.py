from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RecognitionResult:
    object_name: str
    object_category: str
    confidence_score: float


class RecognitionEngine:
    """Keyword-based mock recognizer for MVP development."""

    _INGREDIENTS = {
        "tomato": "西红柿",
        "egg": "鸡蛋",
        "potato": "土豆",
        "onion": "洋葱",
    }
    _PLANTS = {
        "pothos": "绿萝",
        "rose": "玫瑰",
        "cactus": "仙人掌",
        "orchid": "兰花",
    }
    _HOUSEHOLD = {
        "detergent": "洗洁精",
        "bleach": "漂白剂",
        "toothpaste": "牙膏",
        "shampoo": "洗发水",
    }

    def recognize(self, image_ref: str, voice_note: str | None = None) -> RecognitionResult:
        text = f"{image_ref} {voice_note or ''}".lower()

        for keyword, name in self._INGREDIENTS.items():
            if keyword in text:
                return RecognitionResult(name, "食材", 0.94)

        for keyword, name in self._PLANTS.items():
            if keyword in text:
                return RecognitionResult(name, "植物", 0.91)

        for keyword, name in self._HOUSEHOLD.items():
            if keyword in text:
                return RecognitionResult(name, "日常用品", 0.89)

        return RecognitionResult("未知物品", "未分类", 0.52)


class SuggestionEngine:
    def generate(self, object_name: str, object_category: str) -> list[str]:
        if object_category == "食材":
            return [
                f"用 {object_name} 做一道快手菜：切块后与鸡蛋翻炒，10 分钟可完成。",
                f"{object_name} 建议放在阴凉处，2-3 天内使用口感更佳。",
                f"如果缺少配料，可尝试用洋葱或土豆搭配 {object_name} 增加饱腹感。",
            ]

        if object_category == "植物":
            return [
                f"{object_name} 建议每周浇水 1-2 次，保持盆土微湿即可。",
                f"将 {object_name} 放在明亮散射光环境，避免正午暴晒。",
                f"每月检查叶片背面，出现黄斑时及时修剪并通风。",
            ]

        if object_category == "日常用品":
            return [
                f"使用 {object_name} 前先阅读标签说明，按推荐剂量使用。",
                f"{object_name} 建议远离儿童和宠物，避免误触误食。",
                f"使用后密封保存，并记录开封日期以便定期更换。",
            ]

        return [
            "暂未准确识别，建议补拍更清晰角度或补充语音描述。",
            "可手动输入物品名称，我们将基于文本生成建议。",
            "若涉及食用/护理/化学品安全，请优先参考官方说明。",
        ]
