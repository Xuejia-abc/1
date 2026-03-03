const $ = (selector) => document.querySelector(selector);

const state = {
  latestRecognition: null,
};

function currentUserId() {
  return $("#user-id").value.trim();
}

function renderRecognition(record) {
  state.latestRecognition = record;
  $("#recognition-result").hidden = false;
  $("#result-summary").innerHTML = `
    <p><strong>名称:</strong> ${record.object_name}</p>
    <p><strong>分类:</strong> ${record.object_category}</p>
    <p><strong>可信度:</strong> ${(record.confidence_score * 100).toFixed(1)}%</p>
  `;

  const ul = $("#result-suggestions");
  ul.innerHTML = "";
  record.suggestions.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    ul.appendChild(li);
  });
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error || "request_failed");
  }
  return payload;
}

$("#recognition-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const body = {
    user_id: currentUserId(),
    image_ref: $("#image-ref").value.trim(),
    voice_note: $("#voice-note").value.trim() || null,
  };
  try {
    const record = await requestJson("/api/recognitions", {
      method: "POST",
      body: JSON.stringify(body),
    });
    renderRecognition(record);
    alert("识别成功");
  } catch (error) {
    alert(`识别失败: ${error.message}`);
  }
});

$("#copy-suggestions").addEventListener("click", async () => {
  if (!state.latestRecognition) return;
  const text = state.latestRecognition.suggestions.join("\n");
  await navigator.clipboard.writeText(text);
  alert("建议已复制");
});

$("#favorite-recognition").addEventListener("click", async () => {
  if (!state.latestRecognition) return;
  const customTag = prompt("输入收藏标签", "常用建议") || "常用建议";
  try {
    await requestJson("/api/favorites", {
      method: "POST",
      body: JSON.stringify({
        user_id: state.latestRecognition.user_id,
        recognition_id: state.latestRecognition.id,
        custom_tag: customTag,
      }),
    });
    alert("收藏成功");
  } catch (error) {
    alert(`收藏失败: ${error.message}`);
  }
});

$("#build-share-card").addEventListener("click", async () => {
  if (!state.latestRecognition) return;
  try {
    const card = await requestJson("/api/share-cards", {
      method: "POST",
      body: JSON.stringify({ recognition_id: state.latestRecognition.id }),
    });
    $("#share-card").hidden = false;
    $("#share-content").textContent = card.share_text;
  } catch (error) {
    alert(`生成分享卡片失败: ${error.message}`);
  }
});

$("#load-history").addEventListener("click", async () => {
  try {
    const payload = await requestJson(`/api/history?user_id=${encodeURIComponent(currentUserId())}`);
    const list = $("#history-list");
    list.innerHTML = "";
    payload.items.forEach((item) => {
      const li = document.createElement("li");
      li.textContent = `${item.object_name} (${item.object_category}) - ${(item.confidence_score * 100).toFixed(0)}%`;
      list.appendChild(li);
    });
  } catch (error) {
    alert(`加载历史失败: ${error.message}`);
  }
});

$("#load-favorites").addEventListener("click", async () => {
  try {
    const payload = await requestJson(`/api/favorites?user_id=${encodeURIComponent(currentUserId())}`);
    const list = $("#favorites-list");
    list.innerHTML = "";
    payload.items.forEach((item) => {
      const li = document.createElement("li");
      li.textContent = `#${item.id} 识别记录 ${item.recognition_id} ｜ 标签: ${item.custom_tag}`;
      list.appendChild(li);
    });
  } catch (error) {
    alert(`加载收藏失败: ${error.message}`);
  }
});
