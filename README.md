# Smart Lifestyle Assistant MVP (Backend + Visualization)

基于 `PRD.md` 的最小可运行实现，覆盖：
- 拍照/相册引用识别（当前为关键词 mock 识别）
- AI 建议生成（按食材/植物/日用品分类）
- 分享卡片内容生成
- 历史记录与收藏重命名
- 可视化 Web 页面（表单交互 + 结果展示）

## Run

```bash
PYTHONPATH=src python -m life_assistant.server
```

默认启动在 `http://0.0.0.0:8000`，浏览器访问 `http://localhost:8000/` 查看可视化页面。

## API

- `POST /api/recognitions`
- `GET /api/history?user_id=...`
- `POST /api/favorites`
- `PATCH /api/favorites/{id}`
- `GET /api/favorites?user_id=...`
- `POST /api/share-cards`

## Visualization page

- `/`：主页面
- `/static/app.js`：前端交互逻辑
- `/static/styles.css`：样式

## Test

```bash
PYTHONPATH=src pytest
python -m compileall src tests
```
