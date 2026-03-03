# Smart Lifestyle Assistant MVP (Backend)

基于 `PRD.md` 的最小可运行后端实现，覆盖：
- 拍照/相册引用识别（当前为关键词 mock 识别）
- AI 建议生成（按食材/植物/日用品分类）
- 分享卡片内容生成
- 历史记录与收藏重命名

## Run

```bash
PYTHONPATH=src python -m life_assistant.server
```

默认启动在 `http://0.0.0.0:8000`。

## API

- `POST /api/recognitions`
- `GET /api/history?user_id=...`
- `POST /api/favorites`
- `PATCH /api/favorites/{id}`
- `GET /api/favorites?user_id=...`
- `POST /api/share-cards`

## Test

```bash
PYTHONPATH=src pytest
```
