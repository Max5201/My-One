const API_URL = "https://你的后端域名.onrender.com";  // 👈 换成你的 Render 后端地址

// 加载消息列表
async function loadMessages() {
  const res = await fetch(`${API_URL}/messages`);
  const data = await res.json();

  const list = document.getElementById("messages");
  list.innerHTML = "";
  data.forEach(msg => {
    const li = document.createElement("li");
    li.textContent = `${msg.id}. ${msg.text} (${msg.created_at})`;
    list.appendChild(li);
  });
}

// 提交新消息
async function addMessage() {
  const input = document.getElementById("msgInput");
  const text = input.value.trim();
  if (!text) {
    alert("请输入内容！");
    return;
  }

  const res = await fetch(`${API_URL}/add`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });

  if (res.ok) {
    input.value = "";
    await loadMessages();  // 重新加载列表
  } else {
    alert("提交失败！");
  }
}

// 页面加载时自动拉取消息
window.onload = loadMessages;
